import { createRouter, createWebHashHistory } from 'vue-router';

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('../view/home.vue')
    },
    {
        path: '/about',
        name: 'about',
        component: () => import('../view/HelloWorld.vue')
    },
    {
        path: '/resumeEditor/:cv_id',
        name: 'resumeEditor',
        component: () => import('../view/resumeEditor.vue')
    }
]

const router = createRouter({
    'history' : createWebHashHistory(),
    'routes' : routes
});

export default router;
