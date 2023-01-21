<script lang="ts">
import { createPinia } from 'pinia';
import { useScanStore } from '../stores/scan.store';
import router from "vue-router";

    export default {
        name: "Home",
        setup() {
            const portScanReport = useScanStore();
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
                //this.portScanReport.fetchPortScanReport(this.address);
                console.log("Scan")
                this.$router.push('/results')
                await this.portScanReport.fetchDirsearchScanReport(this.address);
                this.portScanReport.fetchBruteForceScanReport();
                this.portScanReport.fetchSQLInjectionScanReport();
            }
        }
    }
</script>

<template>

    <div class="home_wrapper">
        <input 
        v-model="address" 
        placeholder="Enter address here" 
        pattern="http://^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$">
        <br>
        <button @click="scan()">Scan</button>
    </div>

</template>

<style scoped>
    .home_wrapper {
        grid-column-start: 1;
        grid-column-end: -1;

        grid-row-start: 3;

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