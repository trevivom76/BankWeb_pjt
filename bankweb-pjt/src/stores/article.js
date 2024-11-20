import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import axios from "axios";
import { useAccountStore } from "./account";

// 로그인, 로그아웃, 회원가입 기능
export const useArticleStore = defineStore(
  "article",
  () => {
    const articles = ref([]);
    const articledetail = ref(null);
    const API_URL = "http://127.0.0.1:8000";

    const router = useRouter();
    const accountStore = useAccountStore();

    // accountStore에서 가져와야함
    const token = accountStore.token;

    // 전체 게시글 조회 함수
    const getArticles = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/articles/`,
        headers: {
          Authorization: `Token ${token}`,
        },
      })
        .then((response) => {
          console.log("게시글 작성 조회");
          articles.value = response.data;
        })
        .catch((error) => {
          console.log("getArticles error =", error);
        });
    };

    // 게시글 생성 함수
    const createArticle = function (payload) {
      const { title, content, category } = payload;

      axios({
        method: "post",
        url: `${API_URL}/api/v1/articles/create/`,
        data: {
          title,
          content,
          category,
        },
        headers: {
          Authorization: `Token ${token}`,
        },
      })
        .then((response) => {
          console.log("게시글 작성 성공");
          router.push({ name: "community" });
        })
        .catch((error) => {
          console.log("createArticle error =", error);
        });
    };

    // 게시글 detail 조회 함수
    const getArticleDetail = function (payload) {
      const { articleid } = payload;

      axios({
        method: "get",
        url: `${API_URL}/api/v1/articles/${articleid}/`,
      })
        .then((response) => {
          console.log(response);
          articledetail.value = response.data;
        })
        .catch((error) => {
          console.log("getArticleDetail error =", error);
        });
    };

    return { articles, articledetail, token, API_URL, getArticles, createArticle, getArticleDetail };
  },
  { persist: true }
);
