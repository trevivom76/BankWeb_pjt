<template>
  <!-- 자산 성장 시뮬레이션 기반 추천 페이지-->
  <div>
    <h1>자산 성장 시뮬레이션 기반 추천</h1>

    <!-- 맞춤 상품을 위한 필수 입력 정보 -->
    <div>
      <p>
        목표 자산 금액 :
        <input type="text" />
      </p>

      <p>
        목표 달성 기간 :
        <select name="period" id="per">
          <option value="target" disabled hidden selected>목표 기간 선택</option>
          <option value="month6">6개월</option>
          <option value="month12">12개월</option>
          <option value="month24">24개월</option>
          <option value="month36">36개월</option>
        </select>
      </p>

      <p>
        월 저축 가능 금액 :
        <input type="text" />
      </p>

      <p>
        이자 선호도 :
        <input type="text" />
      </p>

      <button>검색</button>
    </div>

    <div></div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const targetasset = ref("");
const targetperiod = ref("12개월");
const cansavemoneypermonth = ref("")
// const 
</script>

<style scoped>
input[type="text"] {
  border: 1px solid #e0e0e0; /* 연한 회색 */
  border-radius: 4px;

  outline: none; /* focus 시 기본 테두리 제거 */
}

input[type="text"]:focus {
  border-color: #0b5bcb; /* focus 시 테두리 색상 변경 */
  box-shadow: 0 0 0 1px #0b5bcb; /* focus 시 그림자 효과 */
}

select {
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 10px 35px 10px 12px;
  font-size: 16px;
  color: #333;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  outline: none;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23666' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
}

select:hover {
  border-color: #0b5bcb80;
  background-color: #f8f9fa;
}

select:focus {
  border-color: #0b5bcb;
  box-shadow: 0 0 0 4px rgba(11, 91, 203, 0.1);
}

/* disabled 옵션 스타일 */
select option[disabled] {
  color: #999;
}

/* 전체 p 태그 스타일링 (선택사항) */
p {
  display: flex;
  align-items: center;
  gap: 10px; /* 텍스트와 select 사이 간격 */
  margin: 10px 0;
  font-size: 16px;
}

button {
  border: 2px solid #0b5bcb; /* 테두리 스타일 */
  border-radius: 4px; /* 모서리 둥글게 */
  padding: 8px 16px; /* 내부 여백 */
  background: none; /* 배경색 없애기 */
  color: #0b5bcb; /* 글자색 */
  cursor: pointer; /* 마우스 포인터 */
}
</style>
