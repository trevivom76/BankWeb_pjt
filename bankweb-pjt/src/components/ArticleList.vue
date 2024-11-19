<template>
  <div>
    <v-data-table :items="items" :headers="headers"></v-data-table>

    <!-- 나중에 수정 -->
    <div v-for="article in articleStore.articles" :key="article.name">
      {{ article.name }}
      {{ article.species }}
      {{ article.diet }}
      {{ article.habitat }}
    </div>
  </div>
</template>

<script setup>
import { useArticleStore } from "@/stores/article";
import { onMounted, ref } from "vue";

const articleStore = useArticleStore();

onMounted(() => {
  articleStore.getArticles();
});

const headers = ref([
  { title: "글 제목", align: "start", key: "name" },
  { title: "카테고리", align: "end", key: "species" },
  { title: "작성자", align: "center", key: "habitat" },
]);
</script>

<style scoped>
/* 테이블 스타일을 커스터마이즈하려면 여기에 추가하세요 */
</style>
