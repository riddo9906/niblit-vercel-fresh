// Conversational AI with memory
const fs = require("fs");

module.exports.chat = function(input, storage) {
    let memory = storage.loadState() || {};
    memory.history = memory.history || [];
    
    // Save query
    memory.history.push({ query: input, timestamp: new Date().toISOString() });
    
    // Simple logic: echo + remember
    let response = "Niblit remembers: " + input;
    
    storage.saveState(memory);
    return response;
};
