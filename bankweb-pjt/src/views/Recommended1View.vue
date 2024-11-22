<template>
  <v-container class="financial-advisor" fluid>
    <!-- 헤더 섹션 -->
    <div class="header-section mb-8">
      <h1 class="text-h4 text-center font-weight-bold mb-2">맞춤 금융상품 추천</h1>
      <p class="text-subtitle-1 text-center text-medium-emphasis">
        고객님의 정보를 입력하시면 최적의 금융상품을 추천해드립니다.
      </p>
    </div>

    <!-- 입력 폼 섹션 -->
    <v-sheet class="form-section mx-auto" max-width="1000" rounded="lg" elevation="1">
      <v-form @submit.prevent="calculateRecommendations">
        <v-container>
          <v-row>
            <v-col cols="12">
              <h2 class="text-h6 mb-4">기본 정보 입력</h2>
            </v-col>
            
            <v-col cols="12" md="6">
              <v-text-field
                v-model="userProfile.age"
                label="나이"
                type="number"
                variant="outlined"
                :rules="[v => !!v || '나이를 입력해주세요']"
                required
                class="input-field"
                prefix="만 "
                suffix="세"
                hide-details="auto"
              ></v-text-field>
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model="userProfile.monthlySalary"
                label="월 급여"
                type="number"
                variant="outlined"
                :rules="[v => !!v || '월 급여를 입력해주세요']"
                required
                class="input-field"
                suffix="원"
                hide-details="auto"
                :hint="formatCurrency(userProfile.monthlySalary) + '원'"
                persistent-hint
              ></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-divider class="my-4"></v-divider>
              <h2 class="text-h6 mb-4">자산 및 목표 설정</h2>
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model="userProfile.currentAssets"
                label="현재 보유 자산"
                type="number"
                variant="outlined"
                :rules="[v => !!v || '현재 자산을 입력해주세요']"
                required
                class="input-field"
                suffix="원"
                hide-details="auto"
                :hint="formatCurrency(userProfile.currentAssets) + '원'"
                persistent-hint
              ></v-text-field>
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model="userProfile.monthlySavings"
                label="월 저축 가능 금액"
                type="number"
                variant="outlined"
                :rules="[v => !!v || '저축 가능 금액을 입력해주세요']"
                required
                class="input-field"
                suffix="원"
                hide-details="auto"
                :hint="formatCurrency(userProfile.monthlySavings) + '원'"
                persistent-hint
              ></v-text-field>
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model="userProfile.targetAmount"
                label="목표 자산"
                type="number"
                variant="outlined"
                :rules="[v => !!v || '목표 금액을 입력해주세요']"
                required
                class="input-field"
                suffix="원"
                hide-details="auto"
                :hint="formatCurrency(userProfile.targetAmount) + '원'"
                persistent-hint
              ></v-text-field>
            </v-col>

            <v-col cols="12" md="6">
              <v-select
                v-model="userProfile.targetPeriod"
                :items="periodOptions"
                label="투자 기간"
                item-title="label"
                item-value="value"
                variant="outlined"
                required
                hide-details="auto"
                class="input-field"
              ></v-select>
            </v-col>

            <v-col cols="12" class="text-center mt-4">
              <v-btn
                type="submit"
                color="primary"
                size="large"
                :loading="loading"
                :disabled="!isFormValid"
                min-width="200"
                class="submit-button"
              >
                맞춤 상품 찾기
                <v-icon end icon="mdi-arrow-right"></v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </v-sheet>

    <!-- 결과 섹션 -->
    <v-slide-y-transition>
      <div v-if="recommendedProducts.savings.length > 0 || recommendedProducts.deposits.length > 0" 
           class="results-section mt-8">
        <v-container>
          <v-row>            <!-- 적금 상품 추천 -->
            <v-col cols="12" md="6">
              <v-card class="product-card">
                <div class="product-card-header pa-4 bg-light-green-lighten-5">
                  <h3 class="text-h5 font-weight-bold mb-1">추천 적금 상품 TOP 5</h3>
                  <div class="text-subtitle-2 text-medium-emphasis">
                    월 {{ formatCurrency(userProfile.monthlySavings) }}원씩 {{ userProfile.targetPeriod }}개월 납입 기준
                  </div>
                </div>

                <v-card-text class="pa-4">
                  <div v-for="(product, index) in recommendedProducts.savings" 
                       :key="'saving-'+index" 
                       class="product-item"
                  >
                    <v-hover v-slot="{ isHovering, props }">
                      <v-card
                        v-bind="props"
                        :elevation="isHovering ? 4 : 1"
                        class="mb-4 transition-swing"
                      >
                        <v-card-item>
                          <div class="d-flex align-center mb-2">
                            <div class="rank-badge mr-3">{{ index + 1 }}</div>
                            <div>
                              <div class="text-h6">{{ product.fin_prdt_nm }}</div>
                              <div class="text-subtitle-2">{{ product.kor_co_nm }}</div>
                            </div>
                          </div>

                          <v-row class="mt-2" dense>
                            <v-col cols="6">
                              <div class="info-label">기본 금리</div>
                              <div class="info-value">{{ product.intr_rate }}%</div>
                            </v-col>
                            <v-col cols="6">
                              <div class="info-label">우대 금리</div>
                              <div class="info-value highlight">최대 {{ product.intr_rate2 }}%</div>
                            </v-col>
                            <v-col cols="12">
                              <div class="info-label">예상 만기 금액</div>
                              <div class="info-value">{{ formatCurrency(product.totalAmount) }}원</div>
                            </v-col>
                            <v-col cols="12">
                              <div class="info-label">이자 수익</div>
                              <div class="info-value text-success">
                                + {{ formatCurrency(product.expectedReturn) }}원
                              </div>
                            </v-col>
                            <v-col cols="12">
                              <div class="info-label">월 납입금</div>
                              <div class="info-value">{{ formatCurrency(product.monthlyPayment) }}원</div>
                            </v-col>
                          </v-row>

                          <v-expand-transition>
                            <div v-if="isHovering">
                              <v-divider class="my-3"></v-divider>
                              <div class="text-caption">
                                <div class="font-weight-bold mb-1">우대조건</div>
                                <div>{{ product.spcl_cnd || '우대조건 없음' }}</div>
                              </div>
                              <div class="text-caption mt-2">
                                <div class="font-weight-bold mb-1">가입대상</div>
                                <div>{{ product.join_member }}</div>
                              </div>
                            </div>
                          </v-expand-transition>
                        </v-card-item>
                      </v-card>
                    </v-hover>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>

            <!-- 예금 상품 추천 -->
            <v-col cols="12" md="6">
              <v-card class="product-card">
                <div class="product-card-header pa-4 bg-blue-lighten-5">
                  <h3 class="text-h5 font-weight-bold mb-1">추천 예금 상품 TOP 5</h3>
                  <div class="text-subtitle-2 text-medium-emphasis">
                    {{ formatCurrency(userProfile.currentAssets) }}원 {{ userProfile.targetPeriod }}개월 예치 기준
                  </div>
                </div>

                <v-card-text class="pa-4">
                  <div v-for="(product, index) in recommendedProducts.deposits" 
                       :key="'deposit-'+index" 
                       class="product-item"
                  >
                    <v-hover v-slot="{ isHovering, props }">
                      <v-card
                        v-bind="props"
                        :elevation="isHovering ? 4 : 1"
                        class="mb-4 transition-swing"
                      >
                        <v-card-item>
                          <div class="d-flex align-center mb-2">
                            <div class="rank-badge mr-3">{{ index + 1 }}</div>
                            <div>
                              <div class="text-h6">{{ product.fin_prdt_nm }}</div>
                              <div class="text-subtitle-2">{{ product.kor_co_nm }}</div>
                            </div>
                          </div>

                          <v-row class="mt-2" dense>
                            <v-col cols="6">
                              <div class="info-label">기본 금리</div>
                              <div class="info-value">{{ product.intr_rate }}%</div>
                            </v-col>
                            <v-col cols="6">
                              <div class="info-label">우대 금리</div>
                              <div class="info-value highlight">최대 {{ product.intr_rate2 }}%</div>
                            </v-col>
                            <v-col cols="12">
                              <div class="info-label">예상 만기 금액</div>
                              <div class="info-value">{{ formatCurrency(product.totalAmount) }}원</div>
                            </v-col>
                            <v-col cols="12">
                              <div class="info-label">이자 수익</div>
                              <div class="info-value text-success">
                                + {{ formatCurrency(product.expectedReturn) }}원
                              </div>
                            </v-col>
                            <v-col cols="12">
                              <div class="info-label">예치 금액</div>
                              <div class="info-value">{{ formatCurrency(product.principal) }}원</div>
                            </v-col>
                          </v-row>

                          <v-expand-transition>
                            <div v-if="isHovering">
                              <v-divider class="my-3"></v-divider>
                              <div class="text-caption">
                                <div class="font-weight-bold mb-1">우대조건</div>
                                <div>{{ product.spcl_cnd || '우대조건 없음' }}</div>
                              </div>
                              <div class="text-caption mt-2">
                                <div class="font-weight-bold mb-1">가입대상</div>
                                <div>{{ product.join_member }}</div>
                              </div>
                            </div>
                          </v-expand-transition>
                        </v-card-item>
                      </v-card>
                    </v-hover>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </div>
    </v-slide-y-transition>
  </v-container>
</template>
            
<script setup>
import { useFinancialStore } from '@/stores/financial';
import { ref, computed, onMounted } from 'vue';

const financialStore = useFinancialStore();

// 기간 선택 옵션
const periodOptions = [
  { value: 6, label: '6개월' },
  { value: 12, label: '1년' },
  { value: 24, label: '2년' },
  { value: 36, label: '3년' },
];

// 상태 관리
const loading = ref(false);
const userProfile = ref({
  age: null,
  currentAssets: null,
  monthlySalary: null,
  monthlySavings: null,
  targetAmount: null,
  targetPeriod: 12
});

const recommendedProducts = ref({
  deposits: [],
  savings: []
});

const depositProducts = ref([]);
const savingProducts = ref([]);

// 폼 유효성 검사
const isFormValid = computed(() => {
  const { age, currentAssets, monthlySalary, monthlySavings, targetAmount, targetPeriod } = userProfile.value;
  return age > 0 && 
         currentAssets >= 0 && 
         monthlySalary > 0 && 
         monthlySavings > 0 && 
         targetAmount > 0 && 
         targetPeriod;
});

// 숫자 포맷팅
const formatCurrency = (value) => {
  if (!value) return '0';
  return new Intl.NumberFormat('ko-KR').format(Math.round(value));
};

// 적금 이자 계산 (단리)
const calculateSavingInterest = (monthlyPayment, rate, period) => {
  const principal = monthlyPayment * period;
  const interest = (principal * (rate/100) * period/12);
  return interest;
};

// 예금 이자 계산 (단리)
const calculateDepositInterest = (principal, rate, period) => {
  return principal * (rate/100) * (period/12);
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

  // 정확히 일치하는 기간 찾기
  const exactMatch = options.find(opt => parseInt(opt.save_trm) === targetPeriod);
  if (exactMatch) return exactMatch;

  // 가장 가까운 기간 찾기
  return options.reduce((prev, curr) => {
    const prevDiff = Math.abs(parseInt(prev.save_trm) - targetPeriod);
    const currDiff = Math.abs(parseInt(curr.save_trm) - targetPeriod);
    return currDiff < prevDiff ? curr : prev;
  });
};

// 추천 상품 계산 부분도 수정
const calculateRecommendations = async () => {
  try {
    loading.value = true;

    // 적금 상품 계산
    const savingsResults = savingProducts.value
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

    // 예금 상품 계산
    const depositsResults = depositProducts.value
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

    // 수익률 기준으로 정렬하고 상위 5개 선택
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
      depositProducts.value = financialStore.deposits;
    }
    if (financialStore.savings && Array.isArray(financialStore.savings)) {
      savingProducts.value = financialStore.savings;
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
}

.header-section {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 0;
}

.form-section {
  background: white;
  padding: 2rem;
  border-radius: 16px;
}

.input-field {
  background-color: #fff;
}

.submit-button {
  border-radius: 8px;
  text-transform: none;
  font-size: 1.1rem;
}

.product-card {
  height: 100%;
  border-radius: 16px;
  overflow: hidden;
}

.product-card-header {
  border-bottom: 1px solid rgba(0,0,0,0.1);
}

.product-item {
  transition: all 0.3s ease;
}

.rank-badge {
  background: #f0f0f0;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.1rem;
}

.info-label {
  color: rgba(0,0,0,0.6);
  font-size: 0.875rem;
  margin-bottom: 4px;
}

.info-value {
  font-weight: 500;
  font-size: 1rem;
}

.info-value.highlight {
  color: #1976d2;
  font-weight: bold;
}

.text-success {
  color: #2e7d32;
  font-weight: bold;
}

.transition-swing {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.5, 1);
}

.results-section {
  margin-bottom: 2rem;
}
</style>