const express = require("express");
const { spawn } = require("child_process");

const app = express();
app.use(express.json());

app.post("/fetch", (req, res) => {
  const python = spawn("python3", ["enter_point.py"]);

  // Send data to Python via stdin
  python.stdin.write(JSON.stringify(req.body));
  python.stdin.end();

  let result = "";
  python.stdout.on("data", (data) => (result += data));

  python.on("close", () => res.send(result));
  python.stderr.on("data", (err) => res.status(400).send("BAD REQUEST"));
});

app.listen(3000, () => console.log("Server running on port 3000"));
