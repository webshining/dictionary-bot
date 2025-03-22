document.addEventListener("DOMContentLoaded", async () => {
	const card = document.querySelector(".card");
	processCard();

	card.addEventListener("mousedown", (e) => onDragStart(e));
	document.addEventListener("mousemove", (e) => onDragMove(e));
	document.addEventListener("mouseup", (e) => onDragEnd(e));

	card.addEventListener("touchstart", (e) => onDragStart(e, card, variantNo, variantYes));
	document.addEventListener("touchmove", (e) => onDragMove(e, card, variantNo, variantYes));
	document.addEventListener("touchend", (e) => onDragEnd(e, card, cardFront, cardBack, variantNo, variantYes));

	card.addEventListener("click", () => onClick());
});
