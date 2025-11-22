import fs from "fs";

export default function handler(req, res) {
    const data = req.query.data || "No data";

    fs.appendFileSync("/tmp/niblit_custom_evolution.log", `${new Date().toISOString()} - ${data}\n`);

    res.status(200).json({ status: "ok", message: "Evolution updated" });
}
