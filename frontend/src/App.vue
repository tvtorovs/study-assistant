<script setup>
import { getSessions } from "./api.js";

async function logSessions() {
  try {
    const sessions = await getSessions();
    console.log(sessions);
  } 
  catch (err) {
    console.error("Failed to load session:", err);
  }
}
</script>

<template>
  <h1>Study Tracker</h1>
  <button @click="logSessions">Log sessions</button>
</template>