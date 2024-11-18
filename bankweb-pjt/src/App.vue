<template>
  <div>
    <v-container fluid style="padding-left: 300px; padding-right: 300px;">
      <CommonHeader />
    </v-container>

    <div class="RouterView-div">
      <v-container fluid style="padding-left: 300px; padding-right: 300px;">
        <RouterView />
      </v-container>
    </div>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router';
import CommonHeader from './components/CommonHeader.vue';



</script>

<style scoped>
.RouterView-div{

  background: #eeeeeee7;
}
</style>