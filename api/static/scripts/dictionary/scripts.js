let timeout_id;
const update_dictionary = async (dictionary_id, name) => {
    clearTimeout(timeout_id);
    timeout_id = setTimeout(async () => {
        await auth_axios.put(`/dictionaries/${dictionary_id}`, { name });
    }, 1000);
};
const delete_word = async (dictionary_id, word_id) => {
    const { data } = await auth_axios.delete(`/words/${dictionary_id}/${word_id}`);
};

const add_word = async (dictionary_id) => {
    const create_input = document.querySelector(".create__content_input");
    const { data } = await auth_axios.post(`/words/${dictionary_id}`, { word: create_input.value });
    console.log(data);
};
