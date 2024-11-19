<template>
  <div>
    <h1 class="mb-10" :style="{ marginLeft: '90px' }">
      BBK
      <span :style="{ color: '#0B5BCB' }">자유</span>
      게시판
    </h1>

    <div class="d-flex justify-space-between align-center mb-5" :style="{ marginLeft: '70px', marginRight: '70px' }">
      <div class="d-flex ga-5">
        <v-btn variant="flat" rounded="lg" color="#D6EFFF" width="100px">전체</v-btn>
        <v-btn variant="tonal" rounded="lg" width="100px">질문/답변</v-btn>
        <v-btn variant="tonal" rounded="lg" width="100px">팁/정보 공유</v-btn>
        <v-btn variant="tonal" rounded="lg" width="100px">자유</v-btn>
      </div>
      <div>
        <v-btn variant="flat" rounded="lg" color="#0B5BCB" width="100px">글쓰기</v-btn>
      </div>
    </div>
  </div>
</template>

<script setup></script>

<style scoped></style>
