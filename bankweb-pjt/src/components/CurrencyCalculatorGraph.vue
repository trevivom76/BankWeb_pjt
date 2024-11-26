<template>
    <div class="exchange-rate-container">
        <!-- 기간 선택 버튼 그룹 -->
        <div class="period-selector">
            <button v-for="period in periods" :key="period.value"
                :class="['period-btn', { active: selectedPeriod === period.value }]"
                @click="changePeriod(period.value)">
                {{ period.label }}
            </button>
        </div>

        <!-- 환율 카드 그리드 -->
        <div class="exchange-grid">
            <div v-for="(currency, index) in currencies" 
                :key="currency.code" 
                class="exchange-card"
                :style="{ animationDelay: `${index * 100}ms` }"
            >
                <div class="card-header">
                    <h3>{{ currency.name }}</h3>
                </div>

                <div class="chart-container">
                    <img :src="`https://ssl.pstatic.net/imgfinance/chart/marketindex/area/${selectedPeriod}/FX_${currency.code}KRW.png`"
                        :alt="currency.name + ' chart'" 
                        class="chart-image" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const selectedPeriod = ref('month');

const periods = [
    { label: '1개월', value: 'month' },
    { label: '3개월', value: 'month3' },
    { label: '1년', value: 'year' },
];

const currencies = ref([
    {
        name: '미국 달러',
        code: 'USD',
    },
    {
        name: '일본 엔',
        code: 'JPY',
    },
    {
        name: '유로',
        code: 'EUR',
    },
    {
        name: '중국 위안',
        code: 'CNY',
    }
]);

const changePeriod = (period) => {
    selectedPeriod.value = period;
};
</script>

<style scoped>
.exchange-rate-container {
    padding: 24px 0px;
    max-width: 1200px;
    margin: 0 auto;
}

.period-selector {
    display: flex;
    justify-content: left;
    gap: 12px;
    margin-bottom: 24px;

    .period-btn {
        padding: 8px 16px;
        border: 1px solid #e0e0e0;
        border-radius: 20px;
        background: white;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 14px;

        &:hover {
            background: #f5f5f5;
        }

        &.active {
            background: #4c4c4c;
            color: white;
            border-color: #212121;
        }
    }
}

.exchange-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
}

.exchange-card {
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    padding: 24px;
    transition: transform 0.3s ease;
    animation: slideUp 0.6s ease-out both;

    &:hover {
        transform: translateY(-4px);
    }

    .card-header {
        margin-bottom: 16px;

        h3 {
            margin: 0 0 8px 0;
            font-size: 18px;
            font-weight: 500;
        }
    }

    .chart-container {
        width: 100%;
        height: 200px;
        background: #f5f5f5;
        border-radius: 8px;
        margin-bottom: 16px;
        overflow: hidden;

        .chart-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
    }
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(50px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@media (max-width: 768px) {
    .exchange-grid {
        grid-template-columns: 1fr;
    }

    .exchange-card {
        padding: 16px;
    }
}
</style>