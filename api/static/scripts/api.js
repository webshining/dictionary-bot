const auth_axios = axios.create();
auth_axios.interceptors.request.use(
    (config) => {
        return config;
    },
    function (error) {
        return Promise.reject(error);
    }
);
const process_word = async (word_id, know) => {
    const { data } = await auth_axios.post(`/words/${word_id}`, { know });
};
const delete_word = async (dictionary_id, word_id) => {
    const { data } = await auth_axios.delete(`/words/${dictionary_id}/${word_id}`);
    window.location.reload();
};
