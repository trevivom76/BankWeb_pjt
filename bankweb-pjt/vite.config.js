import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})

// import { fileURLToPath, URL } from "node:url";

// import { defineConfig } from "vite";
// import vue from "@vitejs/plugin-vue";
// import vueDevTools from "vite-plugin-vue-devtools";

// // https://vite.dev/config/
// export default defineConfig({
//   plugins: [vue(), vueDevTools()],
//   resolve: {
//     alias: {
//       "@": fileURLToPath(new URL("./src", import.meta.url)),
//     },
//   },
//   server: {
//     proxy: {
//       "/api/site/program": {
//         target: "https://www.koreaexim.go.kr", // API 서버 URL
//         changeOrigin: true, // 크로스 도메인 허용
//       },
//     },
//   },
// });

// // ```
// // server: {
// //     proxy: {
// //       "/api": {
// //         target: "https://www.koreaexim.go.kr",
// //         changeOrigin: true,
// //         rewrite: (path) => path.replace(/^\/api/, ""),
// //       },
// //     },
// //   },
// // ```
