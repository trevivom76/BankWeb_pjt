<template>
  <div>
    <div class="container">
      <header class="d-flex align-center mb-7">
        <RouterLink :to="{name:'depositList'}" exact-active-class="active">정기예금</RouterLink>
        <p>|</p>
        <RouterLink :to="{name:'savingList'}" exact-active-class="active">정기적금</RouterLink>
      </header>
    <RouterView />
  </div>
  </div>
</template>

<script setup></script>

<style scoped></style>
