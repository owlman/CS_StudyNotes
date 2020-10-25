<template>
    <div class="box">
        <input type="button" value="-" @click="changeCounter(-1)">
        <input type="text" :value="value" @input="changeInput" />
        <input type="button" value="+" @click="changeCounter(1)">
    </div>
</template>

<script>
    const counter = {
        name: 'counter',
        props : ['value'],
        methods: {
            changeCounter: function(count) {
                this.$emit('input', this.value + count);
            },
            changeInput: function(event) {
                let num = parseInt(event.target.value);
                if(isNaN(num)) {
                    num = 0;
                }
                this.$emit('input', num);
            }
        }
    };
    export default counter;
</script>

<style scoped>
    .box {
        width: 340px;
        padding: 10px;
        background-color: #ccc;
    }
</style>
