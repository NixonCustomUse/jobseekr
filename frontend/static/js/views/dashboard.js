const DashboardView = {
  async render() {
    return `
      <div id="view-dashboard" class="view">
        <div class="view-header">
          <h1>JobSeekr</h1>
          <button class="btn btn-sm btn-outline" onclick="App.logout()">Logout</button>
        </div>
        <div class="section">
          <div class="stats-grid" id="stats-grid">
            <div class="stat-card primary">
              <div class="num" id="stat-total">-</div>
              <div class="label">Jobs Available</div>
            </div>
            <div class="stat-card outline">
              <div class="num" id="stat-applied">-</div>
              <div class="label">Applied</div>
            </div>
          </div>
        </div>
        <div class="section">
          <div class="section-title">
            <span>Latest Jobs</span>
            <span class="see-all" onclick="Router.go('jobs')">See All</span>
          </div>
          <div id="recent-jobs"></div>
        </div>
      </div>
    `;
  },

  async afterRender() {
    this.loadStats();
    this.loadRecentJobs();
  },

  async loadStats() {
    try {
      const [apps, status] = await Promise.all([
        API.listApplications(),
        API.scrapeStatus(),
      ]);
      document.getElementById('stat-applied').textContent = apps.length;
      document.getElementById('stat-total').textContent = status.total_jobs;
    } catch {}
  },

  async loadRecentJobs() {
    const container = document.getElementById('recent-jobs');
    container.innerHTML = '<div class="loading"><div class="spinner"></div><p>Loading jobs...</p></div>';
    try {
      const jobs = await API.listJobs('餐饮');
      if (jobs.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>No jobs yet. Trigger a scrape first.</p></div>';
        return;
      }
      container.innerHTML = jobs.slice(0, 5).map(j => this.jobCard(j)).join('');
      container.querySelectorAll('.job-card').forEach(card => {
        card.addEventListener('click', () => Router.go('job-' + card.dataset.id));
      });
    } catch {
      container.innerHTML = '<div class="empty-state"><p>Failed to load jobs.</p></div>';
    }
  },

  jobCard(j) {
    return `
      <div class="job-card" data-id="${j.id}">
        <div class="company">${j.company || 'Company'}</div>
        <div class="title">${j.title}</div>
        <div class="meta">
          <span>
            <svg viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            ${j.location || 'Malaysia'}
          </span>
          <span>
            <svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            ${j.posted_at ? new Date(j.posted_at).toLocaleDateString() : 'Recent'}
          </span>
        </div>
      </div>
    `;
  }
};
