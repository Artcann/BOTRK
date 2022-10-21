<script lang="ts">
import { createPinia } from 'pinia';
import { usePortScanStore } from '../stores/portScan.store';

    export default {
        name: "Home",
        setup() {
            const portScanReport = usePortScanStore();
            return {
                portScanReport
            }
        },
        data() {
            return {
                address: ""
            }
        },
        methods: {
            async scan() {
                this.portScanReport.fetchPortScanReport(this.address);

                //window.location.href = "/results"
            }
        }
    }
</script>

<template>

    <div class="home_wrapper">
        <input v-model="address" placeholder="Enter address here">
        <br>
        <button @click="scan()">Scan</button>
    </div>

</template>

<style scoped>
    .home_wrapper {
        width: 100%;
    }

    input {
        background-color: white;
        color: #000000;
        border: none;
        border-radius: 10px;
        padding: 15px;
        width: 75%;
        font-size: 30px;
        margin-bottom: 25px;
    }

    button {
        background-color: var(--color-button);
        font-size: 25px;
        padding: 15px 75px;
        margin-top: 25px;
        border-radius: 15px;
    }
</style>