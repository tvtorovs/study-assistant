<script setup>
import { getSessions } from "./api.js";
import { ref, onMounted } from "vue";
import SessionForm from "./components/SessionForm.vue";
import SessionList from "./components/SessionList.vue";

const sessions = ref([]);

async function logSessions() {
  try {
    const sessions = await getSessions();
    console.log(sessions);
  } 
  catch (err) {
    console.error("Failed to load session:", err);
  }
}

async function loadSessions() {
  try {
    sessions.value = await getSessions();
  }
  catch (err) {
    console.error("Failed to load sessions:", err);
  }
}

onMounted(loadSessions);
</script>

<template>
  <h1>Study Tracker</h1>
  <SessionForm @saved="loadSessions" />
  <SessionList :sessions="sessions" @deleted="loadSessions" />
</template>