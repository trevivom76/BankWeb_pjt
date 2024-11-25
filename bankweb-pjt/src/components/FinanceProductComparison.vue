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
/* 전체 컨테이너 */
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: "Arial", sans-serif;
  color: #333;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* 제목 스타일 */
.title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #0b5bcb;
}

/* 부제목 스타일 */
.subtitle {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #0b5bcb;
}

/* 정적 상품 리스트 스타일 */
.static-product-list {
  max-height: 300px;
  overflow-y: auto;
  padding-right: 10px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 스크롤바 스타일링 */
.static-product-list::-webkit-scrollbar {
  width: 8px;
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
  width: 20px;
  height: 20px;
  border: 2px solid #0b5bcb;
  border-radius: 4px;
  margin-right: 10px;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.checkbox-input:checked + .custom-checkbox {
  background-color: #0b5bcb;
  transform: scale(1.1);
}

/* 경고 메시지 스타일 */
.error {
  color: #d32f2f;
  font-size: 14px;
  font-weight: bold;
  margin-top: 10px;
  text-align: center;
}

/* 개월 수 선택 */
.term-select-container {
  margin: 20px 0;
  text-align: center;
}

.term-label {
  font-size: 16px;
  font-weight: bold;
  margin-right: 10px;
}

.term-select {
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background-color: #fff;
  cursor: pointer;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.term-select:hover {
  border-color: #0b5bcb;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.term-select:focus {
  border-color: #0b5bcb;
  box-shadow: 0 0 0 2px rgba(11, 91, 203, 0.3);
  outline: none;
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .container {
    padding: 10px;
  }

  .title {
    font-size: 20px;
  }

  .subtitle {
    font-size: 16px;
  }

  .term-select-container {
    flex-direction: column;
  }

  .term-label {
    margin-bottom: 10px;
  }
}
</style>
