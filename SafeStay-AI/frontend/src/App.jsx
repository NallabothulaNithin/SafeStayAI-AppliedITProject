import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";
const initialForm = { city: "", state: "", bedrooms: "", bathrooms: "", square_feet: "", price: "" };

function Header({ page, setPage, adminToken, onLogout }) {
  return (
    <header className="topbar">
      <div className="topbar-inner wide">
        <button className="brand brand-button" onClick={() => setPage("checker")}>
          <span className="brand-mark">SS</span><span className="brand-name">SafeStay AI</span>
        </button>
        <nav className="nav-actions">
          <button className={page === "checker" ? "nav-link active" : "nav-link"} onClick={() => setPage("checker")}>Listing checker</button>
          <button className={page !== "checker" ? "nav-link active" : "nav-link"} onClick={() => setPage(adminToken ? "dashboard" : "login")}>Admin</button>
          {adminToken && <button className="nav-link logout" onClick={onLogout}>Log out</button>}
        </nav>
      </div>
    </header>
  );
}

function ListingChecker() {
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
    <main className="app-container">
            <section className="info-section">
              <div className="section-head">
                <div className="eyebrow">The process</div>
                <h2>How the check works</h2>
                <p>No listing is saved or shared. The check runs against comparable local rentals only.</p>
              </div>
              <div className="steps">
                <div className="step">
                  <div className="num mono">01</div>
                  <h3>Enter the details</h3>
                  <p>City, state, bedrooms, bathrooms, square footage, and monthly rent — the same facts on any listing.</p>
                </div>
                <div className="step">
                  <div className="num mono">02</div>
                  <h3>Compared to local rentals</h3>
                  <p>The model pulls comparable listings in the same area and checks where this one falls against them.</p>
                </div>
                <div className="step">
                  <div className="num mono">03</div>
                  <h3>Get a clear verdict</h3>
                  <p>A plain result — Normal or Unusual — with the specific reasons behind the score, not just a number.</p>
                </div>
              </div>
            </section>
    
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
    
            <section className="info-section">
              <div className="section-head">
                <div className="eyebrow">Built for</div>
                <h2>People renting under pressure, from a distance</h2>
                <p>Scammers and inflated listings both target the moment someone can't view a place in person.</p>
              </div>
              <div className="persona-grid">
                <div className="case-file">
                  <div className="tab">Case 01</div>
                  <h3>Yousuf, 23</h3>
                  <div className="role">International Master's student</div>
                  <div className="field">
                    <label>Goal</label>
                    <div>Find verified housing before the semester starts, without visiting the city first.</div>
                  </div>
                  <div className="field">
                    <label>Frustration</label>
                    <div>Can't tell a fair listing from an inflated or fake one.</div>
                  </div>
                </div>
    
                <div className="case-file">
                  <div className="tab">Case 02</div>
                  <h3>Arun Kumar, 22</h3>
                  <div className="role">Working professional, relocating for a job</div>
                  <div className="field">
                    <label>Goal</label>
                    <div>Secure housing fast, near work, without overpaying on a tight deadline.</div>
                  </div>
                  <div className="field">
                    <label>Frustration</label>
                    <div>Tight timeline makes it tempting to skip due diligence and just sign.</div>
                  </div>
                </div>
    
                <div className="case-file">
                  <div className="tab">Case 03</div>
                  <h3>Zaplin, 27</h3>
                  <div className="role">Opportunity Card holder</div>
                  <div className="field">
                    <label>Goal</label>
                    <div>Find affordable, verified housing while managing a language barrier.</div>
                  </div>
                  <div className="field">
                    <label>Frustration</label>
                    <div>Delayed landlord responses and unclear terms make listings hard to judge.</div>
                  </div>
                </div>
              </div>
            </section>
          </main>
  );
}

function AdminLogin({ onLogin }) {
  const [credentials, setCredentials] = useState({ username: "", password: "" });
  const [error, setError] = useState(""); 
  const [loading, setLoading] = useState(false);
  const submit = async (event) => 
    { event.preventDefault(); 
        setLoading(true); 
        setError(""); 
        try { const { data } = await axios.post(`${API_URL}/admin/login`, credentials); 
        onLogin(data.access_token); 
    } 
    catch (err) 
    { 
        setError(err.response?.data?.detail || "Login failed. Check that the backend is running."); 

    } 
    finally { setLoading(false); } };
  return <main className="login-page">
    <section className="login-card">
        <div className="login-icon">SS</div>
        <div className="eyebrow">Restricted area</div>
        <h1>Admin login</h1>
        <p>Sign in to view model statistics, evaluation charts, EDA figures, and project screenshots.</p>
        <form onSubmit={submit}>
            <div className="form-group">
                <label>Username</label>
                <input value={credentials.username} onChange={(e) => 
                setCredentials({...credentials, username:e.target.value}
                )} autoComplete="username" required /></div>
                <div className="form-group">
                    <label>Password</label>
                    <input type="password" value={credentials.password} onChange={(e) => 
                    setCredentials({...credentials, password:e.target.value})} autoComplete="current-password" required />
                    </div>{error && <div className="error-banner">{error}</div>
                    }
                    <button className="btn btn-primary login-button" disabled={loading}>{loading ? "Signing in…" : "Sign in to dashboard"}</button>
                    </form>
                    </section>
                    </main>;
}

function DistributionChart({ data }) {
  const max = Math.max(...data.map((item) => item.value), 1);
  return <div className="bar-chart">{data.map((item) => 
  <div className="bar-row" key={item.label}>
    <div className="bar-label">
        <span>{item.label}</span>
        <strong>{item.value.toLocaleString()}</strong>
        </div>
        <div className="bar-track">
            <div className={`bar-fill ${item.label.toLowerCase()}`} style={{width:`${(item.value/max)*100}%`}} /></div>
            </div>
            )}
        </div>;
}

function AdminDashboard({ token, onExpired }) {
  const [dashboard, setDashboard] = useState(null); 
  const [error, setError] = useState(""); 
  const [category, setCategory] = useState("All"); 
  const [selected, setSelected] = useState(null);
  useEffect(() => { 
    axios.get(`${API_URL}/admin/dashboard`, 
        {headers:{Authorization:`Bearer ${token}`}}).then(({data}) => setDashboard(data)).catch((err) => 
            { if (err.response?.status === 401) onExpired(); 
                else setError(err.response?.data?.detail || "Could not load dashboard data."); 
            }); 
        }, 
        [token, onExpired]);
  const categories = useMemo(() => 
    dashboard ? ["All", ...new Set(dashboard.images.map((image) => image.category))] : ["All"], [dashboard]);
  const images = dashboard?.images.filter((image) => category === "All" || image.category === category) || [];
  if (error) 
    return <main className="dashboard-shell">
        <div className="error-banner">{error}</div>
        </main>;
  if (!dashboard) 
    return <main className="dashboard-shell">
        <div className="loading-panel">Loading admin dashboard…</div>
        </main>;
  const m = dashboard.metrics;
  return <main className="dashboard-shell">
    <div className="dashboard-head"><div>
        <div className="eyebrow">Admin workspace</div>
        <h1>Model analytics dashboard</h1>
        <p>Monitor the trained model, prediction distribution, EDA outputs, evaluation graphs, and application evidence.</p>
        </div>
        <span className="status-pill">
            <i /> API connected</span>
            </div>
    <section className="metric-grid">
        {
        [["Model",m.model],
        ["Dataset rows",m.dataset_rows.toLocaleString()],
        ["Features",m.features],
        ["Unusual rate",`${m.unusual_rate}%`],
        ["Predictions",m.total_predictions.toLocaleString()],
        ["Visual assets",m.graph_count]].map(([label,value]) => 
        <article className="metric-card" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
            </article>
        )}
        </section>
    <section className="dashboard-panel overview-grid">
        <div>
            <div className="panel-title"><div>
                <span className="eyebrow">Evaluation</span>
                <h2>Prediction distribution</h2>
                </div>
                <span className="mini-badge">Contamination {(m.contamination*100).toFixed(0)}%</span>
                </div><DistributionChart data={dashboard.prediction_distribution} /></div>
                <div className="summary-stack">
                    <div className="summary-card normal">
                        <span>Normal listings</span>
                        <strong>{m.normal_predictions.toLocaleString()}</strong>
                        <small>Accepted as typical patterns</small>
                        </div>
                        <div className="summary-card unusual">
                            <span>Unusual listings</span>
                            <strong>{m.unusual_predictions.toLocaleString()}</strong>
                            <small>Flagged for manual review</small>
                        </div>
                    </div>
                </section>
    <section className="gallery-section">
        <div className="gallery-heading"><div>
            <span className="eyebrow">Reports gallery</span>
            <h2>All project pictures and graphs</h2>
            <p>Click any image to open a larger preview.</p>
            </div>
            <div className="filter-row">{categories.map((item) => 
                <button key={item} className={category === item ? "filter active" : "filter"} onClick={() => 
                setCategory(item)
                }>{item}
                </button>
            )}
            </div>
            </div>
            <div className="image-grid">{images.map((image) => 
                <button className="image-card" key={image.url} onClick={() => 
                setSelected(image)}>
                    <div className="image-frame">
                        <img src={`${API_URL}${image.url}`} alt={image.title} loading="lazy" />
                        </div>
                        <div className="image-meta">
                            <span>{image.category}</span>
                            <strong>{image.title}</strong>
                        </div>
                </button>)}</div></section>
    {selected && <div className="modal-backdrop" onClick={() => 
        setSelected(null)}>
            <div className="image-modal" onClick={(e) => e.stopPropagation()}>
                <button className="modal-close" onClick={() => setSelected(null)}>×</button>
                <img src={`${API_URL}${selected.url}`} alt={selected.title}/>
                <div>
                    <span>{selected.category}</span>
                    <h3>{selected.title}</h3>
                    </div>
                    </div>
                    </div>
                    }
  </main>;
}

function App() {
  const [page, setPage] = useState("checker");
  const [adminToken, setAdminToken] = useState(() => sessionStorage.getItem("safestay_admin_token") || "");
  const login = (token) => { sessionStorage.setItem("safestay_admin_token", token); setAdminToken(token); setPage("dashboard"); };
  const logout = () => { sessionStorage.removeItem("safestay_admin_token"); setAdminToken(""); setPage("login"); };
  return <div className="app-shell"><Header page={page} setPage={setPage} adminToken={adminToken} onLogout={logout}/>{page === "checker" && <ListingChecker/>}{page === "login" && <AdminLogin onLogin={login}/>} {page === "dashboard" && (adminToken ? <AdminDashboard token={adminToken} onExpired={logout}/> : <AdminLogin onLogin={login}/>) }<footer className="app-footer"><span className="mono">SafeStay AI — statistical listing check, not a guarantee.</span></footer></div>;
}

export default App;