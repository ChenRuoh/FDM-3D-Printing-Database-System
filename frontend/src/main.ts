import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './assets/main.css'

// 导入页面组件
import HomePage from './views/HomePage.vue'
import ParametersPage from './views/ParametersPage.vue'
import MatchingPage from './views/MatchingPage.vue'
import MaterialsPage from './views/MaterialsPage.vue'
import PrintersPage from './views/PrintersPage.vue'

// 定义路由
const routes = [
  { path: '/', component: HomePage },
  { path: '/parameters', component: ParametersPage },
  { path: '/matching', component: MatchingPage },
  { path: '/materials', component: MaterialsPage },
  { path: '/printers', component: PrintersPage }
]

// 创建路由器
const router = createRouter({
  history: createWebHistory(),
  routes
})

// 创建应用
const app = createApp(App)

// 使用路由器
app.use(router)

// 挂载应用
app.mount('#app')