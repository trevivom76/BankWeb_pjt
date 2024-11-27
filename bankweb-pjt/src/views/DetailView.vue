<template>
  <div class="container">
    <div class="card">
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

        <div class="card-title">
          <h1 :style="{ fontWeight: 600, fontSize: '24px' }">
            {{ articledetaildata.title }}
          </h1>
        </div>

        <!-- 글 작성 날짜 + 수정, 삭제 버튼 -->
        <div class="d-flex justify-space-between align-center mb-5">
          <div>
            <p class="article-createdat">{{ formattedCreatedAt }}</p>
          </div>
          <div v-if="accountStore.userinfo.nickname == articledetaildata.user.nickname"
            class="d-flex ga-6 article-update-delete mr-4">
            <a href="#" class="article-update" @click.prevent="showUpdateDialog = true">수정</a>
            <a href="#" class="article-delete" @click.prevent="showDeleteDialog = true">삭제</a>
          </div>
        </div>

        <!-- 글 내용 -->
        <textarea class="article-content" readonly>{{ articledetaildata.content }}</textarea>
      </div>
    </div>

    <!-- 댓글 창 -->
    <div class="comment-container">
      <Comment />
    </div>

    <!-- 삭제 확인 다이얼로그 -->
    <v-dialog v-model="showDeleteDialog" max-width="400">
      <div class="card">
        <div class="icon-container">
          <img src="@/assets/icon/trash_can.png" alt="쓰레기통" class="delete-icon" width="100" height="100">
        </div>
        <p style="font-size: 22px; font-weight: 500; text-align: center;">정말로 게시글을 삭제하시겠습니까?</p>
        <div class="card-footer">
          <button class="btn delete" @click="confirmDelete">삭제하기</button>
          <button class="btn cancel" @click="showDeleteDialog = false">취소</button>
        </div>
      </div>
    </v-dialog>


    <v-dialog v-model="showUpdateDialog" max-width="400">
      <div class="card">
        <div class="icon-container">
          <img src="@/assets/icon/check.png" alt="수정" class="update-icon" width="100" height="100">
        </div>
        <p style="font-size: 22px; font-weight: 500; text-align: center;">게시글을 수정하시겠습니까?</p>
        <div class="card-footer">
          <button class="btn update" @click="confirmUpdate">수정하기</button>
          <button class="btn cancel" @click="showUpdateDialog = false">취소</button>
        </div>
      </div>
    </v-dialog>
  </div>
</template>

<script setup>
import { useArticleStore } from "@/stores/article";
import { ref, computed, watch } from "vue";
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
const showDeleteDialog = ref(false);
const showUpdateDialog = ref(false);
const showCommentDialog = ref(false);

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

// 게시글 삭제 확인
const confirmDelete = async () => {
  isLoading.value = true;
  try {
    const payload = {
      articleid: articledetaildata.value.id,
    };
    await articleStore.deleteArticle(payload);
    showDeleteDialog.value = false;
  } finally {
    isLoading.value = false;
  }
};

// 게시글 수정 확인
const confirmUpdate = () => {
  router.push({
    name: "update",
    params: {
      id: articledetaildata.value.id,
    },
  });
  showUpdateDialog.value = false;
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
.container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.comment-container {
  flex-grow: 1;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.5s ease;
}

.slide-enter-from {
  transform: translateX(-20px);
}

.slide-leave-to {
  transform: translateX(20px);
}

.card {
  background-color: white;
  padding: 48px 40px;
  border-radius: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  animation: card-load 0.8s ease;
}

.card-title {
  display: flex;
  flex-direction: row;
  gap: 4px;
  align-items: center;
  padding: 20px 0 4px;
}

.title {
  font-weight: 600;
  font-size: 24px;
}

.highlight {
  color: #5058cc;
}

@keyframes card-load {
  0% {
    transform: scale(0.95);
    opacity: 0;
  }

  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.location-icon:hover {
  transform: scale(1.2);
}

.profile-img {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
  background-color: #636ACC;
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
  padding: 20px;
  border-color: black;
  border-width: 2px;
  border-style: solid;
  border-radius: 1ch;
}

.gap-button {
  gap: 12px;
}

.btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn.delete {
  background-color: #dc3545;
  color: white;
}

.btn.delete:hover {
  background-color: #bb2d3b;
  transform: translateY(-2px);
}

.btn.cancel {
  background-color: #e9ecef;
  color: #495057;
}

.btn.cancel:hover {
  background-color: #dee2e6;
  transform: translateY(-2px);
}

@keyframes warning {
  0% {
    transform: scale(0.5);
    opacity: 0;
  }

  50% {
    transform: scale(1.2);
  }

  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.card {
  background: white;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.card-footer {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 24px;
}

.icon-container {
  width: 100px;
  height: 100px;
  margin: 0 auto 24px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.delete-icon {
  color: #dc3545;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.1);
  }

  100% {
    transform: scale(1);
  }
}

.update-icon {
  color: #5A87F2;
  animation: pulse 1.5s ease-in-out infinite;
}

.btn.update {
  background-color: #5A87F2;
  color: white;
}

.btn.update:hover {
  background-color: #4A77E2;
  transform: translateY(-2px);
}
</style>
