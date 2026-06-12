const ProfileView = {
  async render() {
    return `
      <div id="view-profile" class="view">
        <div class="view-header">
          <h1>Profile</h1>
          <button class="btn btn-sm btn-outline" onclick="App.logout()">Logout</button>
        </div>
        <div id="profile-content">
          <div class="loading"><div class="spinner"></div><p>Loading profile...</p></div>
        </div>
      </div>
    `;
  },

  async afterRender() {
    const container = document.getElementById('profile-content');
    try {
      const profile = await API.getProfile();
      container.innerHTML = this.buildHTML(profile);
      document.getElementById('profile-form').addEventListener('submit', (e) => this.save(e));
    } catch {
      container.innerHTML = '<div class="empty-state"><p>Please log in.</p></div>';
    }
  },

  buildHTML(p) {
    const skills = p.skills ? (Array.isArray(p.skills) ? p.skills : JSON.parse(p.skills || '[]')) : [];
    return `
      <div class="profile-header">
        <div class="avatar">${(p.name || 'U')[0].toUpperCase()}</div>
        <h2>${p.name || 'User'}</h2>
        <div class="plan-badge">${(p.plan || 'free').toUpperCase()}</div>
      </div>
      <form id="profile-form" style="padding:16px">
        <div class="form-group">
          <label>Email</label>
          <input class="form-input" value="${p.email || ''}" disabled style="opacity:0.6">
        </div>
        <div class="form-group">
          <label>Phone</label>
          <input class="form-input" id="pf-phone" value="${p.phone || ''}" placeholder="012-345 6789">
        </div>
        <div class="form-group">
          <label>Resume / Experience</label>
          <textarea class="form-input" id="pf-resume" placeholder="Describe your work experience...">${p.resume_text || ''}</textarea>
        </div>
        <div class="form-group">
          <label>Skills (comma separated)</label>
          <input class="form-input" id="pf-skills" value="${skills.join(', ')}" placeholder="e.g. waiter, bartender, cashier">
        </div>
        <div class="form-group">
          <label>Preferred Location</label>
          <input class="form-input" id="pf-location" value="${p.preferred_location || ''}" placeholder="e.g. Kuala Lumpur, Penang">
        </div>
        <div class="form-group">
          <label>Preferred Category</label>
          <input class="form-input" id="pf-category" value="${p.preferred_category || '餐饮'}" placeholder="餐饮">
        </div>
        <button class="btn btn-primary" type="submit">Save Profile</button>
      </form>
    `;
  },

  async save(e) {
    e.preventDefault();
    const btn = e.target.querySelector('button[type="submit"]');
    btn.disabled = true;
    btn.textContent = 'Saving...';
    try {
      await API.updateProfile({
        phone: document.getElementById('pf-phone').value,
        resume_text: document.getElementById('pf-resume').value,
        skills: document.getElementById('pf-skills').value.split(',').map(s => s.trim()).filter(Boolean),
        preferred_location: document.getElementById('pf-location').value,
        preferred_category: document.getElementById('pf-category').value,
      });
      btn.textContent = 'Saved ✓';
      setTimeout(() => { btn.disabled = false; btn.textContent = 'Save Profile'; }, 1500);
    } catch (err) {
      btn.disabled = false;
      btn.textContent = 'Save Failed';
    }
  },
};
