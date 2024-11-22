<template>
  <div class="layout">
    <div class="layout-product-list">
      <!-- 적금 상품 리스트 -->
      <div class="interest-products">
        <h2 class="title">적금 상품 리스트</h2>
        <div class="carousel-container">
          <div
            class="carousel"
            :style="{ transform: `translateY(-${currentSavingsIndex * cardHeight}px)` }"
          >
            <div
              class="card"
              v-for="(product, index) in savings"
              :key="'savings-' + product.id"
            >
              <h3>{{ product.fin_prdt_nm }}</h3>
              <p>{{ product.kor_co_nm }}</p>
              <button class="detail-btn" @click="openModal(product, false)">
                상세 보기
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 예금 상품 리스트 -->
      <div class="interest-products">
        <h2 class="title">예금 상품 리스트</h2>
        <div class="carousel-container">
          <div
            class="carousel"
            :style="{ transform: `translateY(-${currentDepositsIndex * cardHeight}px)` }"
          >
            <div
              class="card"
              v-for="(product, index) in deposits"
              :key="'deposits-' + product.id"
            >
              <h3>{{ product.fin_prdt_nm }}</h3>
              <p>{{ product.kor_co_nm }}</p>
              <button class="detail-btn" @click="openModal(product, true)">
                상세 보기
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 예적금 금리 비교 (슬라이드 애니메이션 적용 안됨) -->
    <div class="comparison">
      <FinanceProductComparison :products="likeProducts" />
    </div>
  </div>

  <v-dialog v-model="isModalVisible" width="800">
    <v-card v-if="selectedProduct" class="modal-container">
      <v-card-title class="d-flex align-center justify-space-between">
        <div>
          <div class="bank-label">{{ selectedProduct.kor_co_nm }}</div>
          <p class="product-label">{{ selectedProduct.fin_prdt_nm }}</p>
        </div>
        <button
          :class="['btn_like', { on: isLiked }]"
          @click="toggleLike( selectedProduct.fin_prdt_cd )"
        ></button>
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
import { ref, onMounted, computed, onUnmounted } from 'vue';
import { useAccountStore } from '@/stores/account';
import { useFinancialStore } from '@/stores/financial';
import FinanceProductComparison from '@/components/FinanceProductComparison.vue'
import axios from 'axios';

const accountStore = useAccountStore()
const financialStore = useFinancialStore()

// 상태 관리 변수
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1/deposits'; // Django API 기본 URL
const savings = ref([]); // 적금 상품 리스트
const deposits = ref([]); // 예금 상품 리스트
const likeProducts = computed(() => [...savings.value, ...deposits.value]);
const error = ref(null); // 오류 메시지

// 모달 관련 상태
const isModalVisible = ref(false); // 모달 상태
const selectedProduct = ref(null); // 선택된 상품 정보

const isLiked = ref(false)
const isDeposit = ref(false)

// 현재 페이지와 페이지당 카드 수 관리
const cardHeight = ref(0); // 카드 하나의 높이
const currentSavingsIndex = ref(0); // 적금 리스트 슬라이더의 현재 인덱스
const currentDepositsIndex = ref(0); // 예금 리스트 슬라이더의 현재 인덱스

let savingsSlideInterval = null;
let depositsSlideInterval = null;

// 컴포넌트가 마운트될 때 API 호출
onMounted(async () => {
  await fetchUserSavings();
  await fetchUserDeposits();

  const firstCard = document.querySelector(".card");
  if (firstCard) {
    cardHeight.value = firstCard.offsetHeight + 20; // 카드 높이 + 간격
  }

  // 적금 슬라이더 시작 (적금 상품이 3개 이상일 경우에만 애니메이션 시작)
  if (savings.value.length > 3) {
    savingsSlideInterval = setInterval(() => {
      slideToNext(currentSavingsIndex, savings.value);
    }, 3000); // 3초 간격
  }

  // 예금 슬라이더 시작 (예금 상품이 3개 이상일 경우에만 애니메이션 시작)
  if (deposits.value.length > 3) {
    depositsSlideInterval = setInterval(() => {
      slideToNext(currentDepositsIndex, deposits.value);
    }, 3000); // 3초 간격
  }
});

// 슬라이더 동작
const slideToNext = (currentIndex, products) => {
  if (products.length > 0) {
    const firstProduct = products.shift(); // 첫 번째 카드 제거
    products.push(firstProduct); // 맨 뒤로 추가
    currentIndex.value = 0; // transform 초기화
  }
};

// 슬라이더 정지 (컴포넌트가 사라질 때)
onUnmounted(() => {
  if (savingsSlideInterval) clearInterval(savingsSlideInterval);
  if (depositsSlideInterval) clearInterval(depositsSlideInterval);
});

// API 호출 함수
const fetchUserSavings = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/user/savings/`, {
      headers: {
        Authorization: `Token ${accountStore.token}`, // JWT 토큰 추가
      },
    });
    savings.value = response.data;
  } catch (err) {
    console.error('적금 데이터를 가져오는 중 오류 발생:', err);
    error.value = '적금 데이터를 가져오는 데 실패했습니다.';
  }
};

const fetchUserDeposits = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/user/deposits/`, {
      headers: {
        Authorization: `Token ${accountStore.token}`, // JWT 토큰 추가
      },
    });
    deposits.value = response.data;
  } catch (err) {
    console.error('예금 데이터를 가져오는 중 오류 발생:', err);
    error.value = '예금 데이터를 가져오는 데 실패했습니다.';
  }
};

// 모달 열기
const openModal = async (product, isD) => {
  selectedProduct.value = product;
  isModalVisible.value = true;

  isDeposit.value = isD

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
  fetchUserDeposits();
  fetchUserSavings();
};

const toggleLike = (id) => {
  isLiked.value = !isLiked.value;
  if (isDeposit.value) {
    financialStore.depositToggleLike(id)
  } else {
    financialStore.savingToggleLike(id)
  }
};
</script>

<style scoped>
/* 전체 레이아웃 */
.layout {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Pretendard', sans-serif;
}

/* 관심 상품 리스트 */
.interest-products {
  flex: 1;
  padding: 15px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #333; /* 짙은 회색 텍스트 */
}

/* 슬라이더 */
.carousel-container {
  overflow: hidden;
  height: 300px; /* 카드 3개까지만 보이도록 고정 높이 설정 */
}

.carousel {
  display: flex;
  flex-direction: column;
  transition: transform 0.5s ease-in-out;
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
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1); /* 마우스 오버 시 그림자 강조 */
}

.card h3 {
  font-size: 16px;
  color: #333;
  margin-bottom: 8px;
}

.card p {
  font-size: 12px;
  color: #777;
  margin-bottom: 10px;
}

.detail-btn {
  padding: 8px 12px;
  background: #007bff; /* 파란색 버튼 */
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.detail-btn:hover {
  background: #0056b3; /* 버튼 색상 변화 */
}

/* '상품이 없음' 메시지 */
.no-carousel {
  font-size: 12px;
  color: #999;
  text-align: center;
}

/* 예적금 금리 비교 */
.comparison {
  flex: 2;
  padding: 15px;
  background: #f9f9f9; /* 밝은 회색 배경 */
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.comparison .title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #333;
}

/* 예적금 금리 비교 내부 */
.comparison > div {
  margin-top: 20px;
}

/* 슬라이더 슬라이드 동작 */
.carousel-container {
  position: relative;
}

.carousel {
  display: flex;
  flex-direction: column;
  transition: transform 0.5s ease-in-out;
}

/* 버튼 및 카드 레이아웃 */
.layout .interest-products .carousel-container {
  margin-bottom: 20px;
}

/* 예적금 금리 비교 하위 컴포넌트 */
.interest-products + .interest-products {
  margin-top: 20px;
}


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

  background: #0B5BCB;  
  border-radius: 20px;  

  font-weight: 600;
  font-size: 12px;

  color: #FFFFFF;
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
  background: #E9E9E9;
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
  border-bottom: thin solid #ECEFF5;
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
  animation: beating .5s 1 alternate;
}

@keyframes beating {
  0% {transform: scale(1);}
  40% {transform: scale(1.25);}
  70% {transform: scale(0.9);}
  100% {transform: scale(1);}
}

.close-button {
  display: block;
  padding: 10px 20px; 
  font-size: 16px;
  font-weight: bold; 
  color: #ffffff;
  background-color: #0b5bcb;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s, transform 0.3s;
}

.close-button:hover {
  background-color: #004a9f;
  transform: translateY(-2px);
}

.close-button:active {
  background-color: #003a7e;
  transform: translateY(0);
}
</style>
