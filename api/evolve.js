import fs from "fs";
const STATE_FILE = "/tmp/niblit_state.json";

let state = { version: 1.0 };
try {
    const data = fs.readFileSync(STATE_FILE, "utf8");
    state = JSON.parse(data);
} catch {}

// Evolution: increase version
state.version = (state.version || 1.0) + 0.01;

// Optional: simulate learning from internet (mock)
state.last_learned = `Learned at ${new Date().toISOString()}`;

// Save state
fs.writeFileSync(STATE_FILE, JSON.stringify(state));

console.log(`Niblit evolved to version ${state.version.toFixed(2)} - ${state.last_learned}`);
