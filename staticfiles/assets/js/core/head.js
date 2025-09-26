document.addEventListener("DOMContentLoaded", function () {
  const loginModalEl = document.getElementById("openloginModal");
  const registerModalEl = document.getElementById("openregisterModal");

  function openRegister() {
    const loginModal = bootstrap.Modal.getInstance(loginModalEl);
    if (loginModal) loginModal.hide();

    loginModalEl.addEventListener("hidden.bs.modal", function () {
      bootstrap.Modal.getOrCreateInstance(registerModalEl).show();
      cleanupBackdrops();
    }, { once: true });
  }

  function openLogin() {
    const registerModal = bootstrap.Modal.getInstance(registerModalEl);
    if (registerModal) registerModal.hide();

    registerModalEl.addEventListener("hidden.bs.modal", function () {
      bootstrap.Modal.getOrCreateInstance(loginModalEl).show();
      cleanupBackdrops();
    }, { once: true });
  }

  // Cleanup function: removes duplicate backdrops
  function cleanupBackdrops() {
    const backdrops = document.querySelectorAll(".modal-backdrop");
    if (backdrops.length > 1) {
      backdrops.forEach((b, i) => { if (i < backdrops.length - 1) b.remove(); });
    }
  }

  // Register link inside login modal
  const switchToRegister = document.getElementById("switchToRegister");
  if (switchToRegister) {
    switchToRegister.addEventListener("click", function (e) {
      e.preventDefault();
      openRegister();
    });
  }

  // Login link inside register modal
  const switchToLogin = document.getElementById("switchToLogin");
  if (switchToLogin) {
    switchToLogin.addEventListener("click", function (e) {
      e.preventDefault();
      openLogin();
    });
  }

  // Also cleanup when any modal hides
  [loginModalEl, registerModalEl].forEach(modal => {
    modal.addEventListener("hidden.bs.modal", cleanupBackdrops);
  });
});

