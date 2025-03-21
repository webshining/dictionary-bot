let timeout_id;
const update_dictionary = async (dictionary_id, name) => {
	clearTimeout(timeout_id);
	timeout_id = setTimeout(async () => {
		await auth_axios.put(`/dictionaries/${dictionary_id}`, { name });
	}, 1000);
};

const delete_word = async (dictionary_id, word_id) => {
	const index = window.dictionary.words.findIndex((word) => word && word.id === word_id);
	delete window.dictionary.words[index];
	await auth_axios.delete(`/words/${dictionary_id}/${word_id}`);
};

const add_word = async (dictionary_id, formData) => {
	const { data } = await auth_axios.post(`/words/${dictionary_id}`, formData);
	window.dictionary.words.push(data);
};

const add_word_to_html = (word) => {
	const words_content = document.querySelector(".words__content");
	const word_element = document.createElement("div");
	word_element.classList.add("word__content");
	word_element.setAttribute("key", word.id);

	word_element.innerHTML = `
			<div class="word__text">
				${word.word}<br>${word.translate}
			</div>
			<div class="word__buttons">
				<span class="material-symbols-outlined" onclick="delete_word(${window.dictionary.id}, ${word.id})">
					delete
				</span>
			</div>
		`;

	words_content.appendChild(word_element);
};

const remove_word_from_html = (word_id) => {
	const words_content = document.querySelector(".words__content");
	const element = document.querySelector(`[key="${word_id}"]`);
	element.classList.add("disappearance");

	const scrollPosition = words_content.scrollTop;
	const scrollHeight = words_content.scrollHeight;
	const containerHeight = words_content.clientHeight;

	const distanceToBottom = scrollHeight - containerHeight - scrollPosition;
	if (distanceToBottom < 80) {
		words_content.scrollTop = words_content.scrollTop - 80;
	}

	setTimeout(() => element.remove(), 200);
};
