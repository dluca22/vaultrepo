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
      } //if user has NOT yet added pin, set pin button will be displayed
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

      const delete_account = document.querySelector('#delete_account')
      delete_account.addEventListener('click', () => {
        const modal = document.querySelector('#delete_account_modal')
        modal.style.display = "grid";
        modal.addEventListener('click', close_reset_modal, false);
    });

    /* also worked without formal declaration, i guess it grabs the ID from the page to add the eventlistener */
        const change_email = document.querySelector('#change_email')
        change_email.addEventListener('click', () => {
        const modal = document.querySelector('#change_email_modal')
        modal.style.display = "grid";
        modal.addEventListener('click', close_reset_modal, false);
      });


        const change_masterPassword = document.querySelector('#update_password')
        change_masterPassword.addEventListener('click', () => {
        const modal = document.querySelector('#change_masterPassword_modal')
        modal.style.display = "grid";
        modal.addEventListener('click', close_reset_modal, false);
      });


}


// ===================== HELPER FUNCTIONS ======================================

function close_reset_modal(e) {
    // before was close_modal.bind(modal)   should work the same
  // e.target is where the click event was originated
  // this is the overlay modal itself
  // if click is on the overlay modal (e.g. NOT in the actual form box), it will be dismissed and reset the form
  if (e.target == this) {
    const form = this.querySelector("form");
    this.style.display = "none";
    form.reset();
  }
}
