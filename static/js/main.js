/* China Travel Guide — frontend JS */
(function () {
  "use strict";

  // --- Lazy-load images (native loading=lazy + IntersectionObserver fallback) ---
  function initLazyImages() {
    var imgs = document.querySelectorAll("img[data-src]");
    if (!imgs.length) return;

    if ("loading" in HTMLImageElement.prototype) {
      imgs.forEach(function (img) {
        img.src = img.dataset.src;
        img.removeAttribute("data-src");
      });
      return;
    }
    if ("IntersectionObserver" in window) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var img = entry.target;
            img.src = img.dataset.src;
            img.removeAttribute("data-src");
            observer.unobserve(img);
          }
        });
      });
      imgs.forEach(function (img) { observer.observe(img); });
    } else {
      imgs.forEach(function (img) {
        img.src = img.dataset.src;
        img.removeAttribute("data-src");
      });
    }
  }

  // --- Smooth-scroll TOC links (respect reduced motion) ---
  function initToc() {
    var prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    document.querySelectorAll(".toc a[href^='#']").forEach(function (link) {
      link.addEventListener("click", function (e) {
        var id = link.getAttribute("href").slice(1);
        var target = document.getElementById(id);
        if (!target) return;
        e.preventDefault();
        var y = target.getBoundingClientRect().top + window.pageYOffset - 80;
        if (prefersReduced) {
          window.scrollTo(0, y);
        } else {
          window.scrollTo({ top: y, behavior: "smooth" });
        }
        history.replaceState(null, "", "#" + id);
      });
    });
  }

  // --- Live search suggestions on the search page ---
  function initSearchSuggest() {
    var form = document.querySelector(".search-form-lg");
    if (!form) return;
    var input = form.querySelector("input[name='q']");
    if (!input) return;

    var debounceTimer = null;
    input.addEventListener("input", function () {
      clearTimeout(debounceTimer);
      var q = input.value.trim();
      if (q.length < 2) return;
      debounceTimer = setTimeout(function () {
        fetch("/api/search?q=" + encodeURIComponent(q))
          .then(function (r) { return r.json(); })
          .then(function (data) {
            if (!data.results || !data.results.length) return;
            var hint = document.createElement("div");
            hint.className = "search-hint";
            hint.innerHTML = "<strong>Suggestions:</strong> " +
              data.results.slice(0, 5).map(function (r) {
                return '<a href="' + r.url + '">' + r.title + "</a>";
              }).join(" · ");
            var old = form.querySelector(".search-hint");
            if (old) old.remove();
            form.appendChild(hint);
          })
          .catch(function () { /* silent */ });
      }, 300);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initLazyImages();
    initToc();
    initSearchSuggest();
  });
})();
