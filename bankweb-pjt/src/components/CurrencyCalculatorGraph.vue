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
            <div v-for="currency in currencies" :key="currency.code" class="exchange-card">
                <div class="card-header">
                    <h3>{{ currency.name }}</h3>
                    <div class="currency-info">
                        <span class="currency-code">{{ currency.code }}</span>
                        <span :class="['rate-change', currency.change >= 0 ? 'positive' : 'negative']">
                            {{ currency.change >= 0 ? '+' : '' }}{{ currency.change }}%
                        </span>
                    </div>
                </div>

                <div class="chart-container">
                    <img :src="`https://ssl.pstatic.net/imgfinance/chart/marketindex/area/${selectedPeriod}/FX_${currency.code}KRW.png`"
                        :alt="currency.name + ' chart'" class="chart-image" />
                </div>

                <div class="card-footer">
                    <div class="current-rate">
                        <span class="label">현재 환율:</span>
                        <span class="value">{{ currency.currentRate }}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const selectedPeriod = ref('1M');

const periods = [
    { label: '1개월', value: 'month' },
    { label: '3개월', value: 'month3' },
    { label: '1년', value: 'year' },
];

const currencies = ref([
    {
        name: '미국 달러',
        code: 'USD',
        change: 0.25,
        currentRate: '1,320.50'
    },
    {
        name: '일본 엔',
        code: 'JPY',
        change: -0.15,
        currentRate: '8.8123',
    },
    {
        name: '유로',
        code: 'EUR',
        change: 0.18,
        currentRate: '1,428.30',
    },
    {
        name: '중국 위안',
        code: 'CNY',
        change: -0.32,
        currentRate: '183.25',
    }
]);

const changePeriod = (period) => {
    selectedPeriod.value = period;
};
</script>

<style scoped>
.exchange-rate-container {
    padding: 24px;
    max-width: 1200px;
    margin: 0 auto;
}

.period-selector {
    display: flex;
    justify-content: center;
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
            background: #2196f3;
            color: white;
            border-color: #2196f3;
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
    padding: 20px;
    transition: transform 0.3s ease;

    &:hover {
        transform: translateY(-4px);
    }

    .card-header {
        margin-bottom: 16px;

        h3 {
            margin: 0 0 8px 0;
            font-size: 18px;
            font-weight: 600;
        }

        .currency-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .currency-code {
            font-size: 14px;
            color: #666;
        }

        .rate-change {
            font-size: 14px;
            font-weight: 600;

            &.positive {
                color: #4caf50;
            }

            &.negative {
                color: #f44336;
            }
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

    .card-footer {
        .current-rate {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 14px;

            .label {
                color: #666;
            }

            .value {
                font-weight: 600;
            }
        }
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