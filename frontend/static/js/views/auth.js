const AuthView = {
  async render() {
    return `
      <div id="view-auth" class="view auth-view">
        <div class="logo">JobSeekr</div>
        <p class="tagline">Find your next hospitality job in Malaysia</p>
        <div class="auth-box" id="auth-box">
          <h2 id="auth-title">Welcome back</h2>
          <p class="sub" id="auth-sub">Sign in to continue</p>
          <form id="auth-form">
            <div class="form-group" id="name-group" style="display:none">
              <label>Full Name</label>
              <input class="form-input" id="auth-name" type="text" placeholder="Your name" autocomplete="name">
            </div>
            <div class="form-group">
              <label>Email</label>
              <input class="form-input" id="auth-email" type="email" placeholder="you@example.com" autocomplete="email" required>
            </div>
            <div class="form-group">
              <label>Password</label>
              <input class="form-input" id="auth-password" type="password" placeholder="At least 6 characters" autocomplete="current-password" required>
            </div>
            <div id="auth-error" class="error-text" style="display:none"></div>
            <button class="btn btn-primary" id="auth-submit" type="submit">Sign In</button>
          </form>
          <div class="auth-toggle">
            <span id="auth-toggle-text">Don't have an account?</span>
            <a id="auth-toggle-link">Sign Up</a>
          </div>
        </div>
      </div>
    `;
  },

  isRegister: false,

  afterRender() {
    const form = document.getElementById('auth-form');
    const toggleLink = document.getElementById('auth-toggle-link');
    const nameGroup = document.getElementById('name-group');

    toggleLink.addEventListener('click', () => {
      this.isRegister = !this.isRegister;
      document.getElementById('auth-title').textContent = this.isRegister ? 'Create account' : 'Welcome back';
      document.getElementById('auth-sub').textContent = this.isRegister
        ? 'Start your job search today' : 'Sign in to continue';
      document.getElementById('auth-submit').textContent = this.isRegister ? 'Create Account' : 'Sign In';
      document.getElementById('auth-toggle-text').textContent = this.isRegister
        ? 'Already have an account?' : "Don't have an account?";
      toggleLink.textContent = this.isRegister ? 'Sign In' : 'Sign Up';
      nameGroup.style.display = this.isRegister ? 'block' : 'none';
    });

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = document.getElementById('auth-submit');
      const errorEl = document.getElementById('auth-error');
      const email = document.getElementById('auth-email').value.trim();
      const password = document.getElementById('auth-password').value;
      const name = document.getElementById('auth-name').value.trim();

      errorEl.style.display = 'none';
      submitBtn.disabled = true;
      submitBtn.textContent = this.isRegister ? 'Creating...' : 'Signing in...';

      try {
        if (this.isRegister) {
          await API.register(email, password, name);
        } else {
          await API.login(email, password);
        }
        Router.go('dashboard');
        App.onAuthChange(true);
      } catch (err) {
        errorEl.textContent = err.message;
        errorEl.style.display = 'block';
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = this.isRegister ? 'Create Account' : 'Sign In';
      }
    });
  }
};
