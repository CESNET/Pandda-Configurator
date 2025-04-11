<script setup>
import { defineProps, onMounted, onUpdated } from 'vue';
import enableTooltips from '@/models/tooltipHandler';
import tooltips from '@/models/tooltips';

const props = defineProps({
    tooltipKey: {
        type: String,
        required: true
    }
});

const message = tooltips[props.tooltipKey];

onMounted(async () => {
    enableTooltips();
});

onUpdated(async () => {
    enableTooltips();
});
</script>

<template>
    <span class="input-group-text rounded-end label label-default" data-toggle="tooltip" data-placement="top"
        :title="message">
        <i class="bi bi-info-circle"></i>
    </span>
</template>
