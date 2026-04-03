import { useEffect, useState } from 'react';
import axios from 'axios';

const API = process.env.REACT_APP_API_URL;

export default function History({ refresh }) {
  const [predictions, setPredictions] = useState([]);
  const [loading,     setLoading]     = useState(true);

  useEffect(() => {
    axios.get(`${API}/predictions/`)
      .then(res => setPredictions(res.data))
      .catch(()  => {})
      .finally(() => setLoading(false));
  }, [refresh]);   // re-fetches every time a new prediction is made

  const confClass = (c) =>
    c >= 80 ? 'conf-high' : c >= 50 ? 'conf-mid' : 'conf-low';

  const formatDate = (iso) =>
    new Date(iso).toLocaleString('en-GB', {
      day: '2-digit', month: 'short',
      hour: '2-digit', minute: '2-digit',
    });

  if (loading) return (
    <div className="card">
      <div className="empty-state">Loading history...</div>
    </div>
  );

  return (
    <div className="card">
      <div className="card-title">Recent predictions</div>
      {predictions.length === 0
        ? <div className="empty-state">No predictions yet — upload an image above.</div>
        : (
          <table className="history-table">
            <thead>
              <tr>
                <th>Image</th>
                <th style={{ textAlign: 'center' }}>Character</th>
                <th>Confidence</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {predictions.map(p => (
                <tr key={p.id}>
                  <td>
                    <img
                      src={p.image}
                      alt="uploaded"
                      className="thumb"
                    />
                  </td>
                  <td className="char-cell">{p.predicted}</td>
                  <td>
                    <span className={`conf-pill ${confClass(p.confidence)}`}>
                      {p.confidence}%
                    </span>
                  </td>
                  <td style={{ color: '#6b6b6b' }}>{formatDate(p.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )
      }
    </div>
  );
}