`<template>
    <div class="box">
        <h1>你好， {{ you }}！</h1>
        <input type="text" v-model="you" />
        <input type="button" value="弹出对话框" @click="showMessage">
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
        },
        methods: {
            showMessage: function() {
                this.$emit('show-message', this.who);
            }
        }
    };
    export default sayHello;
</script>

<style scoped>
    .box {
        height: 130px;
        width: 250px;
        background-color: #ccc;
    }
</style>
