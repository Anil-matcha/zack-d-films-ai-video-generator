// Submit and poll a Nano Banana 2.1 text-to-image task through the MuAPI REST API.
// Usage: MUAPI_KEY=... node examples/nano_banana_21.mjs "your prompt"
const BASE_URL = "https://api.muapi.ai/api/v1";
const key = process.env.MUAPI_KEY;
const prompt = process.argv.slice(2).join(" ");
if (!key || !prompt) {
  console.error('Usage: MUAPI_KEY=... node examples/nano_banana_21.mjs "your prompt"');
  process.exit(1);
}

const headers = { "x-api-key": key, "Content-Type": "application/json" };

async function call(url, options = {}) {
  const response = await fetch(url, { headers, ...options });
  if (!response.ok) throw new Error(`HTTP ${response.status}: ${await response.text()}`);
  return response.json();
}

const submitted = await call(`${BASE_URL}/nano-banana-2-1`, {
  method: "POST",
  body: JSON.stringify({ prompt, aspect_ratio: "1:1", resolution: "2k" }),
});
const id = submitted.request_id;
if (!id) throw new Error(`No request_id in response: ${JSON.stringify(submitted)}`);
console.log(`Submitted request: ${id}`);

for (let attempt = 0; attempt < 120; attempt++) {
  const result = await call(`${BASE_URL}/predictions/${id}/result`);
  const status = String(result.status ?? "").toLowerCase();
  if (["completed", "succeeded", "success"].includes(status)) {
    for (const output of [].concat(result.outputs ?? result.output ?? [])) {
      console.log(typeof output === "string" ? output : output.url);
    }
    process.exit(0);
  }
  if (["failed", "error", "cancelled", "canceled"].includes(status)) {
    console.error(`Task ended with status ${status}`, result);
    process.exit(1);
  }
  console.log(`Status: ${status || "pending"}`);
  await new Promise((resolve) => setTimeout(resolve, 5000));
}
throw new Error(`Request ${id} did not finish in time`);
