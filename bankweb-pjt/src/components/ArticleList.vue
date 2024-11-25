<template>
  <div>
    <!-- 버튼 -->
    <div class="category-header">
      <div class="category-tabs">
        <button
          v-for="category in categories"
          :key="category"
          :class="['category-tab', { active: selectedCategory === category }]"
          @click="selectedCategory = category"
        >
          {{ category }}
        </button>
      </div>
      <div>
        <RouterLink :to="{ name: 'create' }" class="btn delete-a-underline-color">글쓰기</RouterLink>
      </div>
    </div>

    <!-- 로딩 상태 표시 -->
    <div v-if="isLoading" class="d-flex justify-center align-center" style="height: 400px">
      <v-progress-circular indeterminate color="primary" :size="50"></v-progress-circular>
    </div>

    <!-- (전체)게시판글 -->
    <div v-else>
      <v-data-table-virtual :items="filteredArticles" :headers="headers" item-class="hover-class">
        <!-- 글 제목을 클릭 시 다른 페이지로 이동 -->
        <template v-slot:item.title="{ item }">
          <RouterLink :to="{ name: 'detail', params: { id: item.id } }" class="table-text">
            {{ item.title }}
          </RouterLink>
        </template>

        <template v-slot:item.category="{ item }">
          <!-- 카테고리별 CSS적용 -->
          <div v-if="item.category == '질문/답변'" class="question-answer">
            <p>{{ item.category }}</p>
          </div>
          <div v-else-if="item.category == '팁/정보 공유'" class="tip-info">
            <p>{{ item.category }}</p>
          </div>
          <div v-else-if="item.category == '자유'" class="free">
            <p>{{ item.category }}</p>
          </div>
        </template>

        <template v-slot:item.user.nickname="{ item }">
          <!-- 프로필이미지, 작성자 출력 -->
          <div class="d-flex justify-center align-center">
            <img :src="item.user.profile_img" alt="프로필 이미지" class="profile-img" />
            <RouterLink to="#" class="table-text ms-2">
              {{ item.user.nickname }}
            </RouterLink>
          </div>
        </template>
      </v-data-table-virtual>
    </div>
  </div>
</template>

<script setup>
import { useArticleStore } from "@/stores/article";
import { computed, onMounted, ref } from "vue";

const articleStore = useArticleStore();

const isLoading = ref(true);
const selectedCategory = ref("전체");

const headers = ref([
  { title: "글 제목", align: "start", key: "title", width: "50%" },
  { title: "카테고리", align: "center", key: "category", width: "35%" },
  { title: "작성자", align: "center", key: "user.nickname", width: "50%" },
]);

const categories = ["전체", "질문/답변", "팁/정보 공유", "자유"];

const filteredArticles = computed(() => {
  if (selectedCategory.value === "전체") {
    return articleStore.articles.filter((article) => ["질문/답변", "팁/정보 공유", "자유"].includes(article.category));
  } else {
    return articleStore.articles.filter((article) => article.category === selectedCategory.value);
  }
});


onMounted(async () => {
  try {
    await articleStore.getArticles();
  } finally {
    isLoading.value = false;
  }
});
</script>

<style scoped>
.delete-a-underline-color {
  text-decoration: none;
}

.table-text {
  text-decoration: none;
  color: #424242;
  font-size: 16px;
  font-weight: 500;
}

.profile-img {
  width: 25px;
}

.question-answer {
  background: #ffeeee;
  border-color: #ffc1c1;
  border-width: 2px;
  border-style: solid;
  border-radius: 1ch;
  margin-left: 30%;
  width: 90px;
  height: 25px;
  font: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.tip-info {
  background: #eefff5;
  border-color: #bdebc5;
  border-width: 2px;
  border-style: solid;
  border-radius: 1ch;
  margin-left: 26%;
  width: 110px;
  height: 25px;
  font: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.free {
  background: #eefcff;
  border-color: #c1ecff;
  border-width: 2px;
  border-style: solid;
  border-radius: 1ch;
  margin-left: 35%;
  width: 66px;
  height: 25px;
  font: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.category-tabs {
  display: flex;
  gap: 10px;
}

.category-tab {
  background-color: #f5f5f5; /* 기본 회색 */
  border: 1px solid #dcdcdc;
  color: #424242;
  border-radius: 20px;
  padding: 8px 16px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s, color 0.3s;
  white-space: nowrap;
}

.category-tab:hover {
  background-color: #e0e0e0; /* 호버 시 밝은 회색 */
  transform: scale(1.05);
}

.category-tab.active {
  background-color: #424242; /* 활성화 시 진한 파란색 */
  color: #ffffff;
  border-color: #303030;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

</style>
