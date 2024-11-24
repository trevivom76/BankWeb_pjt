<template>
  <div class="container">
    <div class="card">
      <h1 :style="{ fontWeight: 600 , fontSize: '24px'}">
        주변은행
        <span :style="{ color: '#0B5BCB' }">검색하기</span>
      </h1>
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
.card {
  background-color: white;
  padding: 48px 40px;
  border-radius: 20px;
}
</style>
