<template>
    <div>
        <header>
            <slot name="title"></slot>            
        </header>
        <main>
            <slot></slot>
        </main>
    </div>
</template>

<script>
    const box = {
        name: 'box'
    };
    export default box;
</script>

<style scoped>
</style>
