import Rack from "./components/Rack";

function App() {
  const ipcHandle = () => window.electron.ipcRenderer.send("ping");

  return (
    <>
      <Rack />
    </>
  );
}

export default App;
