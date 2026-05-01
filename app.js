const express = require("express");
const { spawn } = require("child_process");

const app = express();
app.use(express.json());

app.post("/fetch", (req, res) => {
  const python = spawn("python3", ["enter-point.py"]);

  python.stdin.write(JSON.stringify(req.body));
  python.stdin.end();

  console.log(JSON.stringify(req.body))

  let result = "";
  let hasResponded = false; // flag to prevent double response

  python.stdout.on("data", (data) => (result += data));

  python.stderr.on("data", (err) => {
    console.error("Python log:", err.toString()); // shows in Render logs
    if (!hasResponded) {
        hasResponded = true;
        res.status(400).send("BAD REQUEST");
    }
  });

  python.on("close", () => {
    if (!hasResponded) {
      hasResponded = true;
      res.send(result);
    }
  });
});

app.listen(3000, () => console.log("Server running on http://localhost:3000"))
