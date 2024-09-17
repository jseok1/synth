function Slider(props) {
  const { label, min, max, value, onChange } = props;

  return (
    <div className="slider">
      <input
        type="range"
        id="freq"
        name="freq"
        min={min}
        max={max}
        step={0.01}
        value={value}
        onChange={onChange}
      />
      <label htmlFor="freq">{label}</label>
    </div>
  );
}

export default Slider;
