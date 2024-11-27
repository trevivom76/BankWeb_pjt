<template>
  <div class="container">
    <HomeCarousel class="padding" />
    <div class="container-2 padding">
      <div class="container-3">
        <HomeDeposit />
        <HomeCurrency />
      </div>
      <HomeChatBot class="flex" />
    </div>
    <HomeBanklist />
  </div>
</template>

<script setup>
import HomeBanklist from "@/components/HomeBankList.vue";
import HomeCarousel from "@/components/HomeCarousel.vue";
import HomeChatBot from "@/components/HomeChatBot.vue";
import HomeCurrency from "@/components/HomeCurrency.vue";
import HomeDeposit from "@/components/HomeDeposit.vue";
</script>

<style scoped>
.padding {
  padding-bottom: 20px;
}

.container-2 {
  display: flex;
  flex-direction: row;
  gap: 20px;
  align-items: flex-start;
  /* 위쪽 정렬 */
  justify-content: flex-start;
  /* 왼쪽 정렬 */
}

.container-3 {
  display: flex;
  flex-direction: column;
  flex: 75%;
  gap: 20px;
}

.flex {
  flex: 25%;
  display: flex;
  /* 기본 flex 속성 */
}

@media (max-width: 1200px) {
  .container-2 {
    flex-direction: column;
    /* 작은 화면에서는 세로 배치 */
  }

  .container-3,
  .flex {
    width: 100%;
    /* 각 요소가 전체 너비를 차지 */
  }
}
</style>
