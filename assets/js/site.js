/* Bambine — interacties. Geen dependencies, progressief verbeterend. */
(function () {
  "use strict";

  /* In GoHighLevel staat elke sectie in een eigen blok. Dit script zit in het
     eerste blok en zou dan draaien voordat de secties eronder bestaan, dus
     wachten we tot de pagina volledig is ingelezen. */
  function start() {

    var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var $ = function (s, c) { return (c || document).querySelector(s); };
    var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

    /* 1. Reveal-on-scroll ---------------------------------------------------- */
    var revealables = $$("[data-reveal]");
    if (revealables.length) {
      if (!("IntersectionObserver" in window) || reduced) {
        revealables.forEach(function (el) { el.classList.add("is-in"); });
      } else {
        var io = new IntersectionObserver(function (entries) {
          entries.forEach(function (e) {
            if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
          });
        }, { rootMargin: "0px 0px -12% 0px", threshold: 0.08 });
        revealables.forEach(function (el, i) {
          if (!el.style.getPropertyValue("--d")) {
            var sib = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : i;
            el.style.setProperty("--d", Math.min(sib, 5) * 90 + "ms");
          }
          io.observe(el);
        });
      }
    }

    /* 2. Sticky header + mobiele actiebalk ----------------------------------- */
    var header = $(".site-header");
    var actionBar = $(".action-bar");
    var cover = $(".hero-cover");
    var lastY = window.scrollY;

    /* De hero schuift onder de kop door; die hoogte moet de stijl kennen. */
    function meetKop() {
      if (!header) return;
      document.documentElement.style.setProperty("--header-h", header.offsetHeight + "px");
    }
    meetKop();
    window.addEventListener("resize", meetKop, { passive: true });

    function onScroll() {
      var y = window.scrollY;
      if (header) header.classList.toggle("is-stuck", y > 12);
      /* Doorzichtige kop zolang die nog over het hero-beeld staat. */
      if (header && cover) {
        header.classList.toggle("is-over", y < cover.offsetHeight - header.offsetHeight * 1.5);
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
      if (open) { var f = $("a, button", drawer); if (f) f.focus(); }
      else if (openBtn) openBtn.focus();
    }
    if (openBtn) openBtn.addEventListener("click", function () { setDrawer(drawer.dataset.open !== "true"); });
    $$("[data-drawer-close]").forEach(function (b) { b.addEventListener("click", function () { setDrawer(false); }); });
    if (drawer) $$("a", drawer).forEach(function (a) { a.addEventListener("click", function () { setDrawer(false); }); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && drawer && drawer.dataset.open === "true") setDrawer(false);
    });

    /* 4. FAQ-accordeon ------------------------------------------------------- */
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

    /* 5. Tellers ------------------------------------------------------------- */
    var counters = $$("[data-count]");
    if (counters.length && "IntersectionObserver" in window) {
      var cio = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          cio.unobserve(e.target);
          var el = e.target;
          var to = parseFloat(el.dataset.count);
          var dec = (el.dataset.count.split(".")[1] || "").length;
          var suffix = el.dataset.suffix || "";
          var prefix = el.dataset.prefix || "";
          if (reduced) { el.textContent = prefix + to.toFixed(dec).replace(".", ",") + suffix; return; }
          var start = performance.now();
          var dur = 1400;
          (function tick(now) {
            var p = Math.min(1, (now - start) / dur);
            var eased = 1 - Math.pow(1 - p, 3);
            el.textContent = prefix + (to * eased).toFixed(dec).replace(".", ",") + suffix;
            if (p < 1) requestAnimationFrame(tick);
          })(start);
        });
      }, { threshold: 0.5 });
      counters.forEach(function (c) { cio.observe(c); });
    }

    /* 6. Stappen: voortgangslijn + actieve stap ------------------------------ */
    var steps = $(".steps");
    if (steps && !reduced) {
      var items = $$(".step", steps);
      var ticking = false;
      var update = function () {
        var r = steps.getBoundingClientRect();
        var anchor = window.innerHeight * 0.55;
        var p = Math.max(0, Math.min(1, (anchor - r.top) / Math.max(1, r.height)));
        steps.style.setProperty("--progress", (p * 100).toFixed(2) + "%");
        items.forEach(function (it) {
          var ir = it.getBoundingClientRect();
          it.classList.toggle("is-on", ir.top < anchor && ir.bottom > 0);
        });
        ticking = false;
      };
      window.addEventListener("scroll", function () {
        if (!ticking) { ticking = true; requestAnimationFrame(update); }
      }, { passive: true });
      update();
    }

    /* 7. Zachte parallax in de galerij --------------------------------------- */
    var par = $$("[data-parallax]");
    if (par.length && !reduced) {
      var pTick = false;
      var move = function () {
        par.forEach(function (el) {
          var r = el.getBoundingClientRect();
          if (r.bottom < -200 || r.top > window.innerHeight + 200) return;
          var mid = r.top + r.height / 2 - window.innerHeight / 2;
          var amt = parseFloat(el.dataset.parallax) || 12;
          el.style.transform = "translate3d(0," + (-mid / window.innerHeight * amt).toFixed(2) + "px,0)";
        });
        pTick = false;
      };
      window.addEventListener("scroll", function () {
        if (!pTick) { pTick = true; requestAnimationFrame(move); }
      }, { passive: true });
      move();
    }

    /* 8. Jaartal ------------------------------------------------------------ */
    $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

    /* 9. Actieve pagina in de navigatie -------------------------------------- */
    /* In GoHighLevel staat de navigatie als globale sectie op elke pagina, dus
       de actieve link wordt hier bepaald in plaats van in de opmaak. */
    var hier = window.location.pathname.replace(/\.html$/, "").replace(/\/+$/, "");
    $$(".nav-links a, .drawer-links a").forEach(function (a) {
      var doel = (a.getAttribute("href") || "").split("#")[0].replace(/\.html$/, "").replace(/^\.?\/?/, "/");
      if (doel !== "/" && hier.slice(-doel.length) === doel) a.setAttribute("aria-current", "page");
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
