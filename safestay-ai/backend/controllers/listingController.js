const axios = require("axios");

exports.createListing = async (req, res) => {

  try {

    const data = {
      title: req.body.title || "",
      description: req.body.description || "",
      rent: Number(req.body.rent),
      deposit: Number(req.body.deposit)
    };

    const aiResponse = await axios.post(
      "http://localhost:8000/predict",
      data
    );

    res.status(200).json(aiResponse.data);

  } catch (error) {

    console.log(error.message);

    res.status(500).json({
      message: "AI service failed"
    });
  }
};