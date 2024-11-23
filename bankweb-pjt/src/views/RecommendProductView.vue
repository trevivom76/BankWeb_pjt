<template>
  <div>
    <hr>
    <div>
      <RouterLink :to="{ name: 'recommended1' }">나의 금융 목표 기반 추천</RouterLink>
      |
      <RouterLink :to="{ name: 'recommended2' }">자산 성장 시뮬레이션 기반 추천</RouterLink>
    </div>

    <RouterView />
  </div>
</template>

<script setup>
import { useAccountStore } from "@/stores/account";
import { useProfileStore } from "@/stores/profile";
import { onMounted, ref } from "vue";

const accountStore = useAccountStore();
const profileStore = useProfileStore();
</script>

<style scoped>
.username {
  color: blue;
}
</style>
