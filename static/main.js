
document.addEventListener("DOMContentLoaded", () => {
  const fileRadio = document.querySelector('input[value="file"]');
  const textRadio = document.querySelector('input[value="text"]');
  const fileBox = document.getElementById('file-input-box');
  const textArea = document.getElementById('text-input');
  const reviewForm = document.getElementById('reviewForm');
  const loadingOverlay = document.getElementById('loadingOverlay');
  const refreshBtn = document.getElementById("refreshBtn");
  const suggestionBox = document.getElementById("suggestionBox");
  const fixedCodeBox = document.getElementById("fixedCodeBox");

  function toggleInputs() {
    if (fileRadio.checked) {
      fileBox.style.display = "block";
      textArea.style.display = "none";
    } else {
      fileBox.style.display = "none";
      textArea.style.display = "block";
    }
  }

  fileRadio.addEventListener("change", toggleInputs);
  textRadio.addEventListener("change", toggleInputs);
  toggleInputs();

  // Show loading overlay if form is valid
  if (reviewForm && loadingOverlay) {
    reviewForm.addEventListener("submit", (e) => {
      const inputMethod = reviewForm.querySelector('input[name="inputMethod"]:checked')?.value;
      let valid = false;

      if (inputMethod === "text") {
        const code = textArea.value.trim();
        valid = !!code;
      } else if (inputMethod === "file") {
        const file = reviewForm.querySelector('input[name="codeFile"]').files[0];
        valid = !!file;
      }

      if (valid) {
        loadingOverlay.classList.remove("hidden");
      } else {
        e.preventDefault();
      }
    });
  }

  // Refresh logic
  if (refreshBtn) {
    refreshBtn.addEventListener("click", async () => {
      
      if (textArea) textArea.value = "";
      if (suggestionBox) suggestionBox.remove();
      if (fixedCodeBox) fixedCodeBox.remove();

      
      await fetch('/clear', { method: 'POST' });
    });
  }
});
