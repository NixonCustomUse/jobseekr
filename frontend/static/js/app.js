const App = {
  isAuth: false,

  async init() {
    document.getElementById('app').innerHTML = '';

    // Check auth by trying to load profile
    try {
      await API.getProfile();
      this.isAuth = true;
    } catch {
      this.isAuth = false;
    }

    if (this.isAuth) {
      await this.renderApp();
    } else {
      const html = await AuthView.render();
      document.getElementById('app').innerHTML = html;
      AuthView.afterRender();
    }
  },

  async renderApp() {
    const html = `
      ${await DashboardView.render()}
      ${await JobsView.render()}
      ${JobDetailView.temp()}
      ${await ProfileView.render()}
      ${await ApplicationsView.render()}
      <nav class="bottom-nav">
        <button class="nav-item active" data-view="dashboard" onclick="Router.go('dashboard')">
          <svg viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
          Home
        </button>
        <button class="nav-item" data-view="jobs" onclick="Router.go('jobs')">
          <svg viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/></svg>
          Jobs
        </button>
        <button class="nav-item" data-view="applications" onclick="Router.go('applications')">
          <svg viewBox="0 0 24 24"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
          Applied
        </button>
        <button class="nav-item" data-view="profile" onclick="Router.go('profile')">
          <svg viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          Profile
        </button>
      </nav>
    `;
    document.getElementById('app').innerHTML = html;
    Router.init();
    this.runAfterRender();
  },

  runAfterRender() {
    setTimeout(() => {
      DashboardView.afterRender();
      JobsView.afterRender();
      ProfileView.afterRender();
      ApplicationsView.afterRender();
    }, 50);
  },

  async onAuthChange(authenticated) {
    this.isAuth = authenticated;
    if (authenticated) {
      await this.renderApp();
    } else {
      document.getElementById('app').innerHTML = '';
      const html = await AuthView.render();
      document.getElementById('app').innerHTML = html;
      AuthView.afterRender();
    }
  },

  async logout() {
    try { await API.logout(); } catch {}
    this.isAuth = false;
    document.getElementById('app').innerHTML = '';
    const html = await AuthView.render();
    document.getElementById('app').innerHTML = html;
    AuthView.afterRender();
  },

  toast(msg) {
    const t = document.createElement('div');
    t.className = 'toast';
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 2500);
  },
};

// Hijack Router.go to handle dynamic job detail views
const _origGo = Router.go;
Router.go = function(view, noPush) {
  if (view && view.startsWith('job-')) {
    const id = view.split('-')[1];
    const container = document.getElementById('view-' + view);
    if (!container) {
      // Inject job detail view dynamically
      const appEl = document.getElementById('app');
      const div = document.createElement('div');
      div.id = 'view-' + view;
      div.className = 'view';
      appEl.insertBefore(div, appEl.querySelector('.bottom-nav'));
    }
  }
  _origGo.call(Router, view, noPush);

  // Handle dynamic afterRender for job detail
  if (view && view.startsWith('job-')) {
    const id = view.split('-')[1];
    const el = document.getElementById('view-' + view);
    if (el && el.innerHTML.trim() === '') {
      JobDetailView.render(id).then(html => {
        el.innerHTML = html;
        const realContainer = document.getElementById('view-' + view);
        if (realContainer && realContainer.querySelector('.loading')) {
          JobDetailView.afterRender(id);
        }
      });
    }
  }
};

document.addEventListener('DOMContentLoaded', () => App.init());
