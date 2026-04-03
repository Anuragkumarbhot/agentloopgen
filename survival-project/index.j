import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { Low } from "lowdb";
import { JSONFile } from "lowdb/node";
import { nanoid } from "nanoid";

const adapter = new JSONFile("survival.json");

const db = new Low(adapter, {
  users: []
});

const app = new Hono();
// Database setup
const adapter = new JSONFile("survival.json");
const db = new Low(adapter);

const app = new Hono();

// Initialize database safely
app.use("*", async (c, next) => {
  await db.read();

  if (!db.data) {
    db.data = {
      users: []
    };
  }

  if (!Array.isArray(db.data.users)) {
    db.data.users = [];
  }

  await db.write();

  await next();
});


// Home route
app.get("/", (c) => {
  return c.text("Server running successfully");
});


// Get all users
app.get("/users", async (c) => {
  await db.read();
  return c.json(db.data.users);
});


// Register user
app.post("/register", async (c) => {
  const body = await c.req.json();

  await db.read();

  const existingUser = db.data.users.find(
    (u) => u.email === body.email
  );

  if (existingUser) {
    return c.json({
      message: "User already exists"
    });
  }

  const newUser = {
    id: nanoid(),
    email: body.email,
    password: body.password
  };

  db.data.users.push(newUser);

  await db.write();

  return c.json({
    message: "Registered successfully"
  });
});


// Login user
app.post("/login", async (c) => {
  const body = await c.req.json();

  await db.read();

  const user = db.data.users.find(
    (u) =>
      u.email === body.email &&
      u.password === body.password
  );

  if (!user) {
    return c.json({
      message: "Invalid credentials"
    });
  }

  return c.json({
    message: "Login successful"
  });
});


// Delete user (Admin)
app.delete("/delete-user/:id", async (c) => {
  const id = c.req.param("id");

  await db.read();

  db.data.users = db.data.users.filter(
    (user) => user.id !== id
  );

  await db.write();

  return c.json({
    message: "User deleted"
  });
});


// Start server
serve({
  fetch: app.fetch,
  port: 5000,
});
