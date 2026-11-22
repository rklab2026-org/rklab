// ============ API CONFIG ============
// Use Render URL for live site!
const API_BASE = "https://rklab.onrender.com";

// ============ HELPER: Show status message on page ============
function showStatus(message, type) {
    const el = document.getElementById("auth-status");
    if (el) {
        el.textContent = message;
        el.className = "status-msg " + (type === "success" ? "status-success" : "status-error");
    }
}

// ============ EXPLORE BUTTON (CRITICAL FIX FOR TEST) ============
function showWelcomeAlert() {
    // DO NOT CHANGE THIS TEXT. Playwright test expects exactly: Welcome to RKLab!
    alert("Welcome to RKLab!");
}

// ============ SIGN UP ============
async function handleSignup() {
    const username = document.getElementById("signup-user").value.trim();
    const password = document.getElementById("signup-pass").value;

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
            document.getElementById("signup-user").value = "";
            document.getElementById("signup-pass").value = "";
        } else {
            showStatus(`❌ ${data.detail || "Signup failed!"}`, "error");
        }
    } catch (err) {
        showStatus("🔴 Backend Server Error! Please check Render deployment.", "error");
    }
}

// ============ LOGIN ============
async function handleLogin() {
    const username = document.getElementById("login-user").value.trim();
    const password = document.getElementById("login-pass").value;

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
            document.getElementById("login-pass").value = "";
        } else {
            showStatus(`❌ ${data.detail || "Login failed!"}`, "error");
        }
    } catch (err) {
        showStatus("🔴 Backend Server Error! Please check Render deployment.", "error");
    }
}

// ============ LOAD ITEMS ============
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
        if (document.getElementById("items-list")) {
            document.getElementById("items-list").innerHTML = "<p>Failed to load items.</p>";
        }
    }
}

// Load items when DOM is ready
document.addEventListener("DOMContentLoaded", loadItems);