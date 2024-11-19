<template>
  <div class="d-flex justify-center align-center">
    <v-card class="px-10 pt-12" width="950px" height="785px" rounded="xl">

      <p :style="{ fontWeight: 'bold' , fontSize: '24px'}">
        주변은행
        <span :style="{ color: '#0B5BCB' }">검색하기</span>
      </p>

      <div class="mt-11">
        <BankMapSelect @change="handleRegionChange" />
      </div>

      <BankMap :selected-region="selectedRegion" />
      
    </v-card>
  </div>
</template>

<script setup>
import BankMapSelect from "@/components/BankMapSelect.vue";
import BankMap from "@/components/BankMap.vue";
import { ref } from "vue";

// <BankMapSelect> 에서 선택된 Regin정보를 보관하여 <BankMap> 에 넘겨줌
const selectedRegion = ref({});
const handleRegionChange = (selection) => {
  selectedRegion.value = selection;
};
</script>

<style scoped></style>
