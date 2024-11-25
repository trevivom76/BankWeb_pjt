<template>
  <div class="d-flex justify-center align-center">
    <v-card class="px-10 pt-8" width="950px" height="785px" rounded="xl">
      <v-btn variant="flat" @click="goBack">
        <svg-icon type="mdi" :path="mdiArrowLeft" width="20px"></svg-icon>
        뒤로가기
      </v-btn>

      <p :style="{ fontWeight: 'bold', fontSize: '24px' }" class="mt-5">
        글
        <span :style="{ color: '#0B5BCB' }">수정</span>
        하기
      </p>

      <div class="d-flex ga-2 mt-4">
        <v-select placeholder="카테고리 선택" :items="['질문/답변', '팁/정보 공유', '자유']" width="160px" v-model="category" :rules="[(v) => !!v || '카테고리를 선택해주세요']"></v-select>

        <v-text-field placeholder="제목을 작성해주세요." width="686px" v-model.trim="title" :rules="[(v) => !!v || '제목을 입력해주세요']"></v-text-field>
      </div>

      <textarea placeholder="공유하고싶은 팁이나 정보를 작성해보세요." v-model.trim="content"></textarea>

      <div class="d-flex justify-end">
        <v-btn class="mt-4" variant="flat" @click="updateArticle" rounded="lg" color="#0B5BCB" width="92px" height="36px">
          <p>수정하기</p>
        </v-btn>
      </div>

      <!-- 경고 다이얼로그 -->
      <v-dialog v-model="showDialog" max-width="400">
        <v-card>
          <v-card-text class="pa-6">
            <div class="text-center mb-4">
              <v-icon color="warning" size="32" class="mb-3">mdi-alert-circle</v-icon>
              <p style="font-size: 22px">
                {{ dialogMessage }}
              </p>
            </div>
            <div class="d-flex justify-center">
              <v-btn color="primary" @click="showDialog = false" variant="flat">확인</v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-card>
  </div>
</template>

<script setup>
import { useArticleStore } from "@/stores/article";
import { ref } from "vue";
import { useRouter } from "vue-router";
// pictogrammers mdi icon
import SvgIcon from "@jamescoyle/vue-icon";
import { mdiArrowLeft } from "@mdi/js";

const router = useRouter();
const articleStore = useArticleStore();
const showDialog = ref(false);
const dialogMessage = ref("");

const title = ref(articleStore.articledetail.title);
const content = ref(articleStore.articledetail.content);
const category = ref(articleStore.articledetail.category);

// 폼 유효성 검사
const validateForm = () => {
  if (!category.value) {
    dialogMessage.value = "카테고리를 선택해주세요.";
    return false;
  }
  if (!title.value || title.value.trim() === "") {
    dialogMessage.value = "제목을 입력해주세요.";
    return false;
  }
  if (!content.value || content.value.trim() === "") {
    dialogMessage.value = "내용을 입력해주세요.";
    return false;
  }
  return true;
};

const updateArticle = async () => {
  if (!validateForm()) {
    showDialog.value = true;
    return;
  }

  try {
    const payload = {
      articleid: articleStore.articledetail.id,
      title: title.value,
      content: content.value,
      category: category.value,
    };

    await articleStore.updateArticle(payload);
    router.push({ name: "community" }); // 성공 시 커뮤니티 페이지로 이동
  } catch (error) {
    console.error("게시글 수정 실패:", error);
    dialogMessage.value = "게시글 수정에 실패했습니다. 다시 시도해주세요.";
    showDialog.value = true;
  }
};

// 뒤로가기 함수
const goBack = () => {
  window.history.back();
};
</script>

<style scoped>
textarea {
  width: 100%;
  height: 60%;
  border: 1px solid #797979;
  padding: 34px;
  border-radius: 1cap;
  resize: none; /* 크기 조절 비활성화 */
  font-family: inherit; /* 폰트 상속 */
  line-height: 1.5; /* 행간 설정 */
  outline: none; /* 포커스 테두리 제거 */
}

textarea:focus {
  border-color: #0b5bcb; /* 포커스 시 테두리 색상 변경 */
}

.delete-a-underline-color {
  text-decoration: none;
  color: inherit;
}

.ga-2 {
  gap: 0.5rem;
}

/* 다이얼로그 스타일 */
.v-card-text {
  font-size: 1.1rem;
}

/* 버튼 스타일 */
.v-btn {
  text-transform: none;
}
</style>
