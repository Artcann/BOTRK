import { defineStore } from 'pinia';
import axios from "axios";

export const usePortScanStore = defineStore({
    id: "portScan",
    state: () => ({
        open_ports: {} as any
    }),
    actions: {
        async fetchPortScanReport(address: string) {
            let res = await axios({
                url: "/port_scan/" + address,
                method: 'GET',
                baseURL: "http://127.0.0.1:5000"
            })

            this.open_ports = res.data;
        }
    }
})