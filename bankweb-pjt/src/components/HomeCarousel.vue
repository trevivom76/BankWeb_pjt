<template>
  <div class="carousel">
    <!-- 슬라이드 트랙 -->
    <div class="carousel-track" :style="{ transform: `translateX(-${currentSlide * 100}%)` }">
      <div v-for="(slide, index) in slides" :key="index" class="slide" :class="{ active: index === currentSlide }">
        <img :src="slide.image" alt="Slide Image" class="slide-image" />
        <div class="text-container">
          <div class="text t1" :class="{ fadeOut: isFadingOut }">{{ slide.title }}</div>
          <div class="text t2" :class="{ fadeOut: isFadingOut }">{{ slide.subtitle }}</div>
          <div class="text t3" :class="{ fadeOut: isFadingOut }">{{ slide.description }}</div>
          <button class="text t4" :class="{ fadeOut: isFadingOut }" @click="handleButtonClick(slide.ButtonAction)">{{
            slide.buttonText }}</button>
        </div>
      </div>
    </div>

    <!-- 네비게이션 점 -->
    <div class="slide-nav">
      <div v-for="(slide, index) in slides" :key="index" class="dot" :class="{ active: index === currentSlide }"
        @click="goToSlide(index)"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import deposit_bg1 from "@/assets/icon/carousel.png";
import deposit_bg2 from "@/assets/icon/carousel2.png";
import deposit_bg3 from "@/assets/icon/carousel3.png";
import { useAccountStore } from "@/stores/account";
import { useRouter } from "vue-router";

const accountStore = useAccountStore()
const router = useRouter()

const currentSlide = ref(0);
const isFadingOut = ref(false);
let slideInterval;


// 슬라이드 데이터
const slides = [
  {
    image: deposit_bg1,
    title: "나에게 맞는",
    subtitle: "금융 상품 추천받기",
    description: "내 목표에 꼭 맞는 금융 상품, 지금 바로 찾아보세요!",
    buttonText: "바로가기 >",
    ButtonAction: "recommendproduct"
  },
  {
    image: deposit_bg2,
    title: "빠르고 스마트한",
    subtitle: "환율 계산하기",
    description: "여행 준비? 투자 계획? 환율 계산기로 빠르게 해결하세요!",
    buttonText: "바로가기 >",
    ButtonAction: "currencycalculator",
  },
  {
    image: deposit_bg3,
    title: "은행 방문을 간편하게,",
    subtitle: "주변 지점 확인하기",
    description: "편리하게 내 위치에서 가까운 은행을 찾아보세요!",
    buttonText: "바로가기 >",
    ButtonAction: "aroundbank",
  },
];


// 슬라이드 전환 전/후 애니메이션 처리
const goToSlide = (nextIndex) => {
  isFadingOut.value = true;
  setTimeout(() => {
    currentSlide.value = nextIndex;
    isFadingOut.value = false;
  }, 500);
};


// 버튼 클릭 처리
const handleButtonClick = (action) => {
  if (action === "recommendproduct") {
    if (accountStore.isLogin) {
      router.push({ name: action });
    } else {
      alert("로그인이 필요합니다.");
      router.push({ name: "login" });
    }
  } else {
    router.push({ name: action });
  }
};


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

.carousel-track {
  display: flex;
  transition: transform 1s ease;
}

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

.slide-nav {
  display: flex;
  justify-content: flex-start;
  gap: 8px;
  margin-top: 16px;
}

.slide.active {
  opacity: 1;
}

.slide-image {
  width: 100%;
  height: auto;
  object-fit: cover;
}

.text-container {
  position: absolute;
  top: 47%;
  left: 8%;
  transform: translateY(-50%);
  color: white;
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: flex-start;
}

.text {
  opacity: 0;
  transform: translateX(-50px);
  animation: fade-in-left 1s forwards;
}

.text.fadeOut {
  animation: fade-out-left 0.5s forwards;
}

.t1 {
  font-size: 40px;
  font-weight: bold;
  animation-delay: 0.3s;
}

.t2 {
  font-size: 40px;
  font-weight: bold;
  animation-delay: 0.6s;
}

.t3 {
  font-size: 20px;
  font-weight: light;
  animation-delay: 0.9s;
}

.t4 {
  color: #2F2A78;
  font-size: 16px;
  font-weight: semibold;
  cursor: pointer;
  transition: transform 0.3s ease, background-color 0.3s ease;
  animation-delay: 1.2s;
}

.t4:hover {
  transform: scale(1.1);
}

.slide-nav {
  position: absolute;
  bottom: 60px;
  left: 11%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
}

.dot {
  width: 8px;
  height: 8px;
  background-color: #ccc;
  border-radius: 50%;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.dot.active {
  background-color: #ffffff;
  width: 16px;
  border-radius: 4px;
}

@media (max-width: 1200px) {
  .t1 {
    font-size: 30px;
  }

  .t2 {
    font-size: 30px;
  }

  .t3 {
    font-size: 15px;
  }

  .t4 {
    font-size: 12px;
  }
}

@media (max-width: 800px) {
  .t1 {
    font-size: 20px;
  }

  .t2 {
    font-size: 20px;
  }

  .t3 {
    font-size: 10px;
  }

  .t4 {
    font-size: 8px;
  }
}

@media (max-width: 600px) {
  .t1 {
    font-size: 15px;
  }

  .t2 {
    font-size: 15px;
  }

  .t3 {
    font-size: 7px;
  }

  .t4 {
    font-size: 4px;
  }
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
