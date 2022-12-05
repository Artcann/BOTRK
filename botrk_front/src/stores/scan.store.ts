import { defineStore } from 'pinia';
import axios from "axios";

export const useScanStore = defineStore({
    id: "scan",
    state: () => ({
        open_ports: {} as any,
        nikto_tests_result: [] as Array<String>,
        nikto_report: [] as Array<String>,
        dirsearch_report: {} as any
    }),
    actions: {
        async fetchPortScanReport(address: string) {
            let res = await axios({
                url: "/port_scan?hostname=" + address,
                method: 'GET',
                baseURL: "http://127.0.0.1:5000"
            })

            this.open_ports = res.data;
        },
        async fetchNiktoScanReport(hostname: string) {
            let res = await axios({
                url: "/nikto_scan?hostname=" + hostname,
                method: "GET",
                baseURL: "http://127.0.0.1:5000"
            })

            this.nikto_tests_result = res.data[0];
            this.nikto_report = res.data[1];
        },
        async fetchDirsearchScanReport(hostname: string) {
            let res = await axios({
                url: "/dirsearch_scan?hostname=" + hostname + "&id=testweb",
                method: "GET",
                baseURL: "http://127.0.0.1:5000"
            })

            this.dirsearch_report = res.data;
        }
    }
})