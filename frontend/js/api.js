/* ===================================================
   VEYRA AI — API CLIENT
   Communicates with FastAPI backend REST endpoints
   =================================================== */

const API = {
  baseUrl: '',

  async getHealth() {
    const res = await fetch(`${this.baseUrl}/health`);
    return await res.json();
  },

  async getSystemConfig() {
    const res = await fetch(`${this.baseUrl}/api/system/config`);
    return await res.json();
  },

  async updateSystemConfig(data) {
    const res = await fetch(`${this.baseUrl}/api/system/config`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await res.json();
  },

  async getCampaigns() {
    const res = await fetch(`${this.baseUrl}/api/campaigns`);
    return await res.json();
  },

  async getCampaign(id = 'default') {
    const res = await fetch(`${this.baseUrl}/api/campaigns/${id}`);
    if (!res.ok) throw new Error('Campaign not found');
    return await res.json();
  },

  async approveAllCampaign(id) {
    const res = await fetch(`${this.baseUrl}/api/campaigns/${id}/approve-all`, {
      method: 'POST'
    });
    return await res.json();
  },

  async generate(data) {
    const res = await fetch(`${this.baseUrl}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Generation failed to start');
    }
    return await res.json();
  },

  async pollGenerationJob(jobId) {
    const res = await fetch(`${this.baseUrl}/api/generate/${jobId}`);
    return await res.json();
  },

  async getAssets(params = {}) {
    const query = new URLSearchParams(params).toString();
    const res = await fetch(`${this.baseUrl}/api/assets?${query}`);
    return await res.json();
  },

  async updateAsset(id, data) {
    const res = await fetch(`${this.baseUrl}/api/assets/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await res.json();
  },

  async approveAsset(id) {
    const res = await fetch(`${this.baseUrl}/api/assets/${id}/approve`, {
      method: 'POST'
    });
    return await res.json();
  },

  async regenerateAsset(id, feedback = '') {
    const res = await fetch(`${this.baseUrl}/api/assets/${id}/regenerate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ feedback })
    });
    return await res.json();
  },

  async translateAsset(id, targetLanguage) {
    const res = await fetch(`${this.baseUrl}/api/assets/${id}/translate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ target_language: targetLanguage })
    });
    return await res.json();
  },

  async getBrand() {
    const res = await fetch(`${this.baseUrl}/api/brand`);
    return await res.json();
  },

  async updateBrand(data) {
    const res = await fetch(`${this.baseUrl}/api/brand`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await res.json();
  },

  async getHistory() {
    const res = await fetch(`${this.baseUrl}/api/history`);
    return await res.json();
  }
};
