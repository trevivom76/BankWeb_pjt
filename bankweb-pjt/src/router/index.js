import AroundBankView from "@/views/AroundBankView.vue";
import CommunityView from "@/views/CommunityView.vue";
import CurrencyCalculatorView from "@/views/CurrencyCalculatorView.vue";
import HomeView from "@/views/HomeView.vue";
import InterestRateView from "@/views/InterestRateView.vue";
import LogInView from "@/views/LogInView.vue";
import SiginUpView from "@/views/SiginUpView.vue";
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      //메인 페이지
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      //금리비교 페이지
      path: "/interestrate",
      name: "interestrate",
      component: InterestRateView,
    },
    {
      //환율계산기 페이지
      path: "/currencycalculator",
      name: "currencycalculator",
      component: CurrencyCalculatorView,
    },
    {
      // 주변은행 페이지
      path: "/aroundbank",
      name: "aroundbank",
      component: AroundBankView,
    },
    {
      // 커뮤니티 페이지
      path: "/community",
      name: "community",
      component: CommunityView,
    },
    {
      // 로그인 페이지
      path: "/login",
      name: "login",
      component: LogInView,
    },
    {
      // 로그아웃 페이지
      path: "/signup",
      name: "signup",
      component: SiginUpView,
    },
  ],
});

export default router;
