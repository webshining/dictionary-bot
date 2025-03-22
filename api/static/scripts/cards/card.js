const card = () => document.querySelector(".card");
const cardFront = () => document.querySelector(".card__front");
const cardBack = () => document.querySelector(".card__back");
const variantNo = () => document.querySelector(".variants__no");
const variantYes = () => document.querySelector(".variants__yes");
let isMove = false;
let isDrag = false;
let isActive = false;
let lastOffsetX = 0;
let startX = 0;

const onDragStart = (e) => {
	if (isActive) return;
	startX = getOffsetX(e);
	isDrag = true;

	card().style.transition = "none";
	variantNo().style.transition = "none";
	variantYes().style.transition = "none";
};

const onDragMove = (e) => {
	if (!isDrag || isActive) return;
	const offsetX = getOffsetX(e);
	if (Math.abs(offsetX) > 5 || isMove) {
		if (!isMove) isMove = true;
		card().style.transform = `translateX(${offsetX}px) rotate(${offsetX / 15}deg)`;
		lastOffsetX = offsetX;
		if (offsetX > 0) {
			variantNo().style.opacity = 1;
			variantNo().style.transform = `translateX(${Math.max(-offsetX, -125)}px)`;
			variantYes().style.opacity = "";
			variantYes().style.transform = "";
		} else if (offsetX < 0) {
			variantNo().style.opacity = "";
			variantNo().style.transform = "";
			variantYes().style.opacity = 1;
			variantYes().style.transform = `translateX(${Math.min(-offsetX, 125)}px)`;
		} else {
			variantNo().style.opacity = "";
			variantNo().style.transform = "";
			variantYes().style.opacity = "";
			variantYes().style.transform = "";
		}
	}
};

const onDragEnd = (e) => {
	card().style.transition = "";
	card().style.transform = "";
	variantNo().style.opacity = "";
	variantNo().style.transform = "";
	variantNo().style.transition = "";
	variantYes().style.opacity = "";
	variantYes().style.transform = "";
	variantYes().style.transition = "";

	processCard();

	lastOffsetX = 0;
	startX = 0;
	isDrag = false;
	setTimeout(() => {
		isMove = false;
	}, 300);
};

const onClick = () => {
	if (isMove) return;
	isActive = !isActive;
	card().classList.toggle("active");
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

const processCard = () => {
	let know = undefined;
	if (lastOffsetX < -100) {
		know = true;
	} else if (lastOffsetX > 100) {
		know = false;
	}

	const word_id = card().getAttribute("data-id");
	if (word_id && know !== undefined) {
		console.log("A");
		auth_axios.put(`/words/${window.dictionary.id}/${card().getAttribute("data-id")}`, { know });
		window.dictionary.words = window.dictionary.words.filter((word) => word.id !== Number(word_id));
	}
	if (window.dictionary.words.length > 0) {
		card().setAttribute("data-id", window.dictionary.words[0].id);
		cardFront().innerHTML = `${window.dictionary.words[0].word}`;
		cardBack().innerHTML = `<span>${window.dictionary.words[0].translate}</span>`;
	} else {
		card().removeAttribute("data-id");
		cardFront().innerHTML = `That's all`;
		cardBack().innerHTML = `<span>На этом все</span>`;
	}
};
