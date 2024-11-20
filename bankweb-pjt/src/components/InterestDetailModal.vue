<template>
    <v-dialog v-model="isVisible" max-width="600px">
        <v-card class="py-5 px-3">
            <v-card-title class="d-flex align-center justify-space-between">
            </v-card-title>

            <v-card-text>
                <v-table v-if="depositItem">
                <tbody>
                    <tr v-for="(value, key) in depositItem" :key="key">
                    <td width="28%" class="font-weight-bold">{{ key }}</td>
                    <td v-if="key === '최고 한도'">
                        {{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}
                    </td>
                    <td v-else>{{ value }}</td>
                    </tr>
                </tbody>
                </v-table>
                <div v-else>데이터를 불러오는 중...</div>
            </v-card-text>

            <v-card-actions>
                <v-btn text @click="closeModal">닫기</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script setup>
import { ref, defineProps, defineEmits, watch, onMounted } from "vue";

const props = defineProps({
depositItem: Object, // 부모 컴포넌트에서 전달된 예적금 데이터
modelValue: Boolean, // 모달 열림 상태 (v-model)
});

const emit = defineEmits(["update:modelValue"]);

const isVisible = ref(props.modelValue);
const selectedDeposit = ref({})

// 부모의 modelValue와 동기화
watch(
() => props.modelValue,
(newValue) => {
    isVisible.value = newValue;
}
);

// isVisible 변경 시 부모에 업데이트 알림
watch(isVisible, (newValue) => {
emit("update:modelValue", newValue);
});

const closeModal = () => {
isVisible.value = false;
};

onMounted(() => {
    console.log(props.depositItem)

    // selectedDeposit.value = {
    //     '금융 회사명': props.depositItem['kor_co_nm'],
    //     '금융 상품명': props.depositItem['fin_prdt_nm'],
    //     '가입 방법': props.depositItem['join_way'],
    //     '만기 후 이자율': props.depositItem['mtrt_int'],
    //     '우대 조건': props.depositItem['spcl_cnd'],
    //     '가입 대상': props.depositItem['join_member'],
    //     '가입 제한': props.depositItem['join_deny'] === 1 ? '제한없음' : data['join_deny'] === 2 ? '서민전용' : '일부제한',
    //     '최고 한도': props.depositItem['max_limit'],
    //     '기타 유의사항': props.depositItem['etc_note']
    // }

    // const optionList = props.depositItem.savingoption_set

    // for (const option of optionList) {
    //     if (option.rsrv_type_nm === '자유적립식') {
    //         if (option.save_trm === "6") {
    //             intrRateF.value[0] = option.intr_rate
    //             intrRate2F.value[0] = option.intr_rate2
    //         } else if (option.save_trm === "12") {
    //             intrRateF.value[1] = option.intr_rate
    //             intrRate2F.value[1] = option.intr_rate2
    //         } else if (option.save_trm === "24") {
    //             intrRateF.value[2] = option.intr_rate
    //             intrRate2F.value[2] = option.intr_rate2
    //         } else if (option.save_trm === "36") {
    //             intrRateF.value[3] = option.intr_rate
    //             intrRate2F.value[3] = option.intr_rate2
    //         }
    //         } else {
    //         if (option.save_trm === "6") {
    //             intrRateS.value[0] = option.intr_rate
    //             intrRate2S.value[0] = option.intr_rate2
    //         } else if (option.save_trm === "12") {
    //             intrRateS.value[1] = option.intr_rate
    //             intrRate2S.value[1] = option.intr_rate2
    //         } else if (option.save_trm === "24") {
    //             intrRateS.value[2] = option.intr_rate
    //             intrRate2S.value[2] = option.intr_rate2
    //         } else if (option.save_trm === "36") {
    //             intrRateS.value[3] = option.intr_rate
    //             intrRate2S.value[3] = option.intr_rate2
    //         }
    //     }
    // }
})
</script>

<style lang="scss" scoped>
</style>