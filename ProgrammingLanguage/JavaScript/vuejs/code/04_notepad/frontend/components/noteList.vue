<template>
    <div id="noteList">
        <ul class="tabs">
            <li v-for="note in noteList" :key="note.id">
                <input type="radio"
                    name="tab-note"
                    id="tabNote"
                    :value="note.title" 
                    v-model="checked" />
                <label for="tabNote">{{ note.title }}</label>
                <div id="tab-note" class="tab-content" v-if="checked == note.title">
                    {{ note.text }}
                </div>
            </li>
            <li>
                <input type="radio"
                    name="tab-note"
                    id="tabNote"
                    value="newNote" 
                    v-model="checked" />
                <label for="tabNote"> 添加笔记 </label>
                <div id="tab-note" class="tab-content" v-if="checked == 'newNote'">
                    <table>
                        <tr>
                            <td>笔记标题：</td>
                            <td><input type="text" /></td>                    
                        </tr>
                        <tr>
                            <td>笔记内容：</td>
                            <td><textarea></textarea></td>
                        </tr>
                    </table>
                </div>
            </li>
        </ul>
    </div>
</template>

<script>
    export default {
        name: "noteList",
        data: function() {
            return {
                noteList: [],
                checked: ''
            };
        },
        created: function() {
            this.initData();
        },
        methods: {
            initData: function() {
                this.noteList.push(
                {
                    id: 1,
                    title: '标题1',
                    text: '内容1'
                },
                {
                    id: 2,
                    title: '标题2',
                    text: '内容2'
                });
                this.checked = this.noteList[0].title;
                console.log(this.checked)
            }
        }
    };
</script>

<style scoped>
</style>