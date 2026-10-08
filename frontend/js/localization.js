/* ===================================================
   VEYRA AI — LOCALIZATION ENGINE (i18n)
   Multilingual support: English (en), Tamil (ta), Hindi (hi)
   =================================================== */

const I18n = {
  currentLocale: 'en',
  translations: {},

  async init() {
    const saved = localStorage.getItem('veyra_locale') || 'en';
    await this.setLocale(saved, false);
  },

  async loadLocale(locale) {
    if (this.translations[locale]) return this.translations[locale];
    try {
      const res = await fetch(`/locales/${locale}.json`);
      if (!res.ok) throw new Error(`Could not load locale ${locale}`);
      const data = await res.json();
      this.translations[locale] = data;
      return data;
    } catch (e) {
      console.warn(`Fallback to English locale due to error:`, e);
      if (locale !== 'en') {
        return await this.loadLocale('en');
      }
      return {};
    }
  },

  async setLocale(locale, save = true) {
    this.currentLocale = locale;
    if (save) {
      localStorage.setItem('veyra_locale', locale);
    }
    await this.loadLocale(locale);
    this.translateDOM();
    this.updateLanguageSelectorUI();

    // Trigger custom event so components can update dynamic strings
    window.dispatchEvent(new CustomEvent('localeChanged', { detail: { locale } }));
  },

  t(key, fallback = '') {
    const dict = this.translations[this.currentLocale] || this.translations['en'] || {};
    const parts = key.split('.');
    let curr = dict;
    for (const p of parts) {
      if (curr && typeof curr === 'object' && p in curr) {
        curr = curr[p];
      } else {
        return fallback || key;
      }
    }
    return typeof curr === 'string' ? curr : (fallback || key);
  },

  translateDOM() {
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(el => {
      const key = el.getAttribute('data-i18n');
      const translation = this.t(key);
      if (translation) {
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
          if (el.hasAttribute('placeholder')) {
            el.setAttribute('placeholder', translation);
          }
        } else {
          el.textContent = translation;
        }
      }
    });

    const placeholders = document.querySelectorAll('[data-i18n-placeholder]');
    placeholders.forEach(el => {
      const key = el.getAttribute('data-i18n-placeholder');
      const translation = this.t(key);
      if (translation) {
        el.setAttribute('placeholder', translation);
      }
    });
  },

  updateLanguageSelectorUI() {
    const selects = document.querySelectorAll('.locale-select');
    selects.forEach(select => {
      select.value = this.currentLocale;
    });
  }
};
