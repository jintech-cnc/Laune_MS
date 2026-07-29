// La Une Multiservice — Lightbox Gallery

let lightboxImages = [];
let currentIndex = 0;

function initLightbox() {
  // Build lightbox DOM if not present
  if (document.getElementById('lightbox')) return;

  const lb = document.createElement('div');
  lb.id = 'lightbox';
  lb.innerHTML = `
    <button id="lightbox-close" onclick="closeLightbox()">✕</button>
    <button id="lightbox-prev" onclick="lightboxNav(-1)">‹</button>
    <img id="lightbox-img" src="" alt="">
    <button id="lightbox-next" onclick="lightboxNav(1)">›</button>
    <div id="lightbox-caption"></div>
  `;
  document.body.appendChild(lb);

  lb.addEventListener('click', (e) => {
    if (e.target === lb) closeLightbox();
  });

  document.addEventListener('keydown', (e) => {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft') lightboxNav(-1);
    if (e.key === 'ArrowRight') lightboxNav(1);
  });
}

function openLightbox(images, index) {
  initLightbox();
  lightboxImages = images;
  currentIndex = index;
  showLightboxImage();
  document.getElementById('lightbox').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeLightbox() {
  document.getElementById('lightbox').classList.remove('open');
  document.body.style.overflow = '';
}

function lightboxNav(dir) {
  currentIndex = (currentIndex + dir + lightboxImages.length) % lightboxImages.length;
  showLightboxImage();
}

function showLightboxImage() {
  const img = lightboxImages[currentIndex];
  const el = document.getElementById('lightbox-img');
  const cap = document.getElementById('lightbox-caption');
  const prev = document.getElementById('lightbox-prev');
  const next = document.getElementById('lightbox-next');

  el.style.opacity = '0';
  el.style.transform = 'scale(0.97)';
  el.src = img.src;
  el.onload = () => {
    el.style.transition = 'opacity 0.25s, transform 0.25s';
    el.style.opacity = '1';
    el.style.transform = 'scale(1)';
  };
  cap.textContent = img.caption || '';
  prev.style.display = lightboxImages.length > 1 ? 'flex' : 'none';
  next.style.display = lightboxImages.length > 1 ? 'flex' : 'none';
}

// Auto-init all .gallery-thumb elements
document.addEventListener('DOMContentLoaded', () => {
  const containers = document.querySelectorAll('[data-gallery]');
  containers.forEach(container => {
    const galleryId = container.dataset.gallery;
    const thumbs = container.querySelectorAll('.gallery-thumb');
    const images = Array.from(thumbs).map(t => ({
      src: t.dataset.full || t.querySelector('img')?.src,
      caption: t.dataset.caption || '',
    }));
    thumbs.forEach((thumb, i) => {
      thumb.addEventListener('click', () => openLightbox(images, i));
    });
  });
});
