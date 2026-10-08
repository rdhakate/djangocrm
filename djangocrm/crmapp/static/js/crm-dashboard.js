
let currentCustomerId = null;

function openCustomerModal(customer = null) {
  currentCustomerId = customer?.id || null;
  document.getElementById("modal-title").textContent = customer ? "Edit Customer" : "Add Customer";
  document.getElementById("customer-id").value = customer?.id || "";
  document.getElementById("customer-name").value = customer?.name || "";
  document.getElementById("customer-description").value = customer?.description || "";
  document.getElementById("customer-modal").classList.add("is-active");
  document.querySelector(".modal-card-foot .button.is-danger").style.display = customer ? "inline-block" : "none";
}

function closeCustomerModal() {
  document.getElementById("customer-modal").classList.remove("is-active");
  document.getElementById("customer-form").reset();
  currentCustomerId = null;
}


// 🔐 API helper: sends JWT token in Authorization header
function API(path, options = {}) {
  const token = localStorage.getItem("access");
  if (!token) {
    console.error("No access token found");
    window.location.href = "/login/";
    return;
  }

  return fetch(path, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token
    }
  }).then(res => {
    if (res.status === 401) {
      alert("Session expired. Please login again.");
      localStorage.removeItem("access");
      window.location.href = "/login/";
    }
    return res.json();
  });
}

function saveCustomer() {
  const name = document.getElementById("customer-name").value.trim();
  const description = document.getElementById("customer-description").value.trim();

  if (!name) {
    alert("Customer name is required.");
    return;
  }

  const data = { name, description };
  const id = currentCustomerId;

  const method = id ? "PUT" : "POST";
  const url = id ? `/api/customers/${id}/` : `/api/customers/`;

  API(url, {
    method: method,
    body: JSON.stringify(data),
  })
    .then(response => {
      if (response && response.id) {
        closeCustomerModal();
        loadCustomers(); // refresh list
      } else {
        throw new Error("Invalid response");
      }
    })
    .catch(err => {
      alert("❌ Failed to save customer.");
      console.error(err);
    });
}


function deleteCustomer() {
  if (!currentCustomerId || !confirm("Delete this customer?")) return;

  API(`/api/customers/${currentCustomerId}/`, {
    method: "DELETE",
  })
    .then(() => {
      closeCustomerModal();
      loadCustomers();
    })
    .catch(err => {
      alert("Failed to delete customer.");
      console.error(err);
    });
}

// 🎨 UI Helpers
function setActiveMenu(id) {
  document.querySelectorAll("#sidebar a").forEach(a => a.classList.remove("is-active"));
  const link = document.getElementById(id);
  if (link) link.classList.add("is-active");
}

function toggleSidebar() {
  document.getElementById("sidebar").classList.toggle("is-hidden-touch");
}

// 🚪 Logout
function logout() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  window.location.href = "/login/";
}

// 📊 Dashboard view
function loadDashboard() {
  setActiveMenu("menu-dashboard");
  document.getElementById("content-area").innerHTML = `
    <h2 class="title is-4 has-text-white">📊 Dashboard</h2>
    <div class="columns is-multiline">
      <div class="column is-half">
        <div class="box">
          <h3 class="subtitle has-text-white">Customer Signups</h3>
          <canvas id="signupChart"></canvas>
        </div>
      </div>
      <div class="column is-half">
        <div class="box">
          <h3 class="subtitle has-text-white">Activity Breakdown</h3>
          <canvas id="activityChart"></canvas>
        </div>
      </div>
    </div>`;
  setTimeout(renderCharts, 100);
}

// 📈 Render Charts
function renderCharts() {
  const ctx1 = document.getElementById('signupChart').getContext('2d');
  const ctx2 = document.getElementById('activityChart').getContext('2d');

  new Chart(ctx1, {
    type: 'bar',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr'],
      datasets: [{
        label: 'Customers',
        data: [5, 12, 8, 15],
        backgroundColor: '#4c9aff'
      }]
    },
    options: {
      plugins: { legend: { labels: { color: '#fff' } } },
      scales: {
        x: { ticks: { color: '#ccc' } },
        y: { ticks: { color: '#ccc' } }
      }
    }
  });

  new Chart(ctx2, {
    type: 'pie',
    data: {
      labels: ['Call', 'Meeting', 'Email'],
      datasets: [{
        data: [12, 5, 8],
        backgroundColor: ['#f87171', '#60a5fa', '#34d399']
      }]
    },
    options: {
      plugins: { legend: { labels: { color: '#fff' } } }
    }
  });
}

// 👥 Customers View
function loadCustomers() {
  setActiveMenu("menu-customers");
  document.getElementById("content-area").innerHTML = `<p class="has-text-white">🔄 Loading customers...</p>`;

  API("/api/customers/")
    .then(data => {
      let html = `
        <div class="level">
          <div class="level-left">
            <h2 class="title is-4 has-text-white">👥 Customers</h2>
          </div>
          <div class="level-right">
            <button class="button is-primary" onclick="openCustomerModal()">➕ Add</button>
          </div>
        </div>`;

      if (!data || !data.length) {
        html += `<div class="notification is-warning">No customers found.</div>`;
      } else {
        html += `<div class="columns is-multiline">`;

        data.forEach(c => {
          // Safely encode customer object to pass to JS
          const customerData = encodeURIComponent(JSON.stringify(c));
          html += `
            <div class="column is-4">
              <div class="card">
                <div class="card-content">
                  <p class="title is-6">${c.name}</p>
                  <p class="subtitle is-7 has-text-grey-light">${c.description || 'No description'}</p>
                  <button class="button is-small is-info mt-2"
                    onclick='openCustomerModal(JSON.parse(decodeURIComponent("${customerData}")))'>
                    Edit
                  </button>
                </div>
              </div>
            </div>`;
        });

        html += `</div>`;
      }

      document.getElementById("content-area").innerHTML = html;
    })
    .catch(err => {
      console.error("Failed to load customers", err);
      document.getElementById("content-area").innerHTML = `
        <div class="notification is-danger">❌ Error loading customers: ${err}</div>`;
    });
}


// 📅 Activities View
function loadActivities() {
  setActiveMenu("menu-activities");
  document.getElementById("content-area").innerHTML = `<p class="has-text-white">🔄 Loading activities...</p>`;
  API("/api/activities/")
    .then(data => {
      let html = `<h2 class="title is-4 has-text-white">📅 Activities</h2>`;
      if (!data || !data.length) {
        html += `<div class="notification is-warning">No activities found.</div>`;
      } else {
        html += `<div class="table-container">
          <table class="table is-fullwidth is-hoverable is-striped">
            <thead><tr><th>Title</th><th>Start</th><th>End</th></tr></thead>
            <tbody>`;
        data.forEach(a => {
          html += `<tr>
            <td>${a.title}</td>
            <td>${a.start_datetime}</td>
            <td>${a.end_datetime || '-'}</td>
          </tr>`;
        });
        html += `</tbody></table></div>`;
      }
      document.getElementById("content-area").innerHTML = html;
    })
    .catch(err => {
      console.error("Failed to load activities", err);
      document.getElementById("content-area").innerHTML = `<div class="notification is-danger">Error loading activities</div>`;
    });
}
