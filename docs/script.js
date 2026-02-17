/* ============================================
   AIDE X — Interactive Behaviors
   ============================================ */

(function () {
    'use strict';

    // --- Theme Toggle (SVG icon visibility handled by CSS) ---
    const themeToggle = document.getElementById('themeToggle');
    const html = document.documentElement;

    function setTheme(theme) {
        html.setAttribute('data-theme', theme);
        localStorage.setItem('aidex-theme', theme);
    }

    // Init from localStorage or default dark
    const saved = localStorage.getItem('aidex-theme') || 'dark';
    setTheme(saved);

    themeToggle.addEventListener('click', () => {
        const current = html.getAttribute('data-theme');
        setTheme(current === 'dark' ? 'light' : 'dark');
    });

    // --- Menu Button ---
    const menuBtn = document.getElementById('hamburgerBtn');
    const menuOverlay = document.getElementById('menuOverlay');
    const mainContent = document.getElementById('mainContent');
    const menuLinks = menuOverlay.querySelectorAll('a:not(.menu-cta)');

    function toggleMenu() {
        const isActive = menuBtn.classList.contains('active');
        menuBtn.classList.toggle('active');
        menuOverlay.classList.toggle('active');
        mainContent.classList.toggle('tilted');
        document.body.style.overflow = isActive ? '' : 'hidden';
    }

    menuBtn.addEventListener('click', toggleMenu);

    // Close menu on link click
    menuOverlay.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            if (menuBtn.classList.contains('active')) {
                toggleMenu();
            }
        });
    });

    // Close menu on Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && menuBtn.classList.contains('active')) {
            toggleMenu();
        }
    });

    // --- Top Bar Scroll Effect ---
    const topBar = document.getElementById('topBar');
    let ticking = false;

    function onScroll() {
        if (!ticking) {
            requestAnimationFrame(() => {
                topBar.classList.toggle('scrolled', window.scrollY > 50);
                ticking = false;
            });
            ticking = true;
        }
    }
    window.addEventListener('scroll', onScroll, { passive: true });

    // --- Sidebar Active Tracking ---
    const sidebarItems = document.querySelectorAll('.sidebar-item');
    const sections = document.querySelectorAll('.section');

    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.id;
                sidebarItems.forEach(item => {
                    item.classList.toggle('active', item.dataset.section === id);
                });
                // Also update full-screen menu active state
                menuLinks.forEach(link => {
                    link.classList.toggle('active', link.dataset.section === id);
                });
            }
        });
    }, {
        root: null,
        rootMargin: '-40% 0px -40% 0px',
        threshold: 0
    });

    sections.forEach(section => sectionObserver.observe(section));

    // --- Scroll Reveal Animations ---
    const revealElements = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                revealObserver.unobserve(entry.target); // animate once
            }
        });
    }, {
        root: null,
        rootMargin: '0px 0px -80px 0px',
        threshold: 0.1
    });

    revealElements.forEach(el => revealObserver.observe(el));

    // --- Smooth Scroll for Sidebar & Menu Links ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
    // --- Journey Stepper Tabs ---
    const stepperTabs = document.querySelectorAll('.stepper-tab');
    const stepperPanels = document.querySelectorAll('.stepper-panel');

    function activatePhase(phase) {
        stepperTabs.forEach(t => t.classList.toggle('active', t.dataset.phase === phase));
        stepperPanels.forEach(p => {
            p.classList.toggle('active', p.id === 'panel-' + phase);
        });
    }

    stepperTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            activatePhase(tab.dataset.phase);
            clearInterval(autoStep);  // stop auto-cycling on user click
        });
    });

    // Auto-cycle phases every 5s
    const phases = ['describe', 'decide', 'deliver'];
    let phaseIdx = 0;
    let autoStep = setInterval(() => {
        phaseIdx = (phaseIdx + 1) % phases.length;
        activatePhase(phases[phaseIdx]);
    }, 5000);

})();
