<template>
  <div class="interest-products">
    <h1>관심 상품 리스트</h1>

    <!-- 적금 상품 -->
    <div v-if="savings.length > 0" class="savings">
      <h2>적금 상품</h2>
      <ul>
        <li 
        v-for="saving in savings" 
        :key="saving.id"
        @click="openModal(saving, false)"
        class="clickable-item"
        >
          <strong>{{ saving.fin_prdt_nm }}</strong> ({{ saving.kor_co_nm }})<br />
          - 최대 한도: {{ saving.max_limit || '제한 없음' }}<br />
          - 우대 조건: {{ saving.spcl_cnd || '없음' }}
        </li>
      </ul>
    </div>
    <div v-else>
      <p>관심 있는 적금 상품이 없습니다.</p>
    </div>

    <!-- 예금 상품 -->
    <div v-if="deposits.length > 0" class="deposits">
      <h2>예금 상품</h2>
      <ul>
        <li 
        v-for="deposit in deposits"
        :key="deposit.id"
        @click="openModal(deposit, true)"
        >
          <strong>{{ deposit.fin_prdt_nm }}</strong> ({{ deposit.kor_co_nm }})<br />
          - 최대 한도: {{ deposit.max_limit || '제한 없음' }}<br />
          - 우대 조건: {{ deposit.spcl_cnd || '없음' }}
        </li>
      </ul>
    </div>
    <div v-else>
      <p>관심 있는 예금 상품이 없습니다.</p>
    </div>
  </div>
  <v-dialog v-model="isModalVisible" width="800">
    <v-card v-if="selectedProduct" class="card">
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
        <!-- <DepositChart 
        :intr-rate-data="selectedRowItem['depositRateData']" 
        :intr-rate2-data="selectedRowItem['depositRateData2']"/> -->
      </div>
      <v-card-actions>
        <button class="close-button" @click="closeModal">닫기</button>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAccountStore } from '@/stores/account';
import { useFinancialStore } from '@/stores/financial';
import axios from 'axios';

const accountStore = useAccountStore()
const financialStore = useFinancialStore()

// 상태 관리 변수
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1/deposits'; // Django API 기본 URL
const savings = ref([]); // 적금 상품 리스트
const deposits = ref([]); // 예금 상품 리스트
const error = ref(null); // 오류 메시지

// 모달 관련 상태
const isModalVisible = ref(false); // 모달 상태
const selectedProduct = ref(null); // 선택된 상품 정보

const isLiked = ref(false)
const isDeposit = ref(false)

const comparisonResults = ref([])

// 컴포넌트가 마운트될 때 API 호출
onMounted(async () => {
  await fetchUserSavings();
  await fetchUserDeposits();
  compareRates()
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


// 모달 닫기
const closeModal = () => {
  selectedProduct.value = null;
  isModalVisible.value = false;
  fetchUserDeposits();
  fetchUserSavings();
};


// 좋아요 버튼
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
.interest-products {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.savings, .deposits {
  margin-bottom: 20px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.error {
  color: red;
  font-weight: bold;
  margin-top: 20px;
}

.card {
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
