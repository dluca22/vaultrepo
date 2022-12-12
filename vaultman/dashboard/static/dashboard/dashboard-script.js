document.addEventListener("DOMContentLoaded", () => {
    const url = new URL(document.URL);
  // triggers this script only on dashboard path

//   if path is instance of /dashboard/login OR /register, starts login_page/register function
  if (url.pathname == "/dashboard/login" || url.pathname == "/dashboard/register") {
      login_or_register();
    }
    else if (url.pathname == "/dashboard/") {
        userpage();
    }
});

// toggles between Log-in and Register forms
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


// manage userpage modals and functions
function userpage(){

    // PIN is encrypted in backend
    
    // if instance of button for update_pin (user has already set PIN and can only update it)
    if (document.querySelector("#update_pin")) {
        // when this update_pin button clicked, show pin update form modal
        document.querySelector("#update_pin").addEventListener('click', () =>{
            const pin_update_modal = document.querySelector('#pin_update_modal')
            pin_update_modal.style.display = "grid";

            pin_update_modal.addEventListener('click', close_reset_modal, false)
        })
      } //if user has NOT yet added pin, set pin button will be displayed
      else if(document.querySelector("#set_pin")) {
        document.querySelector("#set_pin").addEventListener('click', () =>{
            const pin_set_modal = document.querySelector('#pin_set_modal')
            pin_set_modal.style.display = "grid";

            pin_set_modal.addEventListener('click', close_reset_modal, false)
        })
      }

    //   modal form to update Master Password, checks account email, pin and current password to grant edit priviledge
      const change_masterPassword = document.querySelector('#update_password')
      change_masterPassword.addEventListener('click', () => {
      const modal = document.querySelector('#change_masterPassword_modal')
      modal.style.display = "grid";
      modal.addEventListener('click', close_reset_modal, false);
    });

    /* also worked without formal declaration, i guess it grabs the ID from the page to add the eventlistener */
    //   modal form to update email, asks MasterPassword to grant edit priviledge
    // LATER  add  OTP confirmation via email
        const change_email = document.querySelector('#change_email')
        change_email.addEventListener('click', () => {
        const modal = document.querySelector('#change_email_modal')
        modal.style.display = "grid";
        modal.addEventListener('click', close_reset_modal, false);
      });


 //   modal for deleting account, asks account info to confirm deleting account
 const delete_account = document.querySelector('#delete_account')
 delete_account.addEventListener('click', () => {
   const modal = document.querySelector('#delete_account_modal')
   modal.style.display = "grid";
   modal.addEventListener('click', close_reset_modal, false);
});

}


// ===================== HELPER FUNCTIONS ======================================

// if user clicks anywhere outside the modal, form gets resetted and modal is hidden
function close_reset_modal(e) {
  if (e.target == this) {
    const form = this.querySelector("form");
    this.style.display = "none";
    form.reset();
  }
}
