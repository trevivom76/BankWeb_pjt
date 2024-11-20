<template>
  <div class="d-flex justify-center align-center">
    <v-card class="px-10 pt-12" width="950px" rounded="xl">
      <p :style="{ fontWeight: 'bold' , fontSize: '24px'}">
        BBK
        <span :style="{ color: '#0B5BCB' }">자유</span>
        게시판
      </p>

      <div class="mt-6">
        <ArticleList />

      </div>

    </v-card>
  </div>
</template>

<script setup>
import ArticleList from "@/components/ArticleList.vue";
</script>

<style scoped></style>
