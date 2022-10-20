<script lang="ts">
    import TheHeader from "./components/TheHeader.vue";

    import Home from "./views/Home.vue";
    import Result from "./views/Result.vue";

    

    const routes : {[key: string]: any}= {
        "/": Home,
        "/results": Result
    }

    export default {
        data() {
            return {
                currentPath: window.location.hash
            };
        },
        computed: {
            currentView() {
                return routes[this.currentPath.slice(1) || "/"];
            }
        },
        mounted() {
            window.addEventListener("hashchange", () => {
                this.currentPath = window.location.hash;
            });
        },
        components: { TheHeader }
}
</script>

<template>
    <TheHeader></TheHeader>
    <component :is="currentView"></component>
</template>

<style>
    @import './assets/base.css';
</style>
