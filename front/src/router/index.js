import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import ParticipantsListPage from '../views/ParticipantsListPage'
import ParticipantProfilePage from '../views/ParticipantProfilePage'
import ParticipantStatsPage from '../views/ParticipantStatsPage'
import RegisterVue from '../views/RegisterVue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/participants',
    name: 'participants',
    component: ParticipantsListPage
  },
  {
    path: '/participants/stats',
    query: { date_from: 'date_from', date_to: 'date_to' },
    name: 'participants_stats',
    component: ParticipantStatsPage
  },
  {
    path: '/participants/:id',
    name: 'current_participants',
    query: { date_from: 'date_from', date_to: 'date_to' },
    component: ParticipantProfilePage,
    props: true
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register/managers',
    name: 'register-managers',
    component: RegisterVue
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
