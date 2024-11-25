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

      <!-- 로딩 상태 표시 -->
      <div v-if="isLoading" class="d-flex justify-center align-center" style="height: 400px">
        <v-progress-circular indeterminate color="primary" :size="50"></v-progress-circular>
      </div>

      <!-- 작성된 댓글 리스트 -->
      <div v-else>
        <!-- 댓글 수정 버튼을 안눌렀다면 -->
        <div v-if="!isCommentUpdating">
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
                  <v-btn
                    class="px-2"
                    rounded="lg"
                    min-width="47px"
                    height="26px"
                    variant="flat"
                    color="#1E9FFB"
                    @click="(isCommentUpdating = true), (clicked_commentId = comment.id), (clicked_commentContent = comment.content)"
                  >
                    수정
                  </v-btn>
                  <v-btn
                    class="px-2"
                    rounded="lg"
                    min-width="47px"
                    height="26px"
                    variant="flat"
                    color="#FF3D3D"
                    @click="
                      showDeleteDialog = true;
                      commentToDelete = comment.id;
                    "
                  >
                    삭제
                  </v-btn>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 댓글 수정 버튼을 눌렀다면 -->
        <div v-else>
          <div v-for="comment in articleStore.comments" :key="comment.id" class="comment">
            <div class="d-flex justify-space-between">
              <div class="d-flex align-center ga-4">
                <img :src="comment.user.profile_img" alt="프로필 이미지" class="profile-img" />

                <div class="d-flex flex-column">
                  <p class="nickname">{{ comment.user.nickname }}</p>

                  <!-- 수정 버튼을 누른 댓글만 텍스트로 변환 -->
                  <textarea v-if="comment.id == clicked_commentId" class="comment-update-textarea" placeholder="댓글을 작성해주세요." v-model="clicked_commentContent"></textarea>
                  <p v-else class="comment-content">{{ comment.content }}</p>
                </div>
              </div>

              <!-- 포맷팅된 날짜 출력 -->
              <div class="d-flex flex-column align-end justify-center ga-2">
                <div>
                  <p class="formated-date">{{ formatDate(comment.created_at) }}</p>
                </div>

                <div v-if="accountStore.userinfo.nickname == comment.user.nickname" class="d-flex ga-2">
                  <!-- 수정 버튼을 누른 댓글만 의 버튼만 수정 완료 버튼으로 변환 -->
                  <v-btn v-if="comment.id == clicked_commentId" class="px-2 update-complete" rounded="lg" min-width="47px" height="26px" variant="flat" @click="updateComment">수정 완료</v-btn>
                  <v-btn v-else class="px-2" rounded="lg" min-width="47px" height="26px" variant="flat" color="#1E9FFB" @click="startEditing(comment)">수정</v-btn>

                  <v-btn class="px-2" rounded="lg" min-width="47px" height="26px" variant="flat" color="#FF3D3D" @click="(showDeleteDialog = true), (commentToDelete = comment.id)">삭제</v-btn>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 댓글 작성 창 -->
        <div>
          <p class="currentuser-nickname">{{ accountStore.userinfo.nickname }}</p>
          <div class="d-flex justify-center align-center ga-4">
            <img :src="userprofileInfo.profile_img" alt="프로필 이미지" class="profile-img" />
            <textarea class="comment-create-textarea" placeholder="댓글을 작성해주세요." v-model="content"></textarea>
          </div>
          <div class="d-flex justify-end align-center">
            <v-btn class="v-btn-create-comment mt-2" rounded="lg" variant="flat" color="#484848" width="72px" height="27px" @click="createComment">작성하기</v-btn>
          </div>
        </div>
      </div>
    </v-card>
  </div>

  <!-- 댓글 삭제 확인 다이얼로그 -->
  <v-dialog v-model="showDeleteDialog" max-width="400">
    <v-card>
      <v-card-text class="pa-6">
        <div class="text-center mb-4">
          <v-icon color="error" size="32" class="mb-3">mdi-alert-circle</v-icon>
          <p style="font-size: 22px">정말로 댓글을 삭제하시겠습니까?</p>
        </div>
        <div class="d-flex justify-center gap-button">
          <v-btn color="error" variant="flat" @click="confirmDelete">삭제</v-btn>
          <v-btn color="grey" variant="flat" @click="showDeleteDialog = false">취소</v-btn>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { useAccountStore } from "@/stores/account";
import { useArticleStore } from "@/stores/article";
import { useProfileStore } from "@/stores/profile";
import { storeToRefs } from "pinia";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";

const articleStore = useArticleStore();
const accountStore = useAccountStore();
const profileStore = useProfileStore();
const route = useRoute();
const content = ref("");
const isLoading = ref(true); // 로딩 상태를 관리하는 ref 추가

const isCommentUpdating = ref(false); // 현재 댓글 수정 버튼을 눌렀는지 아닌지
const clicked_commentId = ref(null);
const clicked_commentContent = ref(null);

const showDeleteDialog = ref(false);
const commentToDelete = ref(null);

// store의 상태를 반응형으로 가져오기
const { userprofile: userprofileInfo } = storeToRefs(profileStore);

onMounted(async () => {
  try {
    // 댓글 리스트 조회
    const payload = {
      articleid: route.params.id,
    };
    await articleStore.getComments(payload);
  } finally {
    isLoading.value = false; // 데이터 로딩이 완료되면 로딩 상태를 false로 변경
  }
});

// 댓글 생성 함수
const createComment = async () => {
  if (!content.value.trim()) {
    alert("댓글 내용을 입력해주세요.");
    return;
  }

  isLoading.value = true; // 댓글 생성 시작시 로딩 상태 true
  try {
    const payload = {
      content: content.value,
      articleid: route.params.id,
    };

    await articleStore.createComment(payload);
    content.value = ""; // 댓글 작성 후 입력 필드 초기화
  } finally {
    isLoading.value = false; // 댓글 생성 완료 후 로딩 상태 false
  }
};

// 기존 deleteComment 함수를 confirmDelete로 변경
const confirmDelete = async () => {
  isLoading.value = true;
  try {
    const payload = {
      articleid: route.params.id,
      commentid: commentToDelete.value,
    };
    await articleStore.deleteComments(payload);
    showDeleteDialog.value = false;
  } finally {
    isLoading.value = false;
  }
};

// 댓글 수정 함수
const updateComment = async () => {
  if (!clicked_commentContent.value.trim()) {
    alert("댓글 내용을 입력해주세요.");
    return;
  }

  isLoading.value = true;
  try {
    const payload = {
      articleid: route.params.id,
      commentid: clicked_commentId.value,
      content: clicked_commentContent.value,
    };
    await articleStore.updateComment(payload);

    // 수정 모드 종료
    isCommentUpdating.value = false;
    clicked_commentId.value = null;
    clicked_commentContent.value = null;
  } catch (error) {
    console.error("댓글 수정 중 오류 발생:", error);
  } finally {
    isLoading.value = false;
  }
};

// 수정 버튼 클릭 이벤트 핸들러 분리
const startEditing = (comment) => {
  isCommentUpdating.value = true;
  clicked_commentId.value = comment.id;
  clicked_commentContent.value = comment.content;
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
  return formattedDate.replace("오전", "").replace("오후", "").trim();
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

.comment-update-textarea {
  width: 250%;
  min-height: 50px;
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
.update-complete {
  background-color: rgb(51, 196, 11);
  color: white;
}
.gap-button {
  gap: 12px; /* 원하는 간격으로 조정 */
}
</style>
