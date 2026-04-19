// Shared sidebar + topbar renderer
function renderSidebar(activePage) {
  const navItems = [
    { id: 'home',      href: 'home.html',      icon: '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',      label: 'Home' },
    { id: 'dashboard', href: 'dashboard.html',  icon: '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>',  label: 'Dashboard' },
    { id: 'employees', href: 'employees.html',  icon: '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',  label: 'Employees' },
    { id: 'reports',   href: 'reports.html',    icon: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>', label: 'Reports' },
    { id: 'about',     href: 'about.html',      icon: '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>', label: 'About' }
  ];

  const sidebarHTML = `
    <div class="sidebar">
      <div class="logo-wrap">
        <div class="logo-icon">A</div>
        <div class="logo-text">AttendPro</div>
      </div>
      <div class="nav-list">
        ${navItems.map(item => `
          <div class="nav-item">
            <a href="${item.href}" class="nav-link${activePage === item.id ? ' active' : ''}">
              <svg viewBox="0 0 24 24">${item.icon}</svg>
              <span>${item.label}</span>
            </a>
          </div>`).join('')}
      </div>
      <div style="margin-top:auto; padding-top:20px; border-top:1px solid var(--border);">
        <a href="login.html" class="nav-link" style="color:var(--red)">
          <svg viewBox="0 0 24 24"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
          <span>Logout</span>
        </a>
      </div>
    </div>
  `;

  document.body.insertAdjacentHTML('afterbegin', sidebarHTML);
}

// Global function to animate progress bars on any page
function animateBars() {
  setTimeout(() => {
    document.querySelectorAll('.kpi-fill, .dept-fill, .month-fill').forEach(fill => {
      const w = fill.getAttribute('data-w');
      if(w) fill.style.width = w + '%';
    });
  }, 400);
}