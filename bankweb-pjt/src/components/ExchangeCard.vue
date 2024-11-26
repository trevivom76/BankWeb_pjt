<template>
    <div class="card">
        <img :src="`https://ssl.pstatic.net/imgfinance/chart/marketindex/area/month/FX_${currency}KRW.png`" alt="환율 그래프"
            class="chart-img">
        <p class="chart-title">{{ name }}</p>
        <a class="link"
            :href="`https://finance.naver.com/marketindex/exchangeDetail.naver?marketindexCd=FX_${currency}KRW`"
            target="_blank" rel="noopener noreferrer">
            {{ name }} 증권페이지 바로가기 >
        </a>
    </div>
</template>

<script setup>
const props = defineProps({
    currency: String,
    name: String,
})
</script>

<style scoped>
.card {
    display: flex;
    flex-direction: column;
    align-items: center;
    /* 자식 요소를 가운데 정렬 */
    width: 100%;
    /* 부모 요소 너비를 기준으로 */
    max-width: 600px;
    /* 최대 너비 제한 */
    margin: 0 auto;
    /* 가운데 정렬 */
}

.chart-img {
    width: 100%;
    /* 부모 요소 너비에 맞춤 */
    height: auto;
    /* 비율 유지 */
    border-radius: 4px;
    /* 모서리 둥글게 (선택사항) */
}

.chart-title {
    text-align: center;
    font-size: 12px;
    font-weight: 500;
}

.link {
    padding: 4px 8px;
    /* 위아래 8px, 좌우 16px */
    text-decoration: underline;
    /* 밑줄 추가 */
    font-size: 9px;
    /* 글씨 크기 */
    font-weight: 500;
    /* 글씨 굵기 */
    color: #33333398;
    /* 글씨 색 */
    cursor: pointer;
    /* 마우스 커서를 손가락 모양으로 */
    margin-top: 8px;
    /* 위쪽 여백 */
    transition: 400ms;
}

.link:hover {
    transform: scale(1.1);
    /* 크기 살짝 확대 */
    font-weight: 700;
    /* 글씨 굵기 */
    color: #333;
    /* 글씨 색 */
}
</style>