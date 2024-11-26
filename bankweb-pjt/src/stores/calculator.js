import { ref } from "vue";
import axios from "axios";
import { defineStore } from "pinia";

export const useCurrencyStore = defineStore("calculator", () => {
  const API_URL = "http://127.0.0.1:8000";
  const currencies = ref([]);
  const error = ref(null);
  const loading = ref(false);

  const fetchCurrencies = async function () {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get(`${API_URL}/api/v1/exchanges/`);
      console.log(response.data);
      currencies.value = response.data.data || [];
    } catch (err) {
      console.error(err);
      error.value = err.response?.data?.message || "데이터를 불러오는 데 실패했습니다.";
    } finally {
      loading.value = false;
    }
  };

  return { currencies, error, loading, fetchCurrencies };
});