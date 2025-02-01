const updateTheme = () => {
    const isDarkTheme = window.Telegram.WebApp.colorScheme === "dark";
    document.documentElement.style.setProperty("--bg", isDarkTheme ? "#F0FFFFFF" : "#5553ce");
    document.documentElement.style.setProperty("--primary", isDarkTheme ? "#F0FFFFFF" : "#1c1c44");
    document.documentElement.style.setProperty("--secondary", isDarkTheme ? "#767e7e" : "#a7a5ff");
};
