const options = {
    baseURL: "",
    withCredentials: true,
    headers: {
        "Content-Type": "application/json",
    },
};
const auth_axios = axios.create(options);
auth_axios.interceptors.request.use(
    (config) => {
        config.headers["initData"] = window.Telegram.WebApp.initData;
        return config;
    },
    function (error) {
        return Promise.reject(error);
    }
);
