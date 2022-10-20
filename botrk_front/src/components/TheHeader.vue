<script lang="ts">
    export default {
        name: "TheHeader",
        methods: {
            redirectToHome() {
                window.location.href = "/";
            }
        }
    }
</script>

<template>
    <div class="header_wrapper">
        <div>
            <h1 @click="redirectToHome" class="title">Project BOTRK</h1>
        </div>
    </div>
</template>

<style>
    .header_wrapper {
        height: 10%;
        width: 100%;
        position: absolute;
        top: 0;
        left: 0;

        background: var(--color-background-soft);
        border-radius: 0 0 20px 20px;

        filter: drop-shadow(0px 10px 4px #00000050)
    }

    .title {
        margin-left: 50px;
        width: fit-content;
        cursor: pointer;
    }

</style>
