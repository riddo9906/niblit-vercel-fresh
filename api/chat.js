import fs from "fs";
const STATE_FILE = "/tmp/niblit_state.json";

// Load chat history
let state = { chat_history: [] };
try {
    const data = fs.readFileSync(STATE_FILE, "utf8");
    state = JSON.parse(data);
} catch {}

const args = process.argv.slice(2);
const userMessage = args.join(" ") || "Hello!";

let response = "I am learning...";

try {
    // Simple learning: if message seen before, recall response
    const found = state.chat_history.find(c => c.user === userMessage);
    if (found) {
        response = found.niblit;
    } else {
        // Generate a simple response (replace with AI or GPT model logic later)
        response = `Niblit processed your message: "${userMessage}"`;
        state.chat_history.push({ user: userMessage, niblit: response });
        fs.writeFileSync(STATE_FILE, JSON.stringify(state));
    }
} catch(e){
    response = "Error in chat module";
}

console.log(response);
