/* ===================================================
   VEYRA AI — WORKSPACE ENGINE
   Renders context banner, strategy, multimodal cards, and inspector
   =================================================== */

const Workspace = {
  currentCampaign: null,
  activeTab: 'all',
  activeTypeFilter: 'all',
  playingAudioId: null,
  audioAnimationFrames: {},

  init() {
    this.bindEvents();
  },

  bindEvents() {
    // Inspector form update
    const updateBtn = document.getElementById('btn-update-context');
    if (updateBtn) {
      updateBtn.addEventListener('click', () => this.handleContextUpdate());
    }

    // Approve all button
    const approveAllBtn = document.getElementById('btn-approve-all');
    if (approveAllBtn) {
      approveAllBtn.addEventListener('click', () => this.handleApproveAll());
    }
  },

  render(campaign) {
    this.currentCampaign = campaign;
    if (!campaign) return;

    // Header info
    const titleEl = document.getElementById('header-campaign-title');
    if (titleEl) titleEl.textContent = campaign.title || campaign.context?.subject || 'Campaign';

    const statusBadgeEl = document.getElementById('header-status-badge');
    if (statusBadgeEl) {
      const isReady = campaign.status === 'CAMPAIGN_READY';
      statusBadgeEl.className = isReady ? 'badge badge-approved' : 'badge badge-ready';
      statusBadgeEl.innerHTML = `<span class="badge-dot"></span><span>${isReady ? I18n.t('workspace.campaign_ready', 'Campaign Ready') : I18n.t('asset.ready_review', 'In Review')}</span>`;
    }

    this.renderContextBanner(campaign.context);
    this.renderStrategyPlan(campaign.strategy_plan);
    this.renderAssets(campaign.assets);
    this.syncInspector(campaign.context);
    this.checkCelebrationState();
  },

  renderContextBanner(ctx) {
    const banner = document.getElementById('workspace-context-banner');
    if (!banner || !ctx) return;

    banner.innerHTML = `
      <div class="context-banner-header">
        <span class="context-concept-pill">
          <span>⚡</span>
          <span>${I18n.t('app.concept', 'ONE CONTEXT → MULTIPLE MEDIA → ONE COORDINATED CAMPAIGN')}</span>
        </span>
        <span class="badge badge-primary">${ctx.region || 'India / Global'}</span>
      </div>
      <div class="context-grid-row">
        <div class="context-meta-item">
          <span class="context-meta-label">${I18n.t('inspector.subject', 'Subject')}</span>
          <span class="context-meta-value" title="${ctx.subject}">${ctx.subject}</span>
        </div>
        <div class="context-meta-item">
          <span class="context-meta-label">${I18n.t('inspector.objective', 'Objective')}</span>
          <span class="context-meta-value" title="${ctx.objective}">${ctx.objective}</span>
        </div>
        <div class="context-meta-item">
          <span class="context-meta-label">${I18n.t('inspector.audience', 'Audience')}</span>
          <span class="context-meta-value" title="${ctx.audience}">${ctx.audience}</span>
        </div>
        <div class="context-meta-item">
          <span class="context-meta-label">${I18n.t('inspector.language', 'Languages')}</span>
          <span class="context-meta-value">${ctx.language}</span>
        </div>
        <div class="context-meta-item">
          <span class="context-meta-label">${I18n.t('inspector.tone', 'Tone')}</span>
          <span class="context-meta-value">${Array.isArray(ctx.tone) ? ctx.tone.join(', ') : ctx.tone}</span>
        </div>
      </div>
    `;
  },

  renderStrategyPlan(plan) {
    const card = document.getElementById('workspace-strategy-card');
    if (!card) return;

    if (!plan) {
      card.style.display = 'none';
      return;
    }

    card.style.display = 'flex';
    const pillarsHtml = (plan.pillars || []).map(p => `
      <div class="strategy-pillar-item">
        <span class="strategy-pillar-bullet">✦</span>
        <span>${p}</span>
      </div>
    `).join('');

    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h4 style="font-size:0.95rem; font-weight:600; display:flex; align-items:center; gap:0.5rem;">
          <span>🎯</span>
          <span>${I18n.t('workspace.strategy_plan', 'AI Content Strategy Plan')}</span>
        </h4>
        <span class="chip">${I18n.currentLocale.toUpperCase()} Adaptation</span>
      </div>
      <p style="font-size:0.875rem; color:var(--color-text-secondary); line-height:1.5;">${plan.summary}</p>
      <div class="strategy-pillars-list">
        ${pillarsHtml}
      </div>
    `;
  },

  renderAssets(assets) {
    const grid = document.getElementById('workspace-assets-grid');
    if (!grid) return;

    if (!assets || assets.length === 0) {
      grid.innerHTML = `
        <div style="grid-column: 1/-1; text-align:center; padding: 3rem 1rem; color:var(--color-text-dim);">
          <p style="font-size:1.1rem; margin-bottom:0.5rem;">No assets generated yet.</p>
          <p style="font-size:0.85rem;">Use the Super Prompt Bar below to start generating your multimodal campaign.</p>
        </div>
      `;
      return;
    }

    // Filter assets
    const filtered = assets.filter(ast => {
      // Tab filter (Platform)
      if (this.activeTab !== 'all') {
        if (!ast.platform.toLowerCase().includes(this.activeTab.toLowerCase())) {
          return false;
        }
      }
      // Type filter
      if (this.activeTypeFilter !== 'all') {
        if (ast.type.toLowerCase() !== this.activeTypeFilter.toLowerCase()) {
          return false;
        }
      }
      return true;
    });

    if (filtered.length === 0) {
      grid.innerHTML = `
        <div style="grid-column: 1/-1; text-align:center; padding: 2.5rem; color:var(--color-text-dim);">
          <p>No assets match the selected filter.</p>
        </div>
      `;
      return;
    }

    grid.innerHTML = filtered.map(ast => this.createAssetCardHTML(ast)).join('');

    // Initialize interactive waveform visualizers for audio cards
    filtered.forEach(ast => {
      if (ast.type === 'AUDIO') {
        this.initAudioWaveform(ast);
      }
    });
  },

  createAssetCardHTML(ast) {
    const isApproved = ast.status === 'APPROVED';
    const statusClass = isApproved ? 'badge-approved' : 'badge-ready';
    const statusText = isApproved ? I18n.t('asset.approved', 'Approved') : I18n.t('asset.ready_review', 'Ready for Review');

    let bodyHTML = '';

    if (ast.type === 'TEXT') {
      bodyHTML = `
        ${ast.hook ? `<div class="text-hook-box">"${ast.hook}"</div>` : ''}
        <div class="text-copy-content">${this.escapeHTML(ast.content || '')}</div>
        ${ast.hashtags && ast.hashtags.length ? `
          <div class="text-hashtags-row">
            ${ast.hashtags.map(t => `<span class="hashtag-chip">${t}</span>`).join('')}
          </div>
        ` : ''}
        ${ast.call_to_action ? `<div class="text-cta-box"><strong>CTA:</strong> ${ast.call_to_action}</div>` : ''}
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.3rem;">
          <small class="mono text-muted">${ast.character_count || (ast.content ? ast.content.length : 0)} ${I18n.t('asset.char_count', 'chars')}</small>
          <span class="badge badge-neutral">${ast.language}</span>
        </div>
      `;
    } else if (ast.type === 'IMAGE') {
      bodyHTML = `
        <div class="image-viewport-wrapper">
          <img src="${ast.media_url || '/assets/stitch_poster.jpg'}" alt="${ast.title}" class="image-preview-element" id="img-${ast.id}" />
          ${ast.overlay_text ? `
            <div class="image-overlay-container" id="overlay-${ast.id}">
              <span class="image-overlay-pill">${ast.overlay_language || 'Localized Text'}</span>
              <p class="image-overlay-text">${ast.overlay_text}</p>
            </div>
          ` : ''}
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span class="chip" onclick="Workspace.toggleOverlay('${ast.id}')">Toggle Localized Overlay</span>
          <span class="badge badge-neutral">${ast.aspect_ratio || '4:5'}</span>
        </div>
        <p style="font-size:0.78rem; color:var(--color-text-dim); line-height:1.4;">${ast.prompt ? ast.prompt.slice(0, 110) + '...' : ''}</p>
      `;
    } else if (ast.type === 'VIDEO') {
      const subsHtml = (ast.subtitles || []).map(s => `
        <div class="subtitle-entry">
          <span class="subtitle-time">${s.start || '00:00'}</span>
          <span>${s.tamil || s.english || s.hindi}</span>
        </div>
      `).join('');

      bodyHTML = `
        <div class="video-viewport-wrapper">
          <img src="${ast.media_url || '/assets/stitch_video.jpg'}" alt="${ast.title}" class="video-preview-element" />
          <div class="video-play-overlay" onclick="ReviewModal.playVideoDemo('${ast.id}')">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
          </div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span class="badge badge-neutral">${ast.aspect_ratio || '9:16'}</span>
          <span class="mono text-muted">${ast.duration_seconds || 30}s Duration</span>
        </div>
        ${subsHtml ? `
          <div class="video-subtitles-box">
            <div style="font-weight:600; font-size:0.75rem; color:var(--color-text-muted); margin-bottom:0.2rem;">Synchronized Subtitles</div>
            ${subsHtml}
          </div>
        ` : ''}
      `;
    } else if (ast.type === 'AUDIO') {
      bodyHTML = `
        <div class="audio-card-body">
          <div class="audio-waveform-container" id="waveform-${ast.id}">
            <!-- Interactive waveform bars dynamically rendered -->
          </div>
          <div class="audio-controls-row">
            <button class="btn btn-glass btn-sm" id="btn-play-${ast.id}" onclick="Workspace.togglePlayAudio('${ast.id}')">
              <span>▶</span>
              <span id="play-text-${ast.id}">${I18n.t('asset.play', 'Play Audio')}</span>
            </button>
            <span class="mono text-muted">${ast.audio_duration || 28.5}s</span>
          </div>
          <div class="audio-transcript-box">
            "${ast.audio_transcript || 'Voice-over audio synthesized in regional Tamil accent.'}"
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <small class="text-muted">${ast.voice_name || 'Dynamic Voice Persona'}</small>
            <span class="badge badge-neutral">${ast.language}</span>
          </div>
        </div>
      `;
    }

    return `
      <div class="asset-card animate-fade-in" id="card-${ast.id}">
        <div class="asset-card-header">
          <div class="asset-meta-group">
            <span class="asset-platform-tag">${ast.platform}</span>
            <span class="badge badge-neutral">${ast.type}</span>
          </div>
          <span class="badge ${statusClass}">
            <span class="badge-dot"></span>
            <span>${statusText}</span>
          </span>
        </div>
        <h4 class="asset-card-title">${ast.title}</h4>
        <div class="asset-card-body">
          ${bodyHTML}
        </div>
        <div class="asset-card-actions">
          <div class="asset-action-btns">
            <button class="btn btn-ghost btn-sm" onclick="ReviewModal.openEdit('${ast.id}')" title="Edit Content">
              <span>✏️</span>
              <span>${I18n.t('asset.edit', 'Edit')}</span>
            </button>
            <button class="btn btn-ghost btn-sm" onclick="ReviewModal.openRegenerate('${ast.id}')" title="Regenerate with feedback">
              <span>🔄</span>
              <span>${I18n.t('asset.regenerate', 'Regenerate')}</span>
            </button>
            <button class="btn btn-ghost btn-sm" onclick="ReviewModal.openTranslate('${ast.id}')" title="Translate into another language">
              <span>🌐</span>
              <span>${I18n.t('asset.translate', 'Translate')}</span>
            </button>
          </div>
          <button class="btn ${isApproved ? 'btn-success' : 'btn-primary'} btn-sm" onclick="Workspace.approveAsset('${ast.id}')">
            <span>${isApproved ? '✓' : '●'}</span>
            <span>${isApproved ? I18n.t('asset.approved', 'Approved') : I18n.t('asset.approve', 'Approve')}</span>
          </button>
        </div>
      </div>
    `;
  },

  initAudioWaveform(ast) {
    const container = document.getElementById(`waveform-${ast.id}`);
    if (!container) return;

    const data = ast.waveform_data && ast.waveform_data.length ? ast.waveform_data : [
      0.15, 0.40, 0.70, 0.90, 0.60, 0.85, 0.35, 0.20, 0.65, 0.95, 0.80, 0.50, 0.75, 0.90, 0.45, 0.25, 0.60, 0.80, 0.70, 0.30
    ];

    container.innerHTML = data.map((val, idx) => {
      const heightPx = Math.max(6, Math.round(val * 56));
      return `<div class="waveform-bar" id="bar-${ast.id}-${idx}" style="height:${heightPx}px;"></div>`;
    }).join('');
  },

  togglePlayAudio(assetId) {
    const playBtn = document.getElementById(`btn-play-${assetId}`);
    const playText = document.getElementById(`play-text-${assetId}`);
    const isCurrentlyPlaying = this.playingAudioId === assetId;

    if (isCurrentlyPlaying) {
      // Pause
      clearInterval(this.audioAnimationFrames[assetId]);
      this.playingAudioId = null;
      if (playText) playText.textContent = I18n.t('asset.play', 'Play Audio');
      if (playBtn) playBtn.querySelector('span:first-child').textContent = '▶';
    } else {
      // If another is playing, stop it
      if (this.playingAudioId) {
        this.togglePlayAudio(this.playingAudioId);
      }
      this.playingAudioId = assetId;
      if (playText) playText.textContent = I18n.t('asset.pause', 'Pause Audio');
      if (playBtn) playBtn.querySelector('span:first-child').textContent = '⏸';

      // Waveform dancing animation
      let step = 0;
      this.audioAnimationFrames[assetId] = setInterval(() => {
        const bars = document.querySelectorAll(`[id^="bar-${assetId}-"]`);
        bars.forEach((bar, idx) => {
          const mod = Math.sin((step + idx * 0.8)) * 0.5 + 0.5;
          const h = Math.max(6, Math.round(mod * 56));
          bar.style.height = `${h}px`;
          if (idx === (step % bars.length)) {
            bar.classList.add('active');
          } else {
            bar.classList.remove('active');
          }
        });
        step++;
      }, 120);

      // Stop automatically after duration
      setTimeout(() => {
        if (this.playingAudioId === assetId) {
          this.togglePlayAudio(assetId);
        }
      }, 10000);
    }
  },

  toggleOverlay(assetId) {
    const overlay = document.getElementById(`overlay-${assetId}`);
    if (overlay) {
      overlay.style.display = overlay.style.display === 'none' ? 'flex' : 'none';
    }
  },

  async approveAsset(assetId) {
    try {
      const updated = await API.approveAsset(assetId);
      Toast.show(`Asset "${updated.title}" approved!`, 'success');

      // Update local asset
      if (this.currentCampaign) {
        const idx = this.currentCampaign.assets.findIndex(a => a.id === assetId);
        if (idx !== -1) {
          this.currentCampaign.assets[idx] = updated;
        }
        // Check if all approved
        if (this.currentCampaign.assets.every(a => a.status === 'APPROVED')) {
          this.currentCampaign.status = 'CAMPAIGN_READY';
        }
        this.render(this.currentCampaign);
      }
    } catch (e) {
      Toast.show(`Approval failed: ${e.message}`, 'error');
    }
  },

  async handleApproveAll() {
    if (!this.currentCampaign) return;
    try {
      const camp = await API.approveAllCampaign(this.currentCampaign.id);
      this.currentCampaign = camp;
      Toast.show('All campaign assets approved! Campaign is ready.', 'success');
      this.render(this.currentCampaign);
    } catch (e) {
      Toast.show(`Error: ${e.message}`, 'error');
    }
  },

  checkCelebrationState() {
    const banner = document.getElementById('workspace-celebration-banner');
    if (!banner || !this.currentCampaign) return;

    const isReady = this.currentCampaign.status === 'CAMPAIGN_READY';
    banner.style.display = isReady ? 'flex' : 'none';
  },

  syncInspector(ctx) {
    if (!ctx) return;
    const subjInput = document.getElementById('inspector-subject');
    const objInput = document.getElementById('inspector-objective');
    const audInput = document.getElementById('inspector-audience');
    const langInput = document.getElementById('inspector-language');
    const regInput = document.getElementById('inspector-region');

    if (subjInput) subjInput.value = ctx.subject || '';
    if (objInput) objInput.value = ctx.objective || '';
    if (audInput) audInput.value = ctx.audience || '';
    if (langInput) langInput.value = ctx.language || '';
    if (regInput) regInput.value = ctx.region || '';
  },

  handleContextUpdate() {
    if (!this.currentCampaign) return;
    const ctx = this.currentCampaign.context;
    ctx.subject = document.getElementById('inspector-subject').value;
    ctx.objective = document.getElementById('inspector-objective').value;
    ctx.audience = document.getElementById('inspector-audience').value;
    ctx.language = document.getElementById('inspector-language').value;
    ctx.region = document.getElementById('inspector-region').value;

    Toast.show('Context Engine parameters updated!', 'success');
    this.renderContextBanner(ctx);
  },

  escapeHTML(str) {
    const div = document.createElement('div');
    div.innerText = str;
    return div.innerHTML;
  }
};
