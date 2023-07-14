import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/Home.vue';
import ConfigForm from "../components/ConfigForm.vue";
import ConfigDetail from "../components/ConfigDetail.vue";
import About from "../components/About.vue";
import Stats from "../components/Stats.vue";

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/stats',
    name: 'Stats',
    component: Stats,
  },
  {
    path: '/about-us',
    name: 'About Us',
    component: About,
  },
  {
    path: '/config',
    name: 'Submit a Config',
    component: ConfigForm,
  },
  {
    path: '/config/:uuid',
    name: 'config-detail',
    component: ConfigDetail,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;