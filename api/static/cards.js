document.addEventListener("DOMContentLoaded", () => {
    axios.post("/auth", { data: window.Telegram.WebApp.initData });

    const card = document.querySelector(".card");

    const variantNo = document.querySelector(".variants__no");
    const variantYes = document.querySelector(".variants__yes");

    const cardFront = document.querySelector(".card__front");
    const cardBack = document.querySelector(".card__back");

    let isDragging = false;
    let isMove = false;
    let startX = 0;

    const updateTheme = () => {
        const isDarkTheme = window.Telegram.WebApp.colorScheme === "dark";
        if (isDarkTheme) {
            cardFront.style.background = "#F0FFFFFF";
            cardFront.style.color = "#767e7e";

            cardBack.style.color = "#F0FFFFFF";

            variantNo.style.color = "#F0FFFFFF";
            variantYes.style.color = "#F0FFFFFF";
        } else {
            cardFront.style.background = "#5553ce";
            cardFront.style.color = "#a7a5ff";

            cardBack.style.color = "#1c1c44";

            variantNo.style.color = "#1c1c44";
            variantYes.style.color = "#1c1c44";
        }
    };

    const onDragStart = (e) => {
        if (card.classList.contains("active")) return;
        isDragging = true;
        startX = e.touches ? e.touches[0].clientX : e.clientX;
    };

    const onDragMove = (e) => {
        if (!isDragging || card.classList.contains("active")) return;

        const currentX = e.touches ? e.touches[0].clientX : e.clientX;
        const offsetX = currentX - startX;

        isMove = true;
        card.style.transform = `translateX(${offsetX}px) rotate(${offsetX / 15}deg)`;
        if (offsetX > 3) {
            variantNo.style.opacity = "1";
            variantYes.style.opacity = "0";
            variantNo.style.transform = `translateX(${-Math.min(offsetX, 125)}px)`;
        } else if (offsetX < -3) {
            variantNo.style.opacity = "0";
            variantYes.style.opacity = "1";
            variantYes.style.transform = `translateX(${-Math.max(offsetX, -125)}px)`;
        }
    };

    const onDragEnd = () => {
        if (!isDragging || card.classList.contains("active")) return;
        isDragging = false;

        card.style.transition = "all 0.2s ease";
        card.style.transform = "none";

        variantNo.style.transition = "all .1s ease";
        variantNo.style.transform = "none";
        variantNo.style.opacity = "0";
        variantYes.style.transition = "all .1s ease";
        variantYes.style.transform = "none";
        variantYes.style.opacity = "0";

        setTimeout(() => {
            variantNo.style.transition = "none";
            variantYes.style.transition = "none";
            card.style.transition = "none";
            isMove = false;
        }, 200);
    };

    const onClick = () => {
        if (isMove) return;
        card.classList.toggle("active");
    };

    // Обработчики событий
    card.addEventListener("mousedown", onDragStart);
    document.addEventListener("mousemove", onDragMove);
    document.addEventListener("mouseup", onDragEnd);

    card.addEventListener("touchstart", onDragStart, { passive: true });
    document.addEventListener("touchmove", onDragMove, { passive: true });
    document.addEventListener("touchend", onDragEnd);

    card.addEventListener("click", onClick);

    // Обновить тему
    updateTheme();
    window.Telegram.WebApp.onEvent("themeChanged", updateTheme);
});
