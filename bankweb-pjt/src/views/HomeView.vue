<template>
  <div class="container">
    <HomeCarousel />
    <div>
      <div>
        <HomeDeposit />
        <HomeCurrency />
      </div>
      <HomeChatBot />
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
</style>
