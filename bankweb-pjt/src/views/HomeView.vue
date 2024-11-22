<template>
  <div>
    <!-- 여기도 컴포넌트 배치하다가 실패했어 미안;; -->
    <HomeCarousel />

    <div class="">
      <HomeDeposit />
      <HomeCurrency />
      <div class="">
        <HomeChatBot />
      </div>
    </div>
    <HomeBanklist />
  </div>
</template>

<script setup>
import HomeBanklist from "@/components/HomeBanklist.vue";
import HomeCarousel from "@/components/HomeCarousel.vue";
import HomeChatBot from "@/components/HomeChatBot.vue";
import HomeCurrency from "@/components/HomeCurrency.vue";
import HomeDeposit from "@/components/HomeDeposit.vue";
</script>

<style scoped></style>
