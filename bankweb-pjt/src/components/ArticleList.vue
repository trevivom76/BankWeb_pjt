<template>
  <div>
    <!-- 버튼 -->
    <div class="d-flex justify-space-between align-center">
      <div class="d-flex ga-5">
        <v-btn variant="flat" rounded="lg" color="#D6EFFF" width="100px" height="31px">전체</v-btn>
        <v-btn variant="tonal" rounded="lg" width="100px" height="31px">질문/답변</v-btn>
        <v-btn variant="tonal" rounded="lg" width="100px" height="31px">팁/정보 공유</v-btn>
        <v-btn variant="tonal" rounded="lg" width="100px" height="31px">자유</v-btn>
      </div>
      <div>
        <v-btn variant="flat" rounded="lg" color="#0B5BCB" width="92px" height="36px">
          <RouterLink :to="{name: 'create'}" class="delete-a-underline-color"> 글쓰기 </RouterLink>
        </v-btn>
      </div>
    </div>

    <!-- 게시판글 -->
    <v-data-table :items="articleStore.articles" :headers="headers">
      <template v-slot:item.title="{ item }">
        <!-- 글 제목을 클릭 시 다른 페이지로 이동 -->
        <RouterLink :to="{ name: 'detail', params: {id: item.id}}" class="delete-a-underline-color">
          {{ item.title }}
        </RouterLink>

      </template>

    </v-data-table>
  </div>
</template>

<script setup>
import { useArticleStore } from "@/stores/article";
import { onMounted, ref } from "vue";

const articleStore = useArticleStore();

// onMounted(() => {
//   articleStore.getArticles();
// });

// Data Table의 헤더 위치와 이름 설정
const headers = ref([
  { title: "글 제목", align: "start", key: "title" },
  { title: "카테고리", align: "center", key: "category" },
  { title: "작성자", align: "center", key: "author" },
]);
</script>

<style scoped>
.delete-a-underline-color {
  text-decoration: none;
  color: inherit;
}
</style>
