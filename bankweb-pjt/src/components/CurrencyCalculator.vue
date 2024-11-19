<template>
  <div>
    <v-container class="pa-4">
      <v-card class="calculator" color="white">
        <v-card-title class="text-h6">환율 계산기</v-card-title>

        <CurrencyCalculatorSelect />
        <v-card-text class="information">환율 계산기는 단순 참고용이므로 위 계산 결과는 환율변동 또는 우대율 적용에 따라 실제 거래 시 적용되는 환율과의 차이가 있을 수 있습니다.</v-card-text>

        <v-card-actions>
          <v-flex xs12 sm4 text-xs-center>
            <v-btn class="custom-button">환전</v-btn>
          </v-flex>
        </v-card-actions>
      </v-card>
    </v-container>
  </div>
</template>

<script setup>
import { VCard, VCardTitle, VCardText, VCardActions, VBtn, VContainer } from "vuetify/components";
import CurrencyCalculatorSelect from "./CurrencyCalculatorSelect.vue"; // CurrencyCalculatorSelect 컴포넌트 가져오기
import { useCurrencyStore } from '@/stores/calculator.js' 
import { onMounted } from "vue";
const currenystore = useCurrencyStore()
onMounted(currenystore.usecurrency)
</script>

<style scoped>
.calculator {
  position: relative;
  width: 949px;
  height: 426px;
  margin: 0 auto;
  border-radius: 20px;
}

.text-h6 {
  position: relative;
  font-weight: bold;
  font-size: 24px;
  left: 40px;
  top: 48px;
  bottom: 349px;
  right: 799px;
}

.information {
  position: absolute;
  left: 56px;
  bottom: 58px;
  right: 188px;
  top: 348px;
  font-size: 11px;
}

.custom-button {
  background-color: #0b5bcb; /* 원하는 색상 코드 */
  color: white; /* 텍스트 색상 */
  font-size: 14px;
  height: 44px;
  width: 71px;
  position: absolute;
  right: 85px;
  bottom: 46px;
}
</style>
