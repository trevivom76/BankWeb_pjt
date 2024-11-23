<template>
  <div>
    <!-- 버튼 -->
    <div class="d-flex justify-space-between align-center">
      <div class="d-flex ga-5">
        <v-btn 
          variant="flat" 
          rounded="lg" 
          :color="selectedCategory === '전체' ? '#D6EFFF' : undefined"
          width="100px" 
          height="31px" 
          @click="selectedCategory = '전체'"
        >전체</v-btn>
        <v-btn 
          variant="flat" 
          rounded="lg" 
          :color="selectedCategory === '질문/답변' ? '#D6EFFF' : undefined"
          width="100px" 
          height="31px" 
          @click="selectedCategory = '질문/답변'"
        >질문/답변</v-btn>
        <v-btn 
          variant="flat" 
          rounded="lg" 
          :color="selectedCategory === '팁/정보 공유' ? '#D6EFFF' : undefined"
          width="100px" 
          height="31px" 
          @click="selectedCategory = '팁/정보 공유'"
        >팁/정보 공유</v-btn>
        <v-btn 
          variant="flat" 
          rounded="lg" 
          :color="selectedCategory === '자유' ? '#D6EFFF' : undefined"
          width="100px" 
          height="31px" 
          @click="selectedCategory = '자유'"
        >자유</v-btn>
      </div>
      <div>
        <RouterLink :to="{ name: 'create' }" class="delete-a-underline-color">글쓰기</RouterLink>
      </div>
    </div>

    <!-- 로딩 상태 표시 -->
    <div v-if="isLoading" class="d-flex justify-center align-center" style="height: 400px">
      <v-progress-circular indeterminate color="primary" :size="50"></v-progress-circular>
    </div>

    <!-- (전체)게시판글 -->
    <div v-else>
      <v-data-table 
        :items="filteredArticles" 
        :headers="headers" 
        :sort-by="[{ key: 'id', order: 'desc' }]"
        :no-data-text="'등록된 게시글이 없습니다.'"
      >
        <!-- 글 제목을 클릭 시 다른 페이지로 이동 -->
        <template v-slot:item.title="{ item }">
          <RouterLink :to="{ name: 'detail', params: { id: item.id } }" class="delete-a-underline-color">
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
            <RouterLink to="#" class="delete-a-underline-color ms-2">
              {{ item.user.nickname }}
            </RouterLink>
          </div>
        </template>
      </v-data-table>
    </div>
  </div>
</template>

<script setup>
import { useArticleStore } from "@/stores/article";
import { computed, onMounted, ref } from "vue";

const articleStore = useArticleStore();
const isLoading = ref(true);

// 어떤 버튼이 선택되어있는지 default는 "전체"
const selectedCategory = ref("전체");

// 모든 게시물 가져오기
onMounted(async () => {
  try {
    await articleStore.getArticles();
  } catch (error) {
    console.error('게시글 로딩 중 에러:', error);
  } finally {
    isLoading.value = false;
  }
});

// Data Table의 헤더 위치와 이름 설정
const headers = ref([
  { title: "글 제목", align: "start", key: "title", width: "50%" },
  { title: "카테고리", align: "center", key: "category", width: "35%" },
  { title: "작성자", align: "center", key: "user.nickname", width: "50%" },
  { title: "", key: "id", align: "center", sortable: false, width: "0%" },
]);

// 선택된 카테고리에 맞춰 필터링된 게시물 리스트
const filteredArticles = computed(() => {
  const articles = articleStore.articles || [];  // 없으면 빈 배열 사용
  
  if (selectedCategory.value === "전체") {
    return articles.filter((article) => ["질문/답변", "팁/정보 공유", "자유"].includes(article.category));
  } else {
    return articles.filter((article) => article.category === selectedCategory.value);
  }
});

// 카테고리 변경 시에도 로딩 상태 처리
const changeCategory = async (category) => {
  isLoading.value = true;
  try {
    selectedCategory.value = category;
    // 필요한 경우 여기에 카테고리 변경과 관련된 비동기 작업 추가
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.delete-a-underline-color {
  text-decoration: none;
  color: inherit;
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
</style>
