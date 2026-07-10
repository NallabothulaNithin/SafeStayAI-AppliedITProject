const express = require("express");
const cors = require("cors");
const listingRoutes = require("./routes/listingRoutes");

const app = express();

app.use(cors());

app.use(express.json());

app.get("/", (req, res) => {
  res.send("Backend Running Successfully");
});

app.use("/api/listings", listingRoutes);

app.listen(5001, () => {
  console.log("Backend running on port 5001");
});