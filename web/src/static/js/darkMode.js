// Funzione per applicare il tema immediatamente
function applyThemeImmediately() {
    const theme = localStorage.getItem('theme');
    if (theme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
    }
}

// Applica il tema immediatamente, prima del caricamento del DOM
applyThemeImmediately();

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
    const toggle = document.getElementById('darkModeToggle');
    const theme = localStorage.getItem('theme');

    // Set initial theme
    if (theme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        toggle.checked = true;
    }

    // Handle theme toggle with smooth transition
    toggle.addEventListener('change', (e) => {
        if (e.target.checked) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            document.documentElement.style.setProperty('--transition-speed', '0.3s');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
            document.documentElement.style.setProperty('--transition-speed', '0.3s');
        }
    });

    // Aggiungi classe per animazioni dopo il caricamento
    document.body.classList.add('content-loaded');
});