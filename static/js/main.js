// La Une Multiservice — Main JS

document.addEventListener('DOMContentLoaded', () => {

  // ── HAMBURGER MENU ──────────────────────────────────
  const hamburger = document.getElementById('hamburger-btn');
  const navMenu   = document.getElementById('nav-menu');
  const navOverlay = document.getElementById('nav-overlay');

  function openMenu() {
    navMenu.classList.add('open');
    navOverlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    hamburger.setAttribute('aria-expanded', 'true');
    hamburger.classList.add('is-open');
  }
  function closeMenu() {
    navMenu.classList.remove('open');
    navOverlay.classList.remove('open');
    document.body.style.overflow = '';
    hamburger.setAttribute('aria-expanded', 'false');
    hamburger.classList.remove('is-open');
  }

  if (hamburger) {
    hamburger.addEventListener('click', () => {
      navMenu.classList.contains('open') ? closeMenu() : openMenu();
    });
  }
  if (navOverlay) navOverlay.addEventListener('click', closeMenu);

  // Close on nav link click (mobile)
  navMenu?.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth < 1024) closeMenu();
    });
  });

  // Close on Escape
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });

  // ── DROPDOWN MOBILE (tap to toggle) ─────────────────
  document.querySelectorAll('.nav-dropdown > a').forEach(toggle => {
    toggle.addEventListener('click', e => {
      if (window.innerWidth < 1024) {
        e.preventDefault();
        const parent = toggle.closest('.nav-dropdown');
        parent.classList.toggle('mobile-open');
      }
    });
  });

  // ── SCROLL REVEAL ───────────────────────────────────
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

  // ── FAQ ACCORDION ───────────────────────────────────
  document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', () => {
      const item   = btn.closest('.faq-item');
      const answer = item.querySelector('.faq-answer');
      const isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(i => {
        i.classList.remove('open');
        i.querySelector('.faq-answer').style.maxHeight = '0';
      });
      if (!isOpen) {
        item.classList.add('open');
        answer.style.maxHeight = answer.scrollHeight + 'px';
      }
    });
  });

  // ── NAVBAR SCROLL ────────────────────────────────────
  const navbar = document.querySelector('.navbar');
  window.addEventListener('scroll', () => {
    if (!navbar) return;
    if (window.scrollY > 60) {
      navbar.style.background   = 'rgba(13,27,42,0.98)';
      navbar.style.boxShadow    = '0 4px 20px rgba(0,0,0,0.3)';
    } else {
      navbar.style.background   = 'rgba(13,27,42,0.95)';
      navbar.style.boxShadow    = 'none';
    }
  }, { passive: true });

  // ── ACTIVE LINK ──────────────────────────────────────
  const path = window.location.pathname;
  document.querySelectorAll('.nav-menu a').forEach(link => {
    if (link.getAttribute('href') === path) link.classList.add('active');
  });

  // ── AUTO-DISMISS ALERTS ──────────────────────────────
  document.querySelectorAll('.alert').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'all 0.4s ease';
      el.style.opacity    = '0';
      el.style.transform  = 'translateY(-10px)';
      setTimeout(() => el.remove(), 400);
    }, 5000);
  });

  // ── SERVICE IMAGE PREVIEW (admin-facing) ─────────────
  const imgInput = document.getElementById('id_hero_image');
  if (imgInput) {
    imgInput.addEventListener('change', e => {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = ev => {
        let preview = document.getElementById('img-preview');
        if (!preview) {
          preview = document.createElement('img');
          preview.id = 'img-preview';
          preview.style.cssText = 'max-width:100%;margin-top:0.5rem;border-radius:8px;max-height:200px;object-fit:cover;';
          imgInput.parentNode.insertBefore(preview, imgInput.nextSibling);
        }
        preview.src = ev.target.result;
      };
      reader.readAsDataURL(file);
    });
  }

});
