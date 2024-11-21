<template>
  <div>
    <header>
      <CommonHeader />
    </header>

    <div class="RouterView-div">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { RouterView } from "vue-router";
import CommonHeader from "./components/CommonHeader.vue";
import 'pretendard/dist/web/static/pretendard.css';

</script>

<style scoped>
.RouterView-div {
  background: #f3f6f8;
  padding-top: 40px;
  padding-bottom: 40px;
}
</style>
