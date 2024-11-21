<template>
    <div class="finance-box">
        <h1>정기적금 <span class="color">검색하기</span></h1>
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
        
        <!-- 정기 적금 테이블 -->
        <v-data-table-virtual
        :items="savingItems" 
        :headers="headers"
        >
          <template #item="{ item }">
            <tr @click="openModal(item)">
              <td align="center">{{ item["공시 제출월"] }}</td>
              <td align="center">{{ item["금융 회사명"] }}</td>
              <td align="center">{{ item["금융 상품명"] }}</td>
              <td align="center">{{ item["6개월 자유"] }}</td>
              <td align="center">{{ item["6개월 정액"] }}</td>
              <td align="center">{{ item["12개월 자유"] }}</td>
              <td align="center">{{ item["12개월 정액"] }}</td>
              <td align="center">{{ item["24개월 자유"] }}</td>
              <td align="center">{{ item["24개월 정액"] }}</td>
              <td align="center">{{ item["36개월 자유"] }}</td>
              <td align="center">{{ item["36개월 정액"] }}</td>
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
        <button
          :class="['btn_like', { on: isLiked }]"
          @click="toggleLike"
        ></button>
      </v-card-title>
      <div>
        <div class="line"></div>
        <v-table>
          <tbody>
            <tr
            v-for="(value, key) in selectedRowItem"
            :key="key"
            >
              <template v-if="['금융 회사명', '금융 상품명', '6개월 자유', '6개월 정액', '12개월 자유','12개월 정액', '24개월 자유','24개월 정액', '36개월 자유','36개월 정액', 'freeSavingData', 'freeSavingData2','freeSavingData3','fixedSavingData','fixedSavingData2','fixedSavingData3'].includes(key)"></template>
              <template v-else>
                <td width="20%" class="table-title">{{ key }}</td>
                <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
                <td v-else>{{ value }}</td>
              </template>
            </tr>
          </tbody>
        </v-table>
        <SavingChart 
        :free-saving-data="selectedRowItem['freeSavingData']" 
        :free-saving-data2="selectedRowItem['freeSavingData2']"
        :free-saving-data3="selectedRowItem['freeSavingData3']"
        :fixed-saving-data="selectedRowItem['fixedSavingData']"
        :fixed-saving-data2="selectedRowItem['fixedSavingData2']"
        :fixed-saving-data3="selectedRowItem['fixedSavingData3']"
        />
      </div>
      <v-card-actions>
        <button class="close-button" @click="closeModal">닫기</button>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { useFinancialStore } from "@/stores/financial";
import { onMounted, ref, watch } from "vue";
import SavingChart from "./SavingChart.vue";

const financialStore = useFinancialStore();
const savingItems = ref([]);
const banks = ref(["전체은행"]);
const selectedBank = ref("전체은행");
const selectedDepositPeriod = ref("전체기간");

const isModalVisible = ref(false)
const selectedRowItem = ref(null)
const isLiked = ref(false)


// 테이블 헤더 설정
const headers = [
  { title: "공시 제출월", value: "공시 제출월", align: "center", width: "15%", sortable: true },
  { title: "금융 회사명", value: "금융 회사명", align: "center", width: "20%", sortable: true },
  { title: "금융 상품명", value: "금융 상품명", align: "center", sortable: true },
  {
    title: "6개월", align: "center", width: "12%", children: [
      { title: "자유", align: "center", width: "6%", value: "6개월 자유" },
      { title: "정액", align: "center", width:"6%", value:"6개월 정액"},
    ]
  },
  {
    title: "12개월", align: "center", width: "12%", children: [
      { title: "자유", align: "center", width: "6%", value: "12개월 자유" },
      { title: "정액", align: "center", width:"6%", value:"12개월 정액"},
    ]
  },
  {
    title: "24개월", align: "center", width: "12%", children: [
      { title: "자유", align: "center", width: "6%", value: "24개월 자유" },
      { title: "정액", align: "center", width:"6%", value:"24개월 정액"},
    ]
  },
  {
    title: "36개월", align: "center", width: "12%", children: [
      { title: "자유", align: "center", width: "6%", value: "36개월 자유" },
      { title: "정액", align: "center", width:"6%", value:"36개월 정액"},
    ]
  },
];


// 이율 데이터를 생성하는 유틸리티 함수
const mapSavingData = (saving) => {
  const terms = ["6", "12", "24", "36"];
  const interestRates = {};
  const freeSavingData = Array(terms.length).fill(0); // [0, 0, 0, 0]
  const freeSavingData2 = Array(terms.length).fill(0); // [0, 0, 0, 0]
  const freeSavingData3 = Array(terms.length).fill(0); // [0, 0, 0, 0]
  const fixedSavingData = Array(terms.length).fill(0); // [0, 0, 0, 0]
  const fixedSavingData2 = Array(terms.length).fill(0); // [0, 0, 0, 0]
  const fixedSavingData3 = Array(terms.length).fill(0); // [0, 0, 0, 0]


  // 각 예치 기간별 데이터 처리
  terms.forEach((term, index) => {
    // 해당 기간의 옵션 필터링
    const options = saving.savingoption_set.filter((opt) => opt.save_trm === term);

    // 초기화: 해당 예치 기간에 대해 자유적립식/정액적립식 구분
    interestRates[term] = { 자유적립식: "", 정액적립식: "" };

    options.forEach((option) => {
      const type = option.rsrv_type_nm; // 자유적립식 or 정액적립식

      if (type === "자유적립식") {
        // 자유적립식 데이터 저장
        interestRates[term]["자유적립식"] = `${option.intr_rate || 0}%`;
        freeSavingData[index] = option.intr_rate || 0;
        freeSavingData2[index] = option.intr_rate2 || 0;
        freeSavingData3[index] = (freeSavingData[index] + freeSavingData2[index]) / 2.0;
      } else if (type === "정액적립식") {
        // 정액적립식 데이터 저장
        interestRates[term]["정액적립식"] = `${option.intr_rate || 0}%`;
        fixedSavingData[index] = option.intr_rate || 0;
        fixedSavingData2[index] = option.intr_rate2 || 0;
        fixedSavingData3[index] = (fixedSavingData[index] + fixedSavingData2[index]) / 2.0;
      }
    });
  });

  const formattedDate = saving.dcls_month
    ? `${saving.dcls_month.slice(0, 4)}년 ${saving.dcls_month.slice(4, 6)}월`
    : "";

  const formattedJoinDen = {
    1: "제한없음",
    2: "서민전용",
  }[saving.join_den] || "일부제한";

  return {
    "공시 제출월": formattedDate,
    "금융 회사명": saving.kor_co_nm,
    "금융 상품명": saving.fin_prdt_nm,
    "가입 방법": saving.join_way,
    "만기 후 이자율": saving.mtrt_int,
    "우대 조건": saving.spcl_cnd,
    "가입 대상": saving.join_member,
    "가입 제한": formattedJoinDen,
    "최고 한도": saving.max_limit,
    "기타 유의사항": saving.etc_note,
    "6개월 자유": `${interestRates["6"]["자유적립식"] || "-"}`,
    "6개월 정액": `${interestRates["6"]["정액적립식"] || "-"}`,
    "12개월 자유": `${interestRates["12"]["자유적립식"] || "-"}`,
    "12개월 정액": `${interestRates["12"]["정액적립식"] || "-"}`,
    "24개월 자유": `${interestRates["24"]["자유적립식"] || "-"}`,
    "24개월 정액": `${interestRates["24"]["정액적립식"] || "-"}`,
    "36개월 자유": `${interestRates["36"]["자유적립식"] || "-"}`,
    "36개월 정액": `${interestRates["36"]["정액적립식"] || "-"}`,
    freeSavingData,
    freeSavingData2,
    freeSavingData3,
    fixedSavingData,
    fixedSavingData2,
    fixedSavingData3,
  };
};


// 검색 데이터에 따른 데이터 필터링
const clickedSearchButton = () => {
    savingItems.value = financialStore.savings
    .filter((saving) => {
      const matchesBank =
        selectedBank.value === "전체은행" || saving.kor_co_nm === selectedBank.value;

      const matchesDepositPeriod =
        selectedDepositPeriod.value === "전체기간" ||
        saving.depositoption_set.some((option) => option.save_trm === String(selectedDepositPeriod.value));

      return matchesBank && matchesDepositPeriod;
    })
    .map(mapSavingData);
};


// 모달창 띄우기
const openModal = function (item) {
  selectedRowItem.value = item
  isModalVisible.value = true
}


// 모달창 닫기
const closeModal = function () {
  isModalVisible.value = false
}


// 좋아요 버튼
const toggleLike = () => {
  isLiked.value = !isLiked.value;
  console.log("좋아요 상태:", isLiked.value);
};


onMounted(() => {
  financialStore.getSavingDatas();
  financialStore.getBankDatas();

  banks.value.push(...financialStore.banks);

  watch(
    () => financialStore.savings,
    (newSavings) => {
      savingItems.value = newSavings.map(mapSavingData);
    },
    { immediate: true }
  );
});

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