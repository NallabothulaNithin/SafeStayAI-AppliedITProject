import ListingForm from "./components/ListingForm";

function App() {

return (

<div className="container">

<div className="hero">

<h1>🏠 SafeStay AI</h1>

<p>
AI Powered Rental Scam Detection Platform
</p>

</div>

<div className="card">

<h2>Check Rental Listing</h2>

<p className="subtitle">
Enter the listing details below to detect possible scams.
</p>

<ListingForm/>

</div>

<div className="features">

<div className="feature">

<h2>🤖</h2>

<h3>AI Detection</h3>

<p>
Machine Learning detects suspicious listings.
</p>

</div>

<div className="feature">

<h2>🛡️</h2>

<h3>Risk Analysis</h3>

<p>
Get Low, Medium or High Risk scores.
</p>

</div>

<div className="feature">

<h2>🏠</h2>

<h3>Housing Safety</h3>

<p>
Helping students avoid rental scams.
</p>

</div>

</div>

</div>

);

}

export default App;