/* ═══════════════════════════════════════════════════════
   LA UNE MULTISERVICE — ANIMATIONS PREMIUM
   ═══════════════════════════════════════════════════════ */

  init() {
    document.addEventListener('mousemove', (e) => {
      this.mx = e.clientX;
      this.my = e.clientY;
      this.cursor.style.transform = `translate(${this.mx - 6}px, ${this.my - 6}px)`;
    });

    // Interactive elements
    const hoverEls = document.querySelectorAll('a, button, .service-card, .project-card, .catalogue-card, .gallery-thumb, [data-cursor]');
    hoverEls.forEach(el => {
      el.addEventListener('mouseenter', () => {
        this.cursor.classList.add('cursor-hover');
        this.follower.classList.add('follower-hover');
      });
      el.addEventListener('mouseleave', () => {
        this.cursor.classList.remove('cursor-hover');
        this.follower.classList.remove('follower-hover');
      });
    });

    this.animate();
  }

  animate() {
    this.fx += (this.mx - this.fx) * 0.12;
    this.fy += (this.my - this.fy) * 0.12;
    this.follower.style.transform = `translate(${this.fx - 20}px, ${this.fy - 20}px)`;
    requestAnimationFrame(() => this.animate());
  }
}

// ── 2. CANVAS PARTICULES HERO ──────────────────────────
class HeroParticles {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.particles = [];
    this.resize();
    this.createParticles();
    window.addEventListener('resize', () => this.resize());
    this.animate();
  }

  resize() {
    if (!this.canvas) return;
    this.canvas.width = this.canvas.offsetWidth;
    this.canvas.height = this.canvas.offsetHeight;
  }

  createParticles() {
    const count = Math.floor((this.canvas.width * this.canvas.height) / 14000);
    this.particles = [];
    for (let i = 0; i < count; i++) {
      this.particles.push({
        x: Math.random() * this.canvas.width,
        y: Math.random() * this.canvas.height,
        r: Math.random() * 2 + 0.5,
        dx: (Math.random() - 0.5) * 0.4,
        dy: (Math.random() - 0.5) * 0.4,
        opacity: Math.random() * 0.6 + 0.1,
        pulse: Math.random() * Math.PI * 2,
      });
    }
  }

  animate() {
    if (!this.canvas) return;
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.particles.forEach(p => {
      p.pulse += 0.02;
      p.x += p.dx;
      p.y += p.dy;
      if (p.x < 0 || p.x > this.canvas.width)  p.dx *= -1;
      if (p.y < 0 || p.y > this.canvas.height) p.dy *= -1;

      const alpha = p.opacity * (0.6 + 0.4 * Math.sin(p.pulse));
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      this.ctx.fillStyle = `rgba(201,168,76,${alpha})`;
      this.ctx.fill();
    });

    // Draw connections
    for (let i = 0; i < this.particles.length; i++) {
      for (let j = i + 1; j < this.particles.length; j++) {
        const a = this.particles[i], b = this.particles[j];
        const dist = Math.hypot(a.x - b.x, a.y - b.y);
        if (dist < 100) {
          this.ctx.beginPath();
          this.ctx.moveTo(a.x, a.y);
          this.ctx.lineTo(b.x, b.y);
          this.ctx.strokeStyle = `rgba(201,168,76,${0.12 * (1 - dist / 100)})`;
          this.ctx.lineWidth = 0.5;
          this.ctx.stroke();
        }
      }
    }
    requestAnimationFrame(() => this.animate());
  }
}

// ── 3. TYPEWRITER ──────────────────────────────────────
class Typewriter {
  constructor(el, texts, opts = {}) {
    this.el = el;
    this.texts = texts;
    this.speed = opts.speed || 80;
    this.deleteSpeed = opts.deleteSpeed || 40;
    this.pause = opts.pause || 2000;
    this.textIndex = 0;
    this.charIndex = 0;
    this.isDeleting = false;
    this.type();
  }

  type() {
    const current = this.texts[this.textIndex];
    if (this.isDeleting) {
      this.el.textContent = current.substring(0, this.charIndex - 1);
      this.charIndex--;
    } else {
      this.el.textContent = current.substring(0, this.charIndex + 1);
      this.charIndex++;
    }

    let delay = this.isDeleting ? this.deleteSpeed : this.speed;

    if (!this.isDeleting && this.charIndex === current.length) {
      delay = this.pause;
      this.isDeleting = true;
    } else if (this.isDeleting && this.charIndex === 0) {
      this.isDeleting = false;
      this.textIndex = (this.textIndex + 1) % this.texts.length;
      delay = 400;
    }
    setTimeout(() => this.type(), delay);
  }
}


// ── 4. CARD 3D TILT ───────────────────────────────────
class Tilt3D {
  constructor(selector, intensity = 8) {
    document.querySelectorAll(selector).forEach(card => {
      card.style.transformStyle = 'preserve-3d';
      card.style.transition = 'transform 0.1s ease';
      card.style.willChange = 'transform';

      // Sheen element
      const sheen = document.createElement('div');
      sheen.className = 'tilt-sheen';
      card.style.position = card.style.position || 'relative';
      card.appendChild(sheen);

      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const cx = rect.left + rect.width / 2;
        const cy = rect.top + rect.height / 2;
        const rx = ((e.clientY - cy) / (rect.height / 2)) * intensity;
        const ry = ((e.clientX - cx) / (rect.width / 2)) * -intensity;
        card.style.transform = `perspective(700px) rotateX(${rx}deg) rotateY(${ry}deg) scale3d(1.03,1.03,1.03)`;

        // Sheen follow
        const px = ((e.clientX - rect.left) / rect.width) * 100;
        const py = ((e.clientY - rect.top) / rect.height) * 100;
        sheen.style.background = `radial-gradient(circle at ${px}% ${py}%, rgba(201,168,76,0.18) 0%, transparent 65%)`;
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(700px) rotateX(0deg) rotateY(0deg) scale3d(1,1,1)';
        card.style.transition = 'transform 0.5s cubic-bezier(0.23,1,0.32,1)';
        sheen.style.background = 'none';
      });
      card.addEventListener('mouseenter', () => {
        card.style.transition = 'transform 0.1s ease';
      });
    });
  }
}

// ── 5. SCROLL REVEAL AVANCÉ ───────────────────────────
class ScrollReveal {
  constructor() {
    this.observer = new IntersectionObserver((entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          const el = entry.target;
          const delay = parseInt(el.dataset.delay || 0);
          const stagger = parseInt(el.dataset.stagger || 0) * (Array.from(el.parentElement?.children || []).indexOf(el));
          setTimeout(() => {
            el.classList.add('sr-visible');
          }, delay + stagger);
          this.observer.unobserve(el);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

    // Auto-assign animation types based on position
    document.querySelectorAll('.reveal').forEach((el, i) => {
      el.classList.add('sr-el');
      const siblings = Array.from(el.parentElement?.children || []);
      const idx = siblings.filter(s => s.classList.contains('reveal')).indexOf(el);
      if (idx > 0) el.dataset.delay = idx * 100;
      this.observer.observe(el);
    });
  }
}

// ── 6. PROGRESS BAR (lecture) ─────────────────────────
function initReadProgress() {
  const bar = document.createElement('div');
  bar.id = 'read-progress';
  document.body.appendChild(bar);
  window.addEventListener('scroll', () => {
    const h = document.documentElement;
    const pct = (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100;
    bar.style.width = pct + '%';
  }, { passive: true });
}

// ── 7. MAGNETIC BUTTONS ───────────────────────────────
function initMagneticButtons() {
  document.querySelectorAll('.btn-primary, .btn-navy, .nav-cta').forEach(btn => {
    btn.addEventListener('mousemove', (e) => {
      const rect = btn.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const dx = (e.clientX - cx) * 0.25;
      const dy = (e.clientY - cy) * 0.25;
      btn.style.transform = `translate(${dx}px, ${dy}px) scale(1.04)`;
    });
    btn.addEventListener('mouseleave', () => {
      btn.style.transform = '';
      btn.style.transition = 'transform 0.4s cubic-bezier(0.23,1,0.32,1)';
    });
    btn.addEventListener('mouseenter', () => {
      btn.style.transition = 'transform 0.1s ease';
    });
  });
}

// ── 8. SMOOTH PAGE TRANSITIONS ────────────────────────
function initPageTransitions() {
  const overlay = document.createElement('div');
  overlay.id = 'page-transition';
  document.body.appendChild(overlay);

  // Fade in on load
  requestAnimationFrame(() => {
    overlay.classList.add('fade-out');
  });

  document.querySelectorAll('a[href]').forEach(link => {
    const href = link.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('mailto') || href.startsWith('tel') || href.startsWith('http') || link.target === '_blank') return;
    link.addEventListener('click', (e) => {
      e.preventDefault();
      overlay.classList.remove('fade-out');
      overlay.classList.add('fade-in');
      setTimeout(() => { window.location.href = href; }, 380);
    });
  });
}

// ── 9. COUNTING ANIMATION (easing) ────────────────────

function initCounters() {
  const easeOut = t => 1 - Math.pow(1 - t, 3);
  document.querySelectorAll('.counter[data-target]').forEach(el => {
    const obs = new IntersectionObserver((entries) => {
      if (!entries[0].isIntersecting) return;
      obs.disconnect();
      const target = parseInt(el.dataset.target);
      const duration = 1800;
      const start = performance.now();
      const animate = (now) => {
        const progress = Math.min((now - start) / duration, 1);
        el.textContent = Math.round(easeOut(progress) * target).toLocaleString('fr-FR');
        if (progress < 1) requestAnimationFrame(animate);
      };
      requestAnimationFrame(animate);
    }, { threshold: 0.5 });
    obs.observe(el);
  });
}
// ── 10. SECTION PARALLAX ──────────────────────────────
function initParallax() {
  const els = document.querySelectorAll('[data-parallax]');
  if (!els.length) return;
  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;
    els.forEach(el => {
      const speed = parseFloat(el.dataset.parallax || 0.3);
      const rect = el.getBoundingClientRect();
      const offset = (rect.top + scrollY - window.innerHeight / 2) * speed;
      el.style.transform = `translateY(${offset * 0.1}px)`;
    });
  }, { passive: true });
}

// ── 11. STAGGER GRID ANIMATION ────────────────────────
function initStaggerGrids() {
  document.querySelectorAll('.services-grid, .grid-3, .grid-4, .grid-2').forEach(grid => {
    const children = Array.from(grid.children);
    children.forEach((child, i) => {
      if (!child.classList.contains('reveal')) {
        child.classList.add('reveal', 'sr-el');
        child.dataset.delay = i * 80;
        child.style.opacity = '0';
      }
    });
  });
}

// ── 12. GOLD RIPPLE ON CLICK ──────────────────────────
function initRipple() {
  document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const ripple = document.createElement('span');
      ripple.className = 'btn-ripple';
      const rect = btn.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      ripple.style.cssText = `
        width:${size}px; height:${size}px;
        left:${e.clientX - rect.left - size/2}px;
        top:${e.clientY - rect.top - size/2}px;
      `;
      btn.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);
    });
  });
}

// ── 13. HERO TEXT GLITCH (subtil) ─────────────────────
function initHeroGlitch() {
  const hero = document.querySelector('.hero h1');
  if (!hero) return;
  setInterval(() => {
    if (Math.random() > 0.97) {
      hero.style.textShadow = `2px 0 rgba(201,168,76,0.4), -2px 0 rgba(21,36,56,0.4)`;
      setTimeout(() => hero.style.textShadow = '', 80);
    }
  }, 800);
}

// ── 14. NAVBAR HIDE/SHOW ON SCROLL ────────────────────
function initSmartNavbar() {
  let lastY = 0;
  const nav = document.querySelector('.navbar');
  if (!nav) return;
  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    if (y > lastY && y > 120) {
      nav.style.transform = 'translateY(-100%)';
    } else {
      nav.style.transform = 'translateY(0)';
    }
    lastY = y;
  }, { passive: true });
}

// ═══════════════════════════════════════════════════════
// INIT ALL
// ═══════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {
  // Only on desktop
  const isMobile = window.innerWidth < 768;

  if (!isMobile) {
    initMagneticButtons();
    new Tilt3D('.service-card', 6);
    new Tilt3D('.catalogue-card', 5);
    new Tilt3D('.blog-card', 4);
  }

  initReadProgress();
  initPageTransitions();
  initCounters();
  initStaggerGrids();
  new ScrollReveal();
  initParallax();
  initRipple();
  initHeroGlitch();
  initSmartNavbar();

  // Particules sur le hero
  if (document.getElementById('hero-canvas')) {
    new HeroParticles('hero-canvas');
  }

  // Typewriter sur le hero
  const twEl = document.getElementById('typewriter-text');
  if (twEl) {
    new Typewriter(twEl, [
      'l\'Architecture',
      'l\'Informatique',
      'la Plomberie',
      'l\'Électricité',
      'la Construction',
      'votre projet',
    ], { speed: 70, deleteSpeed: 35, pause: 2200 });
  }
});
