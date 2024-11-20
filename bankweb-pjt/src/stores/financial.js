import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import axios from "axios";

export const useFinancialStore = defineStore("financial", () => {
    const deposits = ref([]);
    const API_URL = "http://127.0.0.1:8000";

    const router = useRouter()

    // accountStore에서 가져와야함
    // const token = accountStore.token

    // 전체 예금 조회 함수
    const getDepositDatas = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/deposits/deposit/`,
        // headers: {
        //   Authorization: `Token ${token.value}`
        // }
      })
        .then((response) => {
            deposits.value = response.data;
        })
        .catch((error) => {
          console.log("getArticles error =", error);
        });
    };

    return { deposits, getDepositDatas };
  },
  { persist: true }
);
