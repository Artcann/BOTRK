<script lang="ts">
    export default {
        name: "Home",
    }
</script>

<template>

    <div class="home_wrapper">
        <input placeholder="Enter address here">
        <br>
        <button>Scan</button>
    </div>

</template>

<style scoped>
    .home_wrapper {
        width: 100%;
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