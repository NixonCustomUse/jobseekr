const Router = {
  currentView: null,

  init() {
    window.addEventListener('popstate', () => {
      const view = location.hash.slice(1) || 'dashboard';
      this.go(view, true);
    });
    const initial = location.hash.slice(1) || 'dashboard';
    this.go(initial, true);
  },

  go(view, noPush) {
    if (this.currentView) {
      const prev = document.getElementById('view-' + this.currentView);
      if (prev) prev.classList.remove('active');
    }

    const el = document.getElementById('view-' + view);
    if (el) {
      el.classList.add('active');
      this.currentView = view;
      window.scrollTo(0, 0);
      if (!noPush) {
        location.hash = view;
      }
      this.updateNav(view);
    }
  },

  updateNav(view) {
    document.querySelectorAll('.nav-item').forEach(item => {
      item.classList.toggle('active', item.dataset.view === view);
    });
  },
};
