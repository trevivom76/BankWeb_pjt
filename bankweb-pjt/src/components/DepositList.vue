<template>
  <div class="finance-box">
    <h1>정기예금 <span class="color">검색하기</span></h1>
    <div class="select-box">

        <!-- 은행 지점 선택 셀 -->
        <v-select
        label="은행지점"
        :items="banks"
        v-model="selectedBank"
        variant="outlined"
        class="flex-item-bank"
        ></v-select>

        <!-- 예치 기간 선택 셀 -->
        <v-select
        label="예치기간"
        :items="['전체기간', 6, 12, 24, 36]"
        v-model="selectedDepositPeriod"
        variant="outlined"
        class="flex-item-period"
        ></v-select>

        <!-- 검색버튼 -->
        <button
        @click="clickedSearchButton"
        class="search-button">
            검색
        </button>
    </div>

    <!-- 정기 예금 테이블 -->
    <v-data-table-virtual
    :items="depositItems"
    :headers="headers"
    >
      <template #item="{ item }">
        <tr @click="openModal(item)">
          <td align="center">{{ item["공시 제출월"] }}</td>
          <td align="center">{{ item["금융 회사명"] }}</td>
          <td align="center">{{ item["금융 상품명"] }}</td>
          <td align="center">{{ item["6개월"] }}</td>
          <td align="center">{{ item["12개월"] }}</td>
          <td align="center">{{ item["24개월"] }}</td>
          <td align="center">{{ item["36개월"] }}</td>
        </tr>
      </template>
    </v-data-table-virtual>
  </div>
  <v-dialog v-model="isModalVisible" width="800">
    <v-card v-if="selectedRowItem" class="card">
      <v-card-title class="d-flex align-center justify-space-between">
        <div>
          <div class="bank-label">{{ selectedRowItem['금융 회사명'] }}</div>
          <p class="product-label">{{ selectedRowItem['금융 상품명'] }}</p>
        </div>
        <template v-if="isLoggedin">
          <button
            :class="['btn_like', { on: isLiked }]"
            @click="toggleLike(selectedRowItem['금융 상품 ID'])"
          ></button>
        </template>
      </v-card-title>
      <div>
        <div class="line"></div>
        <v-table>
          <tbody>
            <tr
            v-for="(value, key) in selectedRowItem"
            :key="key"
            >
              <template v-if="['금융 회사명', '금융 상품명', '6개월', '12개월', '24개월', '36개월', 'depositRateData', 'depositRateData2', '금융 상품 ID'].includes(key)"></template>
              <template v-else>
                <td width="20%" class="table-title">{{ key }}</td>
                <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
                <td v-else>{{ value }}</td>
              </template>
            </tr>
          </tbody>
        </v-table>
        <DepositChart 
        :intr-rate-data="selectedRowItem['depositRateData']" 
        :intr-rate2-data="selectedRowItem['depositRateData2']"/>
      </div>
      <v-card-actions>
        <button class="close-button" @click="closeModal">닫기</button>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { useFinancialStore } from "@/stores/financial";
import { useAccountStore } from "@/stores/account";
import { onMounted, ref, watch } from "vue";
import DepositChart from "@/components/DepositChart.vue";
import axios from "axios";

const financialStore = useFinancialStore();
const accountStore = useAccountStore();

const depositItems = ref([]);                  // 전체 예금 정보
const banks = ref(["전체은행"]);                // 전체 은행 정보
const selectedBank = ref("전체은행");           // 필터링을 위한 은행 정보
const selectedDepositPeriod = ref("전체기간");  // 필터링을 위한 예치 기간

const selectedRowItem = ref(null) // 예금 리스트에서 선택된 예금 데이터

const isModalVisible = ref(false) // 모달창 활성화 여부
const isLiked = ref(false)        // 예금상품 관심항목으로 등록 여부
const isLoggedin = ref(false)     // 로그인 여부


onMounted(() => {
  financialStore.getDepositDatas();
  financialStore.getBankDatas();

  banks.value.push(...financialStore.banks);
  
  // 로그인 여부 확인
  isLoggedin.value = accountStore.isLogin

  watch(
    () => financialStore.deposits,
    (newDeposits) => {
      depositItems.value = newDeposits.map(mapDepositData);
    },
    { immediate: true }
  );
});


// 테이블 헤더 설정
const headers = [
  { title: "공시 제출월", value: "공시 제출월", align: "center", width: "15%", sortable: true },
  { title: "금융 회사명", value: "금융 회사명", align: "center", width: "20%", sortable: true },
  { title: "금융 상품명", value: "금융 상품명", align: "center", sortable: true },
  { title: "6개월", value: "6개월", align: "center", width: "12%", sortable: true },
  { title: "12개월", value: "12개월", align: "center", width: "12%", sortable: true },
  { title: "24개월", value: "24개월", align: "center", width: "12%", sortable: true },
  { title: "36개월", value: "36개월", align: "center", width: "12%", sortable: true },
];


// 예금 데이터 생성
const mapDepositData = (deposit) => {
  const terms = ["6", "12", "24", "36"];
  const interestRates = {};
  const depositRateData = Array(terms.length).fill(0);
  const depositRateData2 = Array(terms.length).fill(0);

  // 각 예치 기간에 대해 금리 데이터를 처리
  for (const term of terms) {
    const option = deposit.depositoption_set.find((opt) => opt.save_trm === term);
    interestRates[term] = option ? `${option.intr_rate || 0}%` : "";
    const index = terms.indexOf(term);
    depositRateData[index] = option?.intr_rate || 0;
    depositRateData2[index] = option?.intr_rate2 || 0;
  }

  const formattedDate = deposit.dcls_month
    ? `${deposit.dcls_month.slice(0, 4)}년 ${deposit.dcls_month.slice(4, 6)}월`
    : "";

  const formattedJoinDen = {
    1: "제한없음",
    2: "서민전용",
  }[deposit.join_den] || "일부제한";

  return {
    "공시 제출월": formattedDate,
    "금융 회사명": deposit.kor_co_nm,
    "금융 상품명": deposit.fin_prdt_nm,
    "가입 방법": deposit.join_way,
    "만기 후 이자율": deposit.mtrt_int,
    "우대 조건": deposit.spcl_cnd,
    "가입 대상": deposit.join_member,
    "가입 제한": formattedJoinDen,
    "최고 한도": deposit.max_limit,
    "기타 유의사항": deposit.etc_note,
    "6개월": interestRates["6"],
    "12개월": interestRates["12"],
    "24개월": interestRates["24"],
    "36개월": interestRates["36"],
    "금융 상품 ID": deposit.fin_prdt_cd,
    depositRateData: depositRateData,
    depositRateData2: depositRateData2,
  };
};


// 검색 데이터에 따른 데이터 필터링
const clickedSearchButton = async () => {
  await financialStore.getDepositDatas(); 
  depositItems.value = financialStore.deposits
    .filter((deposit) => {
      const matchesBank =
        selectedBank.value === "전체은행" || deposit.kor_co_nm === selectedBank.value;

      const matchesDepositPeriod =
        selectedDepositPeriod.value === "전체기간" ||
        deposit.depositoption_set.some((option) => option.save_trm === String(selectedDepositPeriod.value));

      return matchesBank && matchesDepositPeriod;
    })
    .map(mapDepositData);
};


// 모달창 띄우기
const openModal = async function (item) {
  selectedRowItem.value = item
  isModalVisible.value = true

  // 좋아요 상태를 서버에서 가져오기
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/v1/deposits/deposit/${item["금융 상품 ID"]}/contract-status/`, {
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


// 모달창 닫기
const closeModal = function (){
  isModalVisible.value = false
}


// 좋아요 버튼
const toggleLike = (depositID) => {
  isLiked.value = !isLiked.value;
  financialStore.depositToggleLike(depositID)
};

</script>


<style scoped>
h1 {
  font-size: 24px;
  font-weight: bold;
  
  padding: 0px 0px 24px 40px;
}

.color {
  color: #0B5BCB;
}

.select-box {
  display: flex;
  flex-direction: row;
  padding: 0px 40px;
  gap: 24px;
}

.finance-box {
  background-color: white;
  padding: 24px 0px;
  border-radius: 0px 0px 20px 20px;
}

.flex-item-bank{
  flex: 0 0 40%;
}

.flex-item-period{
  flex: 0 0 20%;
}

.search-button {
  flex: 0 0 15%;
  padding: 12px;
  background-color: #0B5BCB;
  color: white;
  border-radius: 8px;
  font-weight: 800;
  font-size: 14px;
  margin-bottom: 23px;
  transition: background-color 0.3s, color 0.3s, box-shadow 0.3s, transform 0.3s;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.search-button:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
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