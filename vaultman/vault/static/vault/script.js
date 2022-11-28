document.addEventListener("DOMContentLoaded", function () {
  const url = new URL(document.URL);

  //   on access if not autheticated, will be redirected to login page
  if (url.pathname == "/") {
    vault_page();
  } else if (url.pathname.includes("login/")) {
    login_content_page();
  }

  /* else if (base_path == "new_element") {
    new_element_page();
  }*/
});

function vault_page() {
    // gets all login boxes and for each handles the click for entire box or username/ password elements for copy content
  const logins = document.querySelectorAll(".login_box");

  logins.forEach((login) => {
    // clicking on entire box, opens new page with login content
    login.addEventListener("click", view_login, false);
    // clicking on username, gets the text of the username field and copies to clipboard
    login.querySelector(".username-copy").addEventListener("click", (e) => {
      const username = e.currentTarget.firstElementChild.innerText;
      console.log(username);
      navigator.clipboard.writeText(username);
        // avoid propagation for click listeners under it
      e.stopPropagation();
    });

    // if a there is a class selector for .copy-password (password might not be set)
    if (login.querySelector(".copy-passw") !== null) {
    //   if login has password set, clicking on the div.copy-passw starts function for get request for the password to be copied into clipboard
        login.querySelector(".copy-passw").addEventListener("click", copy_password.bind(login));
    }
  });

  // index page modal management

  //   event listener on "New Login" button
    // new_login is the button the user clicks to display the modal
    const new_login = document.querySelector("#show_login_form");
    // login modal is the modal itself to be displayed and handled
    const login_modal = document.querySelector("#new_login_modal");
    new_login.addEventListener("click", () => {
    // get new_login_modal  and show as grid
    login_modal.style.display = "grid";

    // get 3 function buttons for form fields
    const generate_username = document.querySelector("#generate_username");
    const generate_password = document.querySelector("#generate_password");
    const pw_visibility_toggle = document.querySelector("#see_password_toggle");
    pw_visibility_toggle.addEventListener("click", toggle_visibility);
    generate_username.addEventListener("click", random_username);
    generate_password.addEventListener("click", random_password); /*end event listener for password generator */

    // if user clicks anywhere outside the white box, closes the modal(inset) and reset form inside it
    login_modal.addEventListener("click", close_reset_modal, false);
  });

//   const search_form = document.querySelector('#search_form')
//   search_form.addEventListener('enter')

//   event listener on "+ Folder"

  const new_folder = document.querySelector('#new_folder');
  const folder_modal = document.querySelector('#new_folder_modal');
  new_folder.addEventListener('click', () =>{
    folder_modal.style.display = "grid";
    folder_modal.querySelector('#id_name').autofocus; /* NOTE DOESN'T WORK */

    folder_modal.addEventListener('click', close_reset_modal)
  })
}

function view_login(event) {
  id = event.currentTarget.getAttribute("id");
  //   TODO add PIN unlock

  const url = `login/${id}`;
  window.open(url, "_self");
}

// declaration for elements of the pin modal form

function copy_password(e) {
  e.stopPropagation();

  const pin_modal = document.querySelector("#pin_modal");
  const pin_form = pin_modal.querySelector("form");
  const pin_input = pin_form.querySelector("#pin_input");
  const id = this.getAttribute("id");

  // from HTML data-protection attribute
  const status = this.dataset.protection;

  if (status == "unlocked") {
    var pin = false;
    fetch_password(id, pin);
  }
  // STOP TEMPOARANEO  ===================================================================================
  else if (status == "locked") {
    // TEMP paused, set all to NO PROTECT, adding function later (callback hell, one )
    // le variables sono in modals.html
    pin_modal.style.display = "grid";
    pin_modal.addEventListener("click", close_reset_modal, false);
    pin_form.addEventListener("submit", (e) => {
      e.preventDefault();
      var pin = pin_input.value;
      pin_form.reset();
      console.log(pin);
      pin_modal.style.display = "none";
      fetch_password(id, pin);
    });
  }
  // STOP TEMPOARANEO  ===================================================================================
}

function fetch_password(id, pin) {
  fetch(`password/${id}`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "Content-type": "application/json",
    },
    mode: "same-origin",
    body: {'name': JSON.stringify(pin)},
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // LATER add flashy message if success, or error message if not
        // if request successful, adds content to clipboard
        navigator.clipboard.writeText(data.content);
        console.log("PW copied");
      } else if (data.denied) {
        alert(data.message);
      }
    })
    .catch(function () {
      // catches errors in fetch promise request (only on fail of execution like unavailable service)
      // TODO flash message on page
      console.log("error on password fetch request");
    });
}

// ===================================================================================
function login_content_page() {
  const delete_item = document.querySelector("#delete_item");
  const generate_username = document.querySelector("#generate_username");
  const generate_password = document.querySelector("#generate_password");
  const pw_visibility_toggle = document.querySelector("#see_password_toggle");

  // click on view/hide password field that converts input type from "password" to "text"
  pw_visibility_toggle.addEventListener("click", toggle_visibility);

  // fetch request to external api that generates random person, then getting the login.username field from the request
  generate_username.addEventListener("click", random_username);

  // fetch request to function to generate password from util function
  generate_password.addEventListener("click", random_password); /*end event listener for password generator */

  // if div for password_history is present
  if (document.querySelector("#password_history")) {
    const history = document.querySelector("#password_history");
    // get all its list child element
    const previous_passwords = history.querySelectorAll("li");
    // for each add listener to copy innertext to clipboard
    previous_passwords.forEach((item) => {
        item.addEventListener("click", (e) => {
        const value = e.target.innerText;
        navigator.clipboard.writeText(value);
        // TODO add popup for confirmation
      });
    });
  };

  delete_item.addEventListener('click', (e) => {
    const id = e.currentTarget.value;
    const confirm_modal = document.querySelector('#delete_item_confirm')
    const dismiss = confirm_modal.querySelector('button[value="dismiss"]')
    const confirm = confirm_modal.querySelector('button[value="confirm"]')

    confirm_modal.style.display = "grid";
    confirm_modal.addEventListener('click', (e) =>{
        if (e.target == e.currentTarget || e.target == dismiss){
            e.currentTarget.style.display = "none"
        }else if (e.target == confirm){
            fetch(`/delete/${id}`,{
                method : "delete",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-type": "application/json",
                  },
            })
            .then((response) => response.json())
            .then((data) => {
                if (data.success){
                    console.log(data.success);
                    window.location = '/';


                }
                else if (data.denied){
                    console.log(data.message);
                }
            })
        }

    })
    dismiss.addEventListener('click', () => confirm_modal.click())

  })
}
// ===================================================================================

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

// ===================================================================================

function close_modal(e) {
    if (e.target == this) {
      this.style.display = "none";
    }
  }

// ===================================================================================
function random_username() {
    const username_field = document.querySelector("#id_username");
    fetch("https://randomuser.me/api/?inc=login")
      .then((response) => response.json())
      .then((data) => (username_field.value = data.results[0].login.username));
  }
// ===================================================================================
function random_password() {
    // get the input value for the size
    const sizeInput = document.querySelector("#size").value;
    // if no size was set, default to 10 char
    const size = sizeInput ? sizeInput : 10;

    // NOTE add / to go to the absolute path of the app (else would be /login/generate_password)
    // goes to 8000/generate_password/<size>
    fetch(`/generate_password/${size}`)
      .then((response) => response.json())
      .then((data) => {
        const password_input = document.querySelector("#id_password");
        password_input.value = data.password;
      });
  }
// ===================================================================================
function toggle_visibility() {
    const passw_field = document.querySelector("#id_password");
    // ternary operator to change the attribute
    passw_field.getAttribute("type") == "password"
      ? passw_field.setAttribute("type", "text")
      : passw_field.setAttribute("type", "password");
  }


// ===================================================================================

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// fetch request per username generator

/*
fetch('https://randomuser.me/api/?inc=login').then((response)=>response.json()).then((data)=> console.log(data.results[0].login.username))

*/
