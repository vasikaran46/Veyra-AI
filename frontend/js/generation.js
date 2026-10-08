/* ===================================================
   VEYRA AI — GENERATION ORCHESTRATION CLIENT
   Handles Super Prompt Bar, background job polling, & 8-stage Stepper
   =================================================== */

const GenerationManager = {
  activeJobId: null,
  pollInterval: null,
  selectedLanguage: 'English & Tamil',
  selectedPlatforms: ['Instagram', 'LinkedIn', 'YouTube Shorts'],

  init() {
    this.bindEvents();
  },

  bindEvents() {
    const generateBtn = document.getElementById('btn-super-generate');
    const promptInput = document.getElementById('super-prompt-input');

    if (generateBtn) {
      generateBtn.addEventListener('click', () => this.handleGenerate());
    }

    if (promptInput) {
      promptInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.handleGenerate();
        }
      });
    }

    // Quick prompt suggestion chips
    document.querySelectorAll('.quick-prompt-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const text = chip.getAttribute('data-prompt');
        if (promptInput && text) {
          promptInput.value = text;
          promptInput.focus();
        }
      });
    });

    // Language selector pills in prompt bar
    document.querySelectorAll('.prompt-lang-pill').forEach(pill => {
      pill.addEventListener('click', () => {
        document.querySelectorAll('.prompt-lang-pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        this.selectedLanguage = pill.getAttribute('data-lang') || 'English & Tamil';
      });
    });
  },

  async handleGenerate() {
    const input = document.getElementById('super-prompt-input');
    if (!input) return;
    const promptText = input.value.trim();

    if (!promptText) {
      Toast.show('Please enter a campaign prompt to generate content.', 'info');
      input.focus();
      return;
    }

    const generateBtn = document.getElementById('btn-super-generate');
    if (generateBtn) {
      generateBtn.disabled = true;
      generateBtn.innerHTML = `
        <span class="animate-spin">⚙️</span>
        <span>${I18n.t('prompt.generating', 'Orchestrating...')}</span>
      `;
    }

    try {
      Toast.show('Veyra Context Engine initializing multimodal campaign...', 'info');
      this.showStepperCard();

      const jobResp = await API.generate({
        prompt: promptText,
        language: this.selectedLanguage,
        platforms: this.selectedPlatforms
      });

      this.activeJobId = jobResp.job_id;
      this.startPolling(this.activeJobId);
    } catch (e) {
      Toast.show(`Generation error: ${e.message}`, 'error');
      if (generateBtn) {
        generateBtn.disabled = false;
        generateBtn.innerHTML = `
          <span>✨</span>
          <span>${I18n.t('prompt.generate', 'Generate Campaign')}</span>
        `;
      }
    }
  },

  startPolling(jobId) {
    if (this.pollInterval) clearInterval(this.pollInterval);

    this.pollInterval = setInterval(async () => {
      try {
        const status = await API.pollGenerationJob(jobId);
        this.updateStepperUI(status);

        if (status.status === 'COMPLETED') {
          clearInterval(this.pollInterval);
          this.pollInterval = null;
          this.onGenerationComplete(status.campaign);
        } else if (status.status === 'FAILED') {
          clearInterval(this.pollInterval);
          this.pollInterval = null;
          Toast.show(`Generation failed: ${status.error || 'Unknown error'}`, 'error');
          this.resetGenerateBtn();
        }
      } catch (e) {
        console.warn('Poll error:', e);
      }
    }, 600);
  },

  showStepperCard() {
    const card = document.getElementById('workspace-stepper-card');
    if (card) {
      card.style.display = 'flex';
      card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  },

  updateStepperUI(jobData) {
    if (!jobData) return;

    const progressFill = document.getElementById('stepper-progress-fill');
    const percent = Math.round(((jobData.step_index + 1) / jobData.total_steps) * 100);
    if (progressFill) progressFill.style.width = `${percent}%`;

    const statusText = document.getElementById('stepper-current-status');
    if (statusText) statusText.textContent = `${jobData.current_step} (${percent}%)`;

    (jobData.steps || []).forEach(step => {
      const nodeEl = document.getElementById(`step-node-${step.index}`);
      if (nodeEl) {
        nodeEl.className = `step-node ${step.status}`;
        const icon = nodeEl.querySelector('.step-node-icon');
        if (icon) {
          if (step.status === 'completed') {
            icon.innerHTML = '✓';
          } else if (step.status === 'in_progress') {
            icon.innerHTML = '';
          } else {
            icon.innerHTML = '○';
          }
        }
      }
    });
  },

  onGenerationComplete(campaign) {
    Toast.show('All coordinated multimodal assets generated and ready for human review!', 'success');
    this.resetGenerateBtn();
    if (campaign) {
      Workspace.render(campaign);
    }
  },

  resetGenerateBtn() {
    const generateBtn = document.getElementById('btn-super-generate');
    if (generateBtn) {
      generateBtn.disabled = false;
      generateBtn.innerHTML = `
        <span>✨</span>
        <span>${I18n.t('prompt.generate', 'Generate Campaign')}</span>
      `;
    }
  }
};
