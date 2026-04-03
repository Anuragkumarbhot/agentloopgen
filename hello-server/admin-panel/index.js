const express = require("express");
const session = require("express-session");
const mongoose = require("mongoose");
const bcrypt = require("bcryptjs");

const app = express();

/* DATABASE CONNECTION */

mongoose.connect(
"mongodb+srv://aairaanu:mansi1207@cluster0.q04r18b.mongodb.net/adminDB"
)
.then(() => console.log("MongoDB Connected"))
.catch(err => console.log("MongoDB Error:", err));

/* USER MODEL */

const userSchema = new mongoose.Schema({
  username: String,
  password: String,
  role: String
});

const User = mongoose.model("User", userSchema);

/* MIDDLEWARE */

app.use(express.urlencoded({ extended: true }));

app.use(session({
  secret: "secure-secret",
  resave: false,
  saveUninitialized: false
}));

/* CREATE DEFAULT ADMIN */

async function createAdmin() {

  const existing =
    await User.findOne({
      username: "admin"
    });

  if (!existing) {

    const hashed =
      await bcrypt.hash("1234", 10);

    await User.create({
      username: "admin",
      password: hashed,
      role: "admin"
    });

    console.log("Admin user created");

  }

}

createAdmin();

/* LOGIN PAGE */

app.get("/", (req, res) => {

res.send(`
<h2>Login</h2>

<form method="POST" action="/login">

<input name="username" placeholder="Username">

<br><br>

<input type="password"
name="password"
placeholder="Password">

<br><br>

<button>Login</button>

</form>
`);

});

/* LOGIN */

app.post("/login", async (req, res) => {

const user =
await User.findOne({
username: req.body.username
});

if (!user)
return res.send("User not found");

const match =
await bcrypt.compare(
req.body.password,
user.password
);

if (match) {

req.session.user =
user.username;

res.redirect("/dashboard");

} else {

res.send("Wrong password");

}

});

/* DASHBOARD */

app.get("/dashboard", (req, res) => {

if (!req.session.user)
return res.redirect("/");

res.send(`
<h2>Dashboard</h2>

<p>
Welcome ${req.session.user}
</p>

<a href="/logout">
Logout
</a>
`);

});

/* LOGOUT */

app.get("/logout", (req, res) => {

req.session.destroy();

res.redirect("/");

});

/* SERVER */

app.listen(3000, () => {

console.log(
"Server running on http://localhost:3000"
);

});
