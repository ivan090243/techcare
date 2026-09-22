document.addEventListener("DOMContentLoaded", () => {
    // Highlight active nav link
    const path = window.location.pathname;
    document.querySelectorAll(".nav-link, .sidebar-link").forEach((link) => {
        const href = link.getAttribute("href");
        if (href && href !== "/" && path.startsWith(href)) {
            link.classList.add("active");
        } else if (href === "/" && path === "/") {
            link.classList.add("active");
        }
    });

    // Intersection observer for scroll animations
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("animate-fade-in");
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.1 }
    );

    document.querySelectorAll(".reveal-on-scroll").forEach((el) => observer.observe(el));

    // Dashboard mobile sidebar toggle
    const toggle = document.getElementById("sidebarToggle");
    const sidebar = document.querySelector(".dashboard-sidebar");
    if (toggle && sidebar) {
        toggle.addEventListener("click", () => sidebar.classList.toggle("show"));
    }
});
