<template>
  <div class="d-flex justify-center align-center">
    <v-card class="pa-12" width="100%" height="100%" rounded="xl">
      <h1 class="mb-10" :style="{ marginLeft: '90px' }">
        주변은행
        <span :style="{ color: '#0B5BCB' }">검색하기</span>
      </h1>
      <div class="d-flex justify-start align-center mb-5" :style="{ marginLeft: '90px' }">
        <BankMapSelect @change="handleRegionChange" />
      </div>
      <BankMap :selected-region="selectedRegion" />
      <BankMapProducts />
    </v-card>
  </div>
</template>

<script setup>
import BankMapSelect from "@/components/BankMapSelect.vue";
import BankMap from "@/components/BankMap.vue";
import BankMapProducts from "@/components/BankMapProducts.vue";
import { ref } from "vue";

// <BankMapSelect> 에서 선택된 Regin정보를 보관하여 <BankMap> 에 넘겨줌
const selectedRegion = ref({});
const handleRegionChange = (selection) => {
  selectedRegion.value = selection;
};
</script>

<style scoped></style>
