document.addEventListener("DOMContentLoaded", () => {
    const card = document.querySelector(".card");
    const cardFront = document.querySelector(".card__front");
    const cardBack = document.querySelector(".card__back");
    const variantNo = document.querySelector(".variants__no");
    const variantYes = document.querySelector(".variants__yes");
    onChange(card, cardFront, cardBack);

    card.addEventListener("mousedown", (e) => onDragStart(e, card, variantNo, variantYes));
    document.addEventListener("mousemove", (e) => onDragMove(e, card, variantNo, variantYes));
    document.addEventListener("mouseup", (e) => onDragEnd(e, card, cardFront, cardBack, variantNo, variantYes));

    card.addEventListener("touchstart", (e) => onDragStart(e, card, variantNo, variantYes));
    document.addEventListener("touchmove", (e) => onDragMove(e, card, variantNo, variantYes));
    document.addEventListener("touchend", (e) => onDragEnd(e, card, cardFront, cardBack, variantNo, variantYes));

    card.addEventListener("click", () => onClick(card));
});
