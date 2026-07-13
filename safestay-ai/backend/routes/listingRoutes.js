const express = require("express");
const router = express.Router();

router.post("/create", (req, res) => {
    const { title, rent, deposit, description } = req.body;

    res.json({
        risk_level: "Low Risk",
        fraud_score: 12,
        probability: "8%",
        message: "Safe listing",
        received: {
            title,
            rent,
            deposit,
            description
        }
    });
});

module.exports = router;