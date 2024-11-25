<template>
  <div class="nav">
    <!-- 로딩 상태 표시 -->
    <div v-if="isLoading" class="d-flex justify-center align-center" style="height: 400px">
      <v-progress-circular indeterminate color="primary" :size="50"></v-progress-circular>
    </div>

    <div v-else>
      <div class="header">
        <div v-if="isLogin()">
          <div class="first-header">
            <!-- 로그아웃 버튼 -->
            <a @click.prevent="logOut" class="first-header-text">
              <p class="authenticationTag">로그아웃</p>
            </a>
          </div>
        </div>
        <div v-else>
          <div class="first-header">
            <!-- 로그인 버튼 -->
            <RouterLink :to="{ name: 'login' }" class="first-header-text">
              <p class="authenticationTag">로그인</p>
            </RouterLink>
            <img src="@/assets/icon/header_bar.png" height="14px">
            <!-- 회원가입 버튼 -->
            <RouterLink :to="{ name: 'signup' }" class="first-header-text">
              <p class="authenticationTag">회원가입</p>
            </RouterLink>
          </div>
        </div>
      </div>
      <div class="line-header"></div>
      <nav class="header second-header">
        <div class="nav-container">
          <div class="logo-container">
            <a href="#" @click.prevent="goToHome">
              <img src="@/assets/icon/BBK_Logo.png" alt="Example Image" class="logo"/>
            </a>
          </div>
          <div class="nav-bar">
            <!-- 금리비교 태그 -->
            <RouterLink :to="{ name: 'depositList' }">
              <span class="text" :class="{ hovered: isHovered1 }" @mouseover="isHovered1 = true" @mouseleave="isHovered1 = false">금리비교</span>
            </RouterLink>
            <!-- 환율계산 태그 -->
            <RouterLink :to="{ name: 'currencycalculator' }">
              <span class="text" :class="{ hovered: isHovered2 }" @mouseover="isHovered2 = true" @mouseleave="isHovered2 = false">환율계산기</span>
            </RouterLink>
            <!-- 주변은행 태그 -->
            <RouterLink :to="{ name: 'aroundbank' }">
              <span class="text" :class="{ hovered: isHovered3 }" @mouseover="isHovered3 = true" @mouseleave="isHovered3 = false">주변은행</span>
            </RouterLink>
            <template v-if="isLogin">
              <!-- 커뮤니티 태그 -->
              <RouterLink :to="{ name: 'community' }">
                <span class="text" :class="{ hovered: isHovered4 }" @mouseover="isHovered4 = true" @mouseleave="isHovered4 = false">커뮤니티</span>
              </RouterLink>
            </template>
            <template v-else>
              <a href="#" @click="dialog = true">
                <span class="text" :class="{ hovered: isHovered4 }" @mouseover="isHovered4 = true" @mouseleave="isHovered4 = false">커뮤니티</span>
              </a>
            </template>
          </div>

          <RouterLink v-if="isLogin() && userinfo" :to="{ name: 'profilemanage' }">
            <div class="d-flex ga-4">
              <p class="delete-a-underline-color">
                {{ userinfo.nickname }}
              </p>
              <div v-if="userprofileInfo">
                <img 
                  v-show="userprofileInfo.profile_img"
                  :src="userprofileInfo.profile_img" 
                  :alt="userprofileInfo.nickname"
                  class="profile-img"
                  @load="handleImageLoad"
                  @error="handleImageError"
                />
                <v-skeleton-loader
                  v-if="!userprofileInfo.profile_img"
                  type="avatar"
                  width="25"
                  height="25"
                ></v-skeleton-loader>
                <v-avatar v-if="imageError" size="25">
                  {{ userprofileInfo.nickname?.charAt(0) }}
                </v-avatar>
              </div>
            </div>
          </RouterLink>
        </div>
        <RouterLink :to="{ name: 'profilemanage' }">
          <div class="profile-container">
            <p class="nickname-text">{{ accountStore.userinfo.nickname }}</p>
            <div>
              <img :src="profileStore.userprofile.profile_img" alt="프로필 이미지" class="profile-img" />
            </div>
          </div>
        </RouterLink>
      </nav>

      <!-- 로그인 안내 다이얼로그 -->
      <v-dialog v-model="dialog" max-width="380" height="300" persistent>
        <v-card>
          <div class="d-flex flex-column justify-center align-center" style="height: 100%; padding: 24px">
            <!-- 아이콘 크기 조정 --> 
            <svg-icon type="mdi" :path="mdiInformationSlabCircleOutline" style="font-size: 150px; margin-bottom: 24px"></svg-icon>

            <!-- 안내 텍스트 -->
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
import { storeToRefs } from 'pinia';
import { useAccountStore } from "@/stores/account";
import { useProfileStore } from "@/stores/profile";
import { RouterLink, useRouter } from "vue-router";
import SvgIcon from "@jamescoyle/vue-icon";
import { mdiInformationSlabCircleOutline } from "@mdi/js";

const accountStore = useAccountStore();
const profileStore = useProfileStore();
const router = useRouter();

// store의 상태를 반응형으로 가져오기
const { userprofile: userprofileInfo } = storeToRefs(profileStore);
const { userinfo } = storeToRefs(accountStore);

const isHovered1 = ref(false);
const isHovered2 = ref(false);
const isHovered3 = ref(false);
const isHovered4 = ref(false);
const dialog = ref(false);
const isLoading = ref(true);
const imageLoading = ref(true);
const imageError = ref(false);

// 이미지 로드 완료 핸들러
const handleImageLoad = () => {
  imageLoading.value = false;
};

// 이미지 로드 실패 핸들러
const handleImageError = () => {
  imageError.value = true;
  imageLoading.value = false;
  console.log('프로필 이미지 로드 실패');
};

// userinfo 변경 시 항상 프로필 새로 가져오기
watch(userinfo, async (newUserInfo) => {
  if (newUserInfo) {
    try {
      imageLoading.value = true;
      imageError.value = false;
      await profileStore.getProfile({
        username: newUserInfo.username
      });
    } catch (error) {
      console.error('프로필 동기화 실패:', error);
      imageError.value = true;
    }
  }
}, { immediate: true });

// userprofileInfo가 변경될 때마다 이미지 상태 초기화
watch(userprofileInfo, () => {
  if (userprofileInfo.value) {
    imageLoading.value = true;
    imageError.value = false;
  }
});

onMounted(() => {
  isLoading.value = false;
});

const goToHome = () => {
  router.push({ name: "home" });
};

const isLogin = () => {
  return accountStore.isLogin;
};

const logOut = () => {
  // 프로필 정보 초기화 추가
  profileStore.resetProfile();  // 프로필 스토어 초기화
  imageError.value = false;
  imageLoading.value = true;
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
.first-header {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
  padding: 6px 0px;
}

.first-header-text {
  text-decoration: none;
  color: #444444;
  font-weight: 500;
  font-size: 12px;
  padding: 0px 16px;
}

.line-header {
  background-color: #f3f6f8;
  height: 4px;
}

.second-header {
  display: flex;
  align-items: center;
  justify-content: space-between;

}

.nav-container {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 16px 0px;
}

.nav-bar {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 20px;
  padding: 0px 20px;
}

.logo-container {
  flex: 0 0 auto;
}

.logo {
  width: 120px;
  height: auto;
}

.text {
  font-weight: 600;
  font-size: 16px;
  color: rgb(50, 50, 50);
  display: inline-block;
  position: relative;
  text-align: center;
  text-decoration: none;
  transition: transform 0.3s ease, color 0.3s ease;
  width: 75px;
}

.text.hovered {
  color: #2F2A78;
  transform: scale(1.05);
}

.text.hovered::after {
  width: 100%;
}

.profile-container {
  display: flex;
  justify-self: flex-end;
  align-items: center;
  gap: 12px;
}

.nickname-text, a{
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  color: black;
}

.profile-img {
  width: 25px;
  height: 25px;
  object-fit: cover;
  border-radius: 50%;
  transition: opacity 0.3s ease;
}
</style>