<template>
  <div>
    <div>
      <!-- Select 1 -->
      <v-col cols="12">
        <v-row justify="space-between">
          <v-col cols="5" sm="4">
            <v-select width="226px" class="select1" label="Select 1" v-model="selectedCountry" :items="countryCodes" variant="outlined"></v-select>
          </v-col>
          <v-col cols="7" sm="8">
            <div class="currency-display1">
              <v-text-field class="currency-amount" variant="outlined" v-model="money1" solo></v-text-field>
            </div>
          </v-col>
        </v-row>
      </v-col>

      <!-- Select 2 -->
      <v-col cols="12">
        <v-row justify="space-between">
          <v-col cols="5" sm="4">
            <v-select width="226px" class="select2" label="Select 2" v-model="selectedCountry2" :items="countryCodes" variant="outlined"></v-select>
          </v-col>
          <v-col cols="7" sm="8">
            <div class="currency-display2">
              <v-text-field class="currency-amount" variant="outlined" v-model="money2" solo readonly></v-text-field>
            </div>
          </v-col>
        </v-row>
      </v-col>
    </div>

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
          <v-btn class="reset" @click="resetFields">초기화</v-btn>
          <!-- 클릭 시 필드 초기화 함수 실행 -->
        </v-col>

        <v-card-actions>
          <v-btn class="custom-button" @click="convertCurrency">환전</v-btn>
          <!-- 클릭 시 환전 함수 실행 -->
        </v-card-actions>
      </v-row>
    </v-card-actions>
  </div>
</template>

<script setup>
// import CurrencyCalculatorSelect from "./CurrencyCalculatorSelect.vue"; // CurrencyCalculatorSelect 컴포넌트 가져오기
import { ref, onMounted, watch } from "vue"; // Vue Composition API 함수
import { useCurrencyStore } from "@/stores/calculator.js"; // Pinia 스토어 가져오기

const currenystore = useCurrencyStore(); // Pinia 스토어 인스턴스 가져오기
const selectedCountry = ref(""); // 첫 번째 선택된 국가 코드
const selectedCountry2 = ref(""); // 두 번째 선택된 국가 코드
const countryCodes = ref([]); // 국가 코드 목록
const money1 = ref(""); // 입력된 금액
const money2 = ref(""); // 환전된 금액

// 컴포넌트가 마운트될 때 실행
onMounted(() => {
  currenystore.usecurrency(); // Pinia 스토어에서 API 데이터 불러오기

  // currency 데이터가 변경될 때 국가 코드 목록을 업데이트
  watch(
    () => currenystore.currency, // 관찰할 대상: currency 데이터
    (newCurrency) => {
      // 데이터가 변경될 때 실행할 콜백
      if (newCurrency && Array.isArray(newCurrency)) {
        // 데이터가 배열인지 확인
        console.log("Loaded currency data:", newCurrency); // 디버깅용 출력
        countryCodes.value = newCurrency.map((item) => item.cur_unit); // 국가 코드 목록 만들기
      }
    },
    { immediate: true } // 컴포넌트가 마운트될 때도 실행
  );
});

// 환전
const convertCurrency = () => {
  if (!selectedCountry.value || !selectedCountry2.value || !money1.value) {
    alert("금액을 올바르게 입력해주세요!!");
    return;
  }

  // 선택한 국가의 환율 정보 가져오기
  const country1 = currenystore.currency.find((item) => item.cur_unit === selectedCountry.value);

  const country2 = currenystore.currency.find((item) => item.cur_unit === selectedCountry2.value);

  if (country1 && country2) {
    const rate1 = parseFloat(country1.deal_bas_r.replace(",", "")); // 쉼표 제거 후 숫자 변환
    const rate2 = parseFloat(country2.deal_bas_r.replace(",", "")); // 쉼표 제거 후 숫자 변환

    money2.value = ((money1.value * rate1) / rate2).toFixed(2);
  } else {
    alert("해당 국가의 환율 정보를 찾을 수 없습니다.");
  }
};

const reset = () => {
  selectedCountry.value = "";
  selectedCountry2.value = "";
  money1.value = 0;
  money2.value = 0;
};
</script>

<style scoped>
.select1,
.select2 {
  font-size: 11px;
  max-width: 226px; /* 최대 너비 설정 */
  max-height: 44px;
  margin-bottom: 55px; /* 요소 간의 간격을 설정 */
  margin-right: 22px;
  margin-left: 59px;
}

.currency-display1,
.currency-display2 {
  font-size: 11px;
  max-width: 560px; /* 최대 너비 설정 */
  max-height: 44px;
  margin-bottom: 8px; /* 요소 간의 간격을 설정 */
  margin-right: 22px;
 
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

.custom-button {
  background-color: #0b5bcb; /* 원하는 색상 코드 */
  color: white; /* 텍스트 색상 */
  font-size: 14px;
  height: 44px;
  width: 100px; /* 버튼의 크기를 더 명확하게 조정 */
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
