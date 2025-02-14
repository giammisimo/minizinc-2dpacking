// Cookie management functions
function setCookie(name, value, days) {
    const d = new Date();
    d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = "expires=" + d.toUTCString();
    document.cookie = `${name}=${value};${expires};path=/`;
}

function getCookie(name) {
    const cname = name + "=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const cookieArray = decodedCookie.split(';');
    for (let i = 0; i < cookieArray.length; i++) {
        let c = cookieArray[i].trim();
        if (c.indexOf(cname) === 0) {
            return c.substring(cname.length, c.length);
        }
    }
    return "";
}

// Dark mode functionality
function applyDarkMode(isDark) {
    if (isDark) {
        document.documentElement.style.setProperty('--background-color', '#333');
        document.documentElement.style.setProperty('--text-color', '#ddd');
        document.documentElement.style.setProperty('--form-background', '#444');
        document.documentElement.style.setProperty('--input-text-color', '#fff');
        document.documentElement.style.setProperty('--shadow-light', '#555');
        document.documentElement.style.setProperty('--shadow-dark', '#222');
    } else {
        document.documentElement.style.setProperty('--background-color', '#e0e0e0');
        document.documentElement.style.setProperty('--text-color', '#555');
        document.documentElement.style.setProperty('--form-background', '#e0e0e0');
        document.documentElement.style.setProperty('--input-text-color', '#000');
        document.documentElement.style.setProperty('--shadow-light', '#ffffff');
        document.documentElement.style.setProperty('--shadow-dark', '#bebebe');
    }
    // Update toggle state
    document.getElementById('darkModeToggle').checked = isDark;
}

// Initialize dark mode
document.addEventListener('DOMContentLoaded', () => {
    const darkModeToggle = document.getElementById('darkModeToggle');
    
    // Check cookie on startup
    const darkModeCookie = getCookie("darkMode");
    if (darkModeCookie) {
        applyDarkMode(darkModeCookie === "true");
    }

    // Event listener for mode change
    darkModeToggle.addEventListener('change', () => {
        const isDark = darkModeToggle.checked;
        applyDarkMode(isDark);
        setCookie("darkMode", isDark, 7);
    });
});