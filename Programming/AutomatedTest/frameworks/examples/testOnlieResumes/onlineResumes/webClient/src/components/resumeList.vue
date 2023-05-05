<script setup>
    import axios from 'axios';
    import { ref, reactive } from 'vue';
    import { useRouter } from 'vue-router';
    import { useStore } from 'vuex';

    const list = reactive([]);
    const isEmpty = ref(true);
    const store = useStore();
    const router = useRouter();

    const vResumeList = {
        beforeMount: async function () {
            try {
                const res = await axios.get('/resumes/user/'+store.getters.UID);
                if (res.status == 200) {
                    for(let i=0; i < res.data.length; ++i) {
                        list.push(res.data[i]);
                    }
                    isEmpty.value = false;
                }
            } catch (error) {
                if(error.response) {
                    window.alert(error.response.data.message);
                }
            }
        }
    }

    function addResume() {
        router.push('/resumeEditor/newresume');
    }
    function updateResume(cv_id) {
        router.push('/resumeEditor/'+cv_id);
    }
    async function deleteResume(cv_id) {
        try {
            const res = await axios.delete('/resumes/'+cv_id);
            if(res.status == 200) {
                window.alert(res.data.message);
                location.reload();
            }

        } catch (error) {
            if(error.response) {
                window.alert(error.response.data.message);
            }
        }
    }
</script>

<template>
    <div id="resumeList">
        <table v-resume-list  v-show="!isEmpty">
            <tr>
                <th>简历标题</th>
                <th>可执行的操作</th>
            </tr>
            <tr v-for="resume in list" :key="resume.cv_id">
                <td>{{ `${resume.name}在${resume.professional[0].company}公司时` }}</td>
                <td>
                    <input type="button" value="删除"
                                @click="deleteResume(resume.cv_id)" />
                    <input type="button" value="修改"
                                @click="updateResume(resume.cv_id)" />
                </td>
            </tr>
        </table>
        <a href="javascript:void(0)" @click="addResume">
           添加新的简历
        </a>
    </div>
</template>