<script setup>
import { computed } from "vue";
import { Bar } from "vue-chartjs";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, } from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const props = defineProps({ stats: { type: Array, default: () => [] }, });

const chartData = computed(() => ({labels: props.stats.map((s) => s.module), datasets: [{label: "Hours studied", data: props.stats.map((s) => s.hours), }, ], }));

const options = { responsive: true, scales: {y: {beginAtZero: true, title: { display: true, text: "Hours"} }, }, };
</script>

<template>
    <div class="chart-wrapper">
        <p v-if="stats.length === 0">No session data found.</p>
        <Bar v-else :data="chartData" :options="options" />
    </div>
</template>

<style scoped>
.chart-wrapper {
    max-width: 600px;
}
</style>