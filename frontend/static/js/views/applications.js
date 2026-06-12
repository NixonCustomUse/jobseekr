const ApplicationsView = {
  async render() {
    return `
      <div id="view-applications" class="view">
        <div class="view-header">
          <h1>Applications</h1>
          <div style="width:50px"></div>
        </div>
        <div id="apps-list">
          <div class="loading"><div class="spinner"></div><p>Loading applications...</p></div>
        </div>
      </div>
    `;
  },

  async afterRender() {
    const container = document.getElementById('apps-list');
    try {
      const apps = await API.listApplications();
      if (apps.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>No applications yet. Start applying!</p></div>';
        return;
      }
      container.innerHTML = apps.map(a => `
        <div style="padding:12px 16px">
          <div class="app-card">
            <div class="top">
              <div>
                <div class="title">${a.title}</div>
                <div class="company">${a.company || ''}</div>
              </div>
              <span class="status-badge status-${a.status}">${a.status}</span>
            </div>
            <div class="meta">${a.location || ''} · ${new Date(a.applied_at).toLocaleDateString()}</div>
          </div>
        </div>
      `).join('');
    } catch {
      container.innerHTML = '<div class="empty-state"><p>Failed to load applications.</p></div>';
    }
  },
};
