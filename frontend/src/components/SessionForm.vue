<script setup>
import { ref } from "vue";
import { addSession } from "../api.js";

const emit = defineEmits(["saved"]);

const emptyForm = () => ({module: "", topic: "", minutes: 30, notes: ""});
const form = ref(emptyForm());
const error = ref("");

async function submit() {
    error.value = "";
    try {
        await addSession(form.value);
        emit("saved");
        form.value = emptyForm();
    }
    catch (err) {
        error.value = "Could not save: " + err.message;
    }
}
</script>

<template>
    <form @submit.prevent="submit">
        <input v-model="form.module" placeholder="Module" required />
        <input v-model="form.topic" placeholder="Topic" required />
        <input v-model.number="form.minutes" type="number" min="1" required />
        <input v-model="form.notes" placeholder="Notes (optional):" />
        <button type="submit">Add sessions</button>
        <p v-if="error">{{ error }}</p>
    </form>
</template>