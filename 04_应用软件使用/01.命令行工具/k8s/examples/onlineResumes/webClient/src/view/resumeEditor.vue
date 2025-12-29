<script setup>
    import axios from 'axios';
    import { reactive, ref } from 'vue';
    import { useRoute, useRouter } from 'vue-router';
    import { useStore } from 'vuex';

    axios.defaults.withCredentials = true;

    const store = useStore();
    const router = useRouter();
    const route = useRoute();
    
    const title = ref('');
    const resumeData = reactive({
        'name' : '',
        'gender' : '',
        'age' : '',
        'email' : '',
        'phone' : '',
        'education' : [],
        'professional' : []
    });
    const eduData = reactive({
        'school' : '',
        'major' : '',
        'degree' : '',
        'graduation' : ''
    });
    const profData = reactive({
        'company' : '',
        'title' : '',
        'startingDate' : '',
        'endingDate' : ''
    });

    const vEditorDirective = {
        beforeMount: async function() {
            const cv_id = route.params.cv_id;
            if(cv_id == 'newresume') {
                title.value = '添加新的简历';
                resumeData.uid = Number(store.getters.UID);
                resumeData.gender = '男';
            } else if(isNaN(cv_id) == false) {
                title.value = '修改你的简历'
                try {
                    const res = await axios.get('/resumes/'+cv_id);
                    if(res.status == 200) {
                        resumeData.name = res.data[0].name;
                        resumeData.gender = res.data[0].gender;
                        resumeData.age = res.data[0].age;
                        resumeData.email = res.data[0].email;
                        resumeData.phone = res.data[0].phone; 
                        for(let i = 0; i < res.data[0].education.length; ++i) {
                            const tmp ={
                                'school' : res.data[0].education[i].school,
                                'major' : res.data[0].education[i].major,
                                'degree' : res.data[0].education[i].degree,
                                'graduation' : res.data[0].education[i].graduation
                            };
                            resumeData.education.push(tmp);
                        }
                        for(let i = 0; i < res.data[0].professional.length; ++i) {
                            const tmp ={
                                'company' : res.data[0].professional[i].company,
                                'title' : res.data[0].professional[i].title,
                                'startingDate' : res.data[0].professional[i].startingDate,
                                'endingDate' : res.data[0].professional[i].endingDate
                            };
                            resumeData.professional.push(tmp);
                        }
                    }
                } catch (error) {
                    if(error.response) {
                        window.alert(error.response.data.message);
                    }
                }
            }
        }
    }

    function addEdu() {
        // 此处省略了输入检查
        const tmp = Object.assign({}, eduData)
        resumeData.education.push(tmp);
        resetEdu();
    }
    function deleteEdu(index) {
        resumeData.education.splice(index, 1);
    }
    function resetEdu() {
        eduData.school = '';
        eduData.major = '';
        eduData.degree = '';
        eduData.graduation = '';
    }
    function addProf() {
        // 此处省略了输入检查
        const tmp = Object.assign({}, profData)
        resumeData.professional.push(tmp);
        resetProf();
    }
    function deleteProf(index) {
        resumeData.professional.splice(index, 1);
    }
    function resetProf() {
        profData.company = '';
        profData.title = '';
        profData.startingDate = '';
        profData.endingDate = '';
    }

    async function submitData() {
        // 此处省略了输入检查
        try {
            const cv_id = route.params.cv_id;
            let res = [];
            if(cv_id == 'newresume') {
                res = await axios.post(`/resumes/newresume`, resumeData);
            } else if(isNaN(cv_id) == false) {
                res = await axios.put(`/resumes/`+cv_id, resumeData);
            } else {
                window.alert('错误请求');
                return ;
            }
            if(res.status && res.status == 200) {
                window.alert(res.data.message);
                router.push('/');
            }
        } catch (error) {
            if(error.response) {
                window.alert(error.response.data.message);
            }
        }
    }
</script>
<template>
    <div v-editor-directive id="resume_editor">
        <h1> {{ title }} </h1>
        <div id="base_msg">
            <table>
                    <tr>
                        <td>你的名字：</td>
                        <td><input type="text" v-model="resumeData.name" /></td>
                    </tr>
                    <tr>
                        <td>你的性别：</td>
                        <td>
                            <input type="radio" v-model="resumeData.gender" value="男" /> 男
                            <input type="radio" v-model="resumeData.gender" value="女" /> 女
                        </td>
                    </tr>
                    <tr>
                        <td>你的年龄：</td>
                        <td><input type="text" v-model="resumeData.age" /></td>
                    </tr>
                    <tr>
                        <td>电子邮件：</td>
                        <td><input type="text" v-model="resumeData.email" /></td>
                    </tr>
                    <tr>
                        <td>电话号码：</td>
                        <td><input type="tel" v-model="resumeData.phone" /></td>
                    </tr>
                </table>
        </div>
        <div id="education">
            <h2>你的教育经历：</h2>
            <table v-show="resumeData.education.length != 0">
                <tr><th>学校</th><th>学位</th><th>毕业时间</th><th>操作</th></tr>
                <tr v-for="(edu, index) in resumeData.education" :key="index">
                    <td> {{ edu.school }} </td>
                    <td> {{ edu.major+"："+ edu.degree }}</td>
                    <td> {{ edu.graduation }} </td>
                    <td>
                        <input type="button" value="删除" @click="deleteEdu(index)" />
                    </td>
                </tr>
            </table>
            <table>
                <tr>
                    <td>你的学校：</td>
                    <td><input type="text" v-model="eduData.school" /></td>
                </tr>
                <tr>
                    <td>你的专业：</td>
                    <td><input type="text" v-model="eduData.major" /></td>
                </tr>
                <tr>
                    <td>你的学位：</td>
                    <td><input type="text" v-model="eduData.degree" /></td>
                </tr>
                <tr>
                    <td>毕业年份：</td>
                    <td><input type="tel" v-model="eduData.graduation" /></td>
                </tr>
                <tr>
                    <td><input type="button" value="添加" @click="addEdu" /></td>
                    <td><input type="button" value="重置" @click="resetEdu" /></td>
                </tr>
            </table>
        </div>
        <div id="professional">
            <h2>你的职业经历：</h2>
            <table v-show="resumeData.professional.length != 0">
                <tr><th>公司</th><th>职务</th><th>在职时间</th><th>操作</th></tr>
                <tr v-for="(prof, index) in resumeData.professional" :key="index">
                    <td> {{ prof.company }} </td>
                    <td> {{ prof.title }}</td>
                    <td> {{ prof.startingDate + '—' + prof.endingDate }} </td>
                    <td>
                        <input type="button" value="删除" @click="deleteProf(index)" />
                    </td>
                </tr>
            </table>
            <table>
                <tr>
                    <td>你的公司：</td>
                    <td><input type="text" v-model="profData.company" /></td>
                </tr>
                <tr>
                    <td>你的职务：</td>
                    <td><input type="text" v-model="profData.title" /></td>
                </tr>
                <tr>
                    <td>入职年份：</td>
                    <td><input type="text" v-model="profData.startingDate" /></td>
                </tr>
                <tr>
                    <td>离职年份：</td>
                    <td><input type="tel" v-model="profData.endingDate" /></td>
                </tr>
                <tr>
                    <td><input type="button" value="添加" @click="addProf" /></td>
                    <td><input type="button" value="重置" @click="resetProf" /></td>
                </tr>
            </table>
        </div>
            <tr>
                <td><input type="button" value="提交" @click="submitData" /></td>
                <td><input type="button" value="重置" @click="reset" /></td>
            </tr>
    </div>
</template>