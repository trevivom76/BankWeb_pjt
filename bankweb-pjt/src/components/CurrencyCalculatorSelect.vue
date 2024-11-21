<template>
  <div>
    <div>
      <!-- Select 1 -->
      <div class="d-flex justify-space-between ga-5" :style="{ marginRight: '82px' }">
        <v-select class="select1" label="기준 통화 선택" v-model="selectedCountry" :items="countryCodes" variant="outlined"></v-select>
        <div class="currency-display1">
          <v-text-field width="100%" variant="outlined" v-model="formattedMoney1" @input="onInputMoney" solo></v-text-field>

          <!-- 천만~초기화 클릭박스 -->
          <div>
            <div class="button-group d-flex justify-end align-end flex-wrap mb-8 ga-2" :style="{ marginRight: '0px', paddingRight: '0px' }">
              <v-btn class="chunman" color="#686868" @click="addAmount(10000000)">억</v-btn>
              <v-btn class="chunman" color="#686868" @click="addAmount(10000000)">천만</v-btn>
              <v-btn class="baekman" color="#686868" @click="addAmount(1000000)">백만</v-btn>
              <v-btn class="sibman" color="#686868" @click="addAmount(100000)">십만</v-btn>
              <v-btn class="man" color="#686868" @click="addAmount(10000)">만</v-btn>
              <v-btn class="reset" @click="resetFields">초기화</v-btn>
              <!-- 클릭 시 필드 초기화 함수 실행 -->
            </div>
          </div>
        </div>
      </div>

      <!-- Select 2 -->
      <div class="d-flex justify-space-between ga-5" :style="{ marginRight: '82px' }">
        <v-select class="select2" label="바꿀 통화 선택" v-model="selectedCountry2" :items="countryCodes" variant="outlined"></v-select>
        <div class="currency-display2">
          <v-text-field variant="outlined" v-model="formattedMoney2" solo readonly></v-text-field>
          <!-- 클릭 시 환전 함수 실행 -->
          <div class="d-flex justify-space-between align-center mt-4"></div>
        </div>
      </div>

      <div class="d-flex justify-space-between">
        <p class="" :style="{ marginLeft: '59px', marginBottom: '56px' }">
          환율 계산기는 단순 참고용이므로 위 계산 결과는 환율변동 또는 우대율 적용에 따라 실제 거래 시 적용되는 환율과의 차이가 있을 수 있습니다.
        </p>
        <v-btn class="custom-button" @click="convertCurrency" :style="{ marginRight: '82px', marginBottom: '44px' }">환 전</v-btn>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue"; // Vue Composition API 함수
import { useCurrencyStore } from "@/stores/calculator.js"; // Pinia 스토어 가져오기

const currenystore = useCurrencyStore(); // Pinia 스토어 인스턴스 가져오기
const selectedCountry = ref(""); // 첫 번째 선택된 국가 코드
const selectedCountry2 = ref(""); // 두 번째 선택된 국가 코드
const countryCodes = ref([]); // 국가 코드 목록
const money1 = ref(""); // 입력된 실제 값
const formattedMoney1 = ref(""); // 포맷팅된 표시 값
const money2 = ref(""); // 환전된 실제 값
const formattedMoney2 = ref(""); // 포맷팅된 표시 값


const formatNumber = (value) => {
  if (!value) return "0";
  return new Intl.NumberFormat("ko-KR").format(value);
};


// 금액 입력 처리 함수
const onInputMoney = (event) => {
  const value = event.target.value.replace(/[^0-9]/g, ""); // 숫자만 추출
  money1.value = value; // 실제 값 저장
  formattedMoney1.value = formatNumber(value); // 포맷팅된 값 저장
};

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
    formattedMoney2.value = formatNumber(money2.value); // 포맷팅된 값 업데이트
  } else {
    alert("해당 국가의 환율 정보를 찾을 수 없습니다.");
  }  
};  

const addAmount = (amount) => {
  money1.value = (parseFloat(money1.value) || 0) + amount;
  formattedMoney1.value = formatNumber(money1.value); // 포맷팅된 값 업데이트
};  

const resetFields = () => {
  money1.value = "";
  formattedMoney1.value = ""; // 추가
  money2.value = "";
  formattedMoney2.value = ""; // 추가
};  




// 컴포넌트가 마운트될 때 실행
onMounted(() => {
  currenystore.usecurrency(); // Pinia 스토어에서 API 데이터 불러오기
  // currency 데이터가 변경될 때 국가 코드 목록을 업데이트
  watch(
    () => currenystore.currency, // 관찰할 대상: currency 데이터
    (newCurrency) => {          // 데이터가 변경될 때 실행할 콜백
      if (newCurrency && Array.isArray(newCurrency)) {                // 데이터가 배열인지 확인
        countryCodes.value = newCurrency.map((item) => item.cur_unit); // 국가 코드 목록 만들기
      }
    },
    { immediate: true } // 컴포넌트가 마운트될 때도 실행
  );
});
</script>

<style scoped>
.select1,
.select2 {
  font-size: 11px;
  max-width: 226px; /* 최대 너비 설정 */
  max-height: 44px;
  margin-right: 11px;
  margin-left: 59px;
}

.currency-display1,
.currency-display2 {
  width: 65%;
}

.button-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 11px;
  height: 21px;
  text-align: center; /* 텍스트 가운데 정렬 */
  font-family: "Pretendard", sans-serif; /* Pretendard 폰트 적용 */
}

.v-btn {
  min-width: 26px;
  max-width: 36px;
  max-height: 21px;
  font-size: 11px;
  font-weight: 700;
  border-radius: 5px;
  font-family: "Pretendard", sans-serif; /* Pretendard 폰트 적용 */
}

.reset {
  max-width: 45px;
  color: white;
  background-color: #c1c1c1;
}

.custom-button {
  min-width: 71px;
  min-height: 44px;
  background-color: #0b5bcb; /* 원하는 색상 코드 */
  color: white; /* 텍스트 색상 */
  font-size: 14px;
  font-family: "Pretendard", sans-serif; /* Pretendard 폰트 적용 */
  font-weight: 800;
}

p {
  font-size: 11px;
  color: #bdbdbd;
}
</style>

<!-- 'Pretendard', sans-serif -->
