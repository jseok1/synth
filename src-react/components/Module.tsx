import { ReactElement } from "react";
import Rack from "./Rack";

function Module({ children, ...props }): ReactElement | null {
  const { moduleId, isDragging, setRack } = props;

  function handleMouseDown(event: MouseEvent): void {
    setRack(({ modules, cables }: Rack): Rack => {
      modules = { ...modules };

      modules[moduleId] = { ...modules[moduleId], isDraggable: true };

      return { modules, cables };
    });
  }

  return (
    <div className={isDragging ? "is-dragging" : ""} onMouseDown={handleMouseDown}>
      {children}
    </div>
  );
}

export default Module;
