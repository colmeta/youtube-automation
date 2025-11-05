const API_BASE = window.location.origin;

const storyboardForm = document.getElementById("storyboard-form");
const storyboardResponse = document.getElementById("storyboard-response");

const launchForm = document.getElementById("launch-form");
const launchResponse = document.getElementById("launch-response");
const launchSyncBtn = document.getElementById("launch-sync");

function parseList(input) {
  return input
    .split(/\r?\n|,/)
    .map((line) => line.trim())
    .filter(Boolean);
}

function renderJson(target, data) {
  target.textContent = JSON.stringify(data, null, 2);
}

async function handleStoryboard(event) {
  event.preventDefault();
  const data = new FormData(storyboardForm);
  const prompts = parseList(data.get("prompts"));
  if (prompts.length === 0) {
    storyboardResponse.textContent = "Provide at least one frame prompt.";
    return;
  }

  const negativePrompts = parseList(data.get("negative_prompts") || "");
  const frames = prompts.map((prompt, idx) => {
    const frame = { prompt };
    if (idx < negativePrompts.length) {
      frame.negative_prompt = negativePrompts[idx];
    }
    return frame;
  });

  const payload = {
    project_name: data.get("project_name"),
    reference_images: parseList(data.get("reference_images")),
    frames,
    cfg_scale: Number(data.get("cfg_scale")) || 5,
    steps: Number(data.get("steps")) || 28,
    width: Number(data.get("width")) || 768,
    height: Number(data.get("height")) || 1024,
  };

  storyboardResponse.textContent = "Generating storyboard...";

  try {
    const res = await fetch(`${API_BASE}/api/storyboards`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const json = await res.json();
    renderJson(storyboardResponse, json);
  } catch (error) {
    storyboardResponse.textContent = `Error: ${error.message}`;
  }
}

async function launchCampaign(sync = false) {
  const data = Object.fromEntries(new FormData(launchForm).entries());
  const url = sync ? `${API_BASE}/api/launch/sync` : `${API_BASE}/api/launch`;

  launchResponse.textContent = sync ? "Running campaign..." : "Queuing crew run...";

  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    const json = await res.json();
    renderJson(launchResponse, json);
  } catch (error) {
    launchResponse.textContent = `Error: ${error.message}`;
  }
}

storyboardForm?.addEventListener("submit", handleStoryboard);
launchForm?.addEventListener("submit", (event) => {
  event.preventDefault();
  launchCampaign(false);
});

launchSyncBtn?.addEventListener("click", () => launchCampaign(true));
