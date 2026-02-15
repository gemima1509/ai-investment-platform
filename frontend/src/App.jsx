import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [stock, setStock] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeStock = async () => {
    if (!stock) return;

    try {
      setLoading(true);
      const response = await axios.get(
        `http://127.0.0.1:8000/analyze/${stock}`
      );
      setData(response.data);
    } catch (error) {
      alert("Backend not running or invalid stock");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>AI Investment Intelligence Dashboard</h1>

      <div style={styles.inputContainer}>
        <input
          type="text"
          placeholder="Enter stock symbol (AAPL, GOOGL...)"
          value={stock}
          onChange={(e) => setStock(e.target.value)}
          style={styles.input}
        />
        <button onClick={analyzeStock} style={styles.button}>
          Analyze
        </button>
      </div>

      {loading && <p style={{ color: "yellow" }}>Analyzing stock...</p>}

      {data && (
        <div style={styles.card}>
          <h2>{data.stock} Analysis</h2>
          <p>Current Price: ${data.current_price}</p>
          <p>Predicted Price: ${data.predicted_price}</p>
          <p>Risk: {data.risk}</p>
          <p>Confidence: {data.confidence}</p>
          <h3
            style={{
              color: data.decision === "BUY" ? "lime" : "red",
            }}
          >
            Decision: {data.decision}
          </h3>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    backgroundColor: "#0f172a",
    minHeight: "100vh",
    textAlign: "center",
    color: "white",
    paddingTop: "60px",
  },
  title: {
    fontSize: "36px",
    marginBottom: "40px",
  },
  inputContainer: {
    marginBottom: "30px",
  },
  input: {
    padding: "10px",
    fontSize: "16px",
    width: "250px",
    marginRight: "10px",
    borderRadius: "6px",
    border: "none",
  },
  button: {
    padding: "10px 20px",
    fontSize: "16px",
    borderRadius: "6px",
    border: "none",
    backgroundColor: "#2563eb",
    color: "white",
    cursor: "pointer",
  },
  card: {
    backgroundColor: "#1e293b",
    padding: "30px",
    width: "400px",
    margin: "0 auto",
    borderRadius: "10px",
  },
};

export default App;
