import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import axios from "axios";
import { useAccountStore } from "./account";

// 로그인, 로그아웃, 회원가입 기능
export const useArticleStore = defineStore(
  "article",
  () => {
    // let id = 1
    // { 
      //   id: id++,
      //   title: "African Elephant1",
      //   category: "Loxodonta africana1",
      //   author: "Herbivore1",
      // }
    
      
    const articles = ref([]);
    const API_URL = "http://127.0.0.1:8000";

    const router = useRouter()
    const accountStore = useAccountStore()

    // accountStore에서 가져와야함
    const token = accountStore.token

    // 전체 게시글 조회 함수
    const getArticles = function () {
      axios({
        method: "get",
        url: `${API_URL}/api/v1/articles/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
        .then((response) => {
          articles.value = response.data;
        })
        .catch((error) => {
          console.log("getArticles error =", error);
        });
    };

    // 게시글 생성 함수
    const createArticle = function (payload) {
      const { title, content, category } = payload

      axios({
        method: "post",
        url: `${API_URL}/api/v1/articles/`,
        data:{
          title, content, category
        },
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      .then((response) => {
        router.push({name: 'community'})
      })
      .catch((error) => {
        console.log("createArticle error =", error);
      });
    }

    return { articles, API_URL, getArticles, createArticle };
  },
  { persist: true }
);
