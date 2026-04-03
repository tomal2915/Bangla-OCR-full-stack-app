import { useState, useCallback } from 'react';
import axios from 'axios';

const API = process.env.REACT_APP_API_URL;

export default function Uploader({ onNewPrediction }) {
  const [file,       setFile]       = useState(null);
  const [preview,    setPreview]    = useState(null);
  const [result,     setResult]     = useState(null);
  const [loading,    setLoading]    = useState(false);
  const [error,      setError]      = useState(null);
  const [dragging,   setDragging]   = useState(false);

  // ── File selection ──────────────────────────────────────
  const handleFile = useCallback((selected) => {
    if (!selected) return;
    const allowed = ['image/png', 'image/jpeg', 'image/bmp'];
    if (!allowed.includes(selected.type)) {
      setError('Please upload a PNG, JPG, or BMP image.');
      return;
    }
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setResult(null);
    setError(null);
  }, []);

  const onInputChange = (e) => handleFile(e.target.files[0]);

  // ── Drag and drop ───────────────────────────────────────
  const onDragOver  = (e) => { e.preventDefault(); setDragging(true);  };
  const onDragLeave = ()  => setDragging(false);
  const onDrop      = (e) => {
    e.preventDefault();
    setDragging(false);
    handleFile(e.dataTransfer.files[0]);
  };

  // ── Submit to Django API ────────────────────────────────
  const handleSubmit = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', file);

    try {
      const res = await axios.post(`${API}/predict/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(res.data);
      onNewPrediction(res.data);   // tell History to refresh
    } catch (err) {
      const msg = err.response?.data?.error || 'Something went wrong. Is Django running?';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
  };

  // ── Confidence colour ───────────────────────────────────
  const confClass = (c) =>
    c >= 80 ? 'conf-high' : c >= 50 ? 'conf-mid' : 'conf-low';

  const formatBytes = (b) =>
    b < 1024 ? b + ' B' : (b / 1024).toFixed(1) + ' KB';

  // ── Render ──────────────────────────────────────────────
  return (
    <div>

      {/* Result banner */}
      {result && (
        <div className="result-card">
          <div className="result-char">{result.predicted}</div>
          <div className="result-details">
            <div className="result-label">Recognised character</div>
            <div className="result-confidence">
              Confidence: <strong>{result.confidence}%</strong>
            </div>
            <div className="conf-bar-bg">
              <div
                className="conf-bar-fill"
                style={{ width: `${result.confidence}%` }}
              />
            </div>
            <span
              className={`conf-pill ${confClass(result.confidence)}`}
              style={{ marginTop: '8px', display: 'inline-block' }}
            >
              {result.confidence >= 80 ? 'High confidence'
                : result.confidence >= 50 ? 'Medium confidence'
                : 'Low confidence'}
            </span>
          </div>
        </div>
      )}

      {/* Error */}
      {error && <div className="error-box">{error}</div>}

      {/* Upload card */}
      <div className="card">
        <div className="card-title">Upload image</div>

        {/* Drop zone — shown when no file selected */}
        {!file && (
          <div
            className={`drop-zone ${dragging ? 'dragging' : ''}`}
            onDragOver={onDragOver}
            onDragLeave={onDragLeave}
            onDrop={onDrop}
          >
            <input
              type="file"
              accept="image/png, image/jpeg, image/bmp"
              onChange={onInputChange}
            />
            <div className="drop-icon">↑</div>
            <div className="drop-text">Click to browse or drag & drop</div>
            <div className="drop-hint">PNG, JPG, BMP supported</div>
          </div>
        )}

        {/* Preview — shown after file selected */}
        {file && (
          <div className="preview-wrap">
            <img
              src={preview}
              alt="preview"
              className="preview-img"
            />
            <div className="preview-info">
              <div className="preview-name">{file.name}</div>
              <div className="preview-size">{formatBytes(file.size)}</div>
              <div>
                <button
                  className="btn btn-primary"
                  onClick={handleSubmit}
                  disabled={loading}
                >
                  {loading
                    ? <><div className="spinner" /> Recognising...</>
                    : '→ Recognise character'}
                </button>
                <button
                  className="btn btn-ghost"
                  onClick={handleClear}
                  disabled={loading}
                >
                  Clear
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}