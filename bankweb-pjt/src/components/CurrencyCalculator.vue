<template>
  <div>
    <v-card class="calculator container" color="white" justify="center">
      <p :style="{ fontWeight: 'bold', fontSize: '24px', color: 'black' }">환율 계산기</p>
      <CurrencyCalculatorSelect />
    </v-card>
    <div class="container">
      <!-- <CurrencyCalculatorGraph /> -->
    </div>
  </div>
</template>

<script setup>
import { VCard } from "vuetify/components";
import CurrencyCalculatorSelect from "./CurrencyCalculatorSelect.vue"; // CurrencyCalculatorSelect 컴포넌트 가져오기
// import CurrencyCalculatorGraph from "./CurrencyCalculatorGraph.vue";
</script>

<style scoped>
.calculator {
  max-width: 949px; /* 반응형 최대 너비 설정 */
  max-height: 426px;
  border-radius: 20px;
  min-width: 600px;
}

p {
  margin-bottom: 42px; /* 여백을 설정하여 요소 간 간격을 유지 */
  margin-top: 38px;
  margin-left: 31px;
}
</style>
