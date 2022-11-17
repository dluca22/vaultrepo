document.addEventListener("DOMContentLoaded", () => {
  const login_form = document.querySelector("#login_form");
  const login_toggle = document.querySelector("#toggle_login");

  const register_form = document.querySelector("#register_form");
  const register_toggle = document.querySelector("#toggle_register");

  login_toggle.addEventListener("click", () => {
    register_form.classList.add("hidden");
    login_form.classList.remove("hidden");
  });
  register_toggle.addEventListener("click", () => {
    login_form.classList.add("hidden");
    register_form.classList.remove("hidden");
  });
});
