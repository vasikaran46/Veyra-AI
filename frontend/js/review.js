/* ===================================================
   VEYRA AI — REVIEW & REFINEMENT MODALS
   Handles lightweight asset editing, regeneration, and translation
   =================================================== */

const ReviewModal = {
  currentAssetId: null,

  init() {
    this.bindEvents();
  },

  bindEvents() {
    // Close modals on overlay or close button click
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
          this.closeAll();
        }
      });
    });

    document.querySelectorAll('.modal-close-btn').forEach(btn => {
      btn.addEventListener('click', () => this.closeAll());
    });

    // Save Edit
    const saveEditBtn = document.getElementById('btn-save-edit');
    if (saveEditBtn) {
      saveEditBtn.addEventListener('click', () => this.saveEdit());
    }

    // Submit Regenerate
    const submitRegenBtn = document.getElementById('btn-submit-regenerate');
    if (submitRegenBtn) {
      submitRegenBtn.addEventListener('click', () => this.submitRegenerate());
    }

    // Submit Translate
    const submitTransBtn = document.getElementById('btn-submit-translate');
    if (submitTransBtn) {
      submitTransBtn.addEventListener('click', () => this.submitTranslate());
    }
  },

  closeAll() {
    document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('active'));
    this.currentAssetId = null;
  },

  openEdit(assetId) {
    this.currentAssetId = assetId;
    const ast = this.getAsset(assetId);
    if (!ast) return;

    const modal = document.getElementById('modal-edit-asset');
    const titleEl = document.getElementById('edit-modal-title');
    const contentArea = document.getElementById('edit-content-field');
    const ctaField = document.getElementById('edit-cta-field');
    const hookField = document.getElementById('edit-hook-field');

    if (titleEl) titleEl.textContent = `Edit Asset: ${ast.title}`;

    if (contentArea) contentArea.value = ast.content || ast.prompt || ast.audio_transcript || '';
    if (ctaField) {
      ctaField.value = ast.call_to_action || '';
      ctaField.parentElement.style.display = ast.type === 'TEXT' ? 'flex' : 'none';
    }
    if (hookField) {
      hookField.value = ast.hook || '';
      hookField.parentElement.style.display = ast.type === 'TEXT' ? 'flex' : 'none';
    }

    if (modal) modal.classList.add('active');
  },

  async saveEdit() {
    if (!this.currentAssetId) return;
    const content = document.getElementById('edit-content-field')?.value || '';
    const cta = document.getElementById('edit-cta-field')?.value || '';
    const hook = document.getElementById('edit-hook-field')?.value || '';

    try {
      const updated = await API.updateAsset(this.currentAssetId, {
        content: content,
        call_to_action: cta,
        hook: hook,
        prompt: content,
        edit_notes: "Edited by creator"
      });

      this.updateLocalAsset(updated);
      Toast.show('Asset updated successfully!', 'success');
      this.closeAll();
    } catch (e) {
      Toast.show(`Update failed: ${e.message}`, 'error');
    }
  },

  openRegenerate(assetId) {
    this.currentAssetId = assetId;
    const ast = this.getAsset(assetId);
    if (!ast) return;

    const modal = document.getElementById('modal-regenerate-asset');
    const titleEl = document.getElementById('regen-modal-title');
    const feedbackInput = document.getElementById('regen-feedback-input');

    if (titleEl) titleEl.textContent = `Regenerate: ${ast.title}`;
    if (feedbackInput) feedbackInput.value = '';

    if (modal) modal.classList.add('active');
  },

  async submitRegenerate() {
    if (!this.currentAssetId) return;
    const feedback = document.getElementById('regen-feedback-input')?.value || '';

    try {
      Toast.show('Regenerating asset with specialized model...', 'info');
      const updated = await API.regenerateAsset(this.currentAssetId, feedback);
      this.updateLocalAsset(updated);
      Toast.show('Asset successfully regenerated!', 'success');
      this.closeAll();
    } catch (e) {
      Toast.show(`Regeneration failed: ${e.message}`, 'error');
    }
  },

  openTranslate(assetId) {
    this.currentAssetId = assetId;
    const ast = this.getAsset(assetId);
    if (!ast) return;

    const modal = document.getElementById('modal-translate-asset');
    const titleEl = document.getElementById('translate-modal-title');

    if (titleEl) titleEl.textContent = `Translate & Localize: ${ast.title}`;

    if (modal) modal.classList.add('active');
  },

  async submitTranslate() {
    if (!this.currentAssetId) return;
    const targetLang = document.getElementById('translate-target-lang')?.value || 'Tamil';

    try {
      Toast.show(`Culturally translating asset into ${targetLang}...`, 'info');
      const updated = await API.translateAsset(this.currentAssetId, targetLang);
      this.updateLocalAsset(updated);
      Toast.show(`Asset successfully localized to ${targetLang}!`, 'success');
      this.closeAll();
    } catch (e) {
      Toast.show(`Translation failed: ${e.message}`, 'error');
    }
  },

  playVideoDemo(assetId) {
    const ast = this.getAsset(assetId);
    if (!ast) return;

    const modal = document.getElementById('modal-video-preview');
    const titleEl = document.getElementById('video-modal-title');
    const imgEl = document.getElementById('video-modal-img');

    if (titleEl) titleEl.textContent = `Cinematic Reel Preview (9:16) — ${ast.title}`;
    if (imgEl) imgEl.src = ast.media_url || '/assets/stitch_video.jpg';

    if (modal) modal.classList.add('active');
  },

  getAsset(id) {
    if (!Workspace.currentCampaign) return null;
    return Workspace.currentCampaign.assets.find(a => a.id === id);
  },

  updateLocalAsset(updated) {
    if (Workspace.currentCampaign) {
      const idx = Workspace.currentCampaign.assets.findIndex(a => a.id === updated.id);
      if (idx !== -1) {
        Workspace.currentCampaign.assets[idx] = updated;
      }
      Workspace.render(Workspace.currentCampaign);
    }
  }
};
