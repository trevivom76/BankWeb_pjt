<template>
  <div class="container">
    <h2 class="title">예적금 금리 비교</h2>

    <!-- 상품 리스트 -->
    <div>
      <h3 class="subtitle">상품 리스트</h3>
      <div class="static-product-list">
        <div class="product-item" v-for="product in displayProducts" :key="product.id">
          <label class="checkbox-label">
            <input
              type="checkbox"
              class="checkbox-input"
              :value="product"
              @change="toggleProductSelection(product)"
              :disabled="!selectedProducts.find((p) => p.id === product.id) && selectedProducts.length >= 4"
            />
            <span class="custom-checkbox"></span>
            {{ product.fin_prdt_nm }} - {{ product.kor_co_nm }}
          </label>
        </div>
      </div>
    </div>

    <!-- 개월 수 선택 -->
    <div v-if="selectedProducts.length > 0" class="term-select-container">
      <label for="term-select" class="term-label">개월 수 선택:</label>
      <select id="term-select" v-model="selectedTerm" class="term-select">
        <option v-for="term in availableTerms" :key="term" :value="term">{{ term }}개월</option>
      </select>
    </div>
    
    <!-- 경고 메시지 -->
    <div v-if="selectedProducts.length >= 4" class="error">최대 4개의 상품만 비교할 수 있습니다.</div>
    
    <div class="line"></div>

    <!-- 그래프 -->
    <div>
      <h3 class="subtitle">그래프</h3>
      <canvas id="rateComparisonChart"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import Chart from "chart.js/auto";

const props = defineProps({
  products: Array,
});

const displayProducts = ref([]);
const selectedProducts = ref([]); // 선택된 상품 리스트
const selectedTerm = ref("12"); // 기본 개월 수
const availableTerms = ref(["6", "12", "24", "36"]); // 선택 가능한 개월 수
let chart = null; // 그래프 객체

// props의 변경을 감지하고 내부 상태를 업데이트
watch(
  () => props.products,
  (newProducts) => {
    displayProducts.value = [...newProducts];
  },
  { immediate: true }
);

// 상품 선택/해제 핸들러
const toggleProductSelection = (product) => {
  const exists = selectedProducts.value.find((p) => p.id === product.id);

  if (exists) {
    // 이미 선택된 상품 제거
    selectedProducts.value = selectedProducts.value.filter((p) => p.id !== product.id);
  } else if (!exists && selectedProducts.value.length < 4) {
    // 새 상품 추가 및 이율 데이터 저장
    const rates = (product.savingoption_set || product.depositoption_set || []).reduce((acc, option) => {
      acc[option.save_trm] = {
        intr_rate: option.intr_rate,
        intr_rate2: option.intr_rate2,
      };
      return acc;
    }, {});

    const enrichedProduct = {
      id: product.id,
      name: product.fin_prdt_nm,
      bank: product.kor_co_nm,
      rates: rates,
    };
    selectedProducts.value.push(enrichedProduct);
  } else {
    console.warn("최대 4개의 상품만 선택 가능합니다.");
  }

  updateChart(); // 그래프 업데이트
};

// 그래프 업데이트
const updateChart = () => {
  if (chart) {
    chart.destroy(); // 기존 그래프 제거
  }

  const labels = selectedProducts.value.map((product) => product.name);
  const basicRates = selectedProducts.value.map((product) => product.rates[selectedTerm.value]?.intr_rate || 0);
  const preferentialRates = selectedProducts.value.map((product) => product.rates[selectedTerm.value]?.intr_rate2 || 0);

  const ctx = document.getElementById("rateComparisonChart").getContext("2d");
  chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "기본 금리",
          data: basicRates,
          backgroundColor: "rgba(54, 162, 235, 0.5)",
        },
        {
          label: "최고 우대 금리",
          data: preferentialRates,
          backgroundColor: "rgba(255, 99, 132, 0.5)",
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "top",
        },
      },
    },
  });
};

// 개월 수 변경 시 그래프 업데이트
watch(selectedTerm, () => {
  updateChart();
});
</script>

<style scoped>
/* 전체 컨테이너 수정 */
.container {
  height: fit-content; /* 내용물에 맞게 너비 조정 */
  margin: 0 auto;
  padding: 20px;
  color: #333;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* 제목 스타일 */
.title {
  text-align: center;
  font-size: 22px;
  font-weight: 700;
  margin-bottom: 20px;
  color: #424242;
}

/* 부제목 스타일 */
.subtitle {
  font-size: 18px;
  font-weight: bold;
  margin: 16px 0px 12px;
  color: #424242;
}

/* 정적 상품 리스트 스타일 */
.static-product-list {
  max-height: 300px;
  overflow-y: auto;
  background-color: #fff;
  border-radius: 4px;
}

/* 스크롤바 스타일링 */
.static-product-list::-webkit-scrollbar {
  width: 4px;
}

.static-product-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.static-product-list::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.static-product-list::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* 상품 아이템 스타일 */
.product-item {
  padding: 12px;
  border-bottom: 1px solid #eee;
  transition: background-color 0.2s ease;
}

.product-item:last-child {
  border-bottom: none;
}

.product-item:hover {
  background-color: #f5f5f5;
}

.line {
  height: 1px;
  color: #333;
}

/* 체크박스 스타일 */
.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.checkbox-input {
  display: none;
}

.custom-checkbox {
  width: 16px;
  height: 16px;
  border: 2px solid #c0c0c0;
  border-radius: 4px;
  margin-right: 10px;
  position: relative;
  transition: all 0.2s ease;
  background-color: white;
}

/* 체크 아이콘 스타일 */
.custom-checkbox::after {
  content: '';
  position: absolute;
  left: 4px;
  top: 1px;
  width: 5px;
  height: 8px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg) scale(0);
  opacity: 0;
  transition: all 0.2s cubic-bezier(0.12, 0.4, 0.29, 1.46);
}

/* 체크됐을 때 스타일 */
.checkbox-input:checked + .custom-checkbox {
  background-color: #636ACC;
  border-color: #636ACC;
}

.checkbox-input:checked + .custom-checkbox::after {
  transform: rotate(45deg) scale(1);
  opacity: 1;
}

/* 호버 효과 */
.checkbox-label:hover .custom-checkbox {
  border-color: #636ACC;
}

/* 포커스 효과 */
.checkbox-input:focus + .custom-checkbox {
  box-shadow: 0 0 0 2px rgba(99, 106, 204, 0.2);
}

/* 경고 메시지 스타일 */
.error {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #ef4444;
  font-size: 14px;
  font-weight: 500;
  margin-top: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  background-color: #fef2f2;
  border: 1px solid #fee2e2;
  position: relative;
  animation: errorAppear 0.3s ease-out;
}

/* 경고 아이콘 추가 */
.error::before {
  content: '!';
  display: flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  background-color: #ef4444;
  color: white;
  border-radius: 50%;
  font-size: 12px;
  font-weight: bold;
}

/* 호버 효과 */
.error:hover {
  background-color: #fee2e2cb;
  transform: translateY(-1px);
  transition: all 0.2s ease;
}

/* 등장 애니메이션 */
@keyframes errorAppear {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 쉐이크 애니메이션 - 필요시 추가 */
.error.shake {
  animation: errorShake 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
}

@keyframes errorShake {
  0%, 100% {
    transform: translateX(0);
  }
  20%, 60% {
    transform: translateX(-4px);
  }
  40%, 80% {
    transform: translateX(4px);
  }
}
/* 개월 수 선택 컨테이너 */
.term-select-container {
  margin: 24px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

/* 라벨 스타일 */
.term-label {
  font-size: 15px;
  font-weight: 700;
  color: #333;
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 라벨 아이콘 (옵션) */
.term-label::before {
  content: '📅';
  font-size: 16px;
}

/* 셀렉트 박스 컨테이너 */
.term-select-wrapper {
  position: relative;
  width: 120px; /* 너비 증가 */
}

/* 커스텀 화살표 */
.term-select-wrapper::after {
  content: '';
  position: absolute;
  right: 12px;
  top: 50%;
  width: 8px;
  height: 8px;
  border-right: 2px solid #636ACC;
  border-bottom: 2px solid #636ACC;
  transform: translateY(-70%) rotate(45deg);
  pointer-events: none;
  transition: transform 0.3s ease;
}

/* 셀렉트 박스 스타일 */
.term-select {
  width: 100%;
  padding: 8px 30px 8px 12px; /* 패딩 조정 */
  font-size: 14px;
  font-weight: 500;
  color: #2c3e50;
  background-color: #fff;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  cursor: pointer;
  appearance: none;
  transition: all 0.3s ease;
}

/* 셀렉트 박스 호버 효과 */
.term-select:hover {
  border-color: #636ACC;
  background-color: #f8f9fa;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 106, 204, 0.1);
}

/* 셀렉트 박스 포커스 효과 */
.term-select:focus {
  border-color: #636ACC;
  box-shadow: 0 0 0 3px rgba(99, 106, 204, 0.2);
  outline: none;
  background-color: #fff;
}

/* 셀렉트 박스 활성화 시 화살표 회전 */
.term-select:focus + .term-select-wrapper::after {
  transform: translateY(-30%) rotate(-135deg);
}

/* 옵션 스타일링 */
.term-select option {
  padding: 8px;
  font-size: 14px;
  color: #2c3e50;
  background-color: #fff;
}

/* 선택된 옵션 스타일 */
.term-select option:checked {
  background-color: #636ACC;
  color: white;
}

/* 비활성화된 옵션 스타일 */
.term-select option:disabled {
  color: #adb5bd;
  background-color: #f8f9fa;
}

/* 셀렉트 박스 그룹 스타일 */
.term-select optgroup {
  font-weight: 600;
  color: #495057;
  padding: 8px 0;
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .term-select-container {
    flex-direction: row; /* 가로 배열 유지 */
    align-items: center;
    justify-content: flex-start; /* 왼쪽 정렬 */
    gap: 12px;
  }

  .term-select-wrapper {
    width: 100px; /* 모바일에서의 너비 */
  }

  .term-select {
    padding: 8px 25px 8px 10px; /* 모바일에서의 패딩 */
    font-size: 13px;
  }

  .term-label {
    font-size: 14px;
    margin-bottom: 0; /* 마진 제거 */
  }
}
/* 그래프 컨테이너 스타일 */
.graph-container {
  width: 100%;
  margin-top: 20px;
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
