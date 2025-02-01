document.addEventListener("DOMContentLoaded", () => {
    window.Telegram.WebApp.ready();
    updateTheme();
    window.Telegram.WebApp.onEvent("themeChanged", updateTheme);
});
