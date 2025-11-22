async function sendMessage() {
    const input = document.getElementById("userInput");
    const msg = input.value.trim();
    if (!msg) return;

    addMessage("You: " + msg, "user");
    input.value = "";

    const response = await fetch("/api/chat?msg=" + encodeURIComponent(msg));
    const data = await response.json();

    addMessage("Niblit: " + data.reply, "bot");
}

function addMessage(text, cls) {
    const box = document.getElementById("chat-box");
    const div = document.createElement("div");
    div.className = cls;
    div.innerText = text;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
}
