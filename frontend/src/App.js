import { useState } from 'react';
import Uploader from './components/Uploader';
import History  from './components/History';

export default function App() {
  // Each new prediction increments this — History watches it
  // to know when to re-fetch from Django
  const [refreshKey, setRefreshKey] = useState(0);

  const handleNewPrediction = () => setRefreshKey(k => k + 1);

  return (
    <div className="app">
      <div className="app-header">
        <h1>বাংলা OCR — Bangla handwritten text recognition</h1>
        <p>Upload a handwritten Bangla character image to recognise it</p>
      </div>

      <Uploader onNewPrediction={handleNewPrediction} />
      <History  refresh={refreshKey} />
    </div>
  );
}