import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'

import { createRouter, createWebHistory } from "vue-router"

import Home from "./views/Home.vue"
import Result from "./views/Result.vue"

const routes = [
    {path: '/', component: Home},
    {path: '/results', component: Result}
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

const pinia = createPinia();
const app = createApp(App);

app.use(router);
app.use(pinia);

app.mount('#app')
