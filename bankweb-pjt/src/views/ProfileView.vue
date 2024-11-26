<template>
  <div class="container">
    <div class="card">
      <div class="profile-links">
        <RouterLink :to="{ name: 'profilemanage' }" class="profile-link"
          :class="{ active: selectedCategory === 'profilemanage' }" @click="setSelectedCategory('profilemanage')">
          회원정보 관리 페이지
        </RouterLink>
        <RouterLink :to="{ name: 'contractedproduct' }" class="profile-link"
          :class="{ active: selectedCategory === 'contractedproduct' }"
          @click="setSelectedCategory('contractedproduct')">
          관심상품 관리 페이지
        </RouterLink>
        <a href="#" @click.prevent="handleRecommendClick" class="profile-link"
          :class="{ 'disabled-link': !isProfileComplete, active: selectedCategory === 'recommend' }">
          상품 추천받기 페이지
        </a>
      </div>
      <RouterView />
    </div>
    <!-- 경고 다이얼로그 -->
    <v-dialog v-model="showDialog" max-width="400">
      <div class="card">
        <div class="scene">
          <!-- 그림자 -->
          <div class="shadow"></div>
          <div class="cube">
            <img src="@/assets/icon/caution.png" alt="Caution Icon" class="cube-face front" />
            <img src="@/assets/icon/caution_back.png" alt="Caution Icon" class="cube-face back" />
          </div>
        </div>
        <p style="font-size: 22px; font-weight: 500; text-align: center;">금융 상품 맞춤 추천을 위한</p>
        <p style="font-size: 22px; font-weight: 500; text-align: center;">프로필 정보를 입력해주세요</p>
        <div class="card-footer">
          <button class="btn profile" @click="goToProfileManage">프로필 수정하기</button>
          <button class="btn cancel" @click="showDialog = false">취소</button>
        </div>

      </div>
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
const selectedCategory = ref('profilemanage'); // 기본 선택 카테고리

// 프로필이 완성되었는지 확인하는 computed 속성
const isProfileComplete = computed(() => {
  const userInfo = accountStore.userinfo;
  return userInfo &&
    userInfo.age > 0 &&
    userInfo.money > 0 &&
    userInfo.salary > 0;
});

const setSelectedCategory = (category) => {
  selectedCategory.value = category;
};

// 추천 페이지 링크 클릭 핸들러
const handleRecommendClick = () => {
  if (!isProfileComplete.value) {
    showDialog.value = true;
  } else {
    setSelectedCategory('recommend');
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
/* 부모 컨테이너 */
.profile-links {
  display: flex;
  flex-direction: row;
  /* 버튼들을 세로로 정렬 */
  gap: 24px;
  /* 버튼 간 간격 */
  align-items: flex-start;
  /* 왼쪽 정렬 (가운데 정렬을 원하면 center로 변경) */
  margin-bottom: 24px;
}

/* 공통 버튼 스타일 */
.profile-link {
  position: relative;
  color: #424242;
  /* 기본 텍스트 색상 */
  font-size: 18px;
  font-weight: 600;
  text-decoration: none;
  padding: 5px 0;
  transition: color 0.3s ease, transform 0.2s ease;
}

/* 활성화된 선 */
.profile-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  height: 2px;
  /* 선 두께 */
  width: 100%;
  background-color: #5058cc;
  /* 선 색상 */
  transform: scaleX(0);
  /* 초기 상태에서 선 숨김 */
  transform-origin: left;
  transition: transform 0.3s ease;
  /* 선 애니메이션 */
}

/* 활성 상태의 링크 */
.profile-link.active::after {
  transform: scaleX(1);
  /* 선이 유지됨 */
}

.profile-link.active {
  color: #5058cc;
  /* 텍스트 색상 강조 */
}

/* 마우스 호버 */
.profile-link:hover {
  color: #5058cc;
  /* 텍스트 색상 변경 */
  transform: translateX(5px);
  /* 살짝 오른쪽으로 이동 */
}

.profile-link:hover::after {
  transform: scaleX(1);
  /* 선 애니메이션 활성화 */
}

/* 비활성화된 링크 */
.disabled-link {
  color: #bdbdbd;
  /* 흐릿한 색상 */
  cursor: not-allowed;
}

.disabled-link::after {
  background-color: transparent;
  /* 비활성화 상태에서 선 제거 */
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.5s ease;
}

.slide-enter-from {
  transform: translateX(-20px);
}

.slide-leave-to {
  transform: translateX(20px);
}

.card {
  background-color: white;
  padding: 36px 40px 48px 40px;
  border-radius: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  animation: card-load 0.8s ease;
}

.card-footer {
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 20px;
  padding: 20px;
}

@keyframes card-load {
  0% {
    transform: scale(0.95);
    opacity: 0;
  }

  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.location-icon:hover {
  transform: scale(1.2);
  /* 마우스 오버 시 확대 및 회전 */
}

/* 3D 애니메이션 컨테이너 */
.scene {
  width: 200px;
  /* 컨테이너 크기 */
  height: 200px;
  perspective: 1000px;
  /* 3D 원근감 추가 */
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0px auto 40px;
  /* 가운데 정렬 */
  position: relative;
  /* 그림자 배치를 위한 기준 */
}

/* 그림자 */
.shadow {
  position: absolute;
  bottom: -20px;
  /* 그림자를 컨테이너 아래로 배치 */
  width: 150px;
  height: 20px;
  background: radial-gradient(ellipse at center, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0));
  border-radius: 50%;
  z-index: -1;
  /* 3D 객체 아래로 배치 */
  filter: blur(5px);
  /* 부드러운 그림자 효과 */
}

/* 3D 객체 */
.cube {
  width: 100%;
  height: 100%;
  position: relative;
  transform-style: preserve-3d;
  /* 3D 효과 유지 */
  animation: spin 3s infinite linear;
  /* 좌우 회전 애니메이션 */
}

/* 공통 이미지 스타일 */
.cube-face {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  backface-visibility: hidden;
  /* 뒷면 숨김 */
}

/* 앞면 배치 */
.front {
  transform: rotateY(0deg)
    /* 3D 공간에서 앞면 배치 */
}

/* 뒷면 배치 */
.back {
  transform: rotateY(180deg)
    /* 3D 공간에서 뒷면 배치 */
}

/* 3D 회전 애니메이션 정의 */
@keyframes spin {
  0% {
    transform: rotateY(0deg);
    /* 초기 상태 */
  }

  50% {
    transform: rotateY(180deg);
    /* 180도 회전 */
  }

  100% {
    transform: rotateY(360deg);
    /* 360도 회전 */
  }
}

.btn {
  width: 120px;
}

.profile {
  background-color: #389635;
  border-radius: 5px;
}

.cancel {
  background-color: rgb(203, 50, 30);
  border-radius: 5px;
}
</style>