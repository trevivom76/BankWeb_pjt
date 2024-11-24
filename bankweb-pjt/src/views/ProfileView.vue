<template>
  <div class="d-flex justify-center align-center">
    <v-card class="px-10 pt-12" width="950px" min-height="785px" rounded="xl">
      <div>
        <RouterLink :to="{ name: 'profilemanage' }">회원정보 관리 페이지</RouterLink>
        &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
        <RouterLink :to="{ name: 'contractedproduct' }">관심상품 관리 페이지</RouterLink>
        &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
        <!-- 조건부 라우팅을 위해 RouterLink를 a 태그로 변경 -->
        <a href="#" @click.prevent="handleRecommendClick" 
           class="router-link" 
           :class="{ 'disabled-link': !isProfileComplete }">
          상품 추천받기 페이지
        </a>
      </div>

      <RouterView />
    </v-card>

    <!-- 경고 다이얼로그 -->
    <v-dialog v-model="showDialog" max-width="400">
      <v-card>
        <v-card-text class="pa-6">
          <div class="text-center mb-4">
            <v-icon color="warning" size="32" class="mb-3">mdi-alert-circle</v-icon>
            <p  style="font-size: 22px;">
              금융 상품 맞춤 추천을 위해 프로필 정보를 입력해주세요
            </p>
          </div>
          <div class="d-flex justify-center">
            <v-btn
              color="primary"
              @click="goToProfileManage"
              variant="flat"
            >
              프로필 수정하기
            </v-btn>
            <v-btn
              color="grey"
              @click="showDialog = false"
              variant="flat"
              class="ml-2"
            >
              취소
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAccountStore } from "@/stores/account";

const router = useRouter();
const accountStore = useAccountStore();
const showDialog = ref(false);

// 프로필이 완성되었는지 확인하는 computed 속성
const isProfileComplete = computed(() => {
  const userInfo = accountStore.userinfo;
  return userInfo && 
         userInfo.age > 0 && 
         userInfo.money > 0 && 
         userInfo.salary > 0;
});

// 추천 페이지 링크 클릭 핸들러
const handleRecommendClick = () => {
  if (!isProfileComplete.value) {
    showDialog.value = true;
  } else {
    router.push({ name: 'recommended1' });
  }
};

// 프로필 관리 페이지로 이동
const goToProfileManage = () => {
  showDialog.value = false;
  router.push({ name: 'profilemanage' });
};
</script>

<style scoped>
.router-link {
  text-decoration: none;
  color: inherit;
}

.disabled-link {
  cursor: pointer;
  opacity: 0.8;
}

.v-card-text {
  font-size: 1.1rem;
}
</style>