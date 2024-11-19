<template>
  <div>
    <v-card class="pa-12" width="100%" height="100%" rounded="xl">
      <Article />
      <ArticleList />
    </v-card>
  </div>
</template>

<script setup>
import Article from "@/components/Article.vue";
import ArticleList from "@/components/ArticleList.vue";
</script>

<style scoped></style>
