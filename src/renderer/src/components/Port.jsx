function InPort(props) {
  const { moduleId, inPortId, label } = props;

  // edit <g>
  return (
    <div className="port in-port" data-module-id={moduleId} data-in-port-id={inPortId}>
      <div className="port-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="45" stroke="#38383b" strokeWidth="5" fill="#e4e4e4" />
          <circle cx="50" cy="50" r="36.5" stroke="#38383b" strokeWidth="5" fill="#e4e4e4" />
          <circle cx="50" cy="50" r="25" fill="#38383b" />
        </svg>
      </div>
      <div className="port-label">{label}</div>
    </div>
  );
}

function OutPort(props) {
  const { moduleId, outPortId, label } = props;

  // edit <g>
  return (
    <div className="port out-port" data-module-id={moduleId} data-out-port-id={outPortId}>
      <div className="port-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="45" stroke="#38383b" strokeWidth="5" fill="#e4e4e4" />
          <circle cx="50" cy="50" r="36.5" stroke="#38383b" strokeWidth="5" fill="#e4e4e4" />
          <circle cx="50" cy="50" r="25" fill="#38383b" />
        </svg>
      </div>
      <div className="port-label">{label}</div>
    </div>
  );
}

export { InPort, OutPort };
