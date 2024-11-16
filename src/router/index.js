import AroundBankView from '@/views/AroundBankView.vue'
import CommunityView from '@/views/CommunityView.vue'
import CurrencyCalculatorView from '@/views/CurrencyCalculatorView.vue'
import HomeView from '@/views/HomeView.vue'
import InterestRateView from '@/views/InterestRateView.vue'
import LogInView from '@/views/LogInView.vue'
import SiginUpView from '@/views/SiginUpView.vue'
import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/interestrate',
      name: 'interestrate',
      component: InterestRateView
    },
    {
      path: '/currencycalculator',
      name: 'currencycalculator',
      component: CurrencyCalculatorView
    },
    {
      path: '/aroundbank',
      name: 'aroundbank',
      component: AroundBankView
    },
    {
      path: '/community',
      name: 'community',
      component: CommunityView
    },
    {
      path: '/login',
      name: 'login',
      component: LogInView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SiginUpView
    },
  ],
})

export default router
