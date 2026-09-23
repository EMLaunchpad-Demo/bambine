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

  /* 6. Cadeaubon: digitaal of fysiek -------------------------------------- */
  var keuzes = $$('input[name="bon-soort"]');
  var panelen = $$("[data-paneel]");

  /* Het checkout-script zoekt de div vlak vóór zichzelf, dus het komt direct
     achter [data-gc-id]. Pas laden als iemand voor digitaal kiest. */
  function laadCheckout() {
    var box = $(".bon-embed");
    if (!box || box.dataset.geladen) return;
    box.dataset.geladen = "1";
    var doel = $("[data-gc-id]", box);
    var s = document.createElement("script");
    s.src = box.getAttribute("data-gc-src");
    s.async = true;
    s.onload = function () {
      var frame = $("iframe", box);
      if (frame) {
        frame.title = "Digitale cadeaubon van Bambine bestellen";
        frame.addEventListener("load", function () { box.classList.add("is-geladen"); });
      } else {
        box.classList.add("is-geladen");
      }
    };
    doel.parentNode.insertBefore(s, doel.nextSibling);
  }

  function toonBon(soort, scrollen) {
    keuzes.forEach(function (k) { k.checked = k.value === soort; });
    panelen.forEach(function (p) { p.hidden = p.getAttribute("data-paneel") !== soort; });
    if (soort === "digitaal") laadCheckout();
    if (scrollen) {
      var sectie = $("#bestellen");
      if (sectie) sectie.scrollIntoView({ behavior: reduced ? "auto" : "smooth" });
    }
  }

  if (keuzes.length) {
    keuzes.forEach(function (k) {
      k.addEventListener("change", function () {
        toonBon(k.value, false);
        if (history.replaceState) history.replaceState(null, "", "#" + k.value);
      });
    });
    /* #digitaal of #fysiek in de link opent meteen de juiste keuze */
    var volgHash = function () {
      var h = window.location.hash.replace("#", "");
      if (h === "digitaal" || h === "fysiek") { toonBon(h, true); return true; }
      return false;
    };
    window.addEventListener("hashchange", volgHash);
    if (!volgHash()) toonBon((keuzes.filter(function (k) { return k.checked; })[0] || keuzes[0]).value, false);
  }

  /* Bestelformulier fysieke bon: maakt een ingevulde mail klaar */
  var form = $(".bon-form");
  if (form) {
    var wat = $("#bon-wat", form);
    var bedragVeld = $("[data-bedrag]", form);
    var bedrag = $("#bon-bedrag", form);
    var status = $(".bon-status", form);

    wat.addEventListener("change", function () {
      var eigen = wat.value === "bedrag";
      bedragVeld.hidden = !eigen;
      bedrag.required = eigen;
      if (eigen) bedrag.focus();
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var velden = $$("input, select, textarea", form);
      velden.forEach(function (v) { v.removeAttribute("aria-invalid"); });
      /* Alleen het bedragveld mag overgeslagen worden, als het niet van toepassing is. */
      var fout = velden.filter(function (v) {
        var veld = v.closest(".veld");
        return !(veld && veld.hidden) && !v.checkValidity();
      });
      if (fout.length) {
        fout.forEach(function (v) { v.setAttribute("aria-invalid", "true"); });
        status.textContent = "Vul de verplichte velden in.";
        fout[0].focus();
        return;
      }
      var waarde = function (id) { var el = $(id, form); return el ? el.value.trim() : ""; };
      var cadeau = wat.value === "bedrag" ? "Een bedrag van € " + waarde("#bon-bedrag") : wat.value;
      var afhalen = ($('input[name="Afhalen"]:checked', form) || {}).value || "";
      var regels = [
        "Dag Ine,",
        "",
        "Ik wil graag een fysieke cadeaubon bestellen.",
        "",
        "Cadeau: " + cadeau,
        "Afhalen: " + afhalen,
        "Naam: " + waarde("#bon-naam"),
        "E-mail: " + waarde("#bon-mail")
      ];
      if (waarde("#bon-tel")) regels.push("Telefoon: " + waarde("#bon-tel"));
      if (waarde("#bon-noot")) regels.push("", "Opmerking: " + waarde("#bon-noot"));
      regels.push("", "Groetjes,", waarde("#bon-naam"));
      window.location.href = "mailto:info@bambine.be?subject=" +
        encodeURIComponent("Aanvraag fysieke cadeaubon") +
        "&body=" + encodeURIComponent(regels.join("\n"));
      status.textContent = "Je mailprogramma opent met je aanvraag. Verstuur die mail om te bestellen. " +
        "Opent er niets? Mail dan naar info@bambine.be of bel +32 474 78 26 91.";
    });
  }

  /* 7. Jaartal ------------------------------------------------------------ */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
