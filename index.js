const apollo = require("./build/Release/apollo.node");

apollo.startStream();
console.log("started")
setTimeout(() => {
  apollo.stopStream();
}, 3000);
