function Slider(props) {
  const { min, max, onChange, label, id } = props;

  return (
    <div className="slider">
      <input type="range" id="freq" name="freq" min={min} max={max} onChange={onChange} />
      <label htmlFor="freq">{label}</label>
    </div>
  );
}

export default Slider;
