<template>
  <div>
    <CommonHeader />
    <div class="RouterView-div">
      <RouterView />
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