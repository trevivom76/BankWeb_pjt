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
        <v-select placeholder="카테고리 선택" :items="['질문/답변', '팁/정보 공유', '자유']" width="160px" v-model="category"
          :rules="[(v) => !!v || '카테고리를 선택해주세요']"></v-select>

        <v-text-field placeholder="제목을 작성해주세요." width="686px" v-model.trim="title"
          :rules="[(v) => !!v || '제목을 입력해주세요']"></v-text-field>
      </div>

      <textarea placeholder="공유하고싶은 팁이나 정보를 작성해보세요." v-model.trim="content"></textarea>

      <div class="d-flex justify-end">
        <v-btn class="mt-4" variant="flat" @click="updateArticle" rounded="lg" color="#0B5BCB" width="92px"
          height="36px">
          <p>수정하기</p>
        </v-btn>
      </div>

      <!-- 경고 다이얼로그 -->
      <v-dialog v-model="showDialog" max-width="400">
        <div class="card">
          <div class="scene">
            <!-- 그림자 -->
            <div class="shadow"></div>
            <div class="cube">
              <img src="@/assets/icon/caution.png" alt="Caution Icon" class="cube-face front" />
              <img src="@/assets/icon/caution_back.png" alt="Caution Icon" class="cube-face back" />
            </div>
          </div>
          <p style="font-size: 22px; font-weight: 500; text-align: center;">{{ dialogMessage }}</p>
          <div class="card-footer">
            <button class="btn submit" @click="showDialog = false">확인</button>
          </div>
        </div>
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
  resize: none;
  /* 크기 조절 비활성화 */
  font-family: inherit;
  /* 폰트 상속 */
  line-height: 1.5;
  /* 행간 설정 */
  outline: none;
  /* 포커스 테두리 제거 */
}

textarea:focus {
  border-color: #0b5bcb;
  /* 포커스 시 테두리 색상 변경 */
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

.bottom-container {
  width: 100%;
  display: flex;
  flex-direction: row;
  gap: 12px;
  padding-top: 32px;
  align-items: center;
}

/* 3D 애니메이션 컨테이너 */
.scene {
  width: 150px;
  height: 150px;
  perspective: 1000px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0px auto 40px;
  position: relative;
}

/* 그림자 */
.shadow {
  position: absolute;
  bottom: -20px;
  /* 그림자를 컨테이너 아래로 배치 */
  width: 150px;
  height: 20px;
  background: radial-gradient(ellipse at center, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0));
  border-radius: 50%;
  z-index: -1;
  /* 3D 객체 아래로 배치 */
  filter: blur(5px);
  /* 부드러운 그림자 효과 */
}

/* 3D 객체 */
.cube {
  width: 100%;
  height: 100%;
  position: relative;
  transform-style: preserve-3d;
  /* 3D 효과 유지 */
  animation: spin 3s infinite linear;
  /* 좌우 회전 애니메이션 */
}

/* 공통 이미지 스타일 */
.cube-face {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  backface-visibility: hidden;
  /* 뒷면 숨김 */
}

/* 앞면 배치 */
.front {
  transform: rotateY(0deg)
    /* 3D 공간에서 앞면 배치 */
}

/* 뒷면 배치 */
.back {
  transform: rotateY(180deg)
    /* 3D 공간에서 뒷면 배치 */
}

/* 3D 회전 애니메이션 정의 */
@keyframes spin {
  0% {
    transform: rotateY(0deg);
    /* 초기 상태 */
  }

  50% {
    transform: rotateY(180deg);
    /* 180도 회전 */
  }

  100% {
    transform: rotateY(360deg);
    /* 360도 회전 */
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
  /* 마우스 오버 시 확대 및 회전 */
}

.btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn.submit {
  background-color: #666666;
  color: white;
}

.btn.submit:hover {
  background-color: #3f3f3f;
  transform: translateY(-2px);
}
</style>
