<script lang="ts">
import { useScanStore } from '../stores/scan.store';

    export default {
        name: "Result",
        setup() {
            const scanReport = useScanStore();
            return {
                scanReport
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
            <span>Hostname: {{scanReport.nikto_report[1]}}</span>
            <span>IP Address:</span>
            <span>Scan Time:</span>
        </div>
    </div>
    <div class="initial_recap">
        <div class="text-info">
            <h1>Dirsearch scan</h1>
            <p >Scan in progress ...</p>
            <div >
                <p><h3>Scan status:</h3>{{scanReport.dirsearch_report[0]}}</p>
                <h3>Results</h3>
                <div v-for = "url in scanReport.dirsearch_report[1]">
                    {{url}}
                </div>
            </div>
        </div>
    </div>
    <div class="initial_recap">
        <div class="text-info">
            <h1>Bruteforce scan</h1>
            <div v-if="scanReport.brute_force_report[0]">
                <h3>BruteForce scan success, valid credentials are:</h3>
                <p>Username: {{ scanReport.brute_force_report[1][0] }}</p>
                <p>Password: {{ scanReport.brute_force_report[1][1] }}</p>
            </div>
            <p v-else>BruteForce in progress ...</p>
        </div>
    </div>
    <div class="initial_recap">
        <div class="text-info">
            <h1>SQL injection scan</h1>
            <p v-if="!scanReport.sqli_report[0]">Scan in progress ...</p>
            <p v-else-if="!scanReport.sqli_report[0].length ">No SQL Injection vulnerabilities found!</p>
            <div v-else>
                <h2>SQL injection scan success:</h2>
                <h3>Vulnerable URLs:</h3>
                <p v-for="url in scanReport.sqli_report[0]">{{ url }}</p>
                <p v-if="!scanReport.sqli_report[1].length">SQLmap failed to dump the database!</p>
                <div v-else >
                    <h3>SQLmap dumped databases:</h3>
                    <p v-for="dump in scanReport.sqli_report[1]">{{ dump }}</p>
                </div>
            </div>
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
        margin-bottom: 50px
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
        padding: 0 ;
    }

    .text-info span {
        text-decoration: underline;
        margin: 10px;
        display: block;
    }

    .text-info h1 {
        font-weight: bold;
        margin: 10px;
        display: block;
        color: #213547;
    }
</style>