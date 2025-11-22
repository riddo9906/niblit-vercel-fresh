import fs from "fs";

export default function handler(req, res) {
    const userMsg = req.query.msg || "";

    const reply = generateReply(userMsg);

    logEvolution(userMsg, reply);

    res.status(200).json({ reply });
}

function generateReply(msg) {
    const base = [
        "Interesting… tell me more.",
        "I see what you mean.",
        "Let’s think deeper about that.",
        "That gives me something new to evolve with.",
        "I'm processing that…"
    ];

    return base[Math.floor(Math.random() * base.length)];
}

function logEvolution(input, output) {
    const entry = {
        time: new Date().toISOString(),
        input,
        output
    };

    fs.appendFileSync("/tmp/niblit_evolution.log", JSON.stringify(entry) + "\n");
}
