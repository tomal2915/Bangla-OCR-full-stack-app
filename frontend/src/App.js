// App.js

import { useState, useEffect, useCallback } from 'react';
import UploadBox     from './components/UploadBox';
import ResultCard    from './components/ResultCard';
import HistoryTable  from './components/HistoryTable';
import { predictCharacter, fetchHistory } from './api/ocr';
import './App.css';

export default function App() {
  const [selectedFile,  setSelectedFile]  = useState(null);
  const [result,        setResult]        = useState(null);
  const [loading,       setLoading]       = useState(false);
  const [error,         setError]         = useState(null);
  const [history,       setHistory]       = useState([]);
  const [historyLoading,setHistoryLoading]= useState(false);

  // load history on mount
  const loadHistory = useCallback(async () => {
    setHistoryLoading(true);
    try {
      const data = await fetchHistory();
      setHistory(data);
    } catch {
      // history failing silently is fine
    } finally {
      setHistoryLoading(false);
    }
  }, []);

  useEffect(() => { loadHistory(); }, [loadHistory]);

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setResult(null);
    setError(null);
  };

  const handlePredict = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await predictCharacter(selectedFile);
      setResult(data);
      loadHistory(); // refresh history after new prediction
    } catch (err) {
      const msg =
        err.response?.data?.error ||
        'Could not connect to the server. Make sure Django is running.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="app">

      {/* Header */}
      <header className="app-header">
        <h1 className="app-title">বাংলা OCR</h1>
        <p className="app-subtitle">Bangla handwritten character recognition</p>
      </header>

      <main className="app-main">

        {/* Left panel — upload + result */}
        <section className="panel panel-left">
          <h2 className="panel-title">Upload image</h2>

          <UploadBox
            onFileSelect={handleFileSelect}
            loading={loading}
          />

          <div className="action-row">
            <button
              className="btn-predict"
              onClick={handlePredict}
              disabled={!selectedFile || loading}
            >
              {loading ? 'Recognizing...' : 'Recognize character'}
            </button>

            {(selectedFile || result) && (
              <button className="btn-reset" onClick={handleReset}>
                Reset
              </button>
            )}
          </div>

          <ResultCard
            result={result}
            loading={loading}
            error={error}
          />
        </section>

        {/* Right panel — history */}
        <section className="panel panel-right">
          <div className="panel-title-row">
            <h2 className="panel-title">Recent predictions</h2>
            <button className="btn-refresh" onClick={loadHistory}>
              Refresh
            </button>
          </div>

          <HistoryTable
            history={history}
            loading={historyLoading}
          />
        </section>

      </main>
    </div>
  );
}