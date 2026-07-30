import { useState } from "react";
import axios from "axios";
import "./App.css";

const initialForm = {
  city: "",
  state: "",
  bedrooms: "",
  bathrooms: "",
  square_feet: "",
  price: "",
};

function App() {
  const [formData, setFormData] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((previousData) => ({
      ...previousData,
      [name]: value,
    }));
  };

  const handleReset = () => {
    setFormData(initialForm);
    setResult(null);
    setError("");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    const requestData = {
      city: formData.city.trim(),
      state: formData.state.trim(),
      bedrooms: Number(formData.bedrooms),
      bathrooms: Number(formData.bathrooms),
      square_feet: Number(formData.square_feet),
      price: Number(formData.price),
    };

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/predict",
        requestData
      );

      setResult(response.data);
    } catch (requestError) {
      console.error(requestError);

      const detail = requestError.response?.data?.detail;

      if (Array.isArray(detail)) {
        setError(detail.map((item) => item.msg).join(", "));
      } else if (detail) {
        setError(detail);
      } else {
        setError(
          "Unable to connect to the backend. Make sure FastAPI is running on port 8000."
        );
      }
    } finally {
      setLoading(false);
    }
  };

  const isUnusual = result?.prediction === "Unusual";

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="topbar-inner">
          <div className="brand">
            <span className="brand-mark">SS</span>
            <span className="brand-name">SafeStay AI</span>
          </div>
          <div className="topbar-tag">Listing Anomaly Detector</div>
        </div>
      </header>

      <main className="app-container">
        <div className="main-card">
          <div className="intake-head">
            <div className="eyebrow">Case intake</div>
            <h1>Check a rental listing.</h1>
            <p className="lede">
              Enter the listing details below. The model compares it against
              comparable local rentals and flags anything statistically
              unusual before you commit to it.
            </p>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-grid">
              <div className="form-group">
                <label htmlFor="city">City</label>
                <input
                  id="city"
                  name="city"
                  type="text"
                  placeholder="Dallas"
                  value={formData.city}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="state">State</label>
                <input
                  id="state"
                  name="state"
                  type="text"
                  placeholder="TX"
                  value={formData.state}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="bedrooms">Bedrooms</label>
                <input
                  id="bedrooms"
                  name="bedrooms"
                  type="number"
                  min="0"
                  max="20"
                  step="0.5"
                  placeholder="2"
                  value={formData.bedrooms}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="bathrooms">Bathrooms</label>
                <input
                  id="bathrooms"
                  name="bathrooms"
                  type="number"
                  min="0"
                  max="20"
                  step="0.5"
                  placeholder="1"
                  value={formData.bathrooms}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="square_feet">Square feet</label>
                <input
                  id="square_feet"
                  name="square_feet"
                  type="number"
                  min="1"
                  placeholder="900"
                  value={formData.square_feet}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="price">Monthly rent</label>
                <div className="prefixed-input">
                  <span className="prefix">$</span>
                  <input
                    id="price"
                    name="price"
                    type="number"
                    min="1"
                    placeholder="1500"
                    value={formData.price}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>
            </div>

            {error && (
              <div className="error-banner">
                <span className="error-mark">!</span>
                <span>{error}</span>
              </div>
            )}

            <div className="button-row">
              <button
                type="button"
                className="btn btn-ghost"
                onClick={handleReset}
                disabled={loading}
              >
                Clear
              </button>

              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? (
                  <span className="btn-loading">
                    <span className="spinner" aria-hidden="true"></span>
                    Checking listing…
                  </span>
                ) : (
                  "Check listing"
                )}
              </button>
            </div>
          </form>

          {result && (
            <div
              className={`result-card ${
                isUnusual ? "unusual-result" : "normal-result"
              }`}
            >
              <div className="result-head">
                <span
                  className={`verdict-stamp ${isUnusual ? "warn" : "ok"}`}
                >
                  {isUnusual ? "Flagged · Review" : "Verified · Normal"}
                </span>
                <h2>
                  {isUnusual ? "Unusual listing" : "Normal listing"}
                </h2>
              </div>

              <p className="recommendation">{result.review_recommendation}</p>

              <div className="result-details">
                <div className="detail-tile">
                  <span>Anomaly score</span>
                  <strong>{Number(result.anomaly_score).toFixed(4)}</strong>
                </div>

                <div className="detail-tile">
                  <span>Local median rent</span>
                  <strong>
                    ${Number(result.local_median_price).toLocaleString()}
                  </strong>
                </div>

                <div className="detail-tile">
                  <span>Price per square foot</span>
                  <strong>
                    ${Number(result.price_per_sqft).toFixed(2)}
                  </strong>
                </div>

                <div className="detail-tile">
                  <span>Comparable listings</span>
                  <strong>
                    {Number(result.comparison_group_size).toLocaleString()}
                  </strong>
                </div>
              </div>

              <div className="reasons">
                <h3>Reasons</h3>
                <ul>
                  {result.reasons.map((reason, index) => (
                    <li key={index}>
                      <span className="reason-mark">•</span>
                      <span>{reason}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="disclaimer">{result.disclaimer}</div>
            </div>
          )}
        </div>
      </main>

      <footer className="app-footer">
        <span className="mono">
          SafeStay AI — statistical listing check, not a guarantee.
        </span>
      </footer>
    </div>
  );
}

export default App;