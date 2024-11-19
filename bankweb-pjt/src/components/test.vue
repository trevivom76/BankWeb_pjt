<template>
    <div>
      <v-row>
        <v-col cols="12">
          <v-select
            class="select1"
            label="Select 1"
            :items="['California', 'Colorado', 'Florida', 'Georgia', 'Texas', 'Wyoming']"
            variant="outlined"
          ></v-select>
          <div class="currency-display">
            <v-text-field
              class="currency-amount"
              variant="outlined"
              solo
              value="1,000,000"
            ></v-text-field>
          </div>
        </v-col>
  
        <!-- 버튼들과 간격 조정 -->
        <v-row class="button-group" dense>
          <v-col cols="auto">
            <v-btn class="btn">억</v-btn>
          </v-col>
          <v-col cols="auto">
            <v-btn class="btn">천만</v-btn>
          </v-col>
          <v-col cols="auto">
            <v-btn class="btn">백만</v-btn>
          </v-col>
          <v-col cols="auto">
            <v-btn class="btn">십만</v-btn>
          </v-col>
          <v-col cols="auto">
            <v-btn class="btn">만</v-btn>
          </v-col>
          <v-col cols="auto">
            <v-btn class="btn">초기화</v-btn>
          </v-col>
        </v-row>
      </v-row>
    </div>
  </template>
  
  <script setup></script>
  
  <style scoped>
  .select1 {
    width: 100%;
    margin-bottom: 8px; /* Select와 텍스트 필드 사이 간격 */
  }
  
  .currency-display {
    margin-bottom: 8px; /* 텍스트 필드와 버튼 그룹 사이 간격 */
  }
  
  .currency-amount {
    width: 100%;
  }
  
  .button-group {
    gap: 8px; /* 버튼 간 8px 간격 */
  }
  
  .btn {
    background-color: black;
    color: white;
    font-size: 14px;
    min-width: 45px;
    height: 36px;
  }
  </style>
  