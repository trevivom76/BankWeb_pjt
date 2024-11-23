import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import axios from "@/apis";
import { useAccountStore } from "./account";

export const useArticleStore = defineStore(
  "article",
  () => {
    const articles = ref([]);
    const articledetail = ref(null);
    const comments = ref([]);

    const router = useRouter();
    const accountStore = useAccountStore();

    // 전체 게시글 조회 함수
    const getArticles = function () {
      axios({
        method: "get",
        url: `/api/v1/articles/`,
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
        url: `/api/v1/articles/create/`,
        data: {
          title,
          content,
          category,
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
    const getArticleDetail = async function (payload) {
      const { articleid } = payload;
      try {
        const response = await axios({
          method: "get",
          url: `/api/v1/articles/${articleid}/`,
        });
        console.log("단일 게시글 조회 성공");
        articledetail.value = response.data;
        return response.data; // 데이터 반환 추가
      } catch (error) {
        console.log("getArticleDetail error =", error);
        throw error;
      }
    };

    // 게시글 삭제 함수
    const deleteArticle = function (payload) {
      const { articleid } = payload;
      axios({
        method: "delete",
        url: `/api/v1/articles/${articleid}/`,
      })
        .then((response) => {
          console.log("게시글 삭제 성공");
          const index = articles.value.findIndex((article) => articleid == article.id);
          articles.value.splice(index, 1);
          router.push({ name: "community" });
        })
        .catch((error) => {
          console.log("deleteArticle error =", error);
        });
    };

    // 게시글 수정 함수
    const updateArticle = function (payload) {
      const { articleid, title, content, category } = payload;
      axios({
        method: "put",
        url: `/api/v1/articles/${articleid}/`,
        data: {
          title,
          content,
          category,
        },
      })
        .then((response) => {
          console.log("게시글 수정 성공");
          console.log(response);
          router.push({ name: "detail", params:{ id: articleid} });
        })
        .catch((error) => {
          console.log("deleteArticle error =", error);
        });
    };

    // 댓글 생성
    const createComment = async (payload) => {
      const { content, articleid } = payload;

      try {
        const response = await axios.post(`/api/v1/articles/${articleid}/create_comment/`, { content });
        comments.value.push(response.data); // 서버에서 받은 댓글을 바로 추가
      } catch (error) {
        console.error("createComment error:", error);
      }
    };

    // 댓글 조회
    const getComments = async (payload) => {
      const { articleid } = payload;

      try {
        const response = await axios.get(`/api/v1/articles/${articleid}/comment_list/`);
        comments.value = response.data; // 댓글 리스트를 갱신
      } catch (error) {
        console.error("getComments error:", error);
      }
    };

    // 댓글 삭제
    const deleteComments = async (payload) => {
      const { articleid, commentid } = payload;

      try {
        const response = await axios.delete(`/api/v1/articles/${articleid}/comment/${commentid}/`);
        const index = comments.value.findIndex((comment) => commentid == comment.id);
        comments.value.splice(index, 1);
      } catch (error) {
        console.error("deleteComments error:", error);
      }
    };

    // 댓글 수정
    const updateComment = async (payload) => {
      const { articleid, commentid, content } = payload;
    
      try {
        const response = await axios.put(`/api/v1/articles/${articleid}/comment/${commentid}/`, { content });
        // 특정 댓글만 업데이트
        const index = comments.value.findIndex(comment => comment.id === commentid);
        if (index !== -1) {
          comments.value[index] = response.data;
        }
      } catch (error) {
        console.error("updateComment error:", error);
        throw error; // 에러를 상위로 전파
      }
    };

    return {
      articles,
      articledetail,
      comments,
      getArticles,
      createArticle,
      getArticleDetail,
      deleteArticle,
      updateArticle,
      createComment,
      getComments,
      deleteComments,
      updateComment
    };
  },
  {
    persist: {
      paths: ["articles"], // articledetail은 제외
    },
  }
);
