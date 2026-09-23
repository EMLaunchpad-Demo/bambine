/* Bambine — interacties. Geen dependencies, progressief verbeterend. */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* 1. Reveal bij scrollen ------------------------------------------------- */
  var revealables = $$("[data-reveal]");
  if (!("IntersectionObserver" in window) || reduced) {
    revealables.forEach(function (el) { el.classList.add("is-in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -10% 0px", threshold: 0.06 });
    var inBeeld = [];
    revealables.forEach(function (el) {
      if (!el.style.getPropertyValue("--d") && el.parentElement) {
        var sib = Array.prototype.indexOf.call(el.parentElement.children, el);
        el.style.setProperty("--d", Math.min(sib, 5) * 90 + "ms");
      }
      /* Wat bij het laden al in beeld staat, wacht niet op de observer: die
         vuurt niet altijd meteen (bv. in een tabblad op de achtergrond). */
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight && r.bottom > 0) inBeeld.push(el);
      else io.observe(el);
    });
    setTimeout(function () {
      inBeeld.forEach(function (el) { el.classList.add("is-in"); });
    }, 40);
  }

  /* 2. Kop en mobiele actiebalk ------------------------------------------- */
  var header = $(".site-header");
  var actionBar = $(".action-bar");
  var cover = $(".hero-cover");
  var lastY = window.scrollY;

  /* De hero schuift onder de kop door; die hoogte moet de stijl kennen. */
  function meetKop() {
    if (header) document.documentElement.style.setProperty("--header-h", header.offsetHeight + "px");
  }
  meetKop();
  window.addEventListener("resize", meetKop, { passive: true });

  function onScroll() {
    var y = window.scrollY;
    if (header) {
      header.classList.toggle("is-stuck", y > 12);
      /* Doorzichtige kop zolang die nog over het hero-beeld staat. */
      if (cover) header.classList.toggle("is-over", y < cover.offsetHeight - header.offsetHeight * 1.5);
    }
    if (actionBar) actionBar.classList.toggle("is-on", y > 520 || (y > 200 && y < lastY));
    lastY = y;
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* 3. Mobiel menu --------------------------------------------------------- */
  var drawer = $("#drawer");
  var openBtn = $(".nav-toggle");
  function setDrawer(open) {
    if (!drawer) return;
    drawer.dataset.open = open ? "true" : "false";
    drawer.setAttribute("aria-hidden", open ? "false" : "true");
    if (openBtn) openBtn.setAttribute("aria-expanded", open ? "true" : "false");
    document.documentElement.style.overflow = open ? "hidden" : "";
    /* Pas focussen als het menu zichtbaar is; een verborgen element neemt geen focus. */
    if (open) setTimeout(function () { var f = $(".drawer-close", drawer); if (f) f.focus(); }, 60);
    else if (openBtn) openBtn.focus();
  }
  if (openBtn) openBtn.addEventListener("click", function () { setDrawer(drawer.dataset.open !== "true"); });
  $$("[data-drawer-close]").forEach(function (b) { b.addEventListener("click", function () { setDrawer(false); }); });
  if (drawer) $$("a", drawer).forEach(function (a) { a.addEventListener("click", function () { setDrawer(false); }); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && drawer && drawer.dataset.open === "true") setDrawer(false);
  });

  /* 4. Veelgestelde vragen ------------------------------------------------- */
  $$(".faq-item").forEach(function (item) {
    var q = $(".faq-q", item);
    if (!q) return;
    q.addEventListener("click", function () {
      var open = item.classList.contains("is-open");
      var group = item.closest(".faq");
      if (group && !open) {
        $$(".faq-item.is-open", group).forEach(function (o) {
          o.classList.remove("is-open");
          $(".faq-q", o).setAttribute("aria-expanded", "false");
        });
      }
      item.classList.toggle("is-open", !open);
      q.setAttribute("aria-expanded", !open ? "true" : "false");
    });
  });

  /* 5. Kaart: Google Maps pas laden na een klik ---------------------------- */
  $$(".map").forEach(function (map) {
    var btn = $(".map-load", map);
    if (!btn) return;
    btn.addEventListener("click", function () {
      var frame = document.createElement("iframe");
      frame.src = map.getAttribute("data-map");
      frame.title = "Kaart: Bambine, Michiel Jansplein 28/b2 in Lommel";
      frame.loading = "lazy";
      frame.referrerPolicy = "no-referrer-when-downgrade";
      map.appendChild(frame);
      map.classList.add("is-loaded");
      frame.focus();
    });
  });

  /* 6. Jaartal ------------------------------------------------------------ */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
