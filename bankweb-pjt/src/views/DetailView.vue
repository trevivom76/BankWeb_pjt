<template>
  <div class="d-flex justify-center align-center flex-column ga-6">
    <v-card class="px-13 py-12" width="950px" min-height="530px" rounded="xl">
      <!-- 뒤로가기 버튼 -->
      <v-btn variant="flat" @click="goBack" class="mb-4">
        <svg-icon type="mdi" :path="mdiArrowLeft" width="20px"></svg-icon>
        뒤로가기
      </v-btn>

      <!-- 로딩 상태 표시 -->
      <div v-if="isLoading" class="d-flex justify-center align-center" style="height: 400px">
        <v-progress-circular indeterminate color="primary" :size="50"></v-progress-circular>
      </div>

      <div v-else>
        <!-- 프로필, 아이디 -->
        <div class="d-flex justify-space-between">
          <div div class="d-flex align-center">
            <img :src="articledetaildata.user.profile_img" alt="프로필 이미지" class="profile-img" />
            <p class="nickname">
              {{ articledetaildata.user.nickname }}
            </p>
          </div>
          <div class="article-category">
            <p>{{ articledetaildata.category }}</p>
          </div>
        </div>

        <!-- 글 제목 -->
        <p class="article-title">{{ articledetaildata.title }}</p>

        <!-- 글 작성 날짜 + 수정, 삭제 버튼 -->
        <div class="d-flex justify-space-between align-center mb-5">
          <div>
            <p class="article-createdat">{{ formattedCreatedAt }}</p>
          </div>
          <div v-if="accountStore.userinfo.nickname == articledetaildata.user.nickname" class="d-flex ga-6 article-update-delete mr-8">
            <a href="#" class="article-update" @click.prevent="updateArticle">수정</a>
            <a href="#" class="article-delete" @click="deleteArticle(articledetaildata.id)">삭제</a>
          </div>
        </div>

        <!-- 글 내용 -->
        <textarea class="article-content" readonly>
         {{ articledetaildata.content }}
       </textarea
        >
      </div>
    </v-card>

    <!-- 댓글 창 -->
    <Comment />
  </div>
</template>

<script setup>
import { useArticleStore } from "@/stores/article";
import { ref, computed, watch } from "vue"; // watch 추가
import { useRoute, useRouter } from "vue-router";
import SvgIcon from "@jamescoyle/vue-icon";
import { mdiArrowLeft } from "@mdi/js";
import Comment from "@/components/Comment.vue";
import { useProfileStore } from "@/stores/profile";
import { useAccountStore } from "@/stores/account";

const articleStore = useArticleStore();
const profileStore = useProfileStore();
const accountStore = useAccountStore();
const route = useRoute();
const router = useRouter();
const articledetaildata = ref(null);
const isLoading = ref(true);

// 게시글 데이터 가져오는 함수
const fetchArticleDetail = async () => {
  isLoading.value = true;
  try {
    const payload = {
      articleid: route.params.id,
    };
    await articleStore.getArticleDetail(payload);
    articledetaildata.value = articleStore.articledetail;
  } finally {
    isLoading.value = false;
  }
};

// 초기 데이터 로드
fetchArticleDetail();

// route.params.id가 변경될 때마다 데이터 다시 로드
watch(
  () => route.params.id,
  (newId) => {
    if (newId) {
      fetchArticleDetail();
    }
  }
);

// 게시글 삭제 함수
const deleteArticle = async function (articleid) {
  if (window.confirm("정말로 게시글을 삭제하시겠습니까?")) {
    isLoading.value = true;
    try {
      const payload = {
        articleid: articleid,
      };
      await articleStore.deleteArticle(payload);
    } finally {
      isLoading.value = false;
    }
  }
};

// 게시글 수정 함수
const updateArticle = function () {
  if (window.confirm("정말로 게시글을 수정하시겠습니까?")) {
    router.push({ 
      name: 'update', 
      params: { 
        id: articledetaildata.value.id 
      } 
    });
  }
};

// 뒤로가기 함수
const goBack = () => {
  window.history.back();
};

// 날짜 포맷팅
const formattedCreatedAt = computed(() => {
  const createdAt = articleStore.articledetail?.created_at;
  if (!createdAt) return "";

  const date = new Date(createdAt);

  const options = {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  };

  const formattedDate = new Intl.DateTimeFormat("ko-KR", options).format(date);
  return formattedDate.replace("오전", "").replace("오후", "").trim();
});
</script>

<style scoped>
.profile-img {
  width: 44px;
}

.nickname {
  font-size: 16px;
  margin-left: 16px;
}

.article-category {
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 1cap;
  width: 100px;
  height: 36px;
  background-color: #0b5bcb;
  color: white;
}

.article-title {
  margin-top: 20px;
  margin-bottom: 12px;
  font-size: 24px;
  font-weight: bolder;
}

.article-createdat {
  font-size: 13px;
  color: #7d7d7d;
}

.article-update-delete {
  font-size: 15px;
}

.article-update {
  color: #4f4f4f;
}

.article-delete {
  color: #de3c3c;
}

.article-content {
  font-size: 18px;
  width: 100%;
  min-height: 217px;
  padding-top: 20px;
  padding-bottom: 20px;
  border-color: black;
  border-width: 2px;
  border-style: solid;
  border-radius: 1ch;
}
</style>
