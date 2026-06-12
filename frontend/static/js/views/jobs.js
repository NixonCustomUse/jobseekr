const JobsView = {
  jobs: [],

  async render() {
    return `
      <div id="view-jobs" class="view">
        <div class="view-header">
          <button class="back-btn" onclick="Router.go('dashboard')">
            <svg viewBox="0 0 24 24"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
            Back
          </button>
          <h1>Jobs</h1>
          <div style="width:50px"></div>
        </div>
        <div class="search-bar">
          <input class="search-input" id="job-search" type="text" placeholder="Search jobs..." oninput="JobsView.search()">
        </div>
        <div class="filter-chips" id="job-filters">
          <button class="chip active" data-cat="餐饮" onclick="JobsView.filter('餐饮')">🍽 F&B</button>
          <button class="chip" data-cat="" onclick="JobsView.filter('')">All</button>
          <button class="chip" data-cat="厨房" onclick="JobsView.filter('厨房')">👨‍🍳 Kitchen</button>
          <button class="chip" data-cat="服务" onclick="JobsView.filter('服务')">🤵 Service</button>
          <button class="chip" data-cat="管理" onclick="JobsView.filter('管理')">📋 Management</button>
        </div>
        <div id="jobs-list"></div>
      </div>
    `;
  },

  async afterRender() {
    this.currentCat = '餐饮';
    await this.loadJobs();
  },

  async loadJobs() {
    const container = document.getElementById('jobs-list');
    container.innerHTML = '<div class="loading"><div class="spinner"></div><p>Loading jobs...</p></div>';
    try {
      const keyword = (document.getElementById('job-search')?.value || '').trim();
      this.jobs = await API.listJobs(this.currentCat, '', keyword);
      this.renderJobs();
    } catch {
      container.innerHTML = '<div class="empty-state"><p>Failed to load jobs.</p></div>';
    }
  },

  renderJobs() {
    const container = document.getElementById('jobs-list');
    if (this.jobs.length === 0) {
      container.innerHTML = '<div class="empty-state"><p>No jobs found.</p></div>';
      return;
    }
    container.innerHTML = this.jobs.map(j => `
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
    `).join('');
    container.querySelectorAll('.job-card').forEach(card => {
      card.addEventListener('click', () => Router.go('job-' + card.dataset.id));
    });
  },

  filter(cat) {
    this.currentCat = cat;
    document.querySelectorAll('.chip').forEach(c => c.classList.toggle('active', c.dataset.cat === cat));
    this.loadJobs();
  },

  search: (function() {
    let timer;
    return function() {
      clearTimeout(timer);
      timer = setTimeout(() => JobsView.loadJobs(), 300);
    };
  })(),
};

const JobDetailView = {
  jobId: null,

  temp() {
    return '<div id="view-job-holder" style="display:none"></div>';
  },

  async render(id) {
    this.jobId = parseInt(id);
    return `
      <div id="view-job-${id}" class="view">
        <div class="view-header">
          <button class="back-btn" onclick="Router.go('jobs')">
            <svg viewBox="0 0 24 24"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
            Jobs
          </button>
          <h1>Job Detail</h1>
          <div style="width:50px"></div>
        </div>
        <div class="loading"><div class="spinner"></div><p>Loading job...</p></div>
      </div>
    `;
  },

  async afterRender(id) {
    this.jobId = parseInt(id);
    const container = document.getElementById('view-job-' + id);
    try {
      const job = await API.getJob(this.jobId);
      let match = null;
      try { match = await API.matchJob(this.jobId); } catch {}
      container.innerHTML = this.buildHTML(job, match);
      document.getElementById('btn-apply-' + this.jobId)?.addEventListener('click', () => this.apply());
    } catch {
      container.innerHTML = '<div class="empty-state"><p>Job not found.</p></div>';
    }
  },

  buildHTML(job, match) {
    const score = match?.score;
    const badge = score >= 70 ? 'match-high' : score >= 40 ? 'match-mid' : 'match-low';
    return `
      <div class="job-detail-header">
        <div class="company">${job.company || 'Company'}</div>
        <h2>${job.title}</h2>
        <div class="meta">
          <span>📍 ${job.location || 'Malaysia'}</span>
          <span>📅 ${job.posted_at ? new Date(job.posted_at).toLocaleDateString() : 'Recent'}</span>
        </div>
        ${score !== undefined ? `<div class="match-badge ${badge}" style="margin-top:8px">Match: ${score}%</div>` : ''}
      </div>
      <div class="job-detail-body">
        <h3>Description</h3>
        <p>${job.description || 'No description available.'}</p>
      </div>
      <div class="job-detail-actions">
        <button class="btn btn-primary" id="btn-apply-${job.id}">Apply Now</button>
        <button class="btn btn-outline" onclick="window.open('${job.url || ''}','_blank')">View Original</button>
      </div>
    `;
  },

  async apply() {
    const btn = document.getElementById('btn-apply-' + this.jobId);
    btn.disabled = true;
    btn.textContent = 'Applying...';
    try {
      const res = await API.apply({ job_id: this.jobId });
      const el = document.createElement('div');
      el.className = 'apply-result success';
      el.innerHTML = '<div class="label">✅ Application Submitted!</div><p>Your tailored resume and cover letter have been prepared.</p>';
      btn.parentElement.after(el);
      btn.textContent = 'Applied ✓';
    } catch (err) {
      btn.disabled = false;
      btn.textContent = 'Apply Now';
      const el = document.createElement('div');
      el.className = 'apply-result error';
      el.innerHTML = '<div class="label">❌ Failed</div><p>' + err.message + '</p>';
      btn.parentElement.after(el);
    }
  },
};
