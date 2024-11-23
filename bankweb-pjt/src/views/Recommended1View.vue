<template>
  <div class="financial-advisor">
    <!-- 헤더 섹션 -->
    <div class="mb-8">
      <h1 class="text-h4 text-center font-weight-bold mb-2">금융 목표 기반 추천</h1>
      <p class="text-subtitle-1 text-center text-medium-emphasis">
        고객님의 정보를 입력하시면 최적의 금융상품을 추천해드립니다.
      </p>
    </div>

    <!-- 입력 폼 섹션 -->
    <section class="form-section">
      <form @submit.prevent="calculateRecommendations">
        <div class="form-grid">
          <div class="input-group full-width">
            <h2 class="section-title">기본 정보 입력</h2>
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
            <div class="divider"></div>
            <h2 class="section-title">자산 및 목표 설정</h2>
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
// Script content remains mostly the same as the original, just remove Vuetify-specific code
import { useAccountStore } from '@/stores/account';
import { useFinancialStore } from '@/stores/financial';
import { ref, computed, onMounted } from 'vue';

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

// Formatting functions
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

// Computed properties for formatting
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

// Calculation functions remain the same
const calculateSavingInterest = (monthlyPayment, rate, period) => {
  const principal = monthlyPayment * period;
  const interest = (principal * (rate/100) * period/12);
  return interest;
};

const calculateDepositInterest = (principal, rate, period) => {
  return principal * (rate/100) * (period/12);
};

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

const calculateRecommendations = async () => {
  try {
    loading.value = true;

    const savingsResults = financialStore.savings
      .filter(checkAgeLimit)
      .map(product => {
        const option = findBestOption(product, userProfile.value.targetPeriod);
        if (!option) return
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
.financial-advisor {
  background-color: #f5f5f5;
  min-height: 100vh;
  padding: 2rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.header-section {
  text-align: center;
  margin-bottom: 3rem;
}

.title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a237e;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.1rem;
  color: #666;
}

.form-section {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 1000px;
  margin: 0 auto 2rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.input-group {
  display: flex;
  flex-direction: column;
}

.input-group.full-width {
  grid-column: 1 / -1;
}

.section-title {
  font-size: 1.25rem;
  font-weight: 600;

  margin-bottom: 1rem;
}

.divider {
  height: 1px;
  background-color: #e0e0e0;
  margin: 1rem 0;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-group label {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
}

.input-group input,
.input-group select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s;
  width: 100%;
}

.input-group input:focus,
.input-group select:focus {
  outline: none;
  border-color: #1976d2;
  box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.2);
}

.prefix,
.suffix {
  position: absolute;
  color: #666;
  font-size: 0.9rem;
}

.prefix {
  left: 0.75rem;
}

.suffix {
  right: 0.75rem;
}

.submit-section {
  text-align: center;
  margin-top: 2rem;
}

.submit-button {
  background-color: #1976d2;
  color: white;
  padding: 0.75rem 2.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 200px;
}

.submit-button:hover {
  background-color: #1565c0;
}

.submit-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #fff;
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 1s linear infinite;
}

.results-section {
  max-width: 1200px;
  margin: 3rem auto;
}

.products-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.product-category {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.category-header {
  padding: 1.5rem;
}

.saving-header {
  background-color: #e8f5e9;
}

.deposit-header {
  background-color: #e3f2fd;
}

.category-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1a237e;
  margin-bottom: 0.5rem;
}

.category-subtitle {
  color: #666;
  font-size: 0.9rem;
}

.products-list {
  padding: 1.5rem;
}

.product-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  margin-bottom: 1.5rem;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.top-product {
  border: 2px solid #1976d2;
}

.product-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.rank-badge {
  background: #1976d2;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.product-info {
  flex: 1;
}

.product-name {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: #1a237e;
}

.company-name {
  font-size: 0.875rem;
  color: #666;
  margin: 0.25rem 0 0 0;
}

.product-details {
  margin-bottom: 1.5rem;
}

.detail-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-item.full-width {
  grid-column: 1 / -1;
}

.label {
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 0.25rem;
}

.value {
  font-size: 1.1rem;
  font-weight: 500;
}

.highlight {
  color: #1976d2;
  font-weight: 600;
}

.profit {
  color: #2e7d32;
  font-weight: 600;
}

.product-conditions {
  border-top: 1px solid #eee;
  padding-top: 1rem;
  margin-top: 1rem;
}

.conditions-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
}

.conditions-content {
  font-size: 0.875rem;
  color: #666;
  line-height: 1.5;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .financial-advisor {
    padding: 1rem;
  }

  .title {
    font-size: 2rem;
  }

  .form-section,
  .product-category {
    border-radius: 12px;
  }

  .products-container {
    grid-template-columns: 1fr;
  }

  .product-card {
    margin: 1rem;
  }
}
</style>