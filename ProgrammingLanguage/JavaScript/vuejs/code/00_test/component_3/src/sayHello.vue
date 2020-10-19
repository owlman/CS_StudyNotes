<template>
    <div class="box">
        <h1>你好， {{ you }}！</h1>
        <input type="text" v-model="you" />
    </div>
</template>

<script>
    const sayHello = {
        name: 'sayHello',
        props : ['who'],
        data : function() {
            return {
                you: this.who
            }
        }
    };
    export default sayHello;
</script>

<style scoped>
    .box {
        height: 150px;
        width: 250px;
        background-color: #ccc;
    }
</style>