import { ref } from "vue";
import axios from "axios";
import { defineStore } from "pinia";

export const useCurrencyStore = defineStore("calculator", () => {
  const API_URL = "http://127.0.0.1:8000";
  const currency = ref([]);

  const usecurrency = function () {
    axios({
      method: "GET",
      url: `${API_URL}/api/v1/exchanges/`,
    })
      .then((res) => {
        console.log(res.data);
        currency.value = res.data;
      })
      .catch((error) => {
        console.log(error);
      });
  };
  return { currency, usecurrency };
});
