import DepositList from "@/components/DepositList.vue";
import SavingList from "@/components/SavingList.vue";
import AroundBankView from "@/views/AroundBankView.vue";
import CommunityView from "@/views/CommunityView.vue";
import ContractedProductView from "@/views/ContractedProductView.vue";
import CreateView from "@/views/CreateView.vue";
import CurrencyCalculatorView from "@/views/CurrencyCalculatorView.vue";
import DetailView from "@/views/DetailView.vue";
import HomeView from "@/views/HomeView.vue";
import InterestRateView from "@/views/InterestRateView.vue";
import LogInView from "@/views/LogInView.vue";
import ProfileManageView from "@/views/ProfileManageView.vue";
import ProfileView from "@/views/ProfileView.vue";
import Recommended1View from "@/views/Recommended1View.vue";
import Recommended2View from "@/views/Recommended2View.vue";
import RecommendProductView from "@/views/RecommendProductView.vue";
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
      children: [
        {
          path: "deposit",
          name: "depositList",
          component: DepositList,
        },
        {
          path: "saving",
          name: "savingList",
          component: SavingList,
        },
      ],
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
      // 게시글 Detail 페이지
      path: "/articles/:id",
      name: "detail",
      component: DetailView,
    },
    {
      // 게시글 Create 페이지
      path: "/create",
      name: "create",
      component: CreateView,
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
    {
      // 프로필 페이지
      path: "/profile",
      component: ProfileView,
      children: [
        {
          // 회원정보 관리 페이지
          path: "/profilemanage",
          name: "profilemanage",
          component: ProfileManageView,
        },
        {
          // 관심상품 관리 페이지
          path: "/contractedproduct",
          name: "contractedproduct",
          component: ContractedProductView,
        },
        {
          // 상품 추천받기 페이지
          path: "/recommendproduct",
          component: RecommendProductView,
          children: [
            {
              // 나의 금융 목표 기반 추천 페이지
              path: "/recommended1",
              name: "recommended1",
              component: Recommended1View,
            },
            {
              // 자산 성장 시뮬레이션 기반 추천 페이지
              path: "/recommended2",
              name: "recommended2",
              component: Recommended2View,
            },
          ],
        },
      ],
    },
  ],
});

export default router;
