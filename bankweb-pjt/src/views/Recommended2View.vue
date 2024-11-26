<template>
  <div class="financial-advisor">
    <!-- 헤더 섹션 -->
    <div class="mb-8">
      <p class="title">자산 성장 시뮬레이션 기반 추천</p>
      <p class="text-subtitle-1">
        고객님의 정보를 입력하시면 최적의 적금 상품을 추천해드립니다.
      </p>
    </div>

    <!-- 입력 폼 섹션 -->
    <section class="form-section">
      <form @submit.prevent="runSimulation">
        <div class="form-grid">
          <div class="input-group full-width">
            <h2 class="section-title-1">기본 정보 입력</h2>
            <div class="divider"></div>
          </div>
          <div class="input-group">
            <label>나이</label>
            <input v-model.number="userProfile.age" type="number" placeholder="만 나이 입력" required min="0" />
          </div>

          <div class="input-group">
            <label>현재 자산</label>
            <input v-model.number="userProfile.currentAssets" type="number"
              :placeholder="formatCurrency(userProfile.monthlySavings) | 0" required min="0" />
          </div>

          <div class="input-group">
            <label>월 저축액</label>
            <input v-model.number="userProfile.monthlySavings" type="number"
              :placeholder="formatCurrency(userProfile.monthlySavings) | 0" required min="0" />
          </div>

          <div class="input-group">
            <label>저축 기간</label>
            <select v-model="userProfile.period">
              <option v-for="option in periodOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
          </div>

          <div class="input-group">
            <label>이자 선호도</label>
            <div class="radio-group">
              <label class="radio-label">
                <input type="radio" v-model="userProfile.isCompound" :value="true">
                <p>복리</p>
              </label>
              <label class="radio-label">
                <input type="radio" v-model="userProfile.isCompound" :value="false">
                <p>단리</p>
              </label>
            </div>
          </div>
        </div>

        <div class="submit-section">
          <button type="submit" class="submit-button" :disabled="loading">
            <span class="button-content">
              <span v-if="loading" class="loading-spinner"></span>
              {{ loading ? '계산중...' : '맞춤 적금 찾기' }}
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
            <span class="label">예상 만기 금액</span>
            <span class="value">{{ formatCurrency(getFinalAmount()) }}원</span>
          </div>
          <div class="summary-item">
            <span class="label">총 납입금</span>
            <span class="value">{{ formatCurrency(getTotalDeposit()) }}원</span>
          </div>
          <div class="summary-item">
            <span class="label">예상 이자 수익</span>
            <span class="value profit">{{ formatCurrency(getTotalProfit()) }}원</span>
          </div>
        </div>
      </div>

      <!-- 추천 상품 목록 -->
      <div class="recommendations-container">
        <h2 class="section-title">
          추천 적금 상품
          <span class="preference-tag">
            {{ userProfile.isCompound ? '복리' : '단리' }} 선호
          </span>
        </h2>

        <div class="products-grid">
          <div v-for="(product, index) in simulationResults.recommendations" :key="index" class="product-card"
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

              <div class="detail-item full-width">
                <span class="label">월 납입금</span>
                <span class="value">{{ formatCurrency(userProfile.monthlySavings) }}원</span>
              </div>
            </div>

            <div class="product-conditions" v-if="product.spcl_cnd">
              <h4 class="conditions-title">우대조건</h4>
              <p class="conditions-content">{{ product.spcl_cnd }}</p>
            </div>

            <div class="product-conditions">
              <h4 class="conditions-title">가입대상</h4>
              <p class="conditions-content">{{ product.join_member }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import Chart from 'chart.js/auto';
import { useFinancialStore } from '@/stores/financial';
import { useAccountStore } from '@/stores/account';

// 상태 관리
const financialStore = useFinancialStore();
const accountStore = useAccountStore();
const loading = ref(false);
const chartRef = ref(null);
const chart = ref(null);

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
  const interest = (principal * rate / 100 * months / 12) +
    (monthlyDeposit * rate / 100 * (months + 1) / 24);
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
const findBestOption = (product, targetPeriod) => {
  const options = product.savingoption_set;

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

// 시뮬레이션 실행
const runSimulation = async () => {
  try {
    loading.value = true;

    if (financialStore.savings.length === 0) {
      await financialStore.getSavingDatas();
    }

    const processedProducts = financialStore.savings
      .filter(checkAgeLimit)
      .map(product => {
        const option = findBestOption(product, userProfile.value.period);
        if (!option) return null;

        const monthlyAmount = userProfile.value.monthlySavings;
        const initialAmount = userProfile.value.currentAssets;

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
      throw new Error('추천 가능한 적금 상품이 없습니다.');
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

// 컴포넌트 마운트 시 초기화
onMounted(async () => {
  try {
    loading.value = true;
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
.financial-advisor {
  background-color: #f8f9fa;
  padding: 40px;
  transition: all 0.5s ease-in-out;
}

.title {
  font-size: 24px;
  font-weight: 700;
  margin: 6px 0px;
}

.text-subtitle-1 {
  font-size: 18px;
  font-weight: 400;
  margin: 6px 0px;
}

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

.section-title-1 {
  font-size: 18px;
  font-weight: 600;
  color: #636363;
  margin: 18px 0px 6px;
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  color: #2c3e50;
  margin: 24px 8px 16px 8px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e9ecef;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 첫 번째 section-title의 상단 여백 제거 */
.form-grid .section-title:first-child {
  margin-top: 0;
}

/* 추가적으로 뱃지(복리/단리 선호)를 위한 스타일 */
.preference-tag {
  font-size: 14px;
  padding: 4px 12px;
  background: #f1f4f8;
  border-radius: 20px;
  color: #5A87F2;
  font-weight: 500;
  margin-left: auto;
  /* 오른쪽으로 밀어내기 */
}

/* 입력 필드 스타일링 */
label {
  font-size: 14px;
  font-weight: 600;
  color: #2c2c2c;
  width: 80px;
}

input,
select {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.2s ease;
  background-color: white;
}

input {
  text-align: right;
}

input:focus,
select:focus {
  outline: none;
  border-color: #5A87F2;
  box-shadow: 0 0 0 3px rgba(99, 106, 204, 0.15);
}

/* 라디오 그룹 스타일링 */
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
  background: #5A87F2;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 106, 204, 0.2);
}

.submit-button:disabled {
  background: #e2e8f0;
  cursor: not-allowed;
  transform: none;
}

/* 차트 섹션 */
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

/* 결과 섹션 */
.results-section {
  max-width: 1200px;
  margin: 3rem auto;
}

.recommendations-container {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 24px rgba(149, 157, 165, 0.1);
}

.products-grid {
  display: grid;
  gap: 24px;
  margin-top: 24px;
}

/* 상품 카드 */
.product-card {
  background: white;
  border-radius: 16px;
  border: #f4f4f4 1px solid;
  padding: 40px;
  margin: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
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

/* 상품 상세 정보 */
.product-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.product-name {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.company-name {
  font-size: 14px;
  color: #666;
  margin: 4px 0 0;
}

.detail-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.detail-item {
  padding: 12px;
  border-radius: 12px;
  transition: background-color 0.2s ease;
  display: flex;
  justify-content: space-between;
}

.detail-item:hover {
  background: #f1f3f5;
}

.label {
  font-size: 0.9rem;
  color: #718096;
}

.value {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2d3748;
}

.highlight {
  color: #1f4ebc;
}

.profit {
  color: #2F855A;
}

/* 조건 섹션 */
.product-conditions {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 12px;
  margin-top: 1rem;
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
  to {
    transform: rotate(360deg);
  }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .financial-advisor {
    padding: 1rem;
  }

  .form-section {
    padding: 1.5rem;
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

  .recommendations-container {
    padding: 16px;
  }

  .product-card {
    padding: 16px;
    margin: 10px;
  }

  .detail-row {
    grid-template-columns: 1fr;
  }

  .chart-summary {
    grid-template-columns: 1fr;
  }
}

.input-group .radio-group {
  display: flex;
  gap: 24px;
  flex: 1;
}

.input-group {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-weight: 600;
  width: auto;
}

.radio-label input[type="radio"] {
  width: 16px;
  height: 16px;
}

.summary-item {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
</style>