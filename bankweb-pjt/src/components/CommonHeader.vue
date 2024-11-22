<template>
  <div>
    <!-- 로딩 상태 표시 -->
    <div v-if="isLoading" class="d-flex justify-center align-center" style="height: 400px">
      <v-progress-circular indeterminate color="primary" :size="50"></v-progress-circular>
    </div>

    <div v-else>
      <!-- 로그인/로그아웃/회원가입 버튼 위치 -->
      <div class="d-flex justify-end">
        <!-- 로그인/회원가입 버튼 -->
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
        <!-- 인행 로고 네비게이션 주요 컴포넌트 묶음 (아이디 프로필 제외) -->
        <div class="d-flex justify-start align-center ga-10">
          <!-- 은행 로고 -->
          <div>
            <a href="#" @click.prevent="goToHome">
              <img :src="BBK_Logo" alt="Example Image" class="bank-logo" />
            </a>
          </div>

          <!-- 네비게이션바 주요 링크 -->
          <!-- 로그인 되어있다면 -->
          <div v-if="isLogin()">
            <div class="d-flex">
              <div class="text-center">
                <!-- 금리비교 태그 -->
                <RouterLink :to="{ name: 'depositList' }">
                  <span class="text" :class="{ hovered: isHovered1 }" @mouseover="isHovered1 = true" @mouseleave="isHovered1 = false">금리 비교</span>
                </RouterLink>
                &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
                <!-- 환율계산 태그 -->
                <RouterLink :to="{ name: 'currencycalculator' }">
                  <span class="text" :class="{ hovered: isHovered2 }" @mouseover="isHovered2 = true" @mouseleave="isHovered2 = false">환율 계산</span>
                </RouterLink>
                &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
                <!-- 주변은행 태그 -->
                <RouterLink :to="{ name: 'aroundbank' }">
                  <span class="text" :class="{ hovered: isHovered3 }" @mouseover="isHovered3 = true" @mouseleave="isHovered3 = false">주변 은행</span>
                </RouterLink>
                &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
                <!-- 커뮤니티 태그 -->
                <RouterLink :to="{ name: 'community' }">
                  <span class="text" :class="{ hovered: isHovered4 }" @mouseover="isHovered4 = true" @mouseleave="isHovered4 = false">커뮤니티</span>
                </RouterLink>
              </div>

              <!-- 프로필 이미지 + 사용자 아이디 -->
              <RouterLink :to="{ name: 'profilemanage' }">
                <div class="d-flex ga-4">
                  <p class=".delete-a-underline-color">
                    {{ accountStore.userinfo.nickname }}
                  </p>
                  <div>
                    <img :src="profileStore.userprofile.profile_img" alt="프로필 이미지" class="profile-img" />
                  </div>
                </div>
              </RouterLink>
            </div>
          </div>

          <!-- 로그인 되어있지 않다면 -->
          <div v-else>
            <div class="text-center">
              <!-- 금리비교 태그 -->
              <a href="#" @click="dialog = true">
                <span class="text" :class="{ hovered: isHovered1 }" @mouseover="isHovered1 = true" @mouseleave="isHovered1 = false">금리 비교</span>
              </a>
              &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
              <!-- 환율계산 태그 -->
              <a href="#" @click="dialog = true">
                <span class="text" :class="{ hovered: isHovered2 }" @mouseover="isHovered2 = true" @mouseleave="isHovered2 = false">환율 계산</span>
              </a>
              &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
              <!-- 주변은행 태그 -->
              <a href="#" @click="dialog = true">
                <span class="text" :class="{ hovered: isHovered3 }" @mouseover="isHovered3 = true" @mouseleave="isHovered3 = false">주변 은행</span>
              </a>
              &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
              <!-- 커뮤니티 태그 -->
              <a href="#" @click="dialog = true">
                <span class="text" :class="{ hovered: isHovered4 }" @mouseover="isHovered4 = true" @mouseleave="isHovered4 = false">커뮤니티</span>
              </a>
            </div>
          </div>
        </div>
      </nav>

      <!-- 로그인 안내 다이얼로그 -->
      <v-dialog v-model="dialog" max-width="380" height="300" persistent>
        <v-card>
          <div class="d-flex flex-column justify-center align-center" style="height: 100%; padding: 24px">
            <!-- 아이콘 크기 조정 -->
            <svg-icon type="mdi" :path="mdiInformationSlabCircleOutline" style="font-size: 150px; margin-bottom: 24px"></svg-icon>

            <!-- 안내 텍스트 -->
            <p class="text-center" style="font-size: 22px; margin-bottom: 24px; line-height: 1.5">안전한 금융서비스를 위해 로그인 화면으로 이동합니다</p>

            <!-- 원형 프로그레스 바 -->
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
// SvgIcon 컴포넌트와 MDI 아이콘 가져오기
import SvgIcon from "@jamescoyle/vue-icon";
import { mdiAccount } from "@mdi/js";
import { mdiLogout } from "@mdi/js";
import { mdiInformationSlabCircleOutline } from "@mdi/js";

// BBK_Logo 사진 가져오기
import BBK_Logo from "@/images/BBK_Logo.png";

import { RouterLink, useRouter } from "vue-router";
import { useAccountStore } from "@/stores/account";
import { onMounted, ref, watch } from "vue";
import { useProfileStore } from "@/stores/profile";

const accountStore = useAccountStore();
const profileStore = useProfileStore();

const router = useRouter();

const isHovered1 = ref(false);
const isHovered2 = ref(false);
const isHovered3 = ref(false);
const isHovered4 = ref(false);

// dialog 상태를 ref로 선언
const dialog = ref(false);

const isLoading = ref(true); // 로딩 상태를 관리하는 ref 추가

// 프로필 정보 가져오기
onMounted(async () => {
  try {
    const payload = {
      username: accountStore.userinfo.username,
    };
    await profileStore.getProfile(payload);
  } finally {
    isLoading.value = false; // 데이터 로딩이 완료되면 로딩 상태를 false로 변경
  }
});

// 홈페이지로 push하는 함수
const goToHome = () => {
  router.push({ name: "home" });
};

// 로그인 되어있는지 아닌지 확인하는 함수
const isLogin = function () {
  return accountStore.isLogin;
};

const logOut = function () {
  accountStore.logOut();
};

// dialog 값이 변경될 때, watch로 4초 후에 dialog를 false로 설정
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

/* 기본 텍스트 스타일 */
.text {
  font-weight: bold;
  color: black;
  display: inline-block;
  position: relative;
  transition: transform 0.3s ease, color 0.3s ease;
}

/* 호버 상태 */
.text.hovered {
  color: rgb(59, 59, 216);
  transform: scale(1.2);
}

/* 밑줄 효과 (둥근 모서리 적용) */
.text::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -6px; /* 밑줄 위치 */
  width: 0;
  height: 2px; /* 밑줄 두께 */
  background-color: rgb(59, 59, 216);
  transition: width 0.3s ease;
  border-radius: 2px; /* 둥근 모서리 적용 */
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

.delete-a-underline-color {
  text-decoration: none;
  color: inherit;
}
</style>
