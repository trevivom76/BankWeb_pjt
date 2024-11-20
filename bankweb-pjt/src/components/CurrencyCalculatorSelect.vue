<template>
  <div v-for="cur in currenystore.currency">
    {{ cur.cur_unit }}
  </div>

  <div>
    <v-row>
      <!-- Select 1 -->
      <v-col cols="12">
        <v-row justify="space-between">
          <v-col class="allofthem1" cols="5" sm="4">
            <v-select class="select1" label="Select 1" :items="[]" variant="outlined"></v-select>
          </v-col>
          <v-col class="allofthem2" cols="7" sm="8">
            <div class="currency-display1">
              <v-text-field class="currency-amount" variant="outlined" solo value="1,000,000"></v-text-field>
            </div>
          </v-col>
        </v-row>
      </v-col>

      <!-- Select 2 -->
      <v-col cols="12">
        <v-row justify="space-between">
          <v-col class="allofthem1" cols="5" sm="4">
            <v-select class="select2" label="Select 2" :items="['California', 'Colorado', 'Florida', 'Georgia', 'Texas', 'Wyoming']" variant="outlined"></v-select>
          </v-col>
          <v-col class="allofthem2" cols="7" sm="8">
            <v-text-field class="currency-amount currency-display2" variant="outlined" solo value="1,000,000"></v-text-field>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <!-- 천만~초기화 클릭박스 -->
    <v-card-actions>
      <v-row justify="space-between">
        <v-col cols="4" class="text-xs-center">
          <v-btn class="chunman">천만</v-btn>
        </v-col>

        <v-col cols="4" class="text-xs-center">
          <v-btn class="baekman">백만</v-btn>
        </v-col>

        <v-col cols="4" class="text-xs-center">
          <v-btn class="sibman">십만</v-btn>
        </v-col>

        <v-col cols="4" class="text-xs-center">
          <v-btn class="man">만</v-btn>
        </v-col>

        <v-col cols="4" class="text-xs-center">
          <v-btn class="reset">초기화</v-btn>
        </v-col>
      </v-row>
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
/* 기본 스타일을 Flexbox 또는 Grid를 사용하여 반응형으로 설정합니다. */
/* .allofthem1 {
  padding-right: 0px;
}

.allofthem2 {
  padding-left: 0px;
} */

.select1,
.select2 {
  font-size: 11px;
  width: 100%; /* 너비를 부모 요소에 맞추기 */
  width: 226px; /* 최대 너비 설정 */
  max-height: 44px;
  margin-bottom: 55px; /* 요소 간의 간격을 설정 */
  margin-right: 22px;
  margin-left: 59px;
}

.currency-display1,
.currency-display2 {
  font-size: 11px;
  width: 100%; /* 너비를 부모 요소에 맞추기 */
  width: 560px; /* 최대 너비 설정 */
  max-height: 44px;
  margin-bottom: 8px; /* 요소 간의 간격을 설정 */
  margin-right: 22px;
  padding: 0px;
}

/* 버튼 스타일을 반응형으로 설정 */
.eok,
.chunman,
.baekman,
.sibman,
.man,
.reset {
  background-color: black; /* 버튼의 배경 색상 */
  color: white; /* 텍스트 색상 */
  font-size: 11px;
  font-weight: bold;
  height: 21px;
  min-width: 45px; /* 최소 너비 설정 */
  padding: 4px 8px; /* 안쪽 여백 */
  margin: 4px; /* 버튼 간의 간격 */
  text-align: center; /* 텍스트 가운데 정렬 */
}
</style>

<!-- 
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
</style> -->
