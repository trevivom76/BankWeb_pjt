<template>
  <div class="container">
    <div class="card">
      <div class="card-title">
        <img src="@/assets/icon/location.png" alt="" height="30px" class="location-icon">
        <h1 :style="{ fontWeight: 600 , fontSize: '24px'}">
          주변은행
          <span :style="{ color: '#5058cc' }">검색하기</span>
        </h1>
      </div>
      <div>
        <BankMapSelect @change="handleRegionChange" />
      </div>
      <BankMap :selected-region="selectedRegion" />
    </div>
  </div>
</template>

<script setup>
import BankMapSelect from "@/components/BankMapSelect.vue";
import BankMap from "@/components/BankMap.vue";
import { ref } from "vue";

const selectedRegion = ref({});

const handleRegionChange = (selection) => {
  selectedRegion.value = selection;
};
</script>

<style scoped>
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
  padding: 48px 40px;
  border-radius: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  animation: card-load 0.8s ease;
}

.card-title {
  display: flex;
  flex-direction: row;
  gap: 4px;
  align-items: center;
  padding-bottom: 28px;
}

.title {
  font-weight: 600;
  font-size: 24px;
}
.highlight {
  color: #5058cc;
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
  transform: scale(1.2); /* 마우스 오버 시 확대 및 회전 */
}
</style>
