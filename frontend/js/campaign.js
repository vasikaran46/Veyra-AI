/* ===================================================
   VEYRA AI — NAVIGATION & SECONDARY VIEWS
   Manages Campaigns, Content Library, History, Brand Memory, and Settings
   =================================================== */

const NavigationManager = {
  currentView: 'workspace',

  init() {
    this.bindEvents();
  },

  bindEvents() {
    document.querySelectorAll('.nav-item').forEach(item => {
      item.addEventListener('click', () => {
        const view = item.getAttribute('data-view');
        if (view) this.switchView(view);
      });
    });

    // Content library search & filter listeners
    const libSearch = document.getElementById('lib-search-input');
    const libTypeFilter = document.getElementById('lib-type-filter');
    const libPlatformFilter = document.getElementById('lib-platform-filter');

    if (libSearch) libSearch.addEventListener('input', () => this.loadContentLibrary());
    if (libTypeFilter) libTypeFilter.addEventListener('change', () => this.loadContentLibrary());
    if (libPlatformFilter) libPlatformFilter.addEventListener('change', () => this.loadContentLibrary());

    // Brand memory save
    const saveBrandBtn = document.getElementById('btn-save-brand');
    if (saveBrandBtn) saveBrandBtn.addEventListener('click', () => this.saveBrandMemory());

    // Settings save
    const saveSettingsBtn = document.getElementById('btn-save-settings');
    if (saveSettingsBtn) saveSettingsBtn.addEventListener('click', () => this.saveSettings());
  },

  switchView(viewName) {
    this.currentView = viewName;

    // Update nav active states
    document.querySelectorAll('.nav-item').forEach(item => {
      if (item.getAttribute('data-view') === viewName) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });

    // Toggle view containers
    document.querySelectorAll('.app-view').forEach(view => {
      if (view.id === `view-${viewName}`) {
        view.style.display = 'flex';
      } else {
        view.style.display = 'none';
      }
    });

    // Toggle prompt dock & context inspector visibility
    const promptDock = document.querySelector('.prompt-dock-wrapper');
    const inspector = document.querySelector('.app-inspector');

    if (viewName === 'workspace') {
      if (promptDock) promptDock.style.display = 'flex';
      if (inspector) inspector.style.display = 'flex';
    } else {
      if (promptDock) promptDock.style.display = 'none';
      if (inspector) inspector.style.display = 'none';
    }

    // Refresh view data
    if (viewName === 'campaigns') this.loadCampaignsList();
    if (viewName === 'library') this.loadContentLibrary();
    if (viewName === 'history') this.loadHistory();
    if (viewName === 'brand') this.loadBrandMemory();
    if (viewName === 'settings') this.loadSettings();
  },

  async loadCampaignsList() {
    const container = document.getElementById('campaigns-list-container');
    if (!container) return;

    try {
      const list = await API.getCampaigns();
      if (!list || list.length === 0) {
        container.innerHTML = '<p class="text-muted">No campaigns found.</p>';
        return;
      }

      container.innerHTML = list.map(camp => `
        <div class="asset-card" style="padding:1.25rem; display:flex; flex-direction:column; gap:0.75rem;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <h3 style="font-size:1.05rem;">${camp.title}</h3>
            <span class="badge ${camp.status === 'CAMPAIGN_READY' ? 'badge-approved' : 'badge-ready'}">${camp.status}</span>
          </div>
          <p style="font-size:0.85rem; color:var(--color-text-secondary);">${camp.context.objective}</p>
          <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
            <span class="badge badge-neutral">${camp.context.language}</span>
            <span class="badge badge-neutral">${camp.assets.length} Assets</span>
            <span class="badge badge-neutral">${camp.context.region || 'Global'}</span>
          </div>
          <div style="margin-top:auto; padding-top:0.5rem; display:flex; justify-content:flex-end;">
            <button class="btn btn-primary btn-sm" onclick="NavigationManager.openCampaignInWorkspace('${camp.id}')">
              <span>Open in Workspace</span>
            </button>
          </div>
        </div>
      `).join('');
    } catch (e) {
      container.innerHTML = `<p class="text-muted">Error loading campaigns: ${e.message}</p>`;
    }
  },

  async openCampaignInWorkspace(campId) {
    try {
      const camp = await API.getCampaign(campId);
      Workspace.render(camp);
      this.switchView('workspace');
      Toast.show(`Opened "${camp.title}" in workspace`, 'info');
    } catch (e) {
      Toast.show(`Error: ${e.message}`, 'error');
    }
  },

  async loadContentLibrary() {
    const container = document.getElementById('library-assets-container');
    if (!container) return;

    const search = document.getElementById('lib-search-input')?.value || '';
    const type = document.getElementById('lib-type-filter')?.value || '';
    const platform = document.getElementById('lib-platform-filter')?.value || '';

    try {
      const assets = await API.getAssets({ search, asset_type: type, platform });
      if (!assets || assets.length === 0) {
        container.innerHTML = '<p class="text-muted" style="grid-column:1/-1; text-align:center; padding:2rem;">No matching assets in content library.</p>';
        return;
      }

      container.innerHTML = assets.map(ast => Workspace.createAssetCardHTML(ast)).join('');
      assets.forEach(ast => {
        if (ast.type === 'AUDIO') Workspace.initAudioWaveform(ast);
      });
    } catch (e) {
      container.innerHTML = `<p class="text-muted">Error: ${e.message}</p>`;
    }
  },

  async loadHistory() {
    const container = document.getElementById('history-timeline-container');
    if (!container) return;

    try {
      const history = await API.getHistory();
      if (!history || history.length === 0) {
        container.innerHTML = '<p class="text-muted">No generation history recorded.</p>';
        return;
      }

      container.innerHTML = history.map(item => `
        <div class="asset-card" style="padding:1.25rem; display:flex; justify-content:space-between; align-items:center;">
          <div>
            <h4 style="font-size:0.95rem; font-weight:600;">${item.title}</h4>
            <p style="font-size:0.8rem; color:var(--color-text-dim); margin-top:0.2rem;">${item.objective}</p>
            <div style="display:flex; gap:0.5rem; margin-top:0.5rem;">
              <span class="badge badge-neutral">${item.language}</span>
              <span class="badge badge-neutral">${item.asset_count} Assets</span>
              <span class="mono" style="font-size:0.75rem; color:var(--color-text-dim);">${new Date(item.created_at).toLocaleString()}</span>
            </div>
          </div>
          <button class="btn btn-secondary btn-sm" onclick="NavigationManager.openCampaignInWorkspace('${item.campaign_id}')">
            <span>Reopen</span>
          </button>
        </div>
      `).join('');
    } catch (e) {
      container.innerHTML = `<p class="text-muted">Error: ${e.message}</p>`;
    }
  },

  async loadBrandMemory() {
    try {
      const brand = await API.getBrand();
      const nameInput = document.getElementById('brand-name-input');
      const descInput = document.getElementById('brand-desc-input');
      const toneInput = document.getElementById('brand-tone-input');
      const guidelinesInput = document.getElementById('brand-guidelines-input');
      const colorInput = document.getElementById('brand-color-input');

      if (nameInput) nameInput.value = brand.name || '';
      if (descInput) descInput.value = brand.description || '';
      if (toneInput) toneInput.value = (brand.voice_tone || []).join(', ');
      if (guidelinesInput) guidelinesInput.value = brand.guidelines || '';
      if (colorInput) colorInput.value = brand.primary_color || '#7C3AED';
    } catch (e) {
      console.warn('Could not load brand memory:', e);
    }
  },

  async saveBrandMemory() {
    const data = {
      name: document.getElementById('brand-name-input')?.value || '',
      description: document.getElementById('brand-desc-input')?.value || '',
      voice_tone: (document.getElementById('brand-tone-input')?.value || '').split(',').map(s => s.trim()),
      guidelines: document.getElementById('brand-guidelines-input')?.value || '',
      primary_color: document.getElementById('brand-color-input')?.value || '#7C3AED'
    };

    try {
      await API.updateBrand(data);
      Toast.show('Brand Memory saved! Will be inherited across future generations.', 'success');
    } catch (e) {
      Toast.show(`Error: ${e.message}`, 'error');
    }
  },

  async loadSettings() {
    try {
      const cfg = await API.getSystemConfig();
      const demoToggle = document.getElementById('setting-demo-toggle');
      const groqStatus = document.getElementById('setting-groq-status');
      const replicateStatus = document.getElementById('setting-replicate-status');

      if (demoToggle) demoToggle.checked = cfg.demo_mode;
      if (groqStatus) {
        groqStatus.textContent = cfg.has_groq ? 'Connected (Live)' : 'Not Configured (Demo Mode Active)';
        groqStatus.style.color = cfg.has_groq ? 'var(--color-success)' : 'var(--color-warning)';
      }
      if (replicateStatus) {
        replicateStatus.textContent = cfg.has_replicate ? 'Connected (Live)' : 'Not Configured (Demo Mode Active)';
        replicateStatus.style.color = cfg.has_replicate ? 'var(--color-success)' : 'var(--color-warning)';
      }
    } catch (e) {
      console.warn('Could not load system config:', e);
    }
  },

  async saveSettings() {
    const demoMode = document.getElementById('setting-demo-toggle')?.checked;
    try {
      await API.updateSystemConfig({ demo_mode: demoMode });
      Toast.show('System settings updated!', 'success');
    } catch (e) {
      Toast.show(`Error: ${e.message}`, 'error');
    }
  }
};
