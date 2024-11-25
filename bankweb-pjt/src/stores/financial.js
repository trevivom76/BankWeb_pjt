import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import { useAccountStore } from "./account";
import axios from "axios";

export const useFinancialStore = defineStore(
  "financial",
  () => {
    const API_URL = "http://127.0.0.1:8000";

    const accountStore = useAccountStore();

    const deposits = ref([]);
    const savings = ref([]);
    const banks = ref([]);

    const isLiked = ref([]);

    const hasFetchedAllData = ref(false);
    const hasFetchedBanks = ref(false);

    const fetchAllData = () => {
      if (hasFetchedAllData.value) {
        return;
      }

      axios({
        method: "get",
        url: `${API_URL}/api/v1/deposits/`,
      })
        .then((res) => {
          hasFetchedAllData.value = true;
          console.log("예적금 데이터를 성공적으로 불러왔습니다.");
        })
        .catch((error) => {
          console.log("예적금 데이터 가져오기 실패 : ", error);
        });
    };

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
          console.log(res);
          savings.value = res.data;
        })
        .catch((error) => {
          console.log("적금 리스트 조회 오류 : ", error);
        });
    };

    // 은행 정보 조회
    const getBankDatas = function () {
      if (hasFetchedBanks.value) {
        return;
      }

      axios({
        method: "get",
        url: `${API_URL}/api/v1/deposits/bank_list/`,
      })
        .then((res) => {
          banks.value = res.data.banks;
          hasFetchedBanks.value = true;
          console.log("은행 지점 데이터를 성공적으로 가져왔습니다.");
        })
        .catch((error) => {
          console.log("은행 데이터 가져오기 실패 : ", error);
        });
    };

    const depositToggleLikeStatus = async (deposit_id) => {
      try {
        const response = await axios.put(
          `${API_URL}/api/v1/deposits/deposit/${deposit_id}/toggle-like/`,
          {},
          {
            headers: {
              Authorization: `Token ${accountStore.token}`, // 인증 토큰
            },
          }
        );
        return response.data.is_liked;
      } catch (error) {
        console.error("좋아요 상태 업데이트 오류:", error);
        return null;
      }
    };

    const depositToggleLike = async (deposit_id) => {
      const updatedStatus = await depositToggleLikeStatus(deposit_id);
      if (updatedStatus !== null) {
        isLiked.value = updatedStatus;
        console.log(`좋아요 상태 변경: ${isLiked.value}`);
      }
    };

    const savingToggleLikeStatus = async (saving_id) => {
      try {
        const response = await axios.put(
          `${API_URL}/api/v1/deposits/saving/${saving_id}/toggle-like/`,
          {},
          {
            headers: {
              Authorization: `Token ${accountStore.token}`, // 인증 토큰
            },
          }
        );
        return response.data.is_liked;
      } catch (error) {
        console.error("좋아요 상태 업데이트 오류:", error);
        return null;
      }
    };

    const savingToggleLike = async (saving_id) => {
      const updatedStatus = await savingToggleLikeStatus(saving_id);
      if (updatedStatus !== null) {
        isLiked.value = updatedStatus;
        console.log(`좋아요 상태 변경: ${isLiked.value}`);
      }
    };

    return {
      deposits,
      savings,
      banks,
      isLiked,
      fetchAllData,
      getDepositDatas,
      getSavingDatas,
      getBankDatas,
      depositToggleLikeStatus,
      depositToggleLike,
      savingToggleLikeStatus,
      savingToggleLike,
    };
  },
  { persist: true }
);
