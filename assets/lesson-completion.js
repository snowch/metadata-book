/* Manual reading marks, stored separately for each lesson in this book. */
(() => {
  "use strict";
  const prefix = "metadata-book:v1:manual-completion:";
  const links = [...document.querySelectorAll("[data-lesson-link]")];
  const checkbox = document.querySelector("[data-lesson-id]");
  const status = document.querySelector("#lesson-save-status");
  const ids = new Set(links.map(link => link.dataset.lessonLink));
  if (checkbox) ids.add(checkbox.dataset.lessonId);
  // Preserve the explicit choice on this page if storage is unavailable.
  const unsaved = new Map();
  const read = id => {
    if (unsaved.has(id)) return unsaved.get(id);
    try { return localStorage.getItem(prefix + id) === "true"; }
    catch { return false; }
  };
  function render() {
    for (const link of links) {
      const completed = read(link.dataset.lessonLink);
      link.classList.toggle("is-complete", completed);
      link.querySelector(".lesson-done").hidden = !completed;
    }
    if (checkbox) {
      checkbox.checked = read(checkbox.dataset.lessonId);
      status.textContent = unsaved.has(checkbox.dataset.lessonId)
        ? "Progress could not be saved in this browser."
        : "Saved in this browser.";
    }
  }
  if (checkbox) {
    checkbox.closest(".lesson-completion").hidden = false;
    checkbox.addEventListener("change", () => {
      const id = checkbox.dataset.lessonId;
      try {
        localStorage.setItem(prefix + id, String(checkbox.checked));
        unsaved.delete(id);
      } catch { unsaved.set(id, checkbox.checked); }
      render();
    });
  }
  window.addEventListener("pageshow", render);
  window.addEventListener("storage", event => {
    try { if (event.storageArea !== localStorage) return; }
    catch { return; }
    if (event.key === null) unsaved.clear();
    else if (event.key.startsWith(prefix) && ids.has(event.key.slice(prefix.length))) {
      unsaved.delete(event.key.slice(prefix.length));
    } else return;
    // Read the latest value, since storage events can arrive after another edit.
    render();
  });
  render();
})();
