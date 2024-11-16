import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

// pinia-plugin-persistedstate
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css';  // MDI 아이콘 스타일을 불러옵니다.

import App from './App.vue'
import router from './router'

const app = createApp(App)

// Pinia 설정
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)

// Vuetify 설정
const vuetify = createVuetify({
  components,
  directives,
  icons: {
    iconfont: 'mdi',  // Vuetify에서 MDI 아이콘을 사용하도록 설정
  },
})

app.use(vuetify)

// Router 설정
app.use(router)

// 애플리케이션 마운트
app.mount('#app')
