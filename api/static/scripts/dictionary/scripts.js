document.addEventListener("DOMContentLoaded", async () => {
	window.dictionary.words.forEach(add_word_to_html);

	const words_proxy = new Proxy(window.dictionary.words, {
		get(target, prop) {
			return Reflect.get(target, prop);
		},
		set(target, prop, value) {
			if (!isNaN(prop) && target[prop] === undefined) {
				add_word_to_html(value);
			}
			return Reflect.set(target, prop, value);
		},
		deleteProperty(target, prop) {
			if (!isNaN(prop) && target[prop]) {
				const word_id = target[prop].id;
				remove_word_from_html(word_id);
			}
			return Reflect.deleteProperty(target, prop);
		},
	});

	window.dictionary.words = words_proxy;

	const create_form = document.querySelector(".create__content");
	create_form.addEventListener("submit", async (event) => {
		event.preventDefault();
		const formData = new FormData(create_form);
		create_form.reset();
		await add_word(window.dictionary.id, formData);
	});
});
