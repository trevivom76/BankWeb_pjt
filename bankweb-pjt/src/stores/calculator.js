import { ref } from "vue";
import axios from "axios";
import { defineStore } from "pinia";

export const useCurrencyStore = defineStore("calculator", () => {
  const API_URL = "/site/program/financial/exchangeJSON";
  const currency = ref([]);

  const usecurrency = function () {
    axios({
      method: "GET",
      url: API_URL,
      params: {
        authkey: "iz3BGWp5C1LAG1YTUjJ77xeLz7QzemWv",
        data: "AP01",
      },
    })
      .then((res) => {
        console.log(res);
        currency.value = res.data;
      })
      .catch((error) => {
        // error.value = error;
        console.log(error);
      });
  };
  return { currency, usecurrency };
});
