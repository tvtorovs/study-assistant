<script setup>
import { getSessions, getModules, getStats } from "./api.js";
import { ref, watch, onMounted } from "vue";
import SessionForm from "./components/SessionForm.vue";
import SessionList from "./components/SessionList.vue";
import StatsChart from "./components/Stats.vue";

// --------------------------------------------------------------------------------------------------------

const sessions = ref([]);
const modules = ref([]);
const stats = ref([]);

const selectedModule = ref("");
const editing = ref(null);

// --------------------------------------------------------------------------------------------------------

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
    sessions.value = await getSessions(selectedModule.value);
  }
  catch (err) {
    console.error("Failed to load sessions:", err);
  }
}

async function loadModules() {
  try {
    modules.value = await getModules();
    if (selectedModule.value && !modules.value.includes(selectedModule.value)) {
      selectedModule.value = "";
    }
  }
  catch (err) {
    console.error("Failed to load modules:", err);
  }
}

async function loadStats() {
  try {
    stats.value = await getStats();
  }
  catch (err) {
    console.error("Failed to load stats: ", err);
  }
}

async function refresh() {
  await loadModules();
  await loadSessions();
  await loadStats();
}

function onSaved() {
  editing.value = null;
  refresh();
}

function onDeleted() {
  editing.value = null;
  refresh();
}

// --------------------------------------------------------------------------------------------------------

onMounted(refresh);
watch(selectedModule, loadSessions);
</script>

// --------------------------------------------------------------------------------------------------------

<template>
  <main class="app">
    <h1>Study Tracker</h1>

    <section class="stats">
      <StatsChart :stats="stats" />
    </section>

    <div class="add_sessions">
      <SessionForm :session="editing" @saved="onSaved" @cancel="editing = null" />
    </div>
    
    <section class="sessions">
      <label>
        Filter:
        <select v-model="selectedModule">
          <option value="">All modules</option>
          <option v-for="m in modules" :key="m" :value="m">{{ m }}</option>
        </select>
      </label>
      <h3>Session History:</h3>
      <SessionList :sessions="sessions" @edit="editing = $event" @deleted="onDeleted" />
    </section>
  </main>
</template>