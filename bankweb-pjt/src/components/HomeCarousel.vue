<template>
  <div class="carousel">
    <!-- 슬라이드 트랙 -->
    <div class="carousel-track">
      <div
        v-for="(slide, index) in slides"
        :key="index"
        class="slide"
        :class="{ active: index === currentSlide }"
      >
        <img :src="slide.image" alt="Slide Image" class="slide-image" />
        <div class="text-container">
          <div class="text t1" :class="{ fadeOut: isFadingOut }">{{ slide.title }}</div>
          <div class="text t2" :class="{ fadeOut: isFadingOut }">{{ slide.subtitle }}</div>
          <div class="text t3" :class="{ fadeOut: isFadingOut }">{{ slide.description }}</div>
          <button class="btn-detail t4" :class="{ fadeOut: isFadingOut }">{{ slide.buttonText }}</button>
        </div>
      </div>
    </div>

    <!-- 네비게이션 점 -->
    <div class="slide-nav">
      <div
        v-for="(slide, index) in slides"
        :key="index"
        class="dot"
        :class="{ active: index === currentSlide }"
        @click="goToSlide(index)"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import deposit_bg from "@/assets/icon/main_causel_deposit.png";

// 슬라이드 데이터
const slides = [
  {
    image: deposit_bg,
    title: "금융상품 추천",
    subtitle: "나에게 맞는 금융 상품 추천받기",
    description: "내 목표에 꼭 맞는 금융 상품, 지금 바로 찾아보세요!",
    buttonText: "바로가기 >",
  },
  {
    image: deposit_bg,
    title: "환율 조회",
    subtitle: "실시간 환율 정보 확인하기",
    description: "최신 환율 데이터를 제공받고 빠르게 대응하세요!",
    buttonText: "바로가기 >",
  },
  {
    image: deposit_bg,
    title: "주변 은행 찾기",
    subtitle: "가장 가까운 은행 확인",
    description: "편리하게 내 위치에서 가까운 은행을 찾아보세요!",
    buttonText: "바로가기 >",
  },
];

const currentSlide = ref(0);
const isFadingOut = ref(false);
let slideInterval;

// 슬라이드 전환 전/후 애니메이션 처리
const goToSlide = (nextIndex) => {
  isFadingOut.value = true;
  setTimeout(() => {
    currentSlide.value = nextIndex;
    isFadingOut.value = false;
  },1000); // 사라지는 애니메이션 1초
};

// 자동 슬라이드
onMounted(() => {
  slideInterval = setInterval(() => {
    goToSlide((currentSlide.value + 1) % slides.length);
  }, 5000);
});

onUnmounted(() => {
  clearInterval(slideInterval);
});
</script>

<style scoped>
.carousel {
  position: relative;
  width: 100%;
  overflow: hidden;
}

/* 슬라이드 트랙 */
.carousel-track {
  display: flex;
  transition: transform 1s ease;
}

/* 개별 슬라이드 */
.slide {
  flex: 0 0 100%;
  height: auto;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 1s ease;
}

.slide.active {
  opacity: 1;
}

/* 슬라이드 이미지 */
.slide-image {
  width: 100%;
  height: auto;
  object-fit: contain;
}

/* 텍스트 컨테이너 */
.text-container {
  position: absolute;
  top: 50%;
  left: 10%;
  transform: translateY(-50%);
  color: white;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.text {
  font-family: Arial, sans-serif;
  opacity: 0;
  transform: translateX(-50px);
  animation: fade-in-left 1s forwards;
}

.text.fadeOut {
  animation: fade-out-left 1s forwards;
}

.t1 {
  font-size: 36px;
  font-weight: bold;
  animation-delay: 0.3s;
}

.t2 {
  font-size: 24px;
  font-weight: 500;
  animation-delay: 0.6s;
}

.t3 {
  font-size: 16px;
  color: #ddd;
  animation-delay: 0.9s;
}

.t4 {
  background: #636acc;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 20px;
  font-size: 16px;
  cursor: pointer;
  transition: transform 0.3s ease, background-color 0.3s ease;
  animation-delay: 1.2s;
}

.t4:hover {
  transform: scale(1.1);
  background-color: #5058cc;
}

/* 네비게이션 점 */
.slide-nav {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
}

.dot {
  width: 12px;
  height: 12px;
  background-color: #ccc;
  border-radius: 50%;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.dot.active {
  background-color: #636acc;
}

/* 등장 애니메이션 */
@keyframes fade-in-left {
  from {
    opacity: 0;
    transform: translateX(-50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 사라지는 애니메이션 */
@keyframes fade-out-left {
  from {
    opacity: 1;
    transform: translateX(0);
  }
  to {
    opacity: 0;
    transform: translateX(-50px);
  }
}
</style>
