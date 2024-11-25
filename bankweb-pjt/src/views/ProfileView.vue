<template>
  <div class="d-flex justify-center align-center">
    <v-card class="px-10 pt-12" width="950px" min_height="785px" rounded="xl">
      <div>
        <RouterLink :to="{ name: 'profilemanage' }">회원정보 관리 페이지</RouterLink>
        &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
        <RouterLink :to="{ name: 'contractedproduct' }">관심상품 관리 페이지</RouterLink>
        &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
        <RouterLink :to="{ name: 'recommendproduct' }">상품 추천받기 페이지</RouterLink>
      </div>
      <RouterView />
    </v-card>
  </div>
</template>

<script setup></script>

<style scoped></style>
