<template>
  <!-- 레이아웃까지 구성 -->
  <div class="container">
    <v-carousel show-arrows="hover">
      <v-carousel-item src="https://cdn.vuetifyjs.com/images/cards/docks.jpg" cover></v-carousel-item>

      <v-carousel-item src="https://cdn.vuetifyjs.com/images/cards/hotel.jpg" cover></v-carousel-item>

      <v-carousel-item src="https://cdn.vuetifyjs.com/images/cards/sunshine.jpg" cover></v-carousel-item>
    </v-carousel>
  </div>
</template>

<script setup>
</script>

<style scoped>
.container {
  border-radius: 20px;
  overflow: hidden;
}
</style>
