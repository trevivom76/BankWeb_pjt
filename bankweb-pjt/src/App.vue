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
</script>

<style scoped>
.RouterView-div {
  background: #F3F6F8;
  padding-top: 40px;
  padding-bottom: 40px;
}
</style>
