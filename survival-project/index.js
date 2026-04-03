import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { Low } from "lowdb";
import { JSONFile } from "lowdb/node";
import { nanoid } from "nanoid";

const adapter = new JSONFile("survival.json");

const db = new Low(adapter, {
  users: []
});

// Initialize database
await db.read();

if (!db.data) {
  db.data = {
    users: []
  };
}

await db.write();

const app = new Hono();

/* ---------------- REGISTER ---------------- */

app.post("/register", async (c) => {
  const { email, password } = await c.req.json();

  if (!email || !password) {
    return c.json({
      error: "Email and password required"
    }, 400);
  }

  await db.read();

  const existingUser = db.data.users.find(
    u => u.email === email
  );

  if (existingUser) {
    return c.json({
      error: "User already exists"
    }, 400);
  }

  const newUser = {
    id: nanoid(),
    email,
    password,
    role: "user"
  };

  db.data.users.push(newUser);

  await db.write();

  return c.json({
    message: "User registered",
    user: newUser
  });
});

/* ---------------- LOGIN ---------------- */

app.post("/login", async (c) => {
  const { email, password } = await c.req.json();

  await db.read();

  const user = db.data.users.find(
    u => u.email === email && u.password === password
  );

  if (!user) {
    return c.json({
      error: "Invalid credentials"
    }, 401);
  }

  return c.json({
    message: "Login successful",
    user
  });
});

/* ---------------- USERS LIST (ADMIN) ---------------- */

app.get("/users", async (c) => {
  await db.read();

  return c.json(db.data.users);
});

/* ---------------- DELETE USER ---------------- */

app.delete("/delete-user/:id", async (c) => {
  const id = c.req.param("id");

  await db.read();

  db.data.users = db.data.users.filter(
    user => user.id !== id
  );

  await db.write();

  return c.json({
    message: "User deleted"
  });
});

/* ---------------- SERVER ---------------- */

serve({
  fetch: app.fetch,
  port: 4000,
});

console.log(
  "Server with JSON database running on port 4000"
);
