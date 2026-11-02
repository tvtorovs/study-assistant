<script setup>
import { ref, watch } from "vue";
import { addSession, updateSession } from "../api.js";

// --------------------------------------------------------------------------------------------------------

const props = defineProps({session: {type: Object, default: null}, })
const emit = defineEmits(["saved"]);

const emptyForm = () => ({module: "", topic: "", minutes: 30, notes: ""});
const form = ref(emptyForm());
const error = ref("");

// --------------------------------------------------------------------------------------------------------

watch( () => props.session, (s) => { form.value = s ? { ...s } : emptyForm()}, {immediate: true} );

async function submit() {
    error.value = "";
    try {
        if (props.session) {
            await updateSession(props.session.id, form.value);
        } else {
            await addSession(form.value);
        }
        emit("saved");
        form.value = emptyForm();
    }
    catch (err) {
        error.value = "Could not save: " + err.message;
    }
}
</script>

// --------------------------------------------------------------------------------------------------------

<template>
    <form @submit.prevent="submit">
        <h2>{{  session ? "Edit session" : "Add session" }}</h2>
        <input v-model="form.module" placeholder="Module" required />
        <input v-model="form.topic" placeholder="Topic" required />
        <input v-model.number="form.minutes" type="number" min="1" required />
        <input v-model="form.notes" placeholder="Notes (optional):" />
        <button type="submit">{{ session ? "Save changes" : "Add session" }}</button>
        <button v-if="session" type="button" @click="emit('cancel')">Cancel</button>
        <p v-if="error">{{ error }}</p>
    </form>
</template>