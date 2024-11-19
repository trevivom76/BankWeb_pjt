<template>
  <div v-for="cur in currenystore.currency">
    {{ cur.cur_unit }}
  </div>
  <div>
    <v-row>
      <v-col cols="12">
        <v-select class="select1" label="Select 1" :items="[]" variant="outlined"></v-select>
        <div class="currency-display1">
          <v-text-field class="currency-amount" variant="outlined" solo value="1,000,000"></v-text-field>
        </div>
      </v-col>
      <v-col cols="12">
        <v-select class="select2" label="Select 2" :items="['California', 'Colorado', 'Florida', 'Georgia', 'Texas', 'Wyoming']" variant="outlined"></v-select>
        <div class="currency-display2">
          <v-text-field class="currency-amount" variant="outlined" solo value="1,000,000"></v-text-field>
        </div>
      </v-col>
    </v-row>
    <v-card-actions>
      <v-flex xs12 sm4 text-xs-center>
        <v-btn class="chunman">천만</v-btn>
      </v-flex>
      <v-flex xs12 sm4 text-xs-center>
        <v-btn class="baekman">백만</v-btn>
      </v-flex>
      <v-flex xs12 sm4 text-xs-center>
        <v-btn class="sibman">십만</v-btn>
      </v-flex>
      <v-flex xs12 sm4 text-xs-center>
        <v-btn class="man">만</v-btn>
      </v-flex>
      <v-flex xs12 sm4 text-xs-center>
        <v-btn class="reset">초기화</v-btn>
      </v-flex>
    </v-card-actions>
  </div>
</template>

<script setup>
import CurrencyCalculatorSelect from "./CurrencyCalculatorSelect.vue"; // CurrencyCalculatorSelect 컴포넌트 가져오기
import { useCurrencyStore } from "@/stores/calculator.js";
import { onMounted } from "vue";
const currenystore = useCurrencyStore();
onMounted(currenystore.usecurrency);
</script>

<style scoped>
.select1 {
  position: absolute;
  left: 56px;
  right: 667px;
  top: 138px;
  bottom: 244px;
  font-size: 11px;
  width: 226px;
  height: 44px;
  /* border-color: #0b5bcb !important;
    border-width: 2px; */
}

.select2 {
  position: absolute;
  left: 56px;
  right: 667px;
  top: 237px;
  bottom: 145px;
  font-size: 11px;
  width: 226px;
  height: 44px;
}

.currency-display1 {
  position: absolute;
  left: 304px;
  right: 82px;
  top: 140px;
  bottom: 242px;
  font-size: 11px;
  width: 560px;
  height: 44px;
}

.currency-display2 {
  position: absolute;
  left: 304px;
  right: 82px;
  top: 237px;
  bottom: 145px;
  font-size: 11px;
  width: 560px;
  height: 44px;
}

.eok {
  position: absolute;
  background-color: black; /* 원하는 색상 코드 */
  color: white; /* 텍스트 색상 */
  font-size: 11px;
  font-weight: bold;
  height: 21px;
  width: 26px;
  top: 192px;
  bottom: 213px;
  left: 622px;
  right: 301px;
}

.chunman {
  position: absolute;
  background-color: black; /* 원하는 색상 코드 */
  color: white; /* 텍스트 색상 */
  font-size: 11px;
  font-weight: bold;
  height: 21px;
  width: 36px;
  top: 192px;
  bottom: 213px;
  left: 656px;
  right: 257px;
  gap: 8px;
}

.baekman {
  position: absolute;
  background-color: black; /* 원하는 색상 코드 */
  color: white; /* 텍스트 색상 */
  font-size: 11px;
  font-weight: bold;
  width: 36px;
  height: 21px;
  top: 192px;
  bottom: 213px;
  left: 700px;
  right: 213px;
}

.sibman {
  position: absolute;
  background-color: black; /* 원하는 색상 코드 */
  color: white; /* 텍스트 색상 */
  font-size: 11px;
  font-weight: bold;
  width: 36px;
  height: 21px;
  top: 192px;
  bottom: 213px;
  left: 744px;
  right: 169px;
}

.man {
  position: absolute;
  background-color: black; /* 원하는 색상 코드 */
  color: white; /* 텍스트 색상 */
  font-size: 11px;
  font-weight: bold;
  width: 26px;
  height: 21px;
  top: 192px;
  bottom: 213px;
  left: 788px;
  right: 135px;
}

.reset {
  position: absolute;
  background-color: black; /* 원하는 색상 코드 */
  color: white; /* 텍스트 색상 */
  font-size: 11px;
  font-weight: bold;
  width: 45px;
  height: 21px;
  top: 192px;
  bottom: 213px;
  left: 822px;
  right: 82px;
}
</style>
