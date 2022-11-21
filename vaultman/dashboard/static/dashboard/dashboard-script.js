document.addEventListener("DOMContentLoaded", () => {
    const url = new URL(document.URL);
  // triggers this script only on dashboard path

//   if path is instance of /dashboard/login OR /register, starts login_page/register function
  if (url.pathname == "/dashboard/login" || url.pathname == "/dashboard/register") {
      login_or_register();
    }
    else if (url.pathname == "/dashboard/") {
        // manage userpage modals and functions
        userpage();
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

function userpage(){

    // if instance of button for update_pin (user has already set PIN and can only update it)
    if (document.querySelector("#update_pin")) {
        // when this update_pin button clicked, show pin update form modal
        document.querySelector("#update_pin").addEventListener('click', () =>{
            const pin_update_modal = document.querySelector('#pin_update_modal')
            const form = pin_update_modal.querySelector('form')
            pin_update_modal.style.display = "grid";

            // if user clicks anywhere outside the modal, form gets resetted and modal is hidden
            pin_update_modal.addEventListener('click', (e)=> {
                if(e.target == pin_update_modal){
                    pin_update_modal.style.display = "none";
                    form.reset()
                }
            }, false)
        })
      }
      else if(document.querySelector("#set_pin")) {
        document.querySelector("#set_pin").addEventListener('click', () =>{
            const pin_set_modal = document.querySelector('#pin_set_modal')
            const form = pin_set_modal.querySelector('form')
            pin_set_modal.style.display = "grid";

            // if user clicks anywhere outside the modal, form gets resetted and modal is hidden
            pin_set_modal.addEventListener('click', (e)=> {
                if(e.target == pin_set_modal){
                    pin_set_modal.style.display = "none";
                    form.reset()
                }
            }, false)
        })
      }
}
