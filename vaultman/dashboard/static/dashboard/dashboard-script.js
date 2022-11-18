document.addEventListener("DOMContentLoaded", () => {
    const url = new URL(document.URL);
  // triggers this script only on dashboard path

//   if path is instance of /dashboard/login OR /register, starts login_page/register function
  if (url.pathname == "/dashboard/login" || url.pathname == "/dashboard/register") {
    login_or_register();
  }
});

function login_or_register(){
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
};
