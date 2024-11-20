<template>
  <div>
    <v-container class="py-0" fluid style="padding-left: 400px; padding-right: 400px">
      <CommonHeader />
    </v-container>

    <div class="RouterView-div">
      <v-container fluid style="padding-left: 400px; padding-right: 400px">
        <RouterView />
      </v-container>
    </div>
  </div>
</template>

<script setup>
import { RouterView } from "vue-router";
import CommonHeader from "./components/CommonHeader.vue";
</script>

<style scoped>
.RouterView-div {
  background: #eeeeeee7;
}
</style>
