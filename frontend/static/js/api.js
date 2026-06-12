const API = {
  async request(method, path, body) {
    const opts = {
      method,
      headers: { 'Content-Type': 'application/json' },
    };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(path, opts);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Request failed');
    return data;
  },

  register(email, password, name) {
    return this.request('POST', '/api/auth/register', { email, password, name });
  },

  login(email, password) {
    return this.request('POST', '/api/auth/login', { email, password });
  },

  logout() {
    return this.request('POST', '/api/auth/logout');
  },

  getProfile() {
    return this.request('GET', '/api/profile');
  },

  updateProfile(data) {
    return this.request('PUT', '/api/profile', data);
  },

  listJobs(category, location, keyword) {
    const params = new URLSearchParams();
    if (category) params.set('category', category);
    if (location) params.set('location', location);
    if (keyword) params.set('keyword', keyword);
    return this.request('GET', '/api/jobs?' + params.toString());
  },

  getJob(id) {
    return this.request('GET', '/api/jobs/' + id);
  },

  matchJob(id) {
    return this.request('POST', '/api/jobs/' + id + '/match');
  },

  apply(data) {
    return this.request('POST', '/api/applications', data);
  },

  listApplications() {
    return this.request('GET', '/api/applications');
  },

  scrapeStatus() {
    return this.request('GET', '/api/scrape/status');
  },

  triggerScrape() {
    return this.request('POST', '/api/scrape/jobstreet');
  },
};
