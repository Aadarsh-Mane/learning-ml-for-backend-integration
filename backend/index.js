import express from "express";
import axios from "axios";
import cors from "cors";
const PORT = 3000;
const app = express();

app.use(express.json());
app.use(cors());

app.post("/recommend", async (req, res) => {
  //   const { movie } = req.body;

  // Here, replace "http://127.0.0.1:5000" with the actual endpoint of your recommendation engine
  // Make sure the recommendation engine is running and accepting POST requests at "/recommend" with a JSON payload containing a "movie" field.

  // Example:
  const movie = "Inception"; // Replace with the actual movie title you want to recommend
  try {
    const response = await axios.post("http://127.0.0.1:5000/recommend", {
      movie,
    });
    console.log(response);
    const recommendations = response.data;

    res.json(recommendations);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
app.listen(PORT, "0.0.0.0", () => {
  console.log(`Server is running on port ${PORT}`);
});
