<template>
  <div>
    {{ store.userinfo }}
  </div>
</template>

<script setup>
import { useAccountStore } from "@/stores/account";

const store = useAccountStore();
</script>

<stylescoped>

</stylescoped>
