import { defineStore } from 'pinia';
import axios from "axios";

export const useScanStore = defineStore({
    id: "scan",
    state: () => ({
        open_ports: {} as any,
        nikto_tests_result: [] as Array<String>,
        nikto_report: [] as Array<String>,
        dirsearch_report: {} as any,
        sqli_report: {} as any,
        brute_force_report: {} as any
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
                url: "/dirsearch_scan?hostname=" + hostname,
                method: "GET",
                baseURL: "http://127.0.0.1:5000"
            })

            this.dirsearch_report = res.data;
        },
        async fetchSQLInjectionScanReport() {
            let res = await axios({
                url: "/sqlmap_scan",
                method: "GET",
                baseURL: "http://127.0.0.1:5000"
            })

            this.sqli_report = res.data;
        }
        ,
        async fetchBruteForceScanReport() {
            let res = await axios({
                url: "/brute_force_scan",
                method: "GET",
                baseURL: "http://127.0.0.1:5000"
            })

            this.brute_force_report = res.data;
        }
    }
})