<script setup>
import { deleteSession } from "../api.js"

defineProps({ sessions: Array });
const emit = defineEmits(["deleted", "edit"]);

async function remove(id) {
    try {
        await deleteSession(id);
        emit("deleted");
    } 
    catch (err) {
        console.error("Delete failed:", err);
    }
}
</script>

<template>
    <p v-if="sessions.length === 0">No sessions yet.</p>
    <ul v-else>
        <li v-for="s in sessions" :key="s.id">
            <strong>{{ s.module }}</strong>: {{ s.topic }}
            ({{ s.minutes }} min, {{ s.date }})
            <button @click="emit('edit', s)">Edit</button>
            <button @click="remove(s.id)">Delete</button>
        </li>
    </ul>
</template>