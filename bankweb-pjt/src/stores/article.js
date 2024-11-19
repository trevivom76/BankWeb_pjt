import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import axios from "axios";

// 로그인, 로그아웃, 회원가입 기능
export const useArticleStore = defineStore(
  "article",
  () => {
    const articles = ref([
      {
        name: "African Elephant1",
        species: "Loxodonta africana",
        diet: "Herbivore",
        habitat: "Savanna, Forests",
      },
      {
        name: "African Elephant2",
        species: "Loxodonta africana",
        diet: "Herbivore",
        habitat: "Savanna, Forests",
      },
      {
        name: "African Elephant3",
        species: "Loxodonta africana",
        diet: "Herbivore",
        habitat: "Savanna, Forests",
      },
    ]);

    const API_URL = "http://127.0.0.1:8000";

    // 게시글 조회
    const getArticles = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/articles/`,
      })
        .then((response) => {
          articles.value = response.data;
        })
        .catch((error) => {
          console.log("getArticles error =", error);
        });
    };

    return { articles, getArticles };
  },
  { persist: true }
);
