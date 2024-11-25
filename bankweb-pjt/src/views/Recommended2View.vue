<!-- Recommended2View.vue -->
<template>
  <div class="simulation-container">
    <!-- 헤더 섹션 -->
    <div class="mb-8">
      <h1 class="text-h4 text-center font-weight-bold mb-2">자산 성장 시뮬레이션 기반 추천</h1>
      <p class="text-subtitle-1 text-center text-medium-emphasis">
        고객님의 정보를 입력하시면 최적의 금융상품을 추천해드립니다.
      </p>
    </div>

    <!-- 입력 폼 섹션 -->
    <section class="form-section">
      <form @submit.prevent="runSimulation">
        <div class="form-grid">
          <div class="input-group">
            <label>나이</label>
            <input
              v-model.number="userProfile.age"
              type="number"
              placeholder="만 나이 입력"
              required
              min="0"
            />
          </div>

          <div class="input-group">
            <label>현재 자산</label>
            <input
              v-model.number="userProfile.currentAssets"
              type="number"
              placeholder="현재 보유 자산"
              required
              min="0"
            />
            <span class="hint">{{ formatCurrency(userProfile.currentAssets) }}원</span>
          </div>

          <div class="input-group">
            <label>월 저축 가능액</label>
            <input
              v-model.number="userProfile.monthlySavings"
              type="number"
              placeholder="월 저축 가능 금액"
              required
              min="0"
            />
            <span class="hint">{{ formatCurrency(userProfile.monthlySavings) }}원</span>
          </div>

          <div class="input-group">
            <label>투자 기간</label>
            <select v-model="userProfile.period">
              <option v-for="option in periodOptions" 
                      :key="option.value" 
                      :value="option.value">
                {{ option.label }}
              </option>
            </select>
          </div>

          <div class="input-group">
            <label>이자 선호도</label>
            <div class="radio-group">
              <label class="radio-label">
                <input type="radio" v-model="userProfile.isCompound" :value="true">
                <span>복리</span>
              </label>
              <label class="radio-label">
                <input type="radio" v-model="userProfile.isCompound" :value="false">
                <span>단리</span>
              </label>
            </div>
          </div>
        </div>

        <div class="submit-section">
          <button type="submit" class="submit-button" :disabled="loading">
            <span class="button-content">
              <span v-if="loading" class="loading-spinner"></span>
              {{ loading ? '계산중...' : '맞춤 상품 찾기' }}
            </span>
          </button>
        </div>
      </form>
    </section>

    <!-- 결과 섹션 -->
    <section v-if="simulationResults" class="results-section">
      <!-- 성장 그래프 -->
      <div class="chart-container">
        <h2 class="section-title">예상 자산 성장 그래프</h2>
        <div class="chart-wrapper">
          <canvas ref="chartRef"></canvas>
        </div>
        <div class="chart-summary">
          <div class="summary-item">
            <span class="label">예상 최종 자산</span>
            <span class="value">{{ formatCurrency(getFinalAmount()) }}원</span>
          </div>
          <div class="summary-item">
            <span class="label">총 납입금</span>
            <span class="value">{{ formatCurrency(getTotalDeposit()) }}원</span>
          </div>
          <div class="summary-item">
            <span class="label">예상 총 수익</span>
            <span class="value profit">{{ formatCurrency(getTotalProfit()) }}원</span>
          </div>
        </div>
      </div>

      <!-- 추천 상품 목록 -->
      <div class="recommendations-container">
        <h2 class="section-title">
          추천 금융 상품
          <span class="preference-tag">
            {{ userProfile.isCompound ? '복리' : '단리' }} 선호
          </span>
        </h2>

        <div class="products-grid">
          <div v-for="(product, index) in simulationResults.recommendations" 
               :key="index" 
               class="product-card"
               :class="{ 'top-product': index === 0 }">
            <div class="product-header">
              <div class="rank-badge" :class="{ 'top-rank': index === 0 }">
                {{ index + 1 }}
              </div>
              <div class="product-info">
                <h3 class="product-name">{{ product.fin_prdt_nm }}</h3>
                <p class="company-name">{{ product.kor_co_nm }}</p>
              </div>
            </div>

            <div class="product-details">
              <div class="detail-row">
                <div class="detail-item">
                  <span class="label">기본 금리</span>
                  <span class="value">{{ product.intr_rate }}%</span>
                </div>
                <div class="detail-item">
                  <span class="label">우대 금리</span>
                  <span class="value highlight">최대 {{ product.intr_rate2 }}%</span>
                </div>
              </div>
              
              <div class="detail-item full-width">
                <span class="label">예상 만기 금액</span>
                <span class="value">{{ formatCurrency(product.finalAmount) }}원</span>
              </div>
              
              <div class="detail-item full-width">
                <span class="label">총 이자 수익</span>
                <span class="value profit">
                  +{{ formatCurrency(product.totalInterest) }}원
                </span>
              </div>
            </div>

            <div class="product-conditions" v-if="product.spcl_cnd">
              <h4 class="conditions-title">우대조건</h4>
              <p class="conditions-content">{{ product.spcl_cnd }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 상품 상세 모달 -->
    <div v-if="selectedProduct" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ selectedProduct.fin_prdt_nm }}</h3>
          <button class="close-button" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="detail-section">
            <h4>상품 정보</h4>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="label">은행명</span>
                <span class="value">{{ selectedProduct.kor_co_nm }}</span>
              </div>
              <div class="detail-item">
                <span class="label">가입 방법</span>
                <span class="value">{{ selectedProduct.join_way }}</span>
              </div>
              <div class="detail-item">
                <span class="label">가입 대상</span>
                <span class="value">{{ selectedProduct.join_member }}</span>
              </div>
            </div>
          </div>
          
          <div class="detail-section">
            <h4>금리 정보</h4>
            <div class="detail-grid">
              <div class="detail-item">
                <span class="label">기본 금리</span>
                <span class="value">{{ selectedProduct.intr_rate }}%</span>
              </div>
              <div class="detail-item">
                <span class="label">우대 금리</span>
                <span class="value highlight">최대 {{ selectedProduct.intr_rate2 }}%</span>
              </div>
            </div>
          </div>

          <div class="detail-section">
            <h4>우대 조건</h4>
            <p class="conditions">{{ selectedProduct.spcl_cnd || '우대조건 없음' }}</p>
          </div>

          <div class="detail-section">
            <h4>만기 후 이율</h4>
            <p class="conditions">{{ selectedProduct.mtrt_int }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import Chart from 'chart.js/auto';
import { useFinancialStore } from '@/stores/financial';
import { useAccountStore } from '@/stores/account';

// 상태 관리
const financialStore = useFinancialStore();
const loading = ref(false);
const chartRef = ref(null);
const chart = ref(null);
const selectedProduct = ref(null);

const accountStore = useAccountStore()

// 예금/적금 데이터
const deposits = ref([
  /* 여기에 예금 상품 데이터 배열이 들어갑니다 */
]);
const savings = ref([
  /* 여기에 적금 상품 데이터 배열이 들어갑니다 */
]);

// 사용자 프로필 상태
const userProfile = ref({
  age: accountStore.userinfo?.age || null,
  currentAssets: accountStore.userinfo?.money || null,
  monthlySavings: null,
  period: 12,
  isCompound: true
});

// 시뮬레이션 결과
const simulationResults = ref(null);

// 기간 선택 옵션
const periodOptions = [
  { value: 6, label: '6개월' },
  { value: 12, label: '1년' },
  { value: 24, label: '2년' },
  { value: 36, label: '3년' }
];

// 통화 포맷팅 함수
const formatCurrency = (value) => {
  if (!value) return '0';
  return new Intl.NumberFormat('ko-KR').format(Math.round(value));
};

// 복리 이자 계산
const calculateCompoundInterest = (principal, monthlyDeposit, rate, months) => {
  let total = principal;
  for (let i = 0; i < months; i++) {
    total = (total + monthlyDeposit) * (1 + (rate / 100 / 12));
  }
  return total;
};

// 단리 이자 계산
const calculateSimpleInterest = (principal, monthlyDeposit, rate, months) => {
  const totalDeposit = principal + (monthlyDeposit * months);
  const interest = (principal * rate/100 * months/12) + 
                  (monthlyDeposit * rate/100 * (months + 1)/24);
  return totalDeposit + interest;
};

// 성장 데이터 생성
const generateGrowthData = (initialAmount, monthlyDeposit, rate, months, isCompound) => {
  const data = {
    labels: [],
    totalAmount: [],
    principal: [],
    interest: []
  };

  let currentAmount = initialAmount;
  let currentPrincipal = initialAmount;

  for (let month = 0; month <= months; month++) {
    data.labels.push(`${month}개월`);
    
    if (isCompound) {
      currentAmount = calculateCompoundInterest(initialAmount, monthlyDeposit, rate, month);
    } else {
      currentAmount = calculateSimpleInterest(initialAmount, monthlyDeposit, rate, month);
    }
    
    currentPrincipal = initialAmount + (monthlyDeposit * month);
    
    data.totalAmount.push(currentAmount);
    data.principal.push(currentPrincipal);
    data.interest.push(currentAmount - currentPrincipal);
  }

  return data;
};

// 차트 생성
const createChart = (data) => {
  if (!chartRef.value) {
    console.warn('Canvas element not found');
    return;
  }

  if (chart.value) {
    chart.value.destroy();
  }

  try {
    const ctx = chartRef.value.getContext('2d');
    chart.value = new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.labels,
        datasets: [
          {
            label: '총 자산',
            data: data.totalAmount,
            borderColor: '#4CAF50',
            backgroundColor: 'rgba(76, 175, 80, 0.1)',
            tension: 0.4,
            fill: true
          },
          {
            label: '납입원금',
            data: data.principal,
            borderColor: '#2196F3',
            backgroundColor: 'rgba(33, 150, 243, 0.1)',
            tension: 0.4,
            fill: true
          },
          {
            label: '이자수익',
            data: data.interest,
            borderColor: '#FFC107',
            backgroundColor: 'rgba(255, 193, 7, 0.1)',
            tension: 0.4,
            fill: true
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          intersect: false,
          mode: 'index'
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: (context) => {
                return `${context.dataset.label}: ${formatCurrency(context.raw)}원`;
              }
            }
          },
          legend: {
            position: 'top'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: (value) => `${formatCurrency(value)}원`
            }
          }
        }
      }
    });
  } catch (error) {
    console.error('Chart creation error:', error);
  }
};

// 나이 제한 확인
const checkAgeLimit = (product) => {
  if (product.join_deny === 3) {
    const ageMatch = product.join_member.match(/만\s*(\d+).*?(\d+)세/);
    if (ageMatch) {
      const [, minAge, maxAge] = ageMatch;
      return userProfile.value.age >= parseInt(minAge) && 
             userProfile.value.age <= parseInt(maxAge);
    }
  }
  return true;
};

// 최적의 금리 옵션 찾기
const findBestOption = (product, targetPeriod, isDeposit = false) => {
  const options = isDeposit ? product.depositoption_set : product.savingoption_set;
  
  if (!options || !Array.isArray(options)) {
    return null;
  }

  const exactMatch = options.find(opt => parseInt(opt.save_trm) === targetPeriod);
  if (exactMatch) return exactMatch;

  return options.reduce((prev, curr) => {
    const prevDiff = Math.abs(parseInt(prev.save_trm) - targetPeriod);
    const currDiff = Math.abs(parseInt(curr.save_trm) - targetPeriod);
    return currDiff < prevDiff ? curr : prev;
  });
};

// 시뮬레이션 실행 함수 수정
const runSimulation = async () => {
  try {
    loading.value = true;

    // store에서 최신 데이터 확인
    if (financialStore.deposits.length === 0 || financialStore.savings.length === 0) {
      await Promise.all([
        financialStore.getDepositDatas(),
        financialStore.getSavingDatas()
      ]);
    }

    // 적금과 예금 상품 결합하여 처리
    const allProducts = [
      ...financialStore.deposits.map(p => ({ ...p, type: 'deposit' })),
      ...financialStore.savings.map(p => ({ ...p, type: 'saving' }))
    ];

    // 나이 제한 필터링 및 상품별 수익 계산
    const processedProducts = allProducts
      .filter(checkAgeLimit)
      .map(product => {
        const option = findBestOption(
          product, 
          userProfile.value.period, 
          product.type === 'deposit'
        );
        if (!option) return null;

        const monthlyAmount = userProfile.value.monthlySavings;
        const initialAmount = userProfile.value.currentAssets;
        
        // 성장 데이터 계산
        const growthData = generateGrowthData(
          initialAmount,
          monthlyAmount,
          option.intr_rate2,
          userProfile.value.period,
          userProfile.value.isCompound
        );

        const finalAmount = growthData.totalAmount[growthData.totalAmount.length - 1];
        const totalInterest = growthData.interest[growthData.interest.length - 1];

        return {
          ...product,
          intr_rate: option.intr_rate,
          intr_rate2: option.intr_rate2,
          growthData,
          finalAmount,
          totalInterest
        };
      })
      .filter(Boolean);

    // 상품 정렬 및 추천
    const sortedProducts = userProfile.value.isCompound
      ? processedProducts.sort((a, b) => b.intr_rate2 - a.intr_rate2)
      : processedProducts.sort((a, b) => {
          const scoreA = a.intr_rate2 * (parseInt(a.save_trm) / 12);
          const scoreB = b.intr_rate2 * (parseInt(b.save_trm) / 12);
          return scoreB - scoreA;
        });

    // 상위 5개 상품 선택
    const recommendations = sortedProducts.slice(0, 5);

    if (recommendations.length === 0) {
      throw new Error('추천 가능한 상품이 없습니다.');
    }

    // 최적의 상품의 성장 데이터로 차트 생성
    nextTick(() => {
      createChart(recommendations[0].growthData);
    });

    // 결과 저장
    simulationResults.value = {
      recommendations,
      bestProduct: recommendations[0]
    };

  } catch (error) {
    console.error('시뮬레이션 오류:', error);
    // TODO: 사용자에게 에러 메시지 표시
  } finally {
    loading.value = false;
  }
};

// 결과 계산 함수들
const getFinalAmount = () => {
  if (!simulationResults.value?.bestProduct) return 0;
  return simulationResults.value.bestProduct.finalAmount;
};

const getTotalDeposit = () => {
  const months = userProfile.value.period;
  return userProfile.value.currentAssets + 
         (userProfile.value.monthlySavings * months);
};

const getTotalProfit = () => {
  if (!simulationResults.value?.bestProduct) return 0;
  return simulationResults.value.bestProduct.totalInterest;
};

// // 모달 관련 함수들
// const showProductDetails = (product) => {
//   selectedProduct.value = product;
// };

const closeModal = () => {
  selectedProduct.value = null;
};

// script setup 부분 수정
// deposits와 savings ref 제거 후 다음과 같이 수정

onMounted(async () => {
  try {
    loading.value = true;
    
    // 예금과 적금 데이터 로드
    await financialStore.getDepositDatas();
    await financialStore.getSavingDatas();
    
    nextTick(() => {
      if (chartRef.value) {
        createChart({
          labels: [],
          totalAmount: [],
          principal: [],
          interest: []
        });
      }
    });
  } catch (error) {
    console.error('데이터 로드 중 오류 발생:', error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
/* 메인 컨테이너 */
.simulation-container {
  background-color: #f8f9fa;
  padding: 40px;
  transition: all 0.5s ease-in-out;
}

.text-h4 {
  font-size: 24px;
  font-weight: 700;
  margin: 6px 0px;
}

.text-subtitle-1 {
  font-size: 18px;
  font-weight: 400;
  margin: 6px 0px;
}

/* 폼 섹션 */
.form-section {
  background-color: white;
  border-radius: 10px;
  padding: 20px 40px;
  max-width: 1000px;
  transition: transform 0.3s ease;
}

.form-section:hover {
  transform: translateY(-4px);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

/* 입력 그룹 스타일링 */
.input-group {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
}

.input-group.full-width {
  grid-column: 1 / -1;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #636363;
  margin: 18px 0px 6px;
}

/* 입력 필드 스타일링 */
.input-group label {
  font-size: 14px;
  font-weight: 600;
  color: #2c2c2c;
  width: 100px;
}

.input-group input,
.input-group select {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.2s ease;
}

.input-group input:focus,
.input-group select:focus {
  outline: none;
  border-color: #5A87F2;
  box-shadow: 0 0 0 3px rgba(99, 106, 204, 0.15);
}

.hint {
  font-size: 14px;
  color: #718096;
  margin-left: 8px;
}

/* 라디오 버튼 그룹 */
.radio-group {
  display: flex;
  gap: 24px;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

/* 제출 버튼 영역 */
.submit-section {
  margin-top: 36px;
  text-align: center;
}

.submit-button {
  background: #5A87F2;
  color: white;
  border: none;
  padding: 12px 18px;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  min-width: 220px;
  justify-content: center;
}

.submit-button:hover {
  background: #4A77E2;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 106, 204, 0.2);
}

.submit-button:disabled {
  background: #e2e8f0;
  cursor: not-allowed;
  transform: none;
}

/* 결과 섹션 */
.results-section {
  max-width: 1200px;
  margin: 3rem auto;
}

/* 차트 컨테이너 */
.chart-container {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 24px rgba(149, 157, 165, 0.1);
  margin-bottom: 32px;
}

.chart-wrapper {
  height: 400px;
  margin: 24px 0;
}

.chart-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  padding: 24px;
  background: #f8f9fa;
  border-radius: 12px;
}

.summary-item {
  text-align: center;
}

.summary-item .label {
  font-size: 14px;
  color: #718096;
  display: block;
  margin-bottom: 8px;
}

.summary-item .value {
  font-size: 20px;
  font-weight: 600;
  color: #2d3748;
}

.summary-item .value.profit {
  color: #2F855A;
}

/* 추천 상품 컨테이너 */
.recommendations-container {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(149, 157, 165, 0.1);
}

.products-grid {
  display: grid;
  gap: 24px;
  padding: 24px;
}

/* 상품 카드 */
.product-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  border: 1px solid #f4f4f4;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.top-product {
  border: 2px solid #5A87F2;
}

.product-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.rank-badge {
  background: #5A87F2;
  color: white;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

.top-rank {
  background: linear-gradient(135deg, #5A87F2, #2e5cc8);
}

.product-info h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.company-name {
  font-size: 14px;
  color: #666;
  margin: 4px 0 0;
}

/* 상품 상세 정보 */
.detail-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

.detail-item {
  padding: 12px;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.detail-item:hover {
  background: #f1f3f5;
}

.detail-item .label {
  font-size: 14px;
  color: #718096;
}

.detail-item .value {
  font-size: 16px;
  font-weight: 600;
  color: #2d3748;
}

.detail-item .value.highlight {
  color: #1f4ebc;
}

.detail-item .value.profit {
  color: #2F855A;
}

/* 조건 섹션 */
.product-conditions {
  margin-top: 16px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 12px;
}

.conditions-title {
  font-size: 14px;
  font-weight: 600;
  color: #4a5568;
  margin-bottom: 8px;
}

.conditions-content {
  font-size: 14px;
  color: #718096;
  line-height: 1.5;
}

/* 로딩 스피너 */
.loading-spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
  margin-right: 8px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .simulation-container {
    padding: 20px;
  }

  .form-section {
    padding: 20px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .input-group {
    flex-direction: column;
    align-items: stretch;
  }

  .input-group label {
    width: auto;
    margin-bottom: 8px;
  }

  .chart-summary {
    grid-template-columns: 1fr;
  }

  .products-grid {
    grid-template-columns: 1fr;
  }

  .detail-row {
    grid-template-columns: 1fr;
  }
}
</style>