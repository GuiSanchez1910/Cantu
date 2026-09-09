// ---------- CONFIG ----------
    const WHATSAPP_NUMBER = "5541999537953";

    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileNavPanel = document.getElementById('mobileNavPanel');
    const mobileNavBackdrop = document.getElementById('mobileNavBackdrop');

    function closeMobileMenu() {
      mobileNavPanel?.classList.remove('is-open');
      mobileNavBackdrop?.classList.remove('is-open');
      mobileMenuToggle?.setAttribute('aria-expanded', 'false');
      mobileMenuToggle?.setAttribute('aria-label', 'Abrir menu');
    }

    if (mobileMenuToggle && mobileNavPanel && mobileNavBackdrop) {
      mobileMenuToggle.addEventListener('click', () => {
        const isOpen = mobileNavPanel.classList.toggle('is-open');
        mobileNavBackdrop.classList.toggle('is-open', isOpen);
        mobileMenuToggle.setAttribute('aria-expanded', String(isOpen));
        mobileMenuToggle.setAttribute('aria-label', isOpen ? 'Fechar menu' : 'Abrir menu');
      });

      mobileNavBackdrop.addEventListener('click', closeMobileMenu);
      mobileNavPanel.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', closeMobileMenu);
      });

      document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') closeMobileMenu();
      });
    }

    // ---------- Ano atual ----------

    // ---------- WhatsApp links + fallback ----------
    document.querySelectorAll('[data-wa]').forEach(el => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        const msg = el.getAttribute('data-msg') || 'Olá! Gostaria de um orçamento.';
        const url = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(msg)}`;
        const start = Date.now();
        window.open(url, '_blank');
        setTimeout(() => {
          if (!document.hidden && Date.now() - start < 2500) {
            showFallback();
          }
        }, 1500);
      });
    });

    const fallback = document.getElementById('waFallback');
    function showFallback() { fallback.classList.add('show'); }
    document.getElementById('closeFallback').addEventListener('click', () => fallback.classList.remove('show'));
    document.getElementById('copyNumber').addEventListener('click', () => {
      navigator.clipboard?.writeText(WHATSAPP_NUMBER.replace('55', '+55 '));
      const btn = document.getElementById('copyNumber');
      const original = btn.textContent;
      btn.textContent = 'Copiado!';
      setTimeout(() => btn.textContent = original, 1600);
    });

    // ---------- Carousel ----------
    const slides = document.querySelectorAll('.slide');
    const dotsWrap = document.getElementById('dots');
    const heroTitle = document.getElementById('heroTitle');
    const heroDescription = document.getElementById('heroDescription');
    let current = 0;
    slides.forEach((_, i) => {
      const b = document.createElement('button');
      if (i === 0) b.classList.add('active');
      b.setAttribute('aria-label', `Ir para o slide ${i + 1}`);
      b.addEventListener('click', () => goTo(i));
      dotsWrap.appendChild(b);
    });
    function goTo(i) {
      slides[current].classList.remove('active');
      dotsWrap.children[current].classList.remove('active');
      current = (i + slides.length) % slides.length;
      slides[current].classList.add('active');
      dotsWrap.children[current].classList.add('active');
      heroTitle.innerHTML = slides[current].dataset.title;
heroDescription.innerHTML = slides[current].dataset.description;    }
    document.getElementById('nextBtn').addEventListener('click', () => goTo(current + 1));
    document.getElementById('prevBtn').addEventListener('click', () => goTo(current - 1));

    let auto;
    function startAuto() {
      clearInterval(auto);
      auto = setInterval(() => goTo(current + 1), 5000);
    }

    const carousel = document.getElementById('carousel');
    carousel.addEventListener('mouseenter', () => clearInterval(auto));
    carousel.addEventListener('mouseleave', startAuto);

    let touchStartX = 0;
    carousel.addEventListener('touchstart', (event) => {
      touchStartX = event.changedTouches[0].clientX;
      clearInterval(auto);
    }, { passive: true });
    carousel.addEventListener('touchend', (event) => {
      const distance = event.changedTouches[0].clientX - touchStartX;
      if (Math.abs(distance) > 40) goTo(current + (distance < 0 ? 1 : -1));
      startAuto();
    }, { passive: true });

    startAuto();

    // ---------- Product carousel ----------
    document.querySelectorAll('.prod-carousel-wrap').forEach((carouselWrap) => {
      const prodTrack = carouselWrap.querySelector('.prod-track');
      const prodPrevBtn = carouselWrap.querySelector('.prod-car-btn.prev');
      const prodNextBtn = carouselWrap.querySelector('.prod-car-btn.next');
      const prodCards = prodTrack.querySelectorAll('.prod-card');
      let prodIndex = 0;

      function getVisibleCount() {
        if (window.innerWidth <= 560) return 1;
        if (window.innerWidth <= 980) return 2;
        return 4;
      }

      function getMaxIndex() {
        return Math.max(0, prodCards.length - getVisibleCount());
      }

      function getScrollStep() {
        return getVisibleCount() >= 4 ? 2 : 1;
      }

      function updateProdCarousel() {
        const card = prodCards[0];
        if (!card) return;
        const gap = parseFloat(getComputedStyle(prodTrack).gap) || 16;
        const offset = prodIndex * (card.offsetWidth + gap);
        prodTrack.style.transform = `translateX(-${offset}px)`;
        if (prodPrevBtn) prodPrevBtn.disabled = prodIndex <= 0;
        if (prodNextBtn) prodNextBtn.disabled = prodIndex >= getMaxIndex();
      }

      if (prodPrevBtn) {
        prodPrevBtn.addEventListener('click', () => {
          prodIndex = Math.max(0, prodIndex - getScrollStep());
          updateProdCarousel();
        });
      }

      if (prodNextBtn) {
        prodNextBtn.addEventListener('click', () => {
          prodIndex = Math.min(getMaxIndex(), prodIndex + getScrollStep());
          updateProdCarousel();
        });
      }

      window.addEventListener('resize', () => {
        if (prodIndex > getMaxIndex()) prodIndex = getMaxIndex();
        updateProdCarousel();
      });

      updateProdCarousel();
    });

    document.querySelectorAll('[data-gallery]').forEach((gallery) => {
      const images = gallery.querySelectorAll('.prod-images img');
      const dotsWrap = gallery.querySelector('.prod-img-dots');
      const prevBtn = gallery.querySelector('.prod-img-btn.prev');
      const nextBtn = gallery.querySelector('.prod-img-btn.next');
      let imgCurrent = 0;

      if (images.length <= 1) {
        if (prevBtn) prevBtn.style.display = 'none';
        if (nextBtn) nextBtn.style.display = 'none';
        if (dotsWrap) dotsWrap.style.display = 'none';
        return;
      }

      images.forEach((image, index) => {
        image.classList.toggle('active', index === 0);
      });

      if (dotsWrap) {
        dotsWrap.innerHTML = '';
        images.forEach((_, i) => {
          const dot = document.createElement('button');
          dot.type = 'button';
          dot.setAttribute('aria-label', `Ir para a foto ${i + 1}`);
          if (i === 0) dot.classList.add('active');
          dot.addEventListener('click', () => goToImage(i));
          dotsWrap.appendChild(dot);
        });
      }

      function goToImage(i) {
        if (!images.length) return;
        images[imgCurrent].classList.remove('active');
        if (dotsWrap?.children[imgCurrent]) dotsWrap.children[imgCurrent].classList.remove('active');
        imgCurrent = (i + images.length) % images.length;
        images[imgCurrent].classList.add('active');
        if (dotsWrap?.children[imgCurrent]) dotsWrap.children[imgCurrent].classList.add('active');
      }

      if (prevBtn) {
        prevBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          goToImage(imgCurrent - 1);
        });
      }
      if (nextBtn) {
        nextBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          goToImage(imgCurrent + 1);
        });
      }
    });

    // ---------- Reveal on scroll (with stagger for grids) ----------
    document.querySelectorAll('.cat-grid .cat-card').forEach((el, i) => el.style.setProperty('--d', `${i * 90}ms`));
    document.querySelectorAll('.banner-grid .banner-card').forEach((el, i) => el.style.setProperty('--d', `${i * 110}ms`));

    const revealEls = document.querySelectorAll('.reveal, .cat-card, .banner-card');
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    revealEls.forEach(el => io.observe(el));

    // ---------- Page-load entrance ----------
    window.addEventListener('load', () => document.body.classList.add('ready'));
    setTimeout(() => document.body.classList.add('ready'), 400);

    // ---------- Cursor glow inside hero ----------
    const heroEl = document.getElementById('hero');
    const glow = document.getElementById('cursorGlow');
    heroEl.addEventListener('mousemove', (e) => {
      const rect = heroEl.getBoundingClientRect();
      glow.style.left = (e.clientX - rect.left) + 'px';
      glow.style.top = (e.clientY - rect.top) + 'px';
    });
