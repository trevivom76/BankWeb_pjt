<template>
  <div>
    <div>
      <!-- Select 1 -->
      <div class="d-flex justify-space-between ga-5" :style="{ marginRight: '82px' }">
        <v-select class="select1" label="기준 통화 선택" v-model="selectedCountry" :items="countryCodes" variant="outlined"></v-select>
        <div class="currency-display1">
          <v-text-field width="100%" variant="outlined" v-model="formattedMoney1" @input="onInputMoney" solo>
            <template #append-inner>
              <span v-if="selectedCountry" class="currency-symbol">{{ currencySymbols[selectedCountry] }}</span>
              <img v-if="selectedCountry" :src="flagIcons[selectedCountry]" alt="국기" class="flag-icon" />
            </template>
          </v-text-field>

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
          <v-text-field variant="outlined" v-model="formattedMoney2" solo readonly>
            <template #append-inner>
              <span v-if="selectedCountry2" class="currency-symbol">{{ currencySymbols[selectedCountry2] }}</span>
              <img v-if="selectedCountry2" :src="flagIcons[selectedCountry2]" alt="국기" class="flag-icon" />
            </template>
          </v-text-field>

          <!-- <img v-if="selectedCountry2" :src="flagIcons[selectedCountry2]" alt="국기" class="flag-icon" /> -->
          <!-- 클릭 시 환전 함수 실행 -->
          <div class="d-flex justify-space-between align-center mt-4"></div>
        </div>
      </div>

      <div class="d-flex justify-space-between">
        <p class="" :style="{ marginLeft: '59px', marginBottom: '56px' }">
          환율 계산기는 단순 참고용이므로 위 계산 결과는 환율변동 또는 우대율 적용에 따라 실제 거래 시 적용되는 환율과의 차이가 있을 수 있습니다.
        </p>
        <v-btn class="reverse" @click="swapCountries" :style="{ marginRight: '82px', marginBottom: '44px' }">
          <v-icon size="large">mdi-cached</v-icon>
        </v-btn>
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

// 국가 코드 교환 함수
const swapCountries = () => {
  // selectedCountry와 selectedCountry2 교환
  const tempCountry = selectedCountry.value;
  selectedCountry.value = selectedCountry2.value;
  selectedCountry2.value = tempCountry;

  // formattedMoney1과 formattedMoney2 교환
  const tempMoney = formattedMoney1.value;
  formattedMoney1.value = formattedMoney2.value;
  formattedMoney2.value = tempMoney;

  // money1과 money2 교환 (실제 값도 교환)
  const tempActualMoney = money1.value;
  money1.value = money2.value;
  money2.value = tempActualMoney;
};

// 통화 심볼과 국기 매핑
const currencySymbols = {
  USD: "$",
  KRW: "₩",
  EUR: "€",
  'JPY(100)' : "¥",
  AED: "د.إ",
  AUD: "A$",
  BHD: "ب.د",
  BND: "B$",
  CAD: "C$",
  CHF: "CHF",
  CNH: "¥",
  DKK: "kr",
  GBP: "£",
  HKD: "HK$",
  'IDR(100)': "Rp",
  KWD: "KD",
  MYR: "RM",
  NOK: "kr",
  NZD: "NZ$",
  SAR: "ر.س",
  SEK: "kr",
  SGD: "S$",
  THB: "฿",
};

// 국기 표출을 위한 URL 추가, 필요한 국가 코드들(이건 내가 일일히 넣어줘야 함)
const flagIcons = {
  AED: "https://upload.wikimedia.org/wikipedia/commons/c/cb/Flag_of_the_United_Arab_Emirates.svg", // 아랍에미리트 디르함
  AUD: "https://upload.wikimedia.org/wikipedia/commons/b/b9/Flag_of_Australia.svg", // 호주 달러
  BHD: "https://upload.wikimedia.org/wikipedia/commons/2/2c/Flag_of_Bahrain.svg", // 바레인 디나르
  BND: "https://upload.wikimedia.org/wikipedia/commons/9/9c/Flag_of_Brunei.svg", // 브루나이 달러
  CAD: "https://upload.wikimedia.org/wikipedia/commons/c/cf/Flag_of_Canada.svg", // 캐나다 달러
  CHF: "https://upload.wikimedia.org/wikipedia/commons/f/f3/Flag_of_Switzerland.svg", // 스위스 프랑
  CNH: "https://upload.wikimedia.org/wikipedia/commons/f/fa/Flag_of_the_People%27s_Republic_of_China.svg", // 위안화
  DKK: "https://upload.wikimedia.org/wikipedia/commons/9/9c/Flag_of_Denmark.svg", // 덴마크 크로네
  EUR: "https://upload.wikimedia.org/wikipedia/commons/b/b7/Flag_of_Europe.svg", // 유로
  GBP: "https://upload.wikimedia.org/wikipedia/en/a/ae/Flag_of_the_United_Kingdom.svg", // 영국 파운드
  HKD: "https://upload.wikimedia.org/wikipedia/commons/5/5b/Flag_of_Hong_Kong.svg", // 홍콩 달러
  'IDR(100)': "https://upload.wikimedia.org/wikipedia/commons/9/9f/Flag_of_Indonesia.svg", // 인도네시아 루피아
  'JPY(100)' : "https://upload.wikimedia.org/wikipedia/en/9/9e/Flag_of_Japan.svg", // 일본 엔
  KRW: "https://upload.wikimedia.org/wikipedia/commons/0/09/Flag_of_South_Korea.svg", // 한국 원
  KWD: "https://upload.wikimedia.org/wikipedia/commons/a/aa/Flag_of_Kuwait.svg", // 쿠웨이트 디나르
  MYR: "https://upload.wikimedia.org/wikipedia/commons/6/66/Flag_of_Malaysia.svg", // 말레이시아 링기트
  NOK: "https://upload.wikimedia.org/wikipedia/commons/d/d9/Flag_of_Norway.svg", // 노르웨이 크로네
  NZD: "https://upload.wikimedia.org/wikipedia/commons/3/3e/Flag_of_New_Zealand.svg", // 뉴질랜드 달러
  SAR: "https://upload.wikimedia.org/wikipedia/commons/0/0d/Flag_of_Saudi_Arabia.svg", // 사우디 리얄
  SEK: "https://upload.wikimedia.org/wikipedia/commons/4/4c/Flag_of_Sweden.svg", // 스웨덴 크로나
  SGD: "https://upload.wikimedia.org/wikipedia/commons/4/48/Flag_of_Singapore.svg", // 싱가포르 달러
  THB: "https://upload.wikimedia.org/wikipedia/commons/a/a9/Flag_of_Thailand.svg", // 태국 바트
  USD: "https://upload.wikimedia.org/wikipedia/en/a/a4/Flag_of_the_United_States.svg", // 미국 달러
};

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

.reverse {
  min-height: 44px;
  font-size: 11px;
  font-family: "Pretendard", sans-serif; /* Pretendard 폰트 적용 */
  font-weight: 800;
  background-color: #0b5bcb; /* 원하는 색상 코드 */
  color: white; /* 텍스트 색상 */
}

p {
  font-size: 11px;
  color: #bdbdbd;
}

.flag-icon {
  width: 32px;
  height: 20px;
  margin-left: 8px;
}
</style>

<!-- 'Pretendard', sans-serif -->
