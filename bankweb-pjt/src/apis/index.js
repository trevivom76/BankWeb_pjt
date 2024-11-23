import { useAccountStore } from "@/stores/account";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

const instance = axios.create({
  baseURL: API_URL,
});

// 요청(request)를 보낼 때마다 아래의 콜백 함수를 실행하게 가로챈다.
instance.interceptors.request.use(
  (config) => {
    const accountstore = useAccountStore();
    if (accountstore.token) {
      config.headers.Authorization = `Token ${accountstore.token}`;
    }
    return config; // 이 부분을 추가하세요
  },
  (error) => {
    return Promise.reject(error); // 에러 처리도 추가
  }
);

export default instance;
