import { useState, useRef } from 'react';

export default function UploadBox({ onFileSelect, loading }) {
  const [dragOver, setDragOver]   = useState(false);
  const [preview, setPreview]     = useState(null);
  const [fileName, setFileName]   = useState('');
  const inputRef                  = useRef();

  const handleFile = (file) => {
    if (!file) return;

    const allowed = ['image/png', 'image/jpeg', 'image/jpg', 'image/bmp'];
    if (!allowed.includes(file.type)) {
      alert('Please upload a PNG, JPG, or BMP image.');
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      alert('File too large. Maximum size is 5MB.');
      return;
    }

    setFileName(file.name);
    setPreview(URL.createObjectURL(file));
    onFileSelect(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    handleFile(e.dataTransfer.files[0]);
  };

  const handleChange = (e) => handleFile(e.target.files[0]);

  return (
    <div className="upload-wrapper">
      <div
        className={`upload-box ${dragOver ? 'drag-over' : ''} ${preview ? 'has-preview' : ''}`}
        onClick={() => !loading && inputRef.current.click()}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
      >
        <input
          ref={inputRef}
          type="file"
          accept="image/png,image/jpeg,image/jpg,image/bmp"
          onChange={handleChange}
          style={{ display: 'none' }}
        />

        {preview ? (
          <div className="preview-container">
            <img src={preview} alt="Preview" className="preview-img" />
            <p className="file-name">{fileName}</p>
          </div>
        ) : (
          <div className="upload-prompt">
            <div className="upload-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
            </div>
            <p className="upload-title">Drop your image here</p>
            <p className="upload-sub">or click to browse — PNG, JPG, BMP up to 5MB</p>
          </div>
        )}
      </div>
    </div>
  );
}