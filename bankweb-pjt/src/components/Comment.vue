<template>
  <div>
    <v-card class="px-13 py-12" width="950px" min-height="530px" rounded="xl">
      <!-- 댓글 헤더 -->
      <div class="d-flex justify-start align-center ga-3">
        <p :style="{ fontSize: '24px', fontWeight: 'bold' }">댓글</p>
        <div class="comment-cnt">
          {{ articleStore.comments.length }}
        </div>
      </div>

      <!-- 작성된 댓글 리스트 -->
      <div>
        <div v-for="comment in articleStore.comments" :key="comment.id" class="comment">
          <div class="d-flex justify-space-between">
            <div class="d-flex align-center ga-4">
              <img :src="comment.user.profile_img" alt="프로필 이미지" class="profile-img" />

              <div class="d-flex flex-column">
                <p class="nickname">{{ comment.user.nickname }}</p>
                <p class="comment-content">{{ comment.content }}</p>
              </div>
            </div>

            <!-- 포맷팅된 날짜 출력 -->
            <div class="d-flex flex-column align-end justify-center ga-2">
              <div>
                <p class="formated-date">{{ formatDate(comment.created_at) }}</p>
              </div>

              <div v-if="accountStore.userinfo.nickname == comment.user.nickname" class="d-flex ga-2">
                <v-btn class="px-2" rounded="lg" min-width="47px" height="26px" variant="flat" color="#1E9FFB">수정</v-btn>
                <v-btn class="px-2" rounded="lg" min-width="47px" height="26px" variant="flat" color="#FF3D3D" @click="deleteComment(comment.id)">삭제</v-btn>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 댓글 작성 창 -->
      <div>
        <p class="currentuser-nickname">{{ accountStore.userinfo.nickname }}</p>
        <div class="d-flex justify-center align-center ga-4">
          <img :src="articleStore.articledetail.user.profile_img" alt="프로필 이미지" class="profile-img" />
          <textarea class="comment-create-textarea" placeholder="댓글을 작성해주세요." v-model="content"></textarea>
        </div>
        <div class="d-flex justify-end align-center">
          <v-btn class="v-btn-create-comment mt-2" rounded="lg" variant="flat" color="#484848" width="72px" height="27px" @click="createComment">작성하기</v-btn>
        </div>
      </div>
    </v-card>
  </div>
</template>

<script setup>
import { useAccountStore } from "@/stores/account";
import { useArticleStore } from "@/stores/article";
import { useProfileStore } from "@/stores/profile";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

const articleStore = useArticleStore();
const accountStore = useAccountStore();
const profileStore = useProfileStore();
const route = useRoute();
const content = ref("");

onMounted(() => {
  // 댓글 리스트 조회
  const payload1 = {
    articleid: route.params.id,
  };
  articleStore.getComments(payload1);
});

// 댓글 생성 함수
const createComment = async () => {
  if (!content.value.trim()) {
    alert("댓글 내용을 입력해주세요.");
    return;
  }

  const payload = {
    content: content.value,
    articleid: route.params.id,
  };

  await articleStore.createComment(payload);
  content.value = ""; // 댓글 작성 후 입력 필드 초기화
};

// 댓글 삭제 함수
const deleteComment = async (commentid) => {
  if (window.confirm("정말로 댓글을 삭제하시겠습니까?")) {
    const payload = {
      articleid: route.params.id,
      commentid: commentid,
    };
    await articleStore.deleteComments(payload);
  }
};

// 날짜 포맷 함수
const formatDate = (dateString) => {
  const date = new Date(dateString);

  const options = {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  };

  const formattedDate = new Intl.DateTimeFormat("ko-KR", options).format(date);
  return formattedDate.replace("오전", "").replace("오후", "").trim(); // 오전/오후 제거 후 포맷 수정
};
</script>

<style scoped>
.comment-cnt {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #4f84ce;
  border-radius: 1ch;
  width: 25px;
  height: 25px;

  font-size: 13px;
  font-weight: bold;
  color: white;
}

.profile-img {
  width: 44px;
}

.nickname {
  font-size: 18px;
  font-weight: bold;
}

.currentuser-nickname {
  font-size: 18px;
  font-weight: bold;
  margin-left: 60px;
  margin-top: 10px;
  margin-bottom: 7px;
}

.comment-create-textarea {
  width: 100%;
  min-height: 80px;
  background-color: #f5f5f5;
  border-width: 1px;
  border-color: rgb(114, 114, 114);
  border-width: 1px;
  border-style: solid;
  border-radius: 1ch;
  font-size: 16px;
  padding: 15px;
  resize: none;
}

.v-btn-create-comment {
  font-size: 13px;
}

.comment {
  padding: 10px 0;
  border-bottom: 1px solid #e0e0e0;
}

.comment-header {
  font-size: 14px;
  color: #555;
}

.comment-content {
  font-size: 16px;
  margin-top: 5px;
}

.formated-date {
  font-size: 14px;
  color: #7d7d7d;
}

@media (max-width: 768px) {
  .comment-create-textarea {
    width: 100%;
  }
}
</style>
