import { useState } from "react";
import axios from "axios";

function ListingForm() {

  const [form, setForm] = useState({
    title: "",
    rent: "",
    deposit: "",
    description: ""
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async () => {

    try {

      const res = await axios.post(
        "http://localhost:8001/predict",
        form
      );
      console.log("API Response:", res.data);
      console.log(res.data);
      setResult(res.data);

    } catch(error){
        console.log(error.response?.data || error.message);

        alert(
          JSON.stringify(
            error.response?.data || error.message
          )
        );
      }
  };

  return (

    <div>

      <input
        type="text"
        name="title"
        placeholder="Title"
        value={form.title}
        onChange={handleChange}
      />

      <input
        type="number"
        name="rent"
        placeholder="Rent"
        value={form.rent}
        onChange={handleChange}
      />

      <input
        type="number"
        name="deposit"
        placeholder="Deposit"
        value={form.deposit}
        onChange={handleChange}
      />

      <textarea
        name="description"
        placeholder="Description"
        value={form.description}
        onChange={handleChange}
      />

      <button onClick={handleSubmit}>
        Check Fraud
      </button>

      {
        result && (

          <div style={{ marginTop: "20px" }}>

            <h2>{result.risk}</h2>

            <p>
              Fraud Score: {result.fraudScore}
            </p>

            <p>
              Probability: {result.probability}
            </p>

          </div>
        )
      }

    </div>
  );
}

export default ListingForm;