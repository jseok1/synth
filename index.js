const core = require("./build/Release/core.node");

core.startStream();
console.log("started");
setTimeout(() => {
  core.stopStream();
}, 3000);
