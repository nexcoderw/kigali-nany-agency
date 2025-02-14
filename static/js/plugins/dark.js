(() => {
  'use strict';

  const THEME_KEY = 'theme'; // Key for local storage
  const DEFAULT_THEME = 'light'; // Default theme is now always light

  // Retrieves the theme from local storage
  const getStoredTheme = () => localStorage.getItem(THEME_KEY);

  // Stores the theme in local storage
  const setStoredTheme = theme => localStorage.setItem(THEME_KEY, theme);

  // Sets the theme on the document
  const setTheme = theme => {
      document.documentElement.setAttribute('data-bs-theme', theme);
  };

  // Initialize theme based on local storage or default to light
  const initTheme = () => {
      const storedTheme = getStoredTheme();
      setTheme(storedTheme || DEFAULT_THEME);
  };

  // Handles user-initiated theme changes
  const handleThemeChange = () => {
      document.querySelectorAll('[data-bs-theme-value]').forEach(button => {
          button.addEventListener('click', () => {
              const newTheme = button.getAttribute('data-bs-theme-value');
              setStoredTheme(newTheme);
              setTheme(newTheme);
          });
      });
  };

  // Setup event listeners and initialize theme on document load
  window.addEventListener('DOMContentLoaded', () => {
      initTheme();
      handleThemeChange();
  });

  // Update theme if system preference changes and no user preference is set
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
      if (!getStoredTheme()) { // Only react to system changes if no theme has been set by user
          setTheme(e.matches ? 'dark' : DEFAULT_THEME);
      }
  });
})();
