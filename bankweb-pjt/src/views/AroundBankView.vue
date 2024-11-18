<template>
    <div>
        <div class="d-flex justify-center align-center mb-5">
            <BankMapSelect @change="handleRegionChange"/>
        </div>
        <BankMap :selected-region="selectedRegion"/>
        <BankMapProducts/>
    </div>
</template>

<script setup>
import BankMapSelect from '@/components/BankMapSelect.vue';
import BankMap from '@/components/BankMap.vue';
import BankMapProducts from '@/components/BankMapProducts.vue';
import { ref } from 'vue';

// <BankMapSelect> 에서 선택된 Regin정보를 보관하여 <BankMap> 에 넘겨줌
const selectedRegion = ref({})
const handleRegionChange = (selection) => {
    selectedRegion.value = selection
}

</script>

<style scoped>

</style>