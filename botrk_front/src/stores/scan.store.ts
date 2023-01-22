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
        brute_force_report: {} as any,
        scan_xss_report: {} as any
    }),
    actions: {
        async fetchPortScanReport(address: string) {
            let res = await axios({
                url: "/port_scan?hostname=" + address,
                method: 'GET',
                baseURL: "https://botrk-back.artcann.eu"
            })

            this.open_ports = res.data;
        },
        async fetchNiktoScanReport(hostname: string) {
            let res = await axios({
                url: "/nikto_scan?hostname=" + hostname,
                method: "GET",
                baseURL: "https://botrk-back.artcann.eu"
            })

            this.nikto_tests_result = res.data[0];
            this.nikto_report = res.data[1];
        },
        async fetchDirsearchScanReport(hostname: string) {
            let res = await axios({
                url: "/dirsearch_scan?hostname=" + hostname,
                method: "GET",
                baseURL: "https://botrk-back.artcann.eu"
            })

            this.dirsearch_report = res.data;
        },
        async fetchSQLInjectionScanReport() {
            let res = await axios({
                url: "/sqlmap_scan",
                method: "GET",
                baseURL: "https://botrk-back.artcann.eu"
            })

            this.sqli_report = res.data;
        }
        ,
        async fetchBruteForceScanReport() {
            let res = await axios({
                url: "/brute_force_scan",
                method: "GET",
                baseURL: "https://botrk-back.artcann.eu"
            })

            this.brute_force_report = res.data;
        }
        ,
        async fetchXssScanReport() {
            let res = await axios({
                url: "/xss",
                method: "GET",
                baseURL: "https://botrk-back.artcann.eu"
            })
            
            this.scan_xss_report = res.data;
        }
    }
})