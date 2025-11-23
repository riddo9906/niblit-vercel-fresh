const fs = require("fs");

class Storage {
    constructor(filename) {
        this.filename = filename;
    }

    loadState() {
        try {
            return JSON.parse(fs.readFileSync(this.filename));
        } catch (e) {
            return {};
        }
    }

    saveState(state) {
        fs.writeFileSync(this.filename, JSON.stringify(state, null, 2));
    }
}

module.exports.Storage = Storage;
