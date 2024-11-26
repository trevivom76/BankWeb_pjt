<template>
  <div>
    <div class = "box">
      <div class="title-box">
        <img src="@/assets/icon/Calculator_icon.png" alt="예금 계산기 아이콘" class="icon">
        <p class="title">예금 계산기</p>
      </div>
      <article class="cont-select">
        <button class="btn-select" @click="toggleDropDown">
          {{ selectedOption }}
          <img
            src="@/assets/icon/dropdownIcon.png"
            alt="드롭다운 아이콘"
            class="dropdown-icon"
            :class="{ rotated: isDropdownOpen }"
          >
        </button>
        <ul class="list-member" v-show="isDropdownOpen">
          <li v-for="option in options" :key="option">
            <button type="button" @click=" selectOption(option)">{{option}}</button>
          </li>
        </ul>
      </article>
        <div class="btn-box">
          <div class="input-container">
          <template v-if="selectedOption === '열심히 모은 목돈을 예치할 때'">  
            <!-- 예치금액 -->
            <div class="input-group">
              <input
              type="text"
              class="input wide"
              placeholder="예치금액"
              v-model="price"
              />
              <span>원을</span>
            </div>
            
            <!-- 기간 -->
            <div class="input-group">
              <input
              type="text"
              class="input narrow"
              placeholder="기간"
              v-model="month"
              />
              <span>개월 간</span>
            </div>
            
            <!-- 금리 -->
            <div class="input-group">
              <input
              type="text"
              class="input narrow"
              placeholder="금리"
              v-model="percent"
              />
              <span>%의 예금 상품에 저축하면?</span>
            </div>
          </template>
          <template v-if="selectedOption === '매월 일정금액을 저축할 때'">  
            <!-- 예치금액 -->
            <div class="input-group">
              <input
              type="text"
              class="input wide"
              placeholder="월저축액"
              v-model="price"
              />
              <span>원씩</span>
            </div>
            
            <!-- 기간 -->
            <div class="input-group">
              <input
              type="text"
              class="input narrow"
              placeholder="기간"
              v-model="month"
              />
              <span>개월 간</span>
            </div>
            
            <!-- 금리 -->
            <div class="input-group">
              <input
              type="text"
              class="input narrow"
              placeholder="금리"
              v-model="percent"
              />
              <span>%의 적금상품에 저축하면?</span>
            </div>
          </template>
          <template v-if="selectedOption === '목표금액을 모을 때'">  
            <!-- 예치금액 -->
            <div class="input-group">
              <input
              type="text"
              class="input wide"
              placeholder="예치금액"
              v-model="price"
              />
              <span>원을</span>
            </div>
            
            <!-- 기간 -->
            <div class="input-group">
              <input
              type="text"
              class="input narrow"
              placeholder="기간"
              v-model="month"
              />
              <span>개월 간</span>
            </div>
            
            <!-- 금리 -->
            <div class="input-group">
              <input
              type="text"
              class="input narrow"
              placeholder="금리"
              v-model="percent"
              />
              <span>%로 저축한다면?</span>
            </div>
          </template>
        </div>
        <button class="btn" @click="clickedResult">결과</button>
      </div>
      <div class="line"></div>
      <div v-if="totalPrice !== ''">
        <template v-if="selectedOption === '열심히 모은 목돈을 예치할 때'">
          <p class="result-text"><span class="bold-text">{{ price }}</span>원을 <span class="bold-text">{{ month }}</span>개월 간 <span class="bold-text">{{ percent }}</span>%의 예금상품에 저축하시면</p>
          <p class="result-text">이자 <span class="bold-text">{{ interest }}</span>원을 더해 총 <span class="bold-text bold-color">{{ totalPrice }}</span>원을 모으실 수 있습니다.</p>
        </template>
        <template v-if="selectedOption === '매월 일정금액을 저축할 때'">
          <p class="result-text"><span class="bold-text">{{ price }}</span>원을 <span class="bold-text">{{ month }}</span>개월 간 <span class="bold-text">{{ percent }}</span>%의 적금상품에 저축하시면</p>
          <p class="result-text">이자 <span class="bold-text">{{ interest }}</span>원을 더해 총 <span class="bold-text bold-color">{{ totalPrice }}</span>원을 모으실 수 있습니다.</p>
        </template>
        <template v-if="selectedOption === '목표금액을 모을 때'">
          <p class="result-text"><span class="bold-text">{{ price }}</span>원을 목표로 <span class="bold-text">{{ month }}</span>개월 간 <span class="bold-text">{{ percent }}</span>%로 저축하시면</p>
          <p class="result-text">이자 <span class="bold-text">{{ interest }}</span>원을 제하고 월 <span class="bold-text bold-color">{{ totalPrice }}</span>원씩 저축하시면 됩니다.</p>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
const isDropdownOpen = ref(false)
const selectedOption = ref("열심히 모은 목돈을 예치할 때")
const options = ref([
  "열심히 모은 목돈을 예치할 때",
  "매월 일정금액을 저축할 때",
  "목표금액을 모을 때",
])
const price = ref('');
const month = ref('');
const percent = ref('');
const interest = ref('')
const totalPrice = ref('')

// 숫자 포맷팅 함수
const formatNumber = (value) => {
  if (!value) return "";
  return new Intl.NumberFormat().format(value);
};

const toggleDropDown = () => {
  isDropdownOpen.value = !isDropdownOpen.value
  console.log(isDropdownOpen.value)
}

const selectOption = (option) => {
  selectedOption.value = option
  isDropdownOpen.value = false
}

const clickedResult = () => {
  if (!price.value || !month.value || !percent.value ) {
    alert("모든 값을 입력해주세요!")
    return
  }

  // 이자 계산
  const principal = parseFloat(price.value); // 예치금액
  const duration = parseInt(month.value, 10); // 기간
  const rate = parseFloat(percent.value) / 100; // 금리

  if (selectedOption.value === "열심히 모은 목돈을 예치할 때") { 
    const calculatedInterest = Math.round(principal * rate * (duration / 12)); // 이자 계산
    interest.value = formatNumber(calculatedInterest); // 쉼표 추가
    totalPrice.value = formatNumber(principal + calculatedInterest); // 쉼표 추가
    price.value = formatNumber(principal); // 쉼표 추가
  }else if (selectedOption.value === "매월 일정금액을 저축할 때"){
    // 매월 일정금액 적금 계산
    const totalPrincipalAmount = principal * duration; // 총 저축액
    const calculatedInterest =
      principal *
      ((duration * (duration + 1)) / 2) *
      (rate / 100) *
      (1 / 12); // 이자 계산 (단리)
    interest.value = formatNumber(Math.round(calculatedInterest)); // 쉼표 추가
    totalPrice.value = formatNumber(
      totalPrincipalAmount + Math.round(calculatedInterest)
    ); // 총합 계산
  }else {
    const goalAmount = principal
    const requiredMonthlySavings =
      goalAmount /
      (((duration * (duration + 1)) / 2) * (rate / 100) * (1 / 12) + duration); // 필요 월 저축액
    const totalSavingsWithoutInterest = requiredMonthlySavings * duration; // 총 저축액 (이자 제외)
    const calculatedInterest = goalAmount - totalSavingsWithoutInterest; // 이자 계산

    totalPrice.value = formatNumber(Math.ceil(requiredMonthlySavings)); // 월 저축액
    interest.value = formatNumber(Math.round(calculatedInterest)); // 이자
  }
}

</script>

<style scoped>
.box{
  background: #FFFFFF;
  border-radius: 20px;
  padding: 40px;
}

.title-box {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: flex-start;
  align-items: center;
  gap: 4px;
  padding-bottom: 16px;
}

.icon {
  width: 25px;
  height: 25px;
}

.title {
  font-weight: 600;
  font-size: 20px;
  line-height: 24px;
  color: #000000;
}

.cont-select {
  position: relative;
}

.btn-select {
  display: flex;
  width: 100%;
  padding: 6px 12px;
  font-size: 13px;
  line-height: 13px;
  font-weight: 600;
  border: 1px solid #C4C4C4;
  color: #424242;
  box-sizing: border-box;
  border-radius: 8px;
  cursor: pointer;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: space-between;
  align-items: center;
}

.btn-select:hover,
.btn-select:focus {
  border: 1px solid rgb(174, 172, 233);
  outline: 2px solid #e6e4ffaf;
}

/* 드롭다운 리스트 */
.list-member {
  list-style-type: none;
  position: absolute;
  width: 100%;
  top: 50px;
  left: 0;
  padding: 0;
  border: 1px solid #C4C4C4;
  border-radius: 10px;
  background-color: #fff;
  box-shadow: 4px 4px 14px rgba(0, 0, 0, 0.15);
  transition: opacity 0.3s ease, visibility 0.3s ease;
  max-height: 200px;
  overflow-y: auto;
  z-index: 1000;
}

/* v-show 상태 활성화 */
.list-member[v-show="true"] {
  opacity: 1;
  visibility: visible;
}

.list-member[v-show="false"] {
  opacity: 0;
  visibility: hidden;
}

.list-member li {
  padding: 8px;
}

.list-member li button {
  width: 100%;
  padding: 8px 4px;
  border: none;
  font-size: 13px;
  line-height: 13px;
  background-color: transparent;
  text-align: left;
  cursor: pointer;
  color: #676767;
}

.list-member li button:hover {
  background-color: #ffffff87;
  border-radius: 4px;
  color: #424242;
  font-weight: 600;
}

.dropdown-icon {
  width: 24px;
  height: 24px;
  transition: transform 0.3s ease; /* 부드러운 회전 애니메이션 */
}

/* 드롭다운 열림 상태에서 아이콘 회전 */
.dropdown-icon.rotated {
  transform: rotate(180deg);
}

.btn-box {
  display: flex;
  flex-direction: row;
  padding-top: 22px;
  align-items: flex-end;
  justify-content: space-between;
}
/* 버튼 스타일 */
.btn {
  display: flex;
  justify-content: center; /* 텍스트 가운데 정렬 */
  align-items: flex-end; /* 세로 정렬 */
  padding: 6px 16px; /* 내부 여백 */
  background: #636ACC; /* 배경색 */
  border-radius: 32px; /* 둥근 모서리 */
  color: white; /* 텍스트 색상 */
  font-size: 13px; /* 글씨 크기 */
  font-weight: 700; /* 글씨 굵기 */
  cursor: pointer; /* 클릭 가능한 커서 */
  width: auto; /* 버튼 너비를 텍스트에 맞춤 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 선택 사항: 버튼 그림자 */
  transition: transform 0.3s ease, background-color 0.3s ease; /* 선택 사항: 애니메이션 */
}

.btn:active {
  transform: scale(0.95); /* 살짝 줄어듦 */
  background-color: #5058cc; /* 색상 변화 */
}

.btn:hover {
  transform: scale(1.05); /* 호버 시 확대 효과 */
  background-color: #5058cc; /* 호버 시 배경색 변경 */
}
.input-container {
  width: 90%;
  flex-wrap: wrap;
  gap: 8px; /* 요소 간 간격 */
  font-size: 15px;
  font-weight: 600; /* semibold */
}

/* 입력 그룹 */
.input-group {
  display: inline-flex;
  align-items: center;
  padding-bottom: 8px;
  gap: 8px; /* Input과 텍스트 간 간격 */
  flex-wrap: nowrap; /* 화면 크기에 따라 줄바꿈 허용 */
}

/* 기본 Input 스타일 */
.input {
  padding: 8px;
  border: none;
  border-bottom: 2px solid #c4c4c4; /* 기본 밑줄 */
  outline: none;
  font-size: 15px;
  font-weight: 600;
  background-color: #ffffff00; /* 초기 배경색 없음 */
  width: 100% ; /* 기본적으로 100% */
  transition: border-color 0.3s ease, background-color 0.3s ease; /* 애니메이션 */
  text-align: end;
}

/* 너비 설정 */
.input.wide {
  flex: 0 0 70%; /* 고정 너비 20% */
}

.input.narrow {
  flex: 0 0 30%; /* 고정 너비 10% */
}

/* 포커스 시 애니메이션 */
.input:focus {
  border-bottom-color: #636ACC; /* 진한 밑줄 색상 */
}

.input:focus::placeholder {
  color: transparent; /* 포커스 시 Placeholder 숨김 */
}

/* 배경 애니메이션 */
.input:focus{
  transition: width 0.3s ease; /* 부드러운 확장 */
}

/* 텍스트 스타일 */
.input-group span {
  font-size: 15px;
  font-weight: 600; /* semibold */
  white-space: nowrap; /* 텍스트가 한 줄로 유지되도록 설정 */
}

/* 반응형 설정 */
@media screen and (max-width: 600px) {
  .input-group:last-child {
    flex-basis: 100%; /* 마지막 줄은 줄바꿈 */
  }
}

.line {
  height: 1px;
  background: rgba(0, 0, 0, 0.1);
  margin: 25px 0px;
}

.bold-text {
  font-weight: 500;
  font-size: 17px;
}

.result-text {
  font-weight: 350;
  font-size: 16px;
  line-height: 32px;
  letter-spacing: 1px;
}

.bold-color {
  color: #4049c7;
}
</style>

