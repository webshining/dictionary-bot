const auth_axios = axios.create();
auth_axios.interceptors.request.use(
    (config) => {
        config.headers["initData"] = window.Telegram.WebApp.initData;
        return config;
    },
    function (error) {
        return Promise.reject(error);
    }
);
const get_dictionary = async (dictionary_id) => {
    const { data } = await auth_axios.get(`/dictionaries/${dictionary_id}`);
    return data;
};
const update_dictionary = async (dictionary_id, name) => {
    const { data } = await auth_axios.put(`/dictionaries/${dictionary_id}`, { name });
    return data;
};
const get_words = async (dictionary_id) => {
    const { data } = await auth_axios.get(`/words/${dictionary_id}`);
    return data;
};
const process_word = async (dictionary_id, word_id, know) => {
    const { data } = await auth_axios.put(`/words/${dictionary_id}/${word_id}`, { know });
    return data;
};
const delete_word = async (dictionary_id, word_id) => {
    const { data } = await auth_axios.delete(`/words/${dictionary_id}/${word_id}`);
    window.location.reload();
};
