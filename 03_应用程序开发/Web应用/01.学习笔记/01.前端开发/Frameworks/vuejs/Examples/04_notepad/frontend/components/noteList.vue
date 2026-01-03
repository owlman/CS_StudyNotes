<template>
    <div id="noteList">
        <ul class="tabs notes">
            <li>
                <input type="radio"
                    name="tab-note"
                    id="tabNote"
                    value="newNote" 
                    v-model="checked" />
                <label for="tabNote">添加笔记</label>
                <div id="tab-note" class="tab-content" v-if="checked == 'newNote'">
                    <table>
                        <tr>
                            <td>笔记标题：</td>
                            <td>
                                <input type="text" class="inputText"
                                    v-model="newNoteTitle"/>
                            </td>                    
                        </tr>
                        <tr>
                            <td>笔记内容：</td>
                            <td>
                                <textarea rows="10" class="inputText"
                                    v-model="newNoteText" />
                            </td>
                        </tr>
                        <tr>
                            <td><input type="button" value="保存" @click="addNote"></td>
                            <td><input type="button" value="重置" @click="reset"></td>
                        </tr>
                    </table>
                </div>
            </li>
            <li v-for="note in noteList" :key="note.nid">
                <input type="radio"
                    name="tab-note"
                    id="tabNote"
                    :value="note.title" 
                    v-model="checked" />
                <label for="tabNote">{{ note.title }}</label>
                <div id="tab-note" class="tab-content" v-if="checked == note.title">
                    {{ note.text }}
                    <div id="set">
                        <input type="button" value="删除" @click="deleteNote(note.nid)" />
                    </div>
                </div>
            </li>
        </ul>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "noteList",
        props:['uid'],
        data: function() {
            return {
                noteList: [],
                checked: 'newNote',
                newNoteTitle:'',
                newNoteText:''
            };
        },
        created: function() {
            this.getNotes();
        },
        methods: {
            getNotes: function() {
                const that = this;
                axios.get('/notes/get', {
                    params: { uid : that.uid }
                })
                .then(function(res) {
                    if(res.statusText === 'OK') {
                        that.noteList = res.data;
                    }
                })
                .catch(function(err){
                    window.alert('笔记载入失败！');
                });
            },
            addNote: function() {
                if(this.newNoteTitle === '' || this.newNoteText === '') {
                    window.alert('笔记标题和内容都不能为空！');
                    return false;
                }
                const that = this
                axios.post('/notes/add', {
                    title: that.newNoteTitle,
                    text: that.newNoteText,
                    uid: that.uid
                })
                .then(function(res) {
                    if(res.statusText === 'OK') {
                        that.noteList = res.data;
                    }
                })
                .catch(function(err) {
                    window.alert('添加笔记失败！');
                });
                that.reset();
            },
            deleteNote: function(id) {
                const that = this
                axios.delete('/notes/delete', {
                    params: {
                        nid : id,
                        uid: that.uid
                    }
                })
                .then(function(res) {
                    if(res.statusText === 'OK') {
                        that.noteList = res.data;
                        that.checked = 'newNote';
                    }
                })
                .catch(function(err) {
                    window.alert('删除笔记失败！');
                });
            },
            reset: function() {
                this.newNoteTitle = '';
                this.newNoteText = '';
            }
        }
    };
</script>

<style scoped>
    .inputText {
        width: 650px;
    }

    .notes {
        width: auto;
    }
</style>