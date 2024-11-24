<template>
  <div>
    <header>
      <CommonHeader />
    </header>
    <div class="RouterView-div">
      <RouterView />
    </div>
    <footer>
      <CommonFooter />
    </footer>
  </div>
</template>

<script setup>
import { RouterView } from "vue-router";
import CommonHeader from "@/components/CommonHeader.vue";
import CommonFooter from "@/components/CommonFooter.vue";
</script>

<style scoped>
.RouterView-div {
  background: #f3f6f8;
  padding-top: 40px;
  padding-bottom: 40px;
}
</style>
