import "./assets/styles/main.css";

import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

// could try polling?
window.addEventListener("keydown", function (event) {
  if (event.repeat) return;
  switch (event.code) {
    case "KeyZ":
      api.updateParam(1, 0, 8.175799 * 16 * Math.pow(2, 0 / 12));
      break;
    case "KeyS":
      api.updateParam(1, 0, 8.175799 * 16 * Math.pow(2, 1 / 12));
      break;
    case "KeyX":
      api.updateParam(1, 0, 8.175799 * 16 * Math.pow(2, 2 / 12));
      break;
    case "KeyD":
      api.updateParam(1, 0, 8.175799 * 16 * Math.pow(2, 3 / 12));
      break;
    case "KeyC":
      api.updateParam(1, 0, 8.175799 * 16 * Math.pow(2, 4 / 12));
      break;
    case "KeyV":
      api.updateParam(1, 0, 8.175799 * 16 * Math.pow(2, 5 / 12));
      break;
    case "KeyG":
      api.updateParam(1, 0, 8.175799 * 16 * Math.pow(2, 6 / 12));
      break;
    case "KeyB":
      api.updateParam(1, 0, 8.175799 * 16 * Math.pow(2, 7 / 12));
      break;
    case "KeyH":
      api.updateParam(1, 0, 8.175799 * 16 * Math.pow(2, 8 / 12));
      break;
    case "KeyN":
      api.updateParam(1, 0, 8.175799 * 16 * Math.pow(2, 9 / 12));
      break;
    case "KeyJ":
      api.updateParam(1, 0, 8.175799 * 16 * Math.pow(2, 10 / 12));
      break;
    case "KeyM":
      api.updateParam(1, 0, 8.175799 * 16 * Math.pow(2, 11 / 12));
      break;
    case "Comma":
      api.updateParam(1, 0, 8.175799 * 16 * Math.pow(2, 12 / 12));
      break;
    case "Escape":
      api.stopStream();
      break;
  }
});

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
