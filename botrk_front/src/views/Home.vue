<script lang="ts">
import { createPinia } from 'pinia';
import { useScanStore } from '../stores/scan.store';
import router from "vue-router";
import axios from 'axios';

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
                address: "",
                listenner: ""
            }
        },
        methods: {
            async scan() {
                //this.portScanReport.fetchPortScanReport(this.address);
                console.log("Scan")
                this.$router.push('/results')
                if(this.listenner !== "") {
                    const address = this.listenner.split(":")[0]
                    const port = this.listenner.split(":")[1]

                    axios({
                        url: "/reverse_shell?listenner_url=" + address + "&listenner_port=" + port,
                        method: "GET",
                        baseURL: "http://127.0.0.1:5000"
                    })
                }
                await this.portScanReport.fetchDirsearchScanReport(this.address);
                this.portScanReport.fetchXssScanReport();
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
        <label for="listenner">(Optionnal) Address and port of the reverse shell listenner :</label>
        <input 
        v-model="listenner" 
        placeholder="127.0.0.1:4242" 
        pattern="http://^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        name="listenner">
        
        <button @click="scan()">Scan</button>
    </div>

</template>

<style scoped>
    .home_wrapper {
        grid-column-start: 1;
        grid-column-end: -1;

        grid-row-start: 3;

        display: block;
    }

    input {
        background-color: white;
        color: #000000;
        border: none;
        border-radius: 10px;
        padding: 15px;
        width: 75%;
        font-size: 30px;
        
        display: block;
        margin: 0px auto 25px auto;
    }

    button {
        background-color: var(--color-button);
        font-size: 25px;
        padding: 15px 75px;
        margin-top: 25px;
        border-radius: 15px;
        display: block;
        margin: 0px auto 0px auto;
    }

    label {
        font-size: 24px;
        display: block;
        margin-bottom: 15px;
    }
</style>