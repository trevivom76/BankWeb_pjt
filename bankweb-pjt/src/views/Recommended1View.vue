<template>
  <div class="financial-advisor">
    <!-- 헤더 섹션 -->
    <div class="mb-8">
      <p class="title">금융 목표 기반 추천</p>
      <p class="text-subtitle-1">
        고객님의 정보를 입력하시면 최적의 금융상품을 추천해드립니다.
      </p>
    </div>

    <!-- 입력 폼 섹션 -->
    <section class="form-section">
      <form @submit.prevent="calculateRecommendations">
        <div class="form-grid">
          <div class="input-group full-width">
            <h2 class="section-title">기본 정보 입력</h2>
            <div class="divider"></div>
          </div>
          
          <div class="input-group">
            <label>나이</label>
            <div class="input-wrapper">
              <input
                v-model="userProfile.age"
                type="number"
                placeholder="만 나이 입력"
                required
              />
              <span class="suffix">세</span>
            </div>
          </div>

          <div class="input-group">
            <label>월 급여</label>
            <div class="input-wrapper">
              <input
                v-model="formattedMonthlySalary"
                type="text"
                placeholder="월 급여 입력"
                required
              />
              <span class="suffix">원</span>
            </div>
          </div>

          <div class="input-group full-width">
            <h2 class="section-title">자산 및 목표 설정</h2>
            <div class="divider"></div>
          </div>

          <div class="input-group">
            <label>현재 보유 자산</label>
            <div class="input-wrapper">
              <input
                v-model="formattedCurrentAssets"
                type="text"
                placeholder="현재 자산 입력"
                required
              />
              <span class="suffix">원</span>
            </div>
          </div>

          <div class="input-group">
            <label>월 저축 가능 금액</label>
            <div class="input-wrapper">
              <input
                v-model="formattedMonthlySavings"
                type="text"
                placeholder="월 저축 가능액 입력"
                required
              />
              <span class="suffix">원</span>
            </div>
          </div>

          <div class="input-group">
            <label>목표 자산</label>
            <div class="input-wrapper">
              <input
                v-model="formattedTargetAmount"
                type="text"
                placeholder="목표 금액 입력"
                required
              />
              <span class="suffix">원</span>
            </div>
          </div>

          <div class="input-group">
            <label>투자 기간</label>
            <select v-model="userProfile.targetPeriod" required>
              <option v-for="option in periodOptions" 
                      :key="option.value" 
                      :value="option.value">
                {{ option.label }}
              </option>
            </select>
          </div>
        </div>

        <div class="submit-section">
          <button 
            type="submit" 
            class="submit-button"
            :disabled="!isFormValid || loading"
          >
            <span class="button-content">
              <span v-if="loading" class="loading-spinner"></span>
              {{ loading ? '계산중...' : '맞춤 상품 찾기' }}
            </span>
            <span class="icon">→</span>
          </button>
        </div>
      </form>
    </section>

    <!-- 목표 달성 분석 섹션 -->
    <section v-if="recommendedProducts.savings.length > 0 || recommendedProducts.deposits.length > 0" 
             class="goal-analysis-section">
      <div class="analysis-card">
        <h3 class="analysis-title">목표 달성 분석</h3>
        
        <div class="analysis-content">
          <div class="progress-container">
            <div class="progress-bar">
              <div class="progress-fill" 
                   :style="{ width: `${achievementRate}%` }"
                   :class="{ 'high': achievementRate >= 80, 'medium': achievementRate >= 50 && achievementRate < 80 }">
              </div>
            </div>
            <div class="progress-label">{{ achievementRate }}% 달성 예상</div>
          </div>

          <div class="analysis-details">
            <div class="detail-box">
              <span class="label">목표 금액</span>
              <span class="value">{{ formatCurrency(userProfile.targetAmount) }}원</span>
            </div>
            
            <div class="detail-box">
              <span class="label">예상 도달 금액</span>
              <span class="value">{{ formatCurrency(expectedAmount) }}원</span>
            </div>

            <div class="detail-box">
              <span class="label">설정 기간 후 달성률</span>
              <span class="value">{{ achievementRate }}%</span>
            </div>

            <div class="detail-box">
              <span class="label">목표 달성 예상 기간</span>
              <span class="value">{{ formatTimeToGoal }}</span>
            </div>
          </div>

          <div class="analysis-summary">
            <p v-if="monthsToGoal <= userProfile.targetPeriod" class="success-message">
              목표 기간 내 달성이 가능합니다!
            </p>
            <p v-else class="info-message">
              목표 달성을 위해 월 {{ getAdditionalSavingsNeeded }}원의 추가 저축이 필요합니다.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- 결과 섹션 -->
    <section v-if="recommendedProducts.savings.length > 0 || recommendedProducts.deposits.length > 0" 
             class="results-section">
      <div class="products-container">
        <!-- 적금 상품 추천 -->
        <div class="product-category">
          <div class="category-header saving-header">
            <h3 class="category-title">추천 적금 상품 TOP 5</h3>
            <p class="category-subtitle">
              월 {{ formatCurrency(userProfile.monthlySavings) }}원씩 {{ userProfile.targetPeriod }}개월 납입 기준
            </p>
          </div>

          <div class="products-list">
            <div v-for="(product, index) in recommendedProducts.savings" 
                 :key="'saving-'+index" 
                 class="product-card"
                 :class="{ 'top-product': index === 0 }">
              <div class="product-header">
                <div class="rank-badge" :class="{ 'top-rank': index === 0 }">{{ index + 1 }}</div>
                <div class="product-info">
                  <h4 class="product-name">{{ product.fin_prdt_nm }}</h4>
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
                  <span class="value">{{ formatCurrency(product.totalAmount) }}원</span>
                </div>
                
                <div class="detail-item full-width">
                  <span class="label">이자 수익</span>
                  <span class="value profit">
                    + {{ formatCurrency(product.expectedReturn) }}원
                  </span>
                </div>
                
                <div class="detail-item full-width">
                  <span class="label">월 납입금</span>
                  <span class="value">{{ formatCurrency(product.monthlyPayment) }}원</span>
                </div>
              </div>

              <div class="product-conditions" v-if="product.spcl_cnd">
                <h5 class="conditions-title">우대조건</h5>
                <p class="conditions-content">{{ product.spcl_cnd }}</p>
              </div>

              <div class="product-conditions">
                <h5 class="conditions-title">가입대상</h5>
                <p class="conditions-content">{{ product.join_member }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 예금 상품 추천 -->
        <div class="product-category">
          <div class="category-header deposit-header">
            <h3 class="category-title">추천 예금 상품 TOP 5</h3>
            <p class="category-subtitle">
              {{ formatCurrency(userProfile.currentAssets) }}원 {{ userProfile.targetPeriod }}개월 예치 기준
            </p>
          </div>

          <div class="products-list">
            <div v-for="(product, index) in recommendedProducts.deposits" 
                 :key="'deposit-'+index" 
                 class="product-card"
                 :class="{ 'top-product': index === 0 }">
              <div class="product-header">
                <div class="rank-badge" :class="{ 'top-rank': index === 0 }">{{ index + 1 }}</div>
                <div class="product-info">
                  <h4 class="product-name">{{ product.fin_prdt_nm }}</h4>
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
                  <span class="value">{{ formatCurrency(product.totalAmount) }}원</span>
                </div>
                
                <div class="detail-item full-width">
                  <span class="label">이자 수익</span>
                  <span class="value profit">
                    + {{ formatCurrency(product.expectedReturn) }}원
                  </span>
                </div>
                
                <div class="detail-item full-width">
                  <span class="label">예치 금액</span>
                  <span class="value">{{ formatCurrency(product.principal) }}원</span>
                </div>
              </div>

              <div class="product-conditions" v-if="product.spcl_cnd">
                <h5 class="conditions-title">우대조건</h5>
                <p class="conditions-content">{{ product.spcl_cnd }}</p>
              </div>

              <div class="product-conditions">
                <h5 class="conditions-title">가입대상</h5>
                <p class="conditions-content">{{ product.join_member }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAccountStore } from '@/stores/account';
import { useFinancialStore } from '@/stores/financial';

const financialStore = useFinancialStore();
const accountStore = useAccountStore();

const periodOptions = [
  { value: 6, label: '6개월' },
  { value: 12, label: '1년' },
  { value: 24, label: '2년' },
  { value: 36, label: '3년' },
];

const loading = ref(false);
const userProfile = ref({
  age: accountStore.userinfo?.age || null,
  currentAssets: accountStore.userinfo?.money || null,
  monthlySalary: accountStore.userinfo?.salary || null,
  monthlySavings: null,
  targetAmount: null,
  targetPeriod: 12
});

const recommendedProducts = ref({
  deposits: [],
  savings: []
});

const isFormValid = computed(() => {
  const { age, currentAssets, monthlySalary, monthlySavings, targetAmount, targetPeriod } = userProfile.value;
  return age > 0 && 
         currentAssets >= 0 && 
         monthlySalary > 0 && 
         monthlySavings > 0 && 
         targetAmount > 0 && 
         targetPeriod;
});

// 통화 포맷팅 함수
const formatCurrency = (value) => {
  if (!value) return '0';
  return new Intl.NumberFormat('ko-KR').format(Math.round(value));
};

const formatNumber = (value) => {
  if (!value) return '';
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};

const unformatNumber = (value) => {
  if (!value) return '';
  return value.toString().replace(/,/g, '');
};

// 입력값 포맷팅을 위한 computed 속성들
const formattedMonthlySalary = computed({
  get: () => formatNumber(userProfile.value.monthlySalary),
  set: (value) => {
    userProfile.value.monthlySalary = Number(unformatNumber(value));
  }
});

const formattedCurrentAssets = computed({
  get: () => formatNumber(userProfile.value.currentAssets),
  set: (value) => {
    userProfile.value.currentAssets = Number(unformatNumber(value));
  }
});

const formattedMonthlySavings = computed({
  get: () => formatNumber(userProfile.value.monthlySavings),
  set: (value) => {
    userProfile.value.monthlySavings = Number(unformatNumber(value));
  }
});

const formattedTargetAmount = computed({
  get: () => formatNumber(userProfile.value.targetAmount),
  set: (value) => {
    userProfile.value.targetAmount = Number(unformatNumber(value));
  }
});

// 이자 계산 함수들
const calculateSavingInterest = (monthlyPayment, rate, period) => {
  const principal = monthlyPayment * period;
  const interest = (principal * (rate/100) * period/12);
  return interest;
};

const calculateDepositInterest = (principal, rate, period) => {
  return principal * (rate/100) * (period/12);
};

// 나이 제한 확인 함수
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

// 최적의 옵션 찾기
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

// 목표 달성 관련 계산 함수들
const calculateMonthsToGoal = () => {
  const bestSavingRate = recommendedProducts.value.savings[0]?.intr_rate2 || 0;
  const bestDepositRate = recommendedProducts.value.deposits[0]?.intr_rate2 || 0;
  const averageMonthlyRate = ((bestSavingRate + bestDepositRate) / 2) / 12 / 100;

  let accumulated = userProfile.value.currentAssets;
  let months = 0;
  
  while (accumulated < userProfile.value.targetAmount && months < 600) { // 50년 상한
    accumulated += userProfile.value.monthlySavings;
    accumulated *= (1 + averageMonthlyRate);
    months++;
  }
  
  return months;
};

const calculateExpectedAmount = () => {
  const bestSavingRate = recommendedProducts.value.savings[0]?.intr_rate2 || 0;
  const bestDepositRate = recommendedProducts.value.deposits[0]?.intr_rate2 || 0;
  const averageMonthlyRate = ((bestSavingRate + bestDepositRate) / 2) / 12 / 100;

  let accumulated = userProfile.value.currentAssets;
  for (let i = 0; i < userProfile.value.targetPeriod; i++) {
    accumulated += userProfile.value.monthlySavings;
    accumulated *= (1 + averageMonthlyRate);
  }
  return accumulated;
};

// 목표 달성 관련 computed 속성들
const monthsToGoal = computed(() => calculateMonthsToGoal());

const expectedAmount = computed(() => calculateExpectedAmount());

const achievementRate = computed(() => {
  return Math.min(
    Math.round((expectedAmount.value / userProfile.value.targetAmount) * 100),
    100
  );
});

const formatTimeToGoal = computed(() => {
  const months = monthsToGoal.value;
  const years = Math.floor(months / 12);
  const remainingMonths = months % 12;
  
  if (years === 0) {
    return `약 ${remainingMonths}개월`;
  } else if (remainingMonths === 0) {
    return `약 ${years}년`;
  } else {
    return `약 ${years}년 ${remainingMonths}개월`;
  }
});

const getAdditionalSavingsNeeded = computed(() => {
  if (monthsToGoal.value <= userProfile.value.targetPeriod) {
    return 0;
  }
  
  const additionalRequired = Math.ceil(
    (userProfile.value.targetAmount - expectedAmount.value) / userProfile.value.targetPeriod
  );
  
  return formatCurrency(additionalRequired);
});

// 상품 추천 계산 함수
const calculateRecommendations = async () => {
  try {
    loading.value = true;

    const savingsResults = financialStore.savings
      .filter(checkAgeLimit)
      .map(product => {
        const option = findBestOption(product, userProfile.value.targetPeriod);
        if (!option) return null;
        const monthlyPayment = Math.min(
          userProfile.value.monthlySavings,
          product.max_limit || Infinity
        );
        const expectedReturn = calculateSavingInterest(
          monthlyPayment,
          option.intr_rate2,
          userProfile.value.targetPeriod
        );
        const totalAmount = (monthlyPayment * userProfile.value.targetPeriod) + expectedReturn;

        return {
          ...product,
          intr_rate: option.intr_rate,
          intr_rate2: option.intr_rate2,
          expectedReturn,
          totalAmount,
          monthlyPayment
        };
      })
      .filter(product => product && product.expectedReturn > 0);

    const depositsResults = financialStore.deposits
      .filter(checkAgeLimit)
      .map(product => {
        const option = findBestOption(product, userProfile.value.targetPeriod, true);
        if (!option) return null;

        const principal = userProfile.value.currentAssets;
        const expectedReturn = calculateDepositInterest(
          principal,
          option.intr_rate2,
          userProfile.value.targetPeriod
        );
        const totalAmount = principal + expectedReturn;

        return {
          ...product,
          intr_rate: option.intr_rate,
          intr_rate2: option.intr_rate2,
          expectedReturn,
          totalAmount,
          principal
        };
      })
      .filter(product => product && product.expectedReturn > 0);

    recommendedProducts.value = {
      savings: savingsResults
        .sort((a, b) => b.expectedReturn - a.expectedReturn)
        .slice(0, 5),
      deposits: depositsResults
        .sort((a, b) => b.expectedReturn - a.expectedReturn)
        .slice(0, 5)
    };

  } catch (error) {
    console.error('상품 추천 계산 중 오류 발생:', error);
  } finally {
    loading.value = false;
  }
};

// 초기 데이터 로드
onMounted(async () => {
  try {
    loading.value = true;
    if (financialStore.deposits && Array.isArray(financialStore.deposits)) {
      await financialStore.getDepositDatas();
    }
    if (financialStore.savings && Array.isArray(financialStore.savings)) {
      await financialStore.getSavingDatas();
    }
  } catch (error) {
    console.error('데이터 로드 중 오류 발생:', error);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
/* 기존 스타일 유지 */
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
.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  flex: 1;
}

label {
  font-size: 14px;
  font-weight: 600;
  color: #2c2c2c;
  width: 100px;
}

input, select {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.2s ease;
  background-color: white;
}

input:focus, select:focus {
  outline: none;
  border-color: #5A87F2;
  box-shadow: 0 0 0 3px rgba(99, 106, 204, 0.15);
}

.suffix {
  position: absolute;
  right: 1rem;
  color: #718096;
  font-weight: 500;
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
  gap: 8px;
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

/* 목표 달성 분석 섹션 */
.goal-analysis-section {
  margin: 2rem auto;
  max-width: 1000px;
}

.analysis-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.analysis-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.progress-container {
  margin-bottom: 2rem;
}

.progress-bar {
  height: 12px;
  background: #e2e8f0;
  border-radius: 6px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #5A87F2;
  border-radius: 6px;
  transition: width 0.5s ease-in-out;
}

.progress-fill.high {
  background: #48bb78;
}

.progress-fill.medium {
  background: #ecc94b;
}

.progress-label {
  text-align: right;
  margin-top: 0.5rem;
  font-weight: 600;
  color: #2d3748;
}

.analysis-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.detail-box {
  background: #f8fafc;
  padding: 1rem;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.detail-box .label {
  font-size: 0.875rem;
  color: #64748b;
}

.detail-box .value {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1a202c;
}

.analysis-summary {
  background: #f1f5f9;
  padding: 1rem;
  border-radius: 12px;
  margin-top: 1rem;
}

.success-message {
  color: #2f855a;
  font-weight: 600;
}

.info-message {
  color: #2b6cb0;
  font-weight: 600;
}

/* 결과 섹션 스타일 */
.results-section {
  max-width: 1200px;
  margin: 3rem auto;
}

.products-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
  gap: 2rem;
}

.product-category {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(149, 157, 165, 0.1);
}

.saving-header {
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
  padding: 28px;
}

.deposit-header {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  padding: 28px;
}

.category-title {
    font-size: 20px;
    font-weight: 700;
    color: #2c3e50;
    margin-bottom: 8px;
  }

  .category-subtitle {
    font-size: 14px;
    color: #4a5568;
  }

  .products-list {
    padding: 1rem;
  }

  .product-card {
    background: white;
    border-radius: 16px;
    border: 1px solid #f4f4f4;
    padding: 24px;
    margin: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    transition: all 0.3s ease;
  }

  .product-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  }

  .product-card.top-product {
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
    flex-shrink: 0;
  }

  .rank-badge.top-rank {
    background: linear-gradient(135deg, #5A87F2, #2e5cc8);
  }

  .product-info {
    flex: 1;
  }

  .product-name {
    font-size: 18px;
    font-weight: 600;
    color: #2d3748;
    margin: 0;
  }

  .company-name {
    font-size: 14px;
    color: #718096;
    margin: 4px 0 0 0;
  }

  .product-details {
    margin: 20px 0;
  }

  .detail-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 12px;
  }

  .detail-item {
    padding: 12px;
    border-radius: 12px;
    background: #f8fafc;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .detail-item.full-width {
    grid-column: 1 / -1;
  }

  .detail-item .label {
    font-size: 14px;
    color: #64748b;
  }

  .detail-item .value {
    font-size: 16px;
    font-weight: 600;
    color: #2d3748;
  }

  .detail-item .value.highlight {
    color: #5A87F2;
  }

  .detail-item .value.profit {
    color: #2f855a;
  }

  .product-conditions {
    background: #f8fafc;
    padding: 16px;
    border-radius: 12px;
    margin-top: 16px;
  }

  .conditions-title {
    font-size: 14px;
    font-weight: 600;
    color: #4a5568;
    margin: 0 0 8px 0;
  }

  .conditions-content {
    font-size: 14px;
    color: #718096;
    margin: 0;
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
    display: inline-block;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  /* 구분선 */
  .divider {
    height: 1px;
    background-color: #e2e8f0;
    margin: 8px 0;
  }

  /* 반응형 디자인 */
  @media (max-width: 768px) {
    .financial-advisor {
      padding: 16px;
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
      margin-bottom: 4px;
    }

    .products-container {
      grid-template-columns: 1fr;
    }

    .product-card {
      margin: 12px 8px;
      padding: 16px;
    }

    .detail-row {
      grid-template-columns: 1fr;
    }

    .analysis-details {
      grid-template-columns: 1fr;
    }
  }

  @media (max-width: 480px) {
    .category-header {
      padding: 20px;
    }

    .product-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 12px;
    }

    .product-info {
      width: 100%;
    }
  }
</style>