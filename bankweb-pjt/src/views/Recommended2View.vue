<template>
  <div class="recommendation-container">
    {{ financialStore.deposits }}
    <!-- 사용자 정보 입력 폼 -->
    <v-form @submit.prevent="calculateRecommendations" class="input-form">
      <div class="form-section">
        <h3>개인 정보 입력</h3>
        <v-text-field v-model="userInfo.age" label="나이" type="number" required></v-text-field>
        <v-text-field v-model="userInfo.currentAssets" label="현재 자산" type="number" required></v-text-field>
        <v-text-field v-model="userInfo.monthlySalary" label="월 급여" type="number" required></v-text-field>
      </div>

      <div class="form-section">
        <h3>목표 설정</h3>
        <v-text-field v-model="targetInfo.targetAmount" label="목표 자산 금액" type="number" required></v-text-field>

        <p>목표 달성 기간</p>
        <v-select v-model="targetInfo.targetPeriod" :items="periodOptions" item-title="text" item-value="value" label="기간 선택" required></v-select>

        <v-text-field v-model="targetInfo.monthlySavings" label="월 저축 가능 금액" type="number" required></v-text-field>
      </div>

      <v-btn type="submit" color="primary" block>상품 추천받기</v-btn>
    </v-form>

    <!-- 추천 상품 결과 -->
    <div v-if="recommendations.length > 0" class="recommendations">
      <h2>추천 상품 TOP 5</h2>
      <v-card v-for="(rec, index) in recommendations" :key="index" class="mb-4">
        <v-card-title>{{ index + 1 }}. {{ rec.productName }}</v-card-title>
        <v-card-text>
          <p>
            <strong>은행:</strong>
            {{ rec.bankName }}
          </p>
          <p>
            <strong>기본 금리:</strong>
            {{ rec.baseRate }}%
          </p>
          <p>
            <strong>최대 우대 금리:</strong>
            {{ rec.maxRate }}%
          </p>
          <p>
            <strong>예상 만기 수령액:</strong>
            {{ formatCurrency(rec.expectedAmount) }}원
          </p>
          <p>
            <strong>월 납입금:</strong>
            {{ formatCurrency(rec.monthlySavings) }}원
          </p>
          <div v-if="rec.specialConditions" class="mt-2">
            <strong>우대조건:</strong>
            <p>{{ rec.specialConditions }}</p>
          </div>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script setup>
import { useFinancialStore } from "@/stores/financial";
import { ref } from "vue";

const financialStore = useFinancialStore();

const userInfo = ref({
  age: null,
  currentAssets: null,
  monthlySalary: null,
});

const targetInfo = ref({
  targetAmount: null,
  targetPeriod: null,
  monthlySavings: null,
});

const recommendations = ref([]);

const periodOptions = [
  { text: "6개월", value: 6 },
  { text: "12개월", value: 12 },
  { text: "24개월", value: 24 },
  { text: "36개월", value: 36 },
];

const formatCurrency = (value) => {
  return new Intl.NumberFormat("ko-KR").format(value);
};

const calculateExpectedAmount = (principal, rate, months) => {
  // 단리 계산
  const interest = principal * (rate / 100) * (months / 12);
  return Math.round(principal + interest);
};

const calculateMonthlyExpectedAmount = (monthlySavings, rate, months) => {
  let total = 0;
  for (let i = 0; i < months; i++) {
    total += monthlySavings;
    total += monthlySavings * (rate / 100) * ((months - i) / 12);
  }
  return Math.round(total);
};

const calculateRecommendations = () => {
  // 입력값 검증
  if (!userInfo.value.age || !userInfo.value.currentAssets || !userInfo.value.monthlySalary || !targetInfo.value.targetAmount || !targetInfo.value.targetPeriod || !targetInfo.value.monthlySavings) {
    alert("모든 필드를 입력해주세요.");
    return;
  }

  // 사용자 조건에 맞는 상품 필터링
  let eligibleProducts = savingsProducts.filter((product) => {
    // 나이 제한 체크
    if (product.join_deny === 3) {
      if (product.join_member.includes("만 19~34세") && (userInfo.value.age < 19 || userInfo.value.age > 34)) {
        return false;
      }
      // 기타 나이 제한 조건 체크...
    }

    // 월 저축 한도 체크
    if (product.max_limit && targetInfo.value.monthlySavings > product.max_limit) {
      return false;
    }

    // 기간 체크
    return product.savingoption_set.some((option) => option.save_trm === targetInfo.value.targetPeriod.toString());
  });

  // 예상 수익 계산 및 정렬
  const productsWithReturns = eligibleProducts.map((product) => {
    const option = product.savingoption_set.find((opt) => opt.save_trm === targetInfo.value.targetPeriod.toString());

    const expectedAmount = calculateMonthlyExpectedAmount(
      targetInfo.value.monthlySavings,
      option.intr_rate2, // 최대 우대금리 사용
      targetInfo.value.targetPeriod
    );

    return {
      productName: product.fin_prdt_nm,
      bankName: product.kor_co_nm,
      baseRate: option.intr_rate,
      maxRate: option.intr_rate2,
      expectedAmount: expectedAmount,
      monthlySavings: targetInfo.value.monthlySavings,
      specialConditions: product.spcl_cnd,
    };
  });

  // 예상 수익 기준으로 정렬
  recommendations.value = productsWithReturns.sort((a, b) => b.expectedAmount - a.expectedAmount).slice(0, 5);
};
</script>

<style scoped>
.recommendation-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.input-form {
  margin-bottom: 30px;
}

.form-section {
  margin-bottom: 20px;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
}

.recommendations {
  margin-top: 30px;
}

h2 {
  margin-bottom: 20px;
}

.mb-4 {
  margin-bottom: 16px;
}

.mt-2 {
  margin-top: 8px;
}
</style>
