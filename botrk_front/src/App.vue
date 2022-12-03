<script lang="ts">
    import TheHeader from "./components/TheHeader.vue";

    import Home from "./views/Home.vue";
    import Result from "./views/Result.vue";

    

    const routes : {[key: string]: any}= {
        "/": Home,
        "/results": Result
    }

    export default {
        components: { TheHeader }
}
</script>

<template>
    <TheHeader></TheHeader>
    <router-view></router-view>
</template>

<style>
    @import './assets/base.css';
</style>
