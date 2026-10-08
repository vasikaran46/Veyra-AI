/* ===================================================
   VEYRA AI — MAIN APPLICATION ORCHESTRATOR
   Initializes subsystems, toasts, and binds interactions
   =================================================== */

const Toast = {
  container: null,

  init() {
    this.container = document.getElementById('toast-container');
    if (!this.container) {
      this.container = document.createElement('div');
      this.container.id = 'toast-container';
      this.container.className = 'toast-container';
      document.body.appendChild(this.container);
    }
  },

  show(message, type = 'info') {
    if (!this.container) this.init();

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    const icon = type === 'success' ? '✓' : (type === 'error' ? '⚠' : 'ℹ');
    toast.innerHTML = `<span style="font-weight:700;">${icon}</span><span>${message}</span>`;
    this.container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(-10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }
};

document.addEventListener('DOMContentLoaded', async () => {
  Toast.init();
  ThemeManager.init();
  await I18n.init();

  Workspace.init();
  GenerationManager.init();
  ReviewModal.init();
  NavigationManager.init();

  // Bind Asset Platform Tabs
  document.querySelectorAll('.asset-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.asset-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      Workspace.activeTab = tab.getAttribute('data-tab') || 'all';
      if (Workspace.currentCampaign) {
        Workspace.renderAssets(Workspace.currentCampaign.assets);
      }
    });
  });

  // Bind Asset Type Filter Chips
  document.querySelectorAll('.asset-type-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      document.querySelectorAll('.asset-type-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      Workspace.activeTypeFilter = chip.getAttribute('data-type') || 'all';
      if (Workspace.currentCampaign) {
        Workspace.renderAssets(Workspace.currentCampaign.assets);
      }
    });
  });

  // Bind Theme toggle buttons
  document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
    btn.addEventListener('click', () => ThemeManager.toggle());
  });

  // Bind Language selector dropdowns
  document.querySelectorAll('.locale-select').forEach(select => {
    select.addEventListener('change', (e) => {
      I18n.setLocale(e.target.value);
    });
  });

  // Bind Export Campaign Package button
  const exportBtn = document.getElementById('btn-export-campaign');
  if (exportBtn) {
    exportBtn.addEventListener('click', () => {
      Toast.show('Packaging coordinated campaign assets (Text, Visuals, Reel & Audio)...', 'info');
      setTimeout(() => {
        Toast.show('Campaign package ready! Download initiated.', 'success');
      }, 1200);
    });
  }

  // Load and render initial campaign from backend
  try {
    const defaultCamp = await API.getCampaign('default');
    Workspace.render(defaultCamp);
  } catch (e) {
    console.warn('Could not fetch default campaign, using offline demo:', e);
  }

  // Inspect system status for UI badge
  try {
    const cfg = await API.getSystemConfig();
    const modeBadge = document.getElementById('nav-mode-badge');
    if (modeBadge) {
      if (cfg.demo_mode) {
        modeBadge.className = 'badge badge-ready';
        modeBadge.textContent = I18n.t('app.demo_badge', 'DEMO MODE');
      } else {
        modeBadge.className = 'badge badge-approved';
        modeBadge.textContent = I18n.t('app.live_badge', 'AI LIVE');
      }
    }
  } catch (e) {
    console.warn('Could not fetch system config:', e);
  }
});
