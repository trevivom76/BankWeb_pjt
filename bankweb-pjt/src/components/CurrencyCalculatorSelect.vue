<template>
  <div>
    <div class="select-container">
      <v-select class="select1" label="기준 통화 선택" v-model="selectedCountry" :items="countryCodes" variant="outlined" />
      <div class="currency-display1">
        <div class="input-container">
          <img v-if="selectedCountry" :src="flagIcons[selectedCountry]" alt="국기" class="flag-icon" />
          <input type="text" :value="formattedMoney1" @input="onInputMoney" class="money-input" />
          <span v-if="selectedCountry" class="currency-symbol">{{ currencySymbols[selectedCountry] }}</span>
        </div>
      </div>
    </div>

    <div class="button-group">
      <button class="money-btn" @click="addAmount(100000000)">억</button>
      <button class="money-btn" @click="addAmount(10000000)">천만</button>
      <button class="money-btn" @click="addAmount(1000000)">백만</button>
      <button class="money-btn" @click="addAmount(100000)">십만</button>
      <button class="money-btn" @click="addAmount(10000)">만</button>
      <button class="money-btn btn-reset" @click="resetFields">초기화</button>
    </div>

    <div class="select-container pt-3">
      <v-select class="select1" label="바꿀 통화 선택" v-model="selectedCountry2" :items="countryCodes" variant="outlined" />
      <div class="currency-display2">
        <div class="input-container">
          <img v-if="selectedCountry2" :src="flagIcons[selectedCountry2]" alt="국기" class="flag-icon" />
          <input type="text" :value="formattedMoney2" @input="onInputMoney" class="money-input" />
          <span v-if="selectedCountry2" class="currency-symbol">{{ currencySymbols[selectedCountry2] }}</span>
        </div>
      </div>
    </div>

    <div class="bottom-container">
      <p class="text">환율 계산기는 단순 참고용이므로 위 계산 결과는 환율변동 또는 우대율 적용에 따라 실제 거래 시 적용되는 환율과의 차이가 있을 수 있습니다.</p>
      <button class="btn btn-change" @click="swapCountries">
        <v-icon size="large">mdi-cached</v-icon>
      </button>
      <button class="btn btn-check" @click="convertCurrency">환전</button>
    </div>
  </div>

  <!-- 경고 다이얼로그 -->
  <v-dialog v-model="showModal" max-width="400">
    <div class="card">
      <div class="scene">
        <!-- 그림자 -->
        <div class="shadow"></div>
        <div class="cube">
          <img src="@/assets/icon/caution.png" alt="Caution Icon" class="cube-face front" />
          <img src="@/assets/icon/caution_back.png" alt="Caution Icon" class="cube-face back" />
        </div>
      </div>
      <p style="font-size: 22px; font-weight: 500; text-align: center;">{{ modalMessage }}</p>
      <div class="card-footer">
        <button class="btn btn-submit" @click="showModal = !showModal">확인</button>
      </div>
    </div>
  </v-dialog>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useCurrencyStore } from "@/stores/calculator.js";

const currenystore = useCurrencyStore();
const selectedCountry = ref("");
const selectedCountry2 = ref("");
const countryCodes = ref([]);
const money1 = ref("");
const formattedMoney1 = ref("");
const money2 = ref("");
const formattedMoney2 = ref("");

const showModal = ref(false);
const modalMessage = ref("");

const formatNumber = (value) => {
  if (!value) return "0";
  return new Intl.NumberFormat("ko-KR").format(value);
};

const onInputMoney = (event) => {
  const value = event.target.value.replace(/[^0-9]/g, "");
  money1.value = value;
  formattedMoney1.value = formatNumber(value);
};

const convertCurrency = () => {
  if (!selectedCountry.value) {
    modalMessage.value = "기준 통화를 선택해주세요.";
    showModal.value = true;
    return;
  }
  if (!selectedCountry2.value) {
    modalMessage.value = "바꿀 통화를 선택해주세요.";
    showModal.value = true;
    return;
  }
  if (!money1.value) {
    modalMessage.value = "금액을 입력해주세요.";
    showModal.value = true;
    return;
  }

  const country1 = currenystore.currencies.find((item) => item.cur_unit === selectedCountry.value);
  const country2 = currenystore.currencies.find((item) => item.cur_unit === selectedCountry2.value);

  if (country1 && country2) {
    const rate1 = parseFloat(country1.deal_bas_r.replace(",", ""));
    const rate2 = parseFloat(country2.deal_bas_r.replace(",", ""));
    money2.value = ((parseFloat(money1.value) * rate1) / rate2).toFixed(2);
    formattedMoney2.value = formatNumber(money2.value);
  } else {
    modalMessage.value = "해당 국가의 환율 정보를 찾을 수 없습니다.";
    showModal.value = true;
  }
};

const addAmount = (amount) => {
  money1.value = (parseFloat(money1.value) || 0) + amount;
  formattedMoney1.value = formatNumber(money1.value);
};

const resetFields = () => {
  money1.value = "";
  formattedMoney1.value = "";
  money2.value = "";
  formattedMoney2.value = "";
};

const swapCountries = () => {
  [selectedCountry.value, selectedCountry2.value] = [selectedCountry2.value, selectedCountry.value];
  [formattedMoney1.value, formattedMoney2.value] = [formattedMoney2.value, formattedMoney1.value];
  [money1.value, money2.value] = [money2.value, money1.value];
};

const currencySymbols = {
  USD: "$", KRW: "₩", EUR: "€", 'JPY(100)': "¥", AED: "د.إ",
  AUD: "A$", BHD: "ب.د", BND: "B$", CAD: "C$", CHF: "CHF",
  CNH: "¥", DKK: "kr", GBP: "£", HKD: "HK$", 'IDR(100)': "Rp",
  KWD: "KD", MYR: "RM", NOK: "kr", NZD: "NZ$", SAR: "ر.س",
  SEK: "kr", SGD: "S$", THB: "฿"
};

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
  'JPY(100)': "https://upload.wikimedia.org/wikipedia/en/9/9e/Flag_of_Japan.svg", // 일본 엔
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

onMounted(() => {
  currenystore.fetchCurrencies();
});

watch(() => currenystore.currencies, (newCurrencies) => {
  if (newCurrencies && Array.isArray(newCurrencies)) {
    countryCodes.value = newCurrencies.map((item) => item.cur_unit);
  }
}, { immediate: true });

</script>

<style scoped>
.select-container {
  display: flex;
  flex-direction: row;
  width: 100%;
  gap: 16px;
  /* 간격 추가 */
}

.currency-display1,
.currency-display2 {
  flex: 1;
  /* 남은 공간을 모두 차지하도록 설정 */
}

.inner-text {
  display: flex;
  flex-direction: row;
  gap: 4px;

}

.input-container {
  display: flex;
  align-items: center;
  align-content: center;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 15px 12px;
  background: white;
  width: 100%;
}

.flag-icon {
  width: 24px;
  height: 24px;
  object-fit: cover;
  filter:
    drop-shadow(2px 2px 2px rgba(0, 0, 0, 0.4)) drop-shadow(-2px -2px 2px rgba(255, 255, 255, 0.4)) drop-shadow(0 0 5px rgba(0, 0, 0, 0.2));
}

.money-input {
  flex: 1;
  border: none;
  outline: none;
  text-align: right;
  padding: 0 8px;
  font-size: 16px;
}

.currency-symbol {
  width: 40px;
  color: #666;
  font-size: 16px;
  text-align: right;
  flex-shrink: 0;
}

.input-container:focus-within {
  border-color: #000000;
  box-shadow: 0 0 0 1px #000000;
}

.input-container:hover {
  border-color: #666;
}

.button-group {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  gap: 8px;
  margin: 8px 0px 20px 0px;
  height: auto;
}

.money-btn {
  font-weight: 400;
  font-size: 12px;
  background-color: #686868;
  padding: 4px 8px;
  border-radius: 4px;
  color: white;
}

.btn-reset {
  background-color: #C1C1C1;
}

.select1,
.select2 {
  font-size: 11px;
  max-width: 226px;
  max-height: 44px;
  margin-right: 11px;
  flex-shrink: 0;
}

.btn {
  display: inline-block;
}

.btn-check {
  width: 80px;
}

.btn-change {
  width: 60px;
}

.flag-icon {
  width: 32px;
  height: 20px;
  margin-left: 8px;
  flex-shrink: 0;
}

.text {
  width: auto;
  flex: 1;
  font-size: 11px;
  color: #BDBDBD;
}

.bottom-container {
  width: 100%;
  display: flex;
  flex-direction: row;
  gap: 12px;
  padding-top: 32px;
  align-items: center;
}

/* 3D 애니메이션 컨테이너 */
.scene {
  width: 200px;
  /* 컨테이너 크기 */
  height: 200px;
  perspective: 1000px;
  /* 3D 원근감 추가 */
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0px auto 40px;
  /* 가운데 정렬 */
  position: relative;
  /* 그림자 배치를 위한 기준 */
}

/* 그림자 */
.shadow {
  position: absolute;
  bottom: -20px;
  /* 그림자를 컨테이너 아래로 배치 */
  width: 150px;
  height: 20px;
  background: radial-gradient(ellipse at center, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0));
  border-radius: 50%;
  z-index: -1;
  /* 3D 객체 아래로 배치 */
  filter: blur(5px);
  /* 부드러운 그림자 효과 */
}

/* 3D 객체 */
.cube {
  width: 100%;
  height: 100%;
  position: relative;
  transform-style: preserve-3d;
  /* 3D 효과 유지 */
  animation: spin 3s infinite linear;
  /* 좌우 회전 애니메이션 */
}

/* 공통 이미지 스타일 */
.cube-face {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  backface-visibility: hidden;
  /* 뒷면 숨김 */
}

/* 앞면 배치 */
.front {
  transform: rotateY(0deg)
    /* 3D 공간에서 앞면 배치 */
}

/* 뒷면 배치 */
.back {
  transform: rotateY(180deg)
    /* 3D 공간에서 뒷면 배치 */
}

/* 3D 회전 애니메이션 정의 */
@keyframes spin {
  0% {
    transform: rotateY(0deg);
    /* 초기 상태 */
  }

  50% {
    transform: rotateY(180deg);
    /* 180도 회전 */
  }

  100% {
    transform: rotateY(360deg);
    /* 360도 회전 */
  }
}

.card {
  background-color: white;
  padding: 36px 40px 48px 40px;
  border-radius: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  animation: card-load 0.8s ease;
}

.card-footer {
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 20px;
  padding: 20px;
}

@keyframes card-load {
  0% {
    transform: scale(0.95);
    opacity: 0;
  }

  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.location-icon:hover {
  transform: scale(1.2);
  /* 마우스 오버 시 확대 및 회전 */
}

.btn-submit {
  width: 300px;
  font-size: 18px;
  margin-top: 20px;
  background-color: #666666;
}

.btn-submit:hover {
  width: 300px;
  font-size: 18px;
  margin-top: 20px;
  background-color: #3f3f3f;
}
</style>