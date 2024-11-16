function Module({ children, ...props }) {
  const { moduleId, setModules, setCables } = props;

  function handleMouseDown(event) {
    setModules((modules) => {
      modules = { ...modules };

      modules[moduleId] = { ...modules[moduleId], isDragging: true };

      return modules;
    });

    setCables((cables) => {
      cables = { ...cables };

      for (const [cableId, cable] of Object.entries(cables)) {
        if (cable.inModuleId === moduleId) {
          cables[cableId] = { ...cable, inIsDragging: true };
        }

        if (cable.outModuleId === moduleId) {
          cables[cableId] = { ...cable, outIsDragging: true };
        }
      }

      return cables;
    });
  }

  return <div onMouseDown={handleMouseDown}>{children}</div>;
}

export default Module;
