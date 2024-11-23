<!-- CommonHeader.vue -->
<template>
  <div>
    <!-- 로딩 상태 표시 -->
    <div v-if="isLoading" class="d-flex justify-center align-center" style="height: 400px">
      <v-progress-circular indeterminate color="primary" :size="50"></v-progress-circular>
    </div>

    <div v-else>
      <!-- 로그인/로그아웃/회원가입 버튼 위치 -->
      <div class="d-flex justify-end">
        <!-- 로그인 되어있다면 -->
        <div v-if="isLogin()">
          <div>
            <!-- 로그아웃 버튼 -->
            <a href="#" @click.prevent="logOut" class="delete-a-underline-color">
              <p class="authenticationTag">로그아웃</p>
            </a>
          </div>
        </div>

        <!-- 로그인 되어있지 않다면 -->
        <div v-else>
          <div class="d-flex justify-center align-center ga-2">
            <!-- 로그인 버튼 -->
            <RouterLink :to="{ name: 'login' }" class="delete-a-underline-color">
              <p class="authenticationTag">로그인</p>
            </RouterLink>
            &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
            <!-- 회원가입 버튼 -->
            <RouterLink :to="{ name: 'signup' }" class="delete-a-underline-color">
              <p class="authenticationTag">회원가입</p>
            </RouterLink>
          </div>
        </div>
      </div>

      <!-- 네비게이션 바 -->
      <nav class="d-flex justify-space-between align-center">
        <div class="d-flex justify-start align-center ga-10">
          <!-- 은행 로고 -->
          <div>
            <a href="#" @click.prevent="goToHome">
              <img :src="BBK_Logo" alt="은행 로고" class="bank-logo" />
            </a>
          </div>

          <!-- 네비게이션바 주요 링크 -->
          <div v-if="isLogin()">
            <div class="d-flex">
              <div class="text-center">
                <!-- 기본 네비게이션 링크들 -->
                <RouterLink :to="{ name: 'depositList' }">
                  <span class="text" :class="{ hovered: isHovered1 }" @mouseover="isHovered1 = true" @mouseleave="isHovered1 = false">금리 비교</span>
                </RouterLink>
                &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
                <RouterLink :to="{ name: 'currencycalculator' }">
                  <span class="text" :class="{ hovered: isHovered2 }" @mouseover="isHovered2 = true" @mouseleave="isHovered2 = false">환율 계산</span>
                </RouterLink>
                &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
                <RouterLink :to="{ name: 'aroundbank' }">
                  <span class="text" :class="{ hovered: isHovered3 }" @mouseover="isHovered3 = true" @mouseleave="isHovered3 = false">주변 은행</span>
                </RouterLink>
                &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
                <RouterLink :to="{ name: 'community' }">
                  <span class="text" :class="{ hovered: isHovered4 }" @mouseover="isHovered4 = true" @mouseleave="isHovered4 = false">커뮤니티</span>
                </RouterLink>
              </div>
            </div>
          </div>

          <!-- 비로그인 상태의 네비게이션 -->
          <div v-else>
            <div class="text-center">
              <!-- 기본 네비게이션 링크들 -->
              <RouterLink :to="{ name: 'depositList' }">
                <span class="text" :class="{ hovered: isHovered1 }" @mouseover="isHovered1 = true" @mouseleave="isHovered1 = false">금리 비교</span>
              </RouterLink>
              &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
              <RouterLink :to="{ name: 'currencycalculator' }">
                <span class="text" :class="{ hovered: isHovered2 }" @mouseover="isHovered2 = true" @mouseleave="isHovered2 = false">환율 계산</span>
              </RouterLink>
              &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
              <RouterLink :to="{ name: 'aroundbank' }">
                <span class="text" :class="{ hovered: isHovered3 }" @mouseover="isHovered3 = true" @mouseleave="isHovered3 = false">주변 은행</span>
              </RouterLink>
              &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
              <a href="#" @click="dialog = true">
                <span class="text" :class="{ hovered: isHovered4 }" @mouseover="isHovered4 = true" @mouseleave="isHovered4 = false">커뮤니티</span>
              </a>
            </div>
          </div>

          <!-- 프로필 영역 - 조건부 렌더링 추가 -->
          <RouterLink v-if="isLogin() && accountStore.userinfo" :to="{ name: 'profilemanage' }">
            <div class="d-flex ga-4">
              <p class="delete-a-underline-color">
                {{ accountStore.userinfo.nickname }}
              </p>
              <div v-if="userprofileInfo">
                <img :src="userprofileInfo.profile_img" alt="프로필 이미지" class="profile-img" />
              </div>
            </div>
          </RouterLink>
        </div>
      </nav>

      <!-- 로그인 안내 다이얼로그 -->
      <v-dialog v-model="dialog" max-width="380" height="300" persistent>
        <v-card>
          <div class="d-flex flex-column justify-center align-center" style="height: 100%; padding: 24px">
            <svg-icon type="mdi" :path="mdiInformationSlabCircleOutline" style="font-size: 150px; margin-bottom: 24px"></svg-icon>
            <p class="text-center" style="font-size: 22px; margin-bottom: 24px; line-height: 1.5">안전한 금융서비스를 위해 로그인 화면으로 이동합니다</p>
            <v-card-text class="d-flex justify-center align-center pt-0" style="flex-grow: 1; margin-top: 16px">
              <v-progress-circular color="primary" indeterminate disable-shrink size="60" width="8"></v-progress-circular>
            </v-card-text>
          </div>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import { useAccountStore } from "@/stores/account";
import { useProfileStore } from "@/stores/profile";
import { RouterLink, useRouter } from "vue-router";
import SvgIcon from "@jamescoyle/vue-icon";
import { mdiInformationSlabCircleOutline } from "@mdi/js";
import BBK_Logo from "@/images/BBK_Logo.png";

const accountStore = useAccountStore();
const profileStore = useProfileStore();
const router = useRouter();

const isHovered1 = ref(false);
const isHovered2 = ref(false);
const isHovered3 = ref(false);
const isHovered4 = ref(false);
const dialog = ref(false);
const isLoading = ref(true);

const userprofileInfo = profileStore.userprofile

// 프로필 정보 가져오기
onMounted(async () => {
  try {
    if (accountStore.userinfo) {
      const payload = {
        username: accountStore.userinfo.username,
      };
      await profileStore.getProfile(payload);
    }
  } catch (error) {
    console.error('프로필 로딩 중 에러 발생:', error);
  } finally {
    isLoading.value = false;
  }
});

const goToHome = () => {
  router.push({ name: "home" });
};

const isLogin = () => {
  return accountStore.isLogin;
};

const logOut = () => {
  accountStore.logOut();
};

// dialog 관련 watch
watch(dialog, (val) => {
  if (!val) return;
  
  setTimeout(() => {
    dialog.value = false;
    router.push({ name: "login" });
  }, 3000);
});
</script>

<style scoped>
.bank-logo {
  width: 144px;
  height: 53px;
}

.text {
  font-weight: bold;
  color: black;
  display: inline-block;
  position: relative;
  transition: transform 0.3s ease, color 0.3s ease;
}

.text.hovered {
  color: rgb(59, 59, 216);
  transform: scale(1.2);
}

.text::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -6px;
  width: 0;
  height: 2px;
  background-color: rgb(59, 59, 216);
  transition: width 0.3s ease;
  border-radius: 2px;
}

.text.hovered::after {
  width: 100%;
}

.delete-a-underline-color {
  text-decoration: none;
  color: inherit;
}

.authenticationTag {
  font-size: 12px;
  color: #444444;
}

.profile-img {
  width: 25px;
}

.ga-2 {
  gap: 0.5rem;
}

.ga-4 {
  gap: 1rem;
}

.ga-10 {
  gap: 2.5rem;
}
</style>