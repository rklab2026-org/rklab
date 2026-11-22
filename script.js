// ============ API CONFIG ============
// Local dev:   "http://127.0.0.1:8000"
// Production:  "https://rklab.onrender.com"
const API_BASE = "http://127.0.0.1:8000";

// ============ HELPER: Show status message on page ============
function showStatus(message, type) {
    const el = document.getElementById("auth-status");
    el.textContent = message;
    el.className = "status-msg " + (type === "success" ? "status-success" : "status-error");
}

// ============ EXPLORE BUTTON (Existing) ============
function showWelcomeAlert() {
    alert("Welcome to RKLab Frontend! 🚀");
}

// ============ SIGN UP ============
async function handleSignup() {
    const username = document.getElementById("signup-user").value.trim();
    const password = document.getElementById("signup-pass").value;

    // Frontend basic check
    if (!username || !password) {
        showStatus("⚠️ Please fill in both Username and Password!", "error");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/api/signup`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (res.ok) {
            showStatus(`✅ ${data.message} You can now Login!`, "success");
            // Clear inputs
            document.getElementById("signup-user").value = "";
            document.getElementById("signup-pass").value = "";
        } else {
            showStatus(`❌ ${data.detail || "Signup failed!"}`, "error");
        }

    } catch (err) {
        showStatus("🔴 Server not reachable! Is the backend running?", "error");
    }
}

// ============ LOGIN ============
async function handleLogin() {
    const username = document.getElementById("login-user").value.trim();
    const password = document.getElementById("login-pass").value;

    // Frontend basic check
    if (!username || !password) {
        showStatus("⚠️ Please fill in both Username and Password!", "error");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/api/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (res.ok) {
            showStatus(`🎉 Welcome, ${data.username}! Login successful!`, "success");
            // Clear password only
            document.getElementById("login-pass").value = "";
        } else {
            showStatus(`❌ ${data.detail || "Login failed!"}`, "error");
        }

    } catch (err) {
        showStatus("🔴 Server not reachable! Is the backend running?", "error");
    }
}

// ============ LOAD ITEMS (for future use) ============
async function loadItems() {
    try {
        const res = await fetch(`${API_BASE}/api/items`);
        const items = await res.json();
        const listEl = document.getElementById("items-list");

        if (items.length === 0) {
            listEl.innerHTML = "<p>No items found.</p>";
            return;
        }

        listEl.innerHTML = items.map(item => `
            <div class="item-row">
                <span class="item-name">${item.name}</span>
                <span class="item-status">${item.status}</span>
            </div>
        `).join("");
    } catch (err) {
        document.getElementById("items-list").innerHTML = "<p>Failed to load items.</p>";
    }
}

// Auto-load items on page load
loadItems();