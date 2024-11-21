import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import axios from "axios";

export const useFinancialStore = defineStore("financial", () => {
    const API_URL = "http://127.0.0.1:8000";
    const deposits = ref([]);
    const savings = ref([]);
    const banks = ref([]);

    // 전체 예금 조회 함수
    const getDepositDatas = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/deposits/deposit/`,
      })
        .then((res) => {
            deposits.value = res.data;
        })
        .catch((error) => {
          console.log("예금 리스트 조회 오류 : ", error);
        });
    };

    // 전체 적금 조회 함수
    const getSavingDatas = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/deposits/saving/`,
      })
        .then((res) => {
          console.log(res)
          savings.value = res.data;
        })
        .catch((error) => {
          console.log("적금 리스트 조회 오류 : ", error);
        });
    };
    
    // 은행 정보 조회
    const getBankDatas = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/deposits/bank_list/`
      })
        .then((res) => {
          console.log('은행 데이터', res.data.banks)
          banks.value = res.data.banks
        })
        .catch((error) => {
          console.log("은행 데이터 조회 오류 : ", error);
        });
    }

    return { 
      deposits, 
      savings, 
      banks, 
      getDepositDatas, 
      getSavingDatas, 
      getBankDatas 
    };
  },
  { persist: true }
);

