// crm-dashboard.js

function toggleSidebar() {
  document.getElementById("sidebar").classList.toggle("is-hidden-touch");
}

function API(path) {
  return fetch(path, {
    headers: {
      'Authorization': 'Bearer ' + localStorage.getItem("access")
    }
  }).then(res => res.json());
}

function setActiveMenu(id) {
  document.querySelectorAll("#sidebar a").forEach(a => a.classList.remove("is-active"));
  document.getElementById(id).classList.add("is-active");
}

function loadDashboard() {
  setActiveMenu("menu-dashboard");
  document.getElementById("content-area").innerHTML = `
    <h2 class="title is-4 has-text-white">📊 Dashboard</h2>
    <div class="columns is-multiline">
      <div class="column is-half">
        <div class="box" style="background-color: #3a3a3c;">
          <h3 class="subtitle has-text-white">Customer Signups</h3>
          <canvas id="signupChart"></canvas>
        </div>
      </div>
      <div class="column is-half">
        <div class="box" style="background-color: #3a3a3c;">
          <h3 class="subtitle has-text-white">Activity Type Breakdown</h3>
          <canvas id="activityChart"></canvas>
        </div>
      </div>
    </div>`;

  setTimeout(() => renderCharts(), 100);  // slight delay to ensure DOM is ready
}

function loadCustomers() {
  setActiveMenu("menu-customers");

  API('/api/customers/').then(data => {
    let html = `
      <div class="level">
        <div class="level-left">
          <h2 class="title is-4 has-text-white">👥 Customers</h2>
        </div>
        <div class="level-right">
          <button class="button is-primary" onclick="openCustomerModal()">➕ Add Customer</button>
        </div>
      </div>
    `;

    if (data.length === 0) {
      html += `<div class="notification is-warning">No customers found.</div>`;
    } else {
      html += `<div class="columns is-multiline">`;
      data.forEach(c => {
        html += `
          <div class="column is-4">
            <div class="card" style="background-color: #3a3a3c;">
              <div class="card-content has-text-white">
                <p class="title is-6">${c.name}</p>
                <p class="subtitle is-7 has-text-grey-light">${c.description || 'No description'}</p>
              </div>
              <footer class="card-footer">
                <a href="#" class="card-footer-item" onclick='openCustomerModal(true, ${JSON.stringify(c)})'>✏️ Edit</a>
              </footer>
            </div>
          </div>`;
      });
      html += `</div>`;
    }

    document.getElementById("content-area").innerHTML = html;
  });
}

function loadActivities() {
  setActiveMenu("menu-activities");

  API('/api/activities/').then(data => {
    let html = `
      <div class="level">
        <div class="level-left">
          <h2 class="title is-4 has-text-white">📅 Activities</h2>
        </div>
      </div>
    `;

    if (data.length === 0) {
      html += `<div class="notification is-warning">No activities found.</div>`;
    } else {
      html += `<div class="table-container">
        <table class="table is-striped is-fullwidth is-hoverable">
          <thead>
            <tr>
              <th class="has-text-white">Title</th>
              <th class="has-text-white">Start</th>
              <th class="has-text-white">End</th>
              <th class="has-text-white">Location</th>
            </tr>
          </thead>
          <tbody>`;
      data.forEach(a => {
        html += `
          <tr>
            <td class="has-text-white">${a.title}</td>
            <td class="has-text-white">${a.start_datetime}</td>
            <td class="has-text-white">${a.end_datetime || '-'}</td>
            <td class="has-text-white">${a.location || '-'}</td>
          </tr>`;
      });
      html += `</tbody></table></div>`;
    }

    document.getElementById("content-area").innerHTML = html;
  });
}


function renderCharts() {
  const ctxSignup = document.getElementById('signupChart').getContext('2d');
  const ctxActivity = document.getElementById('activityChart').getContext('2d');

  // 🔹 Chart 1: Customer Signups Over Time (Mocked)
  new Chart(ctxSignup, {
    type: 'bar',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [{
        label: 'New Customers',
        data: [12, 19, 10, 15, 22, 18],
        backgroundColor: '#4c9aff'
      }]
    },
    options: {
      plugins: { legend: { labels: { color: '#fff' }}},
      scales: {
        x: { ticks: { color: '#ccc' } },
        y: { ticks: { color: '#ccc' } }
      }
    }
  });

  // 🔹 Chart 2: Activity Type Breakdown (Mocked)
  new Chart(ctxActivity, {
    type: 'pie',
    data: {
      labels: ['Call', 'Meeting', 'Email', 'Follow-up'],
      datasets: [{
        label: 'Activity Types',
        data: [10, 5, 8, 6],
        backgroundColor: ['#f87171', '#60a5fa', '#34d399', '#fbbf24']
      }]
    },
    options: {
      plugins: {
        legend: {
          labels: { color: '#fff' }
        }
      }
    }
  });
}


function logout() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  window.location.href = "/login/";
}

if (!localStorage.getItem("access")) {
  window.location.href = "/login/";
}
