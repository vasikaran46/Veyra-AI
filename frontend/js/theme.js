/* ===================================================
   VEYRA AI — THEME SYSTEM
   Light (Warm Beige/Brown), Dark (Obsidian Glass), System
   =================================================== */

const ThemeManager = {
  currentTheme: 'dark',

  init() {
    const saved = localStorage.getItem('veyra_theme') || 'dark';
    this.setTheme(saved, false);
    
    // Listen to system preference changes if in system mode
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
      if (this.currentTheme === 'system') {
        this.applyThemeToDOM(e.matches ? 'dark' : 'light');
      }
    });
  },

  setTheme(theme, save = true) {
    this.currentTheme = theme;
    if (save) {
      localStorage.setItem('veyra_theme', theme);
    }

    if (theme === 'system') {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      this.applyThemeToDOM(prefersDark ? 'dark' : 'light');
    } else {
      this.applyThemeToDOM(theme);
    }
    this.updateToggleUI();
  },

  applyThemeToDOM(resolvedTheme) {
    document.documentElement.setAttribute('data-theme', resolvedTheme);
  },

  toggle() {
    const next = this.currentTheme === 'dark' ? 'light' : 'dark';
    this.setTheme(next);
  },

  updateToggleUI() {
    const btns = document.querySelectorAll('.theme-toggle-btn');
    btns.forEach(btn => {
      const icon = btn.querySelector('.theme-icon');
      if (icon) {
        if (this.currentTheme === 'dark') {
          icon.innerHTML = '🌙';
          btn.setAttribute('title', 'Switch to Warm Beige (Light Mode)');
        } else {
          icon.innerHTML = '☀️';
          btn.setAttribute('title', 'Switch to Obsidian Glass (Dark Mode)');
        }
      }
    });
  }
};
