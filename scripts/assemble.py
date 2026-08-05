#!/usr/bin/env python3
"""
FFmpeg video assembly engine for Zack D Director.

The assembler keeps the generated shots in beat order, normalizes them to the
vertical 9:16 canvas, adds a subtle zoom to marked impact shots, and joins
adjacent shots with short, readable transitions. Audio is crossfaded along
with the video whenever the source clips contain audio tracks.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys


CANVAS_WIDTH = 720
CANVAS_HEIGHT = 1280
FRAME_RATE = 30
DEFAULT_TRANSITION_DURATION = 0.35
VIDEO_CRF = 23
AUDIO_BITRATE = "96k"
TRANSITIONS = ("fade", "wipeleft", "slideleft", "circleopen")


def _run_probe(args):
    """Run ffprobe and return stdout, raising a useful error on failure."""
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        detail = result.stderr.strip() or "unknown ffprobe error"
        raise RuntimeError(detail)
    return result.stdout.strip()


def _duration(ffprobe, path):
    value = _run_probe([
        ffprobe,
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        path,
    ])
    try:
        duration = float(value)
    except ValueError as exc:
        raise RuntimeError(f"Could not read a duration for {path}") from exc
    if duration <= 0:
        raise RuntimeError(f"Clip has no usable duration: {path}")
    return duration


def _has_audio(ffprobe, path):
    result = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-select_streams",
            "a:0",
            "-show_entries",
            "stream=codec_type",
            "-of",
            "csv=p=0",
            path,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0 and bool(result.stdout.strip())


def _escape_filter_number(value):
    """Format a float for use in an FFmpeg filter expression."""
    return f"{value:.6f}".rstrip("0").rstrip(".")


def _build_filter_graph(clip_info, transition_duration):
    """Build the video/audio filter graph and return it with output labels."""
    filters = []
    video_labels = []
    audio_labels = []

    for info in clip_info:
        video_index = info["video_index"]
        duration = _escape_filter_number(info["duration"])
        video_label = f"v{len(video_labels)}"
        video = (
            f"[{video_index}:v]trim=duration={duration},setpts=PTS-STARTPTS,"
            f"fps={FRAME_RATE},"
            f"scale={CANVAS_WIDTH}:{CANVAS_HEIGHT}:"
            "force_original_aspect_ratio=increase,crop="
            f"{CANVAS_WIDTH}:{CANVAS_HEIGHT},setsar=1,settb=AVTB"
        )
        if info["zoom_impact"]:
            # A small center crop gives impact shots a little more energy
            # without changing their framing or duration.
            video += (
                f",scale={CANVAS_WIDTH + 36}:{CANVAS_HEIGHT + 64}:flags=lanczos,"
                f"crop={CANVAS_WIDTH}:{CANVAS_HEIGHT}:(iw-{CANVAS_WIDTH})/2:"
                f"(ih-{CANVAS_HEIGHT})/2"
            )
        video += ",format=yuv420p"
        filters.append(f"{video}[{video_label}]")
        video_labels.append(video_label)

        audio_index = info["audio_index"]
        audio_label = f"a{len(audio_labels)}"
        audio = (
            f"[{audio_index}:a]"
            f"atrim=duration={duration},asetpts=PTS-STARTPTS,"
            "aresample=48000,aformat=sample_fmts=fltp:"
            "sample_rates=48000:channel_layouts=stereo"
        )
        filters.append(f"{audio}[{audio_label}]")
        audio_labels.append(audio_label)

    if len(video_labels) == 1:
        filters.append(f"[{video_labels[0]}]null[vout]")
    elif transition_duration <= 0:
        joined = "".join(f"[{label}]" for label in video_labels)
        filters.append(f"{joined}concat=n={len(video_labels)}:v=1:a=0[vout]")
    else:
        previous = video_labels[0]
        timeline_duration = clip_info[0]["duration"]
        for index in range(1, len(video_labels)):
            duration = min(
                transition_duration,
                clip_info[index]["duration"],
                timeline_duration,
            )
            duration_text = _escape_filter_number(duration)
            offset = _escape_filter_number(timeline_duration - duration)
            output = f"vx{index}"
            transition = TRANSITIONS[(index - 1) % len(TRANSITIONS)]
            filters.append(
                f"[{previous}][{video_labels[index]}]xfade="
                f"transition={transition}:duration={duration_text}:offset={offset}"
                f"[{output}]"
            )
            previous = output
            timeline_duration += clip_info[index]["duration"] - duration
        filters.append(f"[{previous}]null[vout]")

    if len(audio_labels) == 1:
        filters.append(f"[{audio_labels[0]}]anull[aout]")
    elif transition_duration <= 0:
        joined = "".join(f"[{label}]" for label in audio_labels)
        filters.append(f"{joined}concat=n={len(audio_labels)}:v=0:a=1[aout]")
    else:
        previous = audio_labels[0]
        for index in range(1, len(audio_labels)):
            duration = min(
                transition_duration,
                clip_info[index - 1]["duration"],
                clip_info[index]["duration"],
            )
            output = f"ax{index}"
            filters.append(
                f"[{previous}][{audio_labels[index]}]acrossfade="
                f"d={_escape_filter_number(duration)}:c1=tri:c2=tri[{output}]"
            )
            previous = output
        filters.append(f"[{previous}]anull[aout]")

    return ";".join(filters)


def _build_ffmpeg_command(ffmpeg, clip_info, filter_graph, output_path):
    command = [ffmpeg, "-y", "-hide_banner", "-loglevel", "error"]
    for info in clip_info:
        command.extend(["-i", info["path"]])
        if not info["has_audio"]:
            # Keep a missing audio track from breaking the complete montage.
            command.extend([
                "-f",
                "lavfi",
                "-t",
                _escape_filter_number(info["duration"]),
                "-i",
                "anullsrc=channel_layout=stereo:sample_rate=48000",
            ])
    command.extend([
        "-filter_complex",
        filter_graph,
        "-map",
        "[vout]",
        "-map",
        "[aout]",
        "-shortest",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        str(VIDEO_CRF),
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        AUDIO_BITRATE,
        "-movflags",
        "+faststart",
        output_path,
    ])
    return command


def assemble_video(project_dir, test_mode=False, transition_duration=DEFAULT_TRANSITION_DURATION):
    beats_file = os.path.join(project_dir, "beats.json")
    if not os.path.exists(beats_file):
        print(f"[Error] beats.json not found in {project_dir}.", file=sys.stderr)
        sys.exit(1)

    with open(beats_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    clips_dir = os.path.join(project_dir, "clips")
    output_mp4 = os.path.join(project_dir, "final.mp4")
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        raise RuntimeError("Both ffmpeg and ffprobe must be installed and on PATH.")

    shots_to_assemble = []
    for beat in data.get("beats", []):
        for shot in beat.get("shots", []):
            shot_id = shot["shot_id"]
            clip_path = os.path.join(clips_dir, f"{shot_id}.mp4")
            if not os.path.exists(clip_path):
                raise FileNotFoundError(f"Missing clip for {shot_id}: {clip_path}")
            shots_to_assemble.append({
                "id": shot_id,
                "path": clip_path,
                "zoom_impact": shot.get("zoom_impact", False),
                "camera_move": shot.get("camera_move", "static"),
            })

    if not shots_to_assemble:
        raise RuntimeError("No shots found in beats.json.")
    if transition_duration < 0:
        raise ValueError("transition_duration cannot be negative")

    print(f"[Assembly] Beginning FFmpeg final assembly for '{data.get('project_name')}'...")
    print(f"  Total shots: {len(shots_to_assemble)}")

    clip_info = []
    next_input_index = 0
    for shot in shots_to_assemble:
        duration = _duration(ffprobe, shot["path"])
        has_audio = _has_audio(ffprobe, shot["path"])
        info = {
            **shot,
            "duration": duration,
            "has_audio": has_audio,
            "video_index": next_input_index,
        }
        next_input_index += 1
        if has_audio:
            info["audio_index"] = info["video_index"]
        else:
            info["audio_index"] = next_input_index
            next_input_index += 1
        clip_info.append(info)
        impact = " + impact zoom" if shot["zoom_impact"] else ""
        audio_note = "audio" if has_audio else "silent fallback"
        print(f"  - {shot['id']} ({shot['camera_move']}{impact}; {audio_note}; {duration:.2f}s)")

    filter_graph = _build_filter_graph(clip_info, transition_duration)
    temp_output = f"{output_mp4}.tmp.mp4"
    command = _build_ffmpeg_command(ffmpeg, clip_info, filter_graph, temp_output)

    if test_mode:
        print("\n[Assembly test] Filter graph built successfully; ffmpeg execution skipped.")
        return output_mp4

    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        detail = result.stderr.strip() or "unknown ffmpeg error"
        raise RuntimeError(f"FFmpeg assembly failed:\n{detail}")

    os.replace(temp_output, output_mp4)
    print(f"\n[Assembly complete] Final video compiled at: {output_mp4}")
    return output_mp4


def main():
    parser = argparse.ArgumentParser(description="Assemble clips into a Zack D short with transitions")
    parser.add_argument(
        "project_dir",
        nargs="?",
        default="out/swallow_gum",
        help="Project directory containing beats.json and clips/",
    )
    parser.add_argument(
        "--transition-duration",
        type=float,
        default=DEFAULT_TRANSITION_DURATION,
        help="Duration in seconds for each transition (0 disables transitions)",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Build and validate the FFmpeg graph without rendering a file",
    )
    args = parser.parse_args()

    try:
        assemble_video(
            args.project_dir,
            test_mode=args.test_mode,
            transition_duration=args.transition_duration,
        )
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"[Error] {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
