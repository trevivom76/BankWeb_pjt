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
          <tr @click="handleRowClick(item)">
            <td>{{ item.공시제출일 }}</td>
            <td>{{ item.금융회사명 }}</td>
            <td>{{ item.상품명 }}</td>
            <td>{{ item["6개월"] }}</td>
            <td>{{ item["12개월"] }}</td>
            <td>{{ item["24개월"] }}</td>
            <td>{{ item["36개월"] }}</td>
          </tr>
        </template>
        </v-data-table-virtual>
    </div>
    <InterestDetailModal 
    :depositItem="selectedRowItem"
    v-model="isModalVisible"
    />
</template>

<script setup>
import { useFinancialStore } from "@/stores/financial";
import { onMounted, ref, watch } from "vue";
import InterestDetailModal from "@/components/InterestDetailModal.vue";

const financialStore = useFinancialStore();
const depositItems = ref([]);
const banks = ref(["전체은행"]);
const selectedBank = ref("전체은행");
const selectedDepositPeriod = ref("전체기간");

const selectedRowItem = ref(null)
const isModalVisible = ref(false)

// 테이블 헤더 설정
const headers = [
  { title: "공시제출일", value: "공시제출일", align: "center", width: "15%", sortable: true },
  { title: "금융회사명", value: "금융회사명", align: "center", width: "20%", sortable: true },
  { title: "상품명", value: "상품명", align: "center", sortable: true },
  { title: "6개월", value: "6개월", align: "end", width: "12%", sortable: true },
  { title: "12개월", value: "12개월", align: "end", width: "12%", sortable: true },
  { title: "24개월", value: "24개월", align: "end", width: "12%", sortable: true },
  { title: "36개월", value: "36개월", align: "end", width: "12%", sortable: true },
];

// 이율 데이터를 생성하는 유틸리티 함수
const mapDepositData = (deposit) => {
  const terms = ["6", "12", "24", "36"];
  const interestRates = terms.reduce((rates, term) => {
    const option = deposit.depositoption_set.find((opt) => opt.save_trm === term);
    rates[term] = option ? option.intr_rate + "%" : "";
    return rates;
  }, {});
  const formattedDate = deposit.dcls_month
    ? `${deposit.dcls_month.slice(0, 4)}년 ${deposit.dcls_month.slice(4, 6)}월`
    : "";

  return {
    "공시제출일": formattedDate,
    "금융회사명": deposit.kor_co_nm,
    "상품명": deposit.fin_prdt_nm,
    "6개월": interestRates["6"],
    "12개월": interestRates["12"],
    "24개월": interestRates["24"],
    "36개월": interestRates["36"],
    allDepositData:deposit,
  };
};

// 검색 데이터에 따른 데이터 필터링
const clickedSearchButton = () => {
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


// 각 테이블의 row 클릭시 팝업창 띄우기
const handleRowClick = function (item) {
  selectedRowItem.value = item.allDepositData
  isModalVisible.value = true
  console.log(isModalVisible.value)
}

onMounted(() => {
  financialStore.getDepositDatas();
  financialStore.getBankDatas();

  banks.value.push(...financialStore.banks);

  watch(
    () => financialStore.deposits,
    (newDeposits) => {
      depositItems.value = newDeposits.map(mapDepositData);
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

/*아래 잘 안됨..*/
.custom-select .v-input__control {
  border-color: #0B5BCB; /* 테두리 색상 변경 */
  border-width: 2px; /* 테두리 두께 변경 */
  border-radius: 12px; /* 테두리 둥글기 변경 */
}

.custom-select .v-select__selections {
  height: 40px; /* 셀 높이 변경 */
  padding: 8px 12px; /* 내부 여백 조정 */
}

</style>