<template>
    <div>
        <h1>정기 예금</h1>
        <div class="select-box">
            <v-select
            clearable
            label="은행지점"
            :items="banks"
            v-model="selectedBank"
            variant="outlined"
            ></v-select>
            <v-select
            clearable
            label="예치기간"
            :items="['California', 'Colorado', 'Florida', 'Georgia', 'Texas', 'Wyoming']"
            variant="outlined"
            ></v-select>
            <v-select
            clearable
            label="이자 계산 방식"
            :items="['California', 'Colorado', 'Florida', 'Georgia', 'Texas', 'Wyoming']"
            variant="outlined"
            ></v-select>
        </div>
            <v-data-table 
            :items="depositItems" 
            :headers="headers"
            class="elevation-1"
        ></v-data-table>
    </div>
</template>

<script setup>

import { useFinancialStore } from "@/stores/financial";
import { onMounted, ref, watch } from "vue";

const financialStore = useFinancialStore();
const depositItems = ref([])
const banks = ref(['전체 은행'])
const selectedBank = ref('전체 보기')

// 테이블 헤더 설정
const headers = [
  { title: "공시 제출일", value: "공시 제출일", align: "center", sortable: true },
  { title: "금융 회사명", value: "금융 회사명", align: "center", sortable: true },
  { title: "상품명", value: "상품명", align: "center", sortable: true },
  {
    title: "개월 수에 따른 이율",
    align: "center",
    children: [
        { title: "6개월", value: "6개월 이율", align: "end", sortable: true },
        { title: "12개월", value: "12개월 이율", align: "end", sortable: true },
        { title: "24개월", value: "24개월 이율", align: "end", sortable: true },
        { title: "36개월", value: "36개월 이율", align: "end", sortable: true },
    ]
  }
];
onMounted(() => {
    financialStore.getDepositDatas();
    

     // 데이터를 감시하여 변경이 있을 때마다 처리
    watch(
        () => financialStore.deposits,
        (newDeposits) => {
        depositItems.value = []; // 초기화

        // financialStore.deposits에 접근하여 각 항목을 순회
        for (let depositData of newDeposits) {
            const terms = ["6", "12", "24", "36"];
            const interestRates = {};

            // 각 기간(6, 12, 24, 36개월)에 해당하는 옵션의 이율을 가져옴
            terms.forEach((term) => {
            const option = depositData.depositoption_set.find(
                (opt) => opt.save_trm === term
            );
            interestRates[term] = option ? option.intr_rate + "%" : ""; // 값이 있으면 이율, 없으면 빈 문자열
            });

            // depositData의 속성을 이용해 새로운 객체를 생성
            const depositItem = {
            "공시 제출일": depositData.dcls_month, // 공시 제출일
            "금융 회사명": depositData.kor_co_nm, // 금융 회사명
            "상품명": depositData.fin_prdt_nm, // 상품명
            "6개월 이율": interestRates["6"], // 6개월 이율 (없으면 빈 값)
            "12개월 이율": interestRates["12"], // 12개월 이율 (없으면 빈 값)
            "24개월 이율": interestRates["24"], // 24개월 이율 (없으면 빈 값)
            "36개월 이율": interestRates["36"], // 36개월 이율 (없으면 빈 값)
            };

            // depositItems 배열에 생성한 객체를 추가
            depositItems.value.push(depositItem);
        }
        },
        { immediate: true } // 즉시 실행
    );
});

</script>

<style scoped>

/* 테이블 높이 설정*/
.v-data-table__tr {
  height: 200px; /*외안되?*/
}

.v-data-table {
  background-color: #f9f9f9; /* 배경색 설정 */
  border-radius: 12px;
  overflow: hidden;
}

.v-data-table__th {
    border-top: 2px solid #ECEFF5 !important;
    border-bottom: 2px solid #ECEFF5 !important;
}

.select-box {
    display: flex;
    flex-direction: row;
    gap: 24px;
}
</style>