import { Low } from "lowdb";
import { JSONFile } from "lowdb/node";

// Create adapter
const adapter = new JSONFile("survival.json");

// IMPORTANT: provide default data
const defaultData = {
  users: []
};

const db = new Low(adapter, defaultData);

// Read database
await db.read();

// Write if empty
await db.write();

export default db;
