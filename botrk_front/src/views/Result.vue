<script lang="ts">
import { useScanStore } from '../stores/scan.store';

    export default {
        name: "Result",
        setup() {
            const portScanReport = useScanStore();
            return {
                portScanReport
            }
        },
    }
</script>

<template>
    <div class="initial_recap">
        <div class="score-recap">
            <span>0/20</span>
        </div>
        <div class="text-info">
            <span>Hostname: {{portScanReport.nikto_report[1]}}</span>
            <span>IP Address:</span>
            <span>Scan Time:</span>
        </div>
        
    </div>
</template>

<style>
    .initial_recap {
        text-align: left;
        background-color: var(--blue-soft);
        padding: 50px;
        border-radius: 20px;
        font-weight: 500;
        font-size: larger;
        display: flex;

        align-items: center;

        grid-column-start: 2;
        grid-column-end: -2;
    }

    .score-recap {
        display: inline-block;
        width: 150px;
        height: 150px;
        background-color: var(--blue);
        
        text-align: center;
        vertical-align: middle;
        border-radius: 20px;
    }

    .score-recap span {
        line-height: 150px;
        font-size: xx-large;
        
    }

    .text-info {
        display: inline-block;
        padding: 0 150px;
    }

    .text-info span {
        text-decoration: underline;
        margin: 10px;
        display: block;
    }
</style>