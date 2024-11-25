<template>
  <div class="layout">
    <div class="layout-product-list">
      <!-- 적금 상품 리스트 -->
      <div class="interest-products">
        <h2 class="title">적금 상품 리스트</h2>
        <div v-if="!isSavingsExpanded" class="carousel-container">
          <div class="carousel" :style="{ transform: `translateY(-${currentSavingsIndex * cardHeight}px)` }">
            <div class="card" v-for="(product, index) in savings" :key="'savings-' + product.id">
              <p>{{ product.kor_co_nm }}</p>
              <h3>{{ product.fin_prdt_nm }}</h3>
              <button @click="openModal(product, false)">상세 보기 ></button>
            </div>
          </div>
        </div>
        <div v-else class="product-list">
          <div class="card" v-for="(product, index) in savings" :key="'savings-' + product.id">
            <p>{{ product.kor_co_nm }}</p>
            <h3>{{ product.fin_prdt_nm }}</h3>
            <button @click="openModal(product, false)">상세 보기 ></button>
          </div>
        </div>
        <button class="expand-btn" @click="toggleSavingsExpand">
          {{ isSavingsExpanded ? "접기" : "펼치기" }}
        </button>
      </div>

      <!-- 예금 상품 리스트 -->
      <div class="interest-products">
        <h2 class="title">예금 상품 리스트</h2>
        <div v-if="!isDepositsExpanded" class="carousel-container">
          <div class="carousel" :style="{ transform: `translateY(-${currentDepositsIndex * cardHeight}px)` }">
            <div class="card" v-for="(product, index) in deposits" :key="'deposits-' + product.id">
              <p>{{ product.kor_co_nm }}</p>
              <h3>{{ product.fin_prdt_nm }}</h3>
              <button @click="openModal(product, true)">상세 보기 ></button>
            </div>
          </div>
        </div>
        <div v-else class="product-list">
          <div class="card" v-for="(product, index) in deposits" :key="'deposits-' + product.id">
            <p>{{ product.kor_co_nm }}</p>
            <h3>{{ product.fin_prdt_nm }}</h3>
            <button @click="openModal(product, true)">상세 보기 ></button>
          </div>
        </div>
        <button class="expand-btn" @click="toggleDepositsExpand">
          {{ isDepositsExpanded ? "접기" : "펼치기" }}
        </button>
      </div>
    </div>

    <!-- 예적금 금리 비교 -->
    <div class="comparison">
      <FinanceProductComparison :products="likeProducts" />
    </div>
  </div>

  <!-- Modal 부분 -->
  <v-dialog v-model="isModalVisible" width="800">
    <v-card v-if="selectedProduct" class="modal-container">
      <v-card-title class="d-flex align-center justify-space-between">
        <div>
          <div class="bank-label">{{ selectedProduct.kor_co_nm }}</div>
          <p class="product-label">{{ selectedProduct.fin_prdt_nm }}</p>
        </div>
        <button :class="['btn_like', { on: isLiked }]" @click="toggleLike(selectedProduct.fin_prdt_cd)"></button>
      </v-card-title>
      <div>
        <div class="line"></div>
        <v-table>
          <tbody>
            <tr>
              <td width="20%" class="table-title">공시 제출월</td>
              <td>{{ `${selectedProduct.dcls_month.slice(0, 4)}년 ${selectedProduct.dcls_month.slice(4, 6)}월` }}</td>
            </tr>
            <tr>
              <td width="20%" class="table-title">가입 방법</td>
              <td>{{ selectedProduct.join_way }}</td>
            </tr>
            <tr>
              <td width="20%" class="table-title">만기 후 이자율</td>
              <td>{{ selectedProduct.mtrt_int }}</td>
            </tr>
            <tr>
              <td width="20%" class="table-title">우대 조건</td>
              <td>{{ selectedProduct.spcl_cnd }}</td>
            </tr>
            <tr>
              <td width="20%" class="table-title">가입 대상</td>
              <td>{{ selectedProduct.join_member }}</td>
            </tr>
            <tr>
              <td width="20%" class="table-title">가입 제한</td>
              <td>{{ selectedProduct.join_deny === 1 ? "제한없음" : "서민전용" || "일부제한" }}</td>
            </tr>
            <tr>
              <td width="20%" class="table-title">최고 한도</td>
              <td>{{ selectedProduct.max_limit?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") || "없음" }}</td>
            </tr>
            <tr>
              <td width="20%" class="table-title">기타 유의사항</td>
              <td>{{ selectedProduct.etc_note }}</td>
            </tr>
          </tbody>
        </v-table>
      </div>
      <v-card-actions>
        <button class="close-button" @click="closeModal">닫기</button>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from "vue";
import { useAccountStore } from "@/stores/account";
import { useFinancialStore } from "@/stores/financial";
import FinanceProductComparison from "@/components/FinanceProductComparison.vue";
import axios from "axios";

const accountStore = useAccountStore();
const financialStore = useFinancialStore();

// 상태 관리 변수
const API_BASE_URL = "http://127.0.0.1:8000/api/v1/deposits";
const originalSavings = ref([]); // 원본 데이터
const originalDeposits = ref([]); // 원본 데이터
const savings = ref([]); // carousel용
const deposits = ref([]); // carousel용

const likeProducts = computed(() => {
  return [...originalSavings.value, ...originalDeposits.value];
});

const error = ref(null);

// 모달 관련 상태
const isModalVisible = ref(false);
const selectedProduct = ref(null);
const isLiked = ref(false);
const isDeposit = ref(false);

// 펼치기 상태 관리
const isSavingsExpanded = ref(false);
const isDepositsExpanded = ref(false);

// carousel 관련 상태
const cardHeight = ref(0);
const currentSavingsIndex = ref(0);
const currentDepositsIndex = ref(0);

let savingsSlideInterval = null;
let depositsSlideInterval = null;

// API 호출 함수
const fetchUserSavings = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/user/savings/`, {
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    });
    originalSavings.value = response.data;
    savings.value = [...response.data];
  } catch (err) {
    console.error("적금 데이터를 가져오는 중 오류 발생:", err);
    error.value = "적금 데이터를 가져오는 데 실패했습니다.";
  }
};

const fetchUserDeposits = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/user/deposits/`, {
      headers: {
        Authorization: `Token ${accountStore.token}`,
      },
    });
    originalDeposits.value = response.data;
    deposits.value = [...response.data];
  } catch (err) {
    console.error("예금 데이터를 가져오는 중 오류 발생:", err);
    error.value = "예금 데이터를 가져오는 데 실패했습니다.";
  }
};

// Carousel 관련 함수
const startSliders = () => {
  if (savings.value.length > 3 && !isSavingsExpanded.value) {
    savingsSlideInterval = setInterval(() => {
      slideToNext(currentSavingsIndex, savings.value);
    }, 3000);
  }

  if (deposits.value.length > 3 && !isDepositsExpanded.value) {
    depositsSlideInterval = setInterval(() => {
      slideToNext(currentDepositsIndex, deposits.value);
    }, 3000);
  }
};

const slideToNext = (currentIndex, products) => {
  if (products.length > 0) {
    const firstProduct = products.shift();
    products.push(firstProduct);
    currentIndex.value = 0;
  }
};

// 펼치기/접기 토글 함수
const toggleSavingsExpand = () => {
  isSavingsExpanded.value = !isSavingsExpanded.value;
  if (isSavingsExpanded.value && savingsSlideInterval) {
    clearInterval(savingsSlideInterval);
    savingsSlideInterval = null;
  } else if (!isSavingsExpanded.value && savings.value.length > 3) {
    savingsSlideInterval = setInterval(() => {
      slideToNext(currentSavingsIndex, savings.value);
    }, 3000);
  }
};

const toggleDepositsExpand = () => {
  isDepositsExpanded.value = !isDepositsExpanded.value;
  if (isDepositsExpanded.value && depositsSlideInterval) {
    clearInterval(depositsSlideInterval);
    depositsSlideInterval = null;
  } else if (!isDepositsExpanded.value && deposits.value.length > 3) {
    depositsSlideInterval = setInterval(() => {
      slideToNext(currentDepositsIndex, deposits.value);
    }, 3000);
  }
};

onMounted(async () => {
  await fetchUserSavings();
  await fetchUserDeposits();

  const firstCard = document.querySelector(".card");
  if (firstCard) {
    cardHeight.value = firstCard.offsetHeight + 20;
  }

  startSliders();
});

onUnmounted(() => {
  if (savingsSlideInterval) clearInterval(savingsSlideInterval);
  if (depositsSlideInterval) clearInterval(depositsSlideInterval);
});

// 모달 열기
const openModal = async (product, isD) => {
  selectedProduct.value = product;
  isModalVisible.value = true;
  isDeposit.value = isD;

  // 좋아요 상태를 서버에서 가져오기
  if (isD) {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/v1/deposits/deposit/${product.fin_prdt_cd}/contract-status/`, {
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      });
      isLiked.value = response.data.is_liked;
    } catch (error) {
      console.error("좋아요 상태 확인 오류:", error);
      isLiked.value = false;
    }
  } else {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/v1/deposits/saving/${product.fin_prdt_cd}/contract-status/`, {
        headers: {
          Authorization: `Token ${accountStore.token}`,
        },
      });
      isLiked.value = response.data.is_liked;
    } catch (error) {
      console.error("좋아요 상태 확인 오류:", error);
      isLiked.value = false;
    }
  }
};

const closeModal = () => {
  selectedProduct.value = null;
  isModalVisible.value = false;
  // 모달이 닫힐 때 데이터를 새로 불러옴
  fetchUserDeposits();
  fetchUserSavings();
};

const toggleLike = (id) => {
  isLiked.value = !isLiked.value;
  if (isDeposit.value) {
    financialStore.depositToggleLike(id);
  } else {
    financialStore.savingToggleLike(id);
  }
};
</script>

<style scoped>
.layout {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: "Pretendard", sans-serif;
}

.interest-products {
  flex: 1;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 20px;
  color: #333;
}

/* 슬라이더 */
.carousel-container {
  overflow: hidden;
  height: 400px;
}

.carousel {
  display: flex;
  flex-direction: column;
  transition: transform 0.5s ease-in-out;
}

/* 펼쳐진 상품 리스트 */
.product-list {
  max-height: 600px;
  overflow-y: auto;
  padding-right: 10px;
}

.product-list::-webkit-scrollbar {
  width: 4px;
}

.product-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.product-list::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.product-list::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* 카드 디자인 */
.card {
  background: #ffffff;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  transition: transform 0.3s ease-in-out;
  height: 120px;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.card h3 {
  font-size: 17px;
  color: #333;
  margin-bottom: 8px;
}

.card p {
  display: flex;
  justify-content: center;
  align-content: center;
  align-items: center;
  padding: 4px 12px; 
  background: #5A87F2;
  border-radius: 32px;
  color: white;
  width: auto; 
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  font-size: 11px;
  font-weight: 400;
  margin-bottom: 12px;
}

.card button {
  font-size: 12px;
}
/* 펼치기 버튼 */
.expand-btn {
  width: 100%;
  padding: 8px;
  margin-top: 10px;
  background: #f0f0f0;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.expand-btn:hover {
  background: #e0e0e0;
  transform: translateY(-2px);
}

.expand-btn:active {
  transform: translateY(0);
}

/* 예적금 금리 비교 */
.comparison {
  flex: 2;
}

/* 모달 스타일 */
.modal-container {
  padding: 40px;
}

.bank-label {
  display: inline-flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  padding: 4px 16px;
  background: #5A87F2;
  border-radius: 20px;
  font-weight: 600;
  font-size: 12px;
  color: #ffffff;
  white-space: nowrap;
}

.product-label {
  padding: 16px 2px;
  font-weight: 700;
  font-size: 24px;
  line-height: 29px;
}

.line {
  width: 100%;
  height: 2px;
  background: #e9e9e9;
}

.v-card-title {
  padding: 0px;
}

.table-title {
  padding: 0px;
  font-weight: 700;
  font-size: 16px;
  color: black;
}

.v-table > .v-table__wrapper > table > tbody > tr > td {
  padding: 12px 0px;
}

.v-table .v-table__wrapper > table > tbody > tr:not(:last-child) > td {
  border-bottom: thin solid #eceff5;
}

td {
  font-size: 14px;
}

.btn_like {
  width: 40px;
  height: 40px;
  background: url("../assets/icon/unlikes_heart.png") no-repeat center / 40px;
  cursor: pointer;
  margin: 5px;
}

.btn_like.on {
  background: url("../assets/icon/likes_heart.png") no-repeat center / 40px;
  animation: beating 0.5s 1 alternate;
}

@keyframes beating {
  0% {
    transform: scale(1);
  }
  40% {
    transform: scale(1.25);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    transform: scale(1);
  }
}

.close-button {
  display: block;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  color: #ffffff;
  background-color: #5A87F2;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s, transform 0.3s;
}

.close-button:hover {
  background-color: #3F75F2;
  transform: translateY(-2px);
}

.close-button:active {
  background-color: #3F75F2;
  transform: translateY(0);
}

/* 레이아웃 관련 추가 스타일 */
.layout-product-list {
  display: flex;
  flex-direction: column;
  flex: 1;
  gap: 20px;
}

/* 반응형 스타일 */
@media (max-width: 1200px) {
  .layout {
    flex-direction: column;
    padding: 0 20px;
  }

  .comparison {
    margin-top: 20px;
  }
}

@media (max-width: 768px) {
  .layout {
    padding: 0 10px;
  }

  .interest-products {
    padding: 10px;
  }

  .card {
    padding: 10px;
  }

  .modal-container {
    padding: 20px;
  }
}
</style>
