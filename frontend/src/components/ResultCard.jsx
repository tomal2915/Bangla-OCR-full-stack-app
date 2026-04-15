export default function ResultCard({ result, loading, error }) {
  if (loading) {
    return (
      <div className="result-card loading">
        <div className="spinner" />
        <p className="result-label">Recognizing character...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="result-card error">
        <div className="error-icon">✕</div>
        <p className="result-label">Recognition failed</p>
        <p className="error-msg">{error}</p>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="result-card empty">
        <p className="result-label">Upload an image to see the result</p>
      </div>
    );
  }

  const confidencePct = Math.round(result.confidence * 100);
  const barColor =
    confidencePct >= 80 ? '#1D9E75' :
    confidencePct >= 50 ? '#BA7517' : '#E24B4A';

  return (
    <div className="result-card success">
      <p className="result-label">Recognized character</p>

      <div className="character-display">
        {result.character}
      </div>

      <div className="confidence-section">
        <div className="confidence-row">
          <span className="confidence-label">Confidence</span>
          <span className="confidence-value" style={{ color: barColor }}>
            {confidencePct}%
          </span>
        </div>
        <div className="confidence-bar-bg">
          <div
            className="confidence-bar-fill"
            style={{ width: `${confidencePct}%`, background: barColor }}
          />
        </div>
      </div>
    </div>
  );
}