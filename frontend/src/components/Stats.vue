<script setup>
import { ref, computed } from "vue";
import { Bar, Pie } from "vue-chartjs";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend, } from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend);

const props = defineProps({ stats: { type: Array, default: () => [] }, });

const chartData = computed(() => ({
    labels: props.stats.map((s) => s.module), 
    datasets: [{
        label: "Time studied", 
        data: props.stats.map((s) => s.hours), 
        backgroundColor: props.stats.map((_, i) => colorPalette[i % colorPalette.length]), 
    }], 
}));

const options = computed(() => ({
    responsive: true,
    plugins: {
        legend: {display: chartType.value === "pie" },
        tooltip: {
            callbacks: {
                label: (ctx) => `${ctx.label}: ${formatTime(ctx.raw)}`,
            },
        },
    },
    scales:
        chartType.value === "bar"
         ? {
            y: {
                beginAtZero: true,
                ticks: { callback: (value) => formatTime(value) },
            },
         }
         : {},
}));

const chartType = ref("bar");

const colorPalette = ["#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#edc948", "#b07aa1"]

function formatTime(hours) {
    const totalMin = Math.round(hours * 60);
    if (totalMin < 60) return `${totalMin} min`;
    const h = Math.floor(totalMin / 60);
    const m = totalMin % 60;
    return m === 0 ? `${h} h` : `${h} h ${m} min`;
}

</script>

<template>
    <div class="chart-wrapper">
        <p v-if="stats.length === 0">No session data found.</p>
        <template v-else>
            <div class="toggle">
                <button :class="{ active: chartType === 'bar' }" @click="chartType = 'bar'">Bar</button>
                <button :class="{ active: chartType === 'pie' }" @click="chartType = 'pie'">Pie</button>
            </div>
            <Bar v-if="chartType === 'bar'" :data="chartData" :options="options" />
            <Pie v-else :data="chartData" :options="options" />
        </template>
    </div>
</template>

<style scoped>
.chart-wrapper {
    max-width: 600px;
}
.toggle button.active {
    font-weight: bold;
    text-decoration: underline;
}
</style>