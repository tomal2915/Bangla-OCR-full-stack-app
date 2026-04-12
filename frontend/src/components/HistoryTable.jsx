// HistoryTable.jsx

export default function HistoryTable({ history, loading }) {
  if (loading) {
    return <p className="history-status">Loading history...</p>;
  }

  if (!history || history.length === 0) {
    return <p className="history-status">No predictions yet.</p>;
  }

  return (
    <div className="history-wrapper">
      <table className="history-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Character</th>
            <th>Confidence</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {history.map((item, idx) => {
            const pct = Math.round(item.confidence * 100);
            const color =
              pct >= 80 ? '#1D9E75' :
              pct >= 50 ? '#BA7517' : '#E24B4A';

            return (
              <tr key={item.id}>
                <td className="history-num">{idx + 1}</td>
                <td className="history-char">{item.character}</td>
                <td>
                  <span className="history-badge" style={{ color, background: color + '18' }}>
                    {pct}%
                  </span>
                </td>
                <td className="history-time">
                  {new Date(item.created_at).toLocaleString('en-GB', {
                    day: '2-digit', month: 'short',
                    hour: '2-digit', minute: '2-digit'
                  })}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}