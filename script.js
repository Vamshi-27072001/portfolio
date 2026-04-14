/* =============================================
   VAMSHI YADAV GOLLA — PORTFOLIO JS
============================================= */
'use strict';

/* ---- LOADER ---- */
const loader = document.getElementById('loader');
document.body.style.overflow = 'hidden';
window.addEventListener('load', () => {
  setTimeout(() => {
    loader.classList.add('hidden');
    document.body.style.overflow = '';
    revealOnScroll();
  }, 1300);
});

/* ---- THEME TOGGLE ---- */
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');
const html = document.documentElement;
const saved = localStorage.getItem('theme');
if (saved) html.setAttribute('data-theme', saved);
updateIcon(html.getAttribute('data-theme'));

themeToggle.addEventListener('click', () => {
  const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  updateIcon(next);
});

function updateIcon(t) {
  themeIcon.className = t === 'dark' ? 'ri-sun-line' : 'ri-moon-line';
}

/* ---- NAVBAR ---- */
const navbar = document.getElementById('navbar');
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('section[id]');

window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', scrollY > 20);
  let cur = '';
  sections.forEach(s => { if (scrollY >= s.offsetTop - 100) cur = s.id; });
  navLinks.forEach(l => {
    l.classList.toggle('active', l.getAttribute('href') === '#' + cur);
  });
}, { passive: true });

/* ---- MOBILE MENU ---- */
const hamburger = document.getElementById('hamburger');
const navLinksEl = document.getElementById('navLinks');
hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('active');
  navLinksEl.classList.toggle('open');
  document.body.classList.toggle('no-scroll');
});
navLinksEl.querySelectorAll('.nav-link').forEach(l => {
  l.addEventListener('click', () => {
    hamburger.classList.remove('active');
    navLinksEl.classList.remove('open');
    document.body.classList.remove('no-scroll');
  });
});

/* ---- SCROLL REVEAL ---- */
const revealEls = document.querySelectorAll('.reveal');
const revealObs = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const siblings = [...entry.target.parentElement.querySelectorAll('.reveal')];
      entry.target.style.transitionDelay = (siblings.indexOf(entry.target) * 70) + 'ms';
      entry.target.classList.add('visible');
      revealObs.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });

function revealOnScroll() {
  revealEls.forEach(el => revealObs.observe(el));
}

/* ---- SKILL BAR ANIMATION ---- */
document.querySelectorAll('.skill-fill').forEach(f => {
  new IntersectionObserver(([e]) => {
    if (e.isIntersecting) { f.style.width = f.dataset.width + '%'; }
  }, { threshold: 0.3 }).observe(f);
});

/* ---- PROJECT FILTER ---- */
const filterBtns = document.querySelectorAll('.filter-btn');
const projectCards = document.querySelectorAll('.project-showcase');

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const filter = btn.dataset.filter;
    projectCards.forEach(card => {
      const match = filter === 'all' || card.dataset.category === filter;
      card.classList.toggle('hidden', !match);
    });
  });
});

/* ---- CONTACT FORM ---- */
const form = document.getElementById('contactForm');
const fields = {
  name:    { el: document.getElementById('name'),    err: document.getElementById('nameError'),    msg: 'Please enter your name.' },
  email:   { el: document.getElementById('email'),   err: document.getElementById('emailError'),   msg: 'Please enter a valid email.' },
  subject: { el: document.getElementById('subject'), err: document.getElementById('subjectError'), msg: 'Please enter a subject.' },
  message: { el: document.getElementById('message'), err: document.getElementById('messageError'), msg: 'Please enter a message.' },
};

function validateField(f) {
  const v = f.el.value.trim();
  if (!v) { setErr(f, true); return false; }
  if (f.el.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) { setErr(f, true); return false; }
  setErr(f, false); return true;
}
function setErr(f, show) {
  f.el.classList.toggle('error', show);
  f.err.textContent = show ? f.msg : '';
  f.err.classList.toggle('visible', show);
}

Object.values(fields).forEach(f => {
  f.el.addEventListener('blur', () => validateField(f));
  f.el.addEventListener('input', () => { if (f.el.classList.contains('error')) validateField(f); });
});

form.addEventListener('submit', e => {
  e.preventDefault();
  let ok = true;
  Object.values(fields).forEach(f => { if (!validateField(f)) ok = false; });
  if (!ok) return;

  const btn = form.querySelector('button[type="submit"]');
  const txt = form.querySelector('.btn-text');
  const load = form.querySelector('.btn-loading');
  const success = document.getElementById('formSuccess');

  txt.hidden = true; load.hidden = false; btn.disabled = true;
  setTimeout(() => {
    txt.hidden = false; load.hidden = true; btn.disabled = false;
    success.hidden = false; form.reset();
    setTimeout(() => { success.hidden = true; }, 5000);
  }, 1500);
});

/* ---- BACK TO TOP ---- */
const btt = document.getElementById('backToTop');
window.addEventListener('scroll', () => { btt.classList.toggle('visible', scrollY > 400); }, { passive: true });
btt.addEventListener('click', () => { scrollTo({ top: 0, behavior: 'smooth' }); });

/* ---- SMOOTH SCROLL ---- */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (!target) return;
    e.preventDefault();
    const top = target.offsetTop - (parseInt(getComputedStyle(html).getPropertyValue('--nav-h')) || 68);
    scrollTo({ top, behavior: 'smooth' });
  });
});

/* ---- HIRE-ME FLOATING WIDGET ---- */
const hireWidget = document.getElementById('hireWidget');
const hireToggle = document.getElementById('hireWidgetToggle');
if (hireWidget && hireToggle) {
  hireToggle.addEventListener('click', (e) => {
    e.stopPropagation();
    const isOpen = hireWidget.classList.toggle('open');
    hireToggle.setAttribute('aria-expanded', String(isOpen));
  });
  document.addEventListener('click', (e) => {
    if (!hireWidget.contains(e.target)) {
      hireWidget.classList.remove('open');
      hireToggle.setAttribute('aria-expanded', 'false');
    }
  });
}

/* ---- SUBTLE CARD HOVER ---- */
document.querySelectorAll('.skill-card, .cert-card, .metric').forEach(card => {
  card.addEventListener('mousemove', e => {
    const r = card.getBoundingClientRect();
    const x = ((e.clientX - r.left) / r.width - .5) * 6;
    const y = ((e.clientY - r.top) / r.height - .5) * -6;
    card.style.transform = `perspective(600px) rotateY(${x}deg) rotateX(${y}deg) translateY(-4px)`;
  });
  card.addEventListener('mouseleave', () => { card.style.transform = ''; });
});
