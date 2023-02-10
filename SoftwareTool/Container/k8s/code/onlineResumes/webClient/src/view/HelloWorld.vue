<script setup>
    import { ref } from 'vue'

    const msg = ref('About Vue.js 3.x');
    const count = ref(0)
</script>

<template>
    <h1>{{ msg }}</h1>
    <p>
        Recommended IDE setup:
        <a href="https://code.visualstudio.com/" target="_blank">VS Code</a>
        +
        <a href="https://github.com/johnsoncodehk/volar" target="_blank">Volar</a>
    </p>
    <p>
        <a href="https://vitejs.dev/guide/features.html" target="_blank">
            Vite Documentation
        </a>
        |
        <a href="https://v3.vuejs.org/" target="_blank">Vue 3 Documentation</a>
    </p>
    <button type="button" @click="count++">count is: {{ count }}</button>
</template>

<style scoped>
    a {
    color: #42b983;
    }
</style>
