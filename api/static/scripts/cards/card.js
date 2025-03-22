let isDragging = false;
let isMove = false;
let startX = 0;
let isActive = false;

const onDragStart = (e, card, variantNo, variantYes) => {
	if (isActive) return;
	isDragging = true;
	startX = e.touches ? e.touches[0].clientX : e.clientX;

	toggleDraggingClass(card, variantNo, variantYes);
};

const onDragMove = (e, card, variantNo, variantYes) => {
	if (!isDragging || isActive) return;

	const offsetX = getOffsetX(e);

	if (Math.abs(offsetX) > 5 || isMove) {
		if (!isMove) isMove = true;
		card.style.transform = `translateX(${offsetX}px) rotate(${offsetX / 15}deg)`;
	}
	updateVariantStyles(variantNo, variantYes, undefined, undefined, offsetX);
};

const onDragEnd = (e, card, cardFront, cardBack, variantNo, variantYes) => {
	if (!isDragging || isActive) return;
	isDragging = false;
	toggleDraggingClass(card, variantNo, variantYes);
	card.style.transform = "none";
	updateVariantStyles(variantNo, variantYes);
	const offsetX = getOffsetX(e);
	if (offsetX >= 100) onChange(card, cardFront, cardBack, false);
	else if (offsetX <= -100) onChange(card, cardFront, cardBack, true);
	setTimeout(() => {
		isMove = false;
	}, 200);
};

const onClick = (card) => {
	if (isMove) return;
	card.classList.toggle("active");
	isActive = card.classList.contains("active");
};

const onChange = (card, cardFront, cardBack, know = null) => {
	const word_id = card.getAttribute("data-id");
	if (word_id) {
		auth_axios.put(`/words/${dictionary.id}/${word_id}`, { know });
		window.dictionary.words = window.dictionary.words.filter((word) => word.id != word_id);
	}
	if (window.dictionary.words.length > 0) {
		card.setAttribute("data-id", window.dictionary.words[0].id);
		cardFront.innerHTML = `${window.dictionary.words[0].word}`;
		cardBack.innerHTML = `<span>${window.dictionary.words[0].translate}</span>`;
	} else {
		card.removeAttribute("data-id");
		cardFront.innerHTML = `That's all`;
		cardBack.innerHTML = `<span>На этом все</span>`;
	}
};

const updateVariantStyles = (variantNo, variantYes, param = undefined, value = undefined, offsetX = 0) => {
	if (param && value) {
		variantNo.style["param"] = value;
		variantYes.style["param"] = value;
	} else if (offsetX > 5) {
		variantNo.style.opacity = "1";
		variantYes.style.opacity = "0";
		variantNo.style.transform = `translateX(${-Math.min(offsetX, 125)}px)`;
	} else if (offsetX < -5) {
		variantNo.style.opacity = "0";
		variantYes.style.opacity = "1";
		variantYes.style.transform = `translateX(${-Math.max(offsetX, -125)}px)`;
	} else {
		variantNo.style.opacity = "0";
		variantYes.style.opacity = "0";

		variantNo.style.transform = "none";
		variantYes.style.transform = "none";
	}
};
const getOffsetX = (e) => {
	if (e.touches && e.touches.length > 0) {
		return e.touches[0].clientX - startX;
	} else if (e.changedTouches && e.changedTouches.length > 0) {
		return e.changedTouches[0].clientX - startX;
	} else {
		return e.clientX - startX;
	}
};
const toggleDraggingClass = (...items) => {
	for (i of items) {
		i.classList.toggle("dragging_on");
	}
};
