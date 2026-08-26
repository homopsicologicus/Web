(function () {
  "use strict";

  var root = document.documentElement;
  var STORAGE_KEY = "hp-theme";

  function isDark() {
    return root.getAttribute("data-theme") === "dark";
  }

  function setTheme(theme) {
    if (theme) {
      root.setAttribute("data-theme", theme);
    } else {
      root.removeAttribute("data-theme");
    }
    updateToggleUI();
  }

  function currentTheme() {
    var attr = root.getAttribute("data-theme");
    if (attr === "dark" || attr === "light") return attr;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function updateToggleUI() {
    var btn = document.querySelector(".theme-toggle");
    if (!btn) return;
    var dark = isDark();
    btn.setAttribute("aria-pressed", String(dark));
    btn.setAttribute("aria-label", dark ? "Cambiar a tema claro" : "Cambiar a tema oscuro");
    btn.title = dark ? "Cambiar a tema claro" : "Cambiar a tema oscuro";
  }

  /* Si el script inline del <head> no aplicó tema, aplica el guardado */
  if (!root.getAttribute("data-theme")) {
    try {
      var saved = localStorage.getItem(STORAGE_KEY);
      if (saved === "dark" || saved === "light") root.setAttribute("data-theme", saved);
    } catch (e) { /* storage unavailable */ }
  }
  updateToggleUI();

  function toggle() {
    var next = currentTheme() === "dark" ? "light" : "dark";
    root.classList.add("theme-fade");
    setTheme(next);
    try {
      localStorage.setItem(STORAGE_KEY, next);
    } catch (e) { /* storage unavailable */ }
    clearTimeout(toggle._t);
    toggle._t = setTimeout(function () {
      root.classList.remove("theme-fade");
    }, 700);
  }

  /* Clic directo + delegation como respaldo */
  document.addEventListener("click", function (e) {
    var t = e.target;
    while (t && t !== document) {
      if (t.classList && t.classList.contains("theme-toggle")) {
        toggle();
        return;
      }
      t = t.parentNode;
    }
  });

  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () {
    if (!root.getAttribute("data-theme")) updateToggleUI();
  });

  /* ---- Parallax sutil del hero ---- */
  var heroMedia = document.querySelector(".hero-media");
  if (heroMedia && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var ticking = false;
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        heroMedia.style.transform = "translateY(" + (window.scrollY * 0.18) + "px)";
        ticking = false;
      });
    }, { passive: true });
  }

  /* ---- Reveal on scroll ---- */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* ---- Footer year ---- */
  var yearEl = document.querySelector(".footer-year");
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  /* ---- Accordion: solo uno abierto a la vez ---- */
  var detailsEls = Array.prototype.slice.call(document.querySelectorAll(".faq"));
  detailsEls.forEach(function (d) {
    d.addEventListener("toggle", function () {
      if (!d.open) return;
      detailsEls.forEach(function (other) {
        if (other !== d) other.open = false;
      });
    });
  });

  /* ---- Tooltips ---- */
  var tipEls = document.querySelectorAll("[data-tip]");
  if (tipEls.length) {
    var tipBox = document.createElement("span");
    tipBox.className = "tooltip-tip";
    tipBox.setAttribute("role", "tooltip");
    tipBox.hidden = true;
    document.body.appendChild(tipBox);

    function positionTip(el) {
      var r = el.getBoundingClientRect();
      tipBox.style.top = (r.top - tipBox.offsetHeight - 8 + window.scrollY) + "px";
      tipBox.style.left = (r.left + window.scrollX) + "px";
    }

    tipEls.forEach(function (el) {
      function show() {
        tipBox.textContent = el.getAttribute("data-tip");
        tipBox.hidden = false;
        positionTip(el);
      }
      function hide() {
        tipBox.hidden = true;
      }
      el.addEventListener("mouseenter", show);
      el.addEventListener("mouseleave", hide);
      el.addEventListener("focus", show);
      el.addEventListener("blur", hide);
      window.addEventListener("resize", hide);
    });
  }

  /* ---- Scrollspy (índice "en esta página") ---- */
  var toc = document.querySelector(".toc");
  if (toc && "IntersectionObserver" in window) {
    var tocLinks = Array.prototype.slice.call(toc.querySelectorAll("a[href^='#']"));
    var targets = tocLinks.map(function (a) { return document.querySelector(a.getAttribute("href")); }).filter(Boolean);
    if (targets.length) {
      var spy = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var id = entry.target.getAttribute("id");
            tocLinks.forEach(function (a) {
              a.classList.toggle("is-active", a.getAttribute("href") === "#" + id);
            });
          }
        });
      }, { rootMargin: "-20% 0px -70% 0px" });
      targets.forEach(function (t) { spy.observe(t); });
    }

    var toggle = document.querySelector(".toc-toggle");
    if (toggle) {
      toggle.addEventListener("click", function () {
        var hidden = toc.hasAttribute("hidden");
        if (hidden) {
          toc.removeAttribute("hidden");
          toggle.setAttribute("aria-expanded", "true");
        } else {
          toc.setAttribute("hidden", "");
          toggle.setAttribute("aria-expanded", "false");
        }
      });
    }
  }
})();