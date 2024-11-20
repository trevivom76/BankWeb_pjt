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
    const comments = ref([]);

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

    // 단일 게시글 조회 함수
    const getArticleDetail = function (payload) {
      const { articleid } = payload;
      axios({
        method: "get",
        url: `${API_URL}/api/v1/articles/${articleid}/`,
      })
        .then((response) => {
          console.log("단일 게시글 조회 성공");
          articledetail.value = response.data;
        })
        .catch((error) => {
          console.log("getArticleDetail error =", error);
        });
    };

    // 게시글 삭제 함수
    const deleteArticle = function (payload) {
      const { articleid } = payload;
      axios({
        method: "delete",
        url: `${API_URL}/api/v1/articles/${articleid}/`,
        headers: {
          Authorization: `Token ${token}`,
        },
      })
        .then((response) => {
          console.log("게시글 삭제 성공");
          const index = articles.value.findIndex((article) => articleid == article.id)
          articles.value.splice( index ,1);
          router.push({ name: "community" });
        })
        .catch((error) => {
          console.log("deleteArticle error =", error);
        });
    };

    // 댓글 생성
    const createComment = async (payload) => {
    const { content, articleid } = payload;

    try {
      const response = await axios.post(`${API_URL}/api/v1/articles/${articleid}/create_comment/`, { content },
      {
        headers: {
          Authorization: `Token ${token}`,
        }
      });
      comments.value.push(response.data); // 서버에서 받은 댓글을 바로 추가
    } catch (error) {
      console.error("createComment error:", error);
    }
  };

  // 댓글 조회
  const getComments = async (payload) => {
    const { articleid } = payload;

    try {
      const response = await axios.get(`${API_URL}/api/v1/articles/${articleid}/comment_list/`,
        {
          headers: {
            Authorization: `Token ${token}`,
          }
        }
      );
      comments.value = response.data; // 댓글 리스트를 갱신
    } catch (error) {
      console.error("getComments error:", error);
    }
  };
  
  // 댓글 삭제
  const deleteComments = async (payload) => {
    const { articleid, commentid } = payload;

    try {
      const response = await axios.delete(`${API_URL}/api/v1/articles/${articleid}/comment/${commentid}/`,
        {
          headers: {
            Authorization: `Token ${token}`,
          }
        }
      );
      const index = comments.value.findIndex((comment) => commentid == comment.id)
      comments.value.splice( index ,1);
    } catch (error) {
      console.error("deleteComments error:", error);
    }
  };

    return { 
      articles,
      articledetail,
      comments,
      token,
      API_URL,
      getArticles,
      createArticle,
      getArticleDetail,
      deleteArticle,
      createComment,
      getComments,
      deleteComments
    };
  },
  { persist: true }
);
