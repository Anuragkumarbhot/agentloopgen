cat > index.js << 'EOF'import { Hono } from "hono"; import 
{ serve } from "@hono/node-server"; import { Low } from 
"lowdb"; import { JSONFile } from "lowdb/node"; import { 
Hono } from "hono"; import { serve } from 
"@hono/node-server";// Setup database const adapter = new 
JSONFile("db.json"); const db = new Low(adapter, { users: 
[] });

// Initialize database
const app = new Hono();await db.read(); db.data ||= { 
users: [] };

const app = new Hono(); app.get("/", (c) => { return 
  c.text("Server running successfully");// Home route
});app.get("/", (c) => {
  return c.text("Server running successfully"); serve({}); 
  fetch: app.fetch, port: 3000,// Add user
});app.post("/add-user", async (c) => {
EOF const body = await c.req.json();

  await db.read(); D ^C db.data.users.push({ nano index.js 
id: Date.now(),
    name: body.name, age: body.age, serve({ }); fetch: 
  app.fetch, await db.write(); port: 4000, return c.json({
}); message: "User added successfully",
  });
});

// Get users
app.get("/users", async (c) => {
  await db.read();
  return c.json(db.data.users);
});

// Delete user
app.delete("/delete-user/:id", async (c) => {
  const id = parseInt(c.req.param("id"));

  await db.read();

  db.data.users = db.data.users.filter(
    (user) => user.id !== id
  );

  await db.write();

  return c.json({
    message: "User deleted successfully",
  });
});

console.log("Server with JSON database running on port 4000");

serve({
  fetch: app.fetch,
  port: 4000,
});
