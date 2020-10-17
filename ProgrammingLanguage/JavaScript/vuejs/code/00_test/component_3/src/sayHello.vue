<template>
    <div>
        <h1>你好， {{ you }}！</h1>
        <input type="text" v-model="you" />
    </div>
</template>

<script>
    export default {
        name: 'sayHello',
        props : ['who'],
        data : function() {
            return {
                you: this.who
            }
        }
    };
</script>

<style>
    /* 如有必要还可以设置一些样式 */
</style>