// ==========================================
// RKLab - Main Interactive Script
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    console.log("RKLab System Initialized Successfully!");

    const exploreBtn = document.getElementById('explore-btn');

    if (exploreBtn) {
        exploreBtn.addEventListener('click', () => {
            alert("🚀 Welcome to RKLab!\n\nGet ready to Learn Development, Testing & DevOps!");
        });
    }
});