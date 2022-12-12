// ====== LISTENS ON DOM CONTENT LOADED AND BASED ON THE URL TRIGGERS DIFFERENT FUNCTIONS ===

document.addEventListener("DOMContentLoaded", function () {
  const url = new URL(document.URL);
  const darkmode = document.querySelector('#darkmode_toggle')
  darkmode.addEventListener("click", toggle_darkmode, false);

  //   on access if not autheticated, will be redirected to login page
  if (url.pathname == "/") {
    vault_page();
  } else if (url.pathname.includes("login/")) {
    login_content_page();
  }

  //   looks for password fields, append view button and listen for click to run toggle function
  const pw_fields = document.querySelectorAll('input[type="password"]');
  pw_fields.forEach((pwF) => {
    const toggle = document.createElement("img");
    toggle.src = "/static/icons/show.svg";
    toggle.alt = "password view toggle";
    toggle.classList.add("w-8", "h-8", "bg-blue-600", "rounded-full", "m-1");

    pwF.parentNode.append(toggle);
    toggle.addEventListener("click", toggle_visibility);
  });
});

// ============= JS TO HANDLE THE MAIN PAGE HTML & REQUESTS ===============================================
function vault_page() {
  // gets all login boxes and for each handles the click for entire box or username/ password elements for copy content
  const logins = document.querySelectorAll(".login_box");

  logins.forEach((login) => {
    // clicking on entire box, opens new page with login content
    login.addEventListener("click", view_login, false);
    // clicking on username, gets the text of the username field and copies to clipboard
    login.querySelector(".username-copy").addEventListener("click", (e) => {
      const username = e.currentTarget.firstElementChild.innerText;
      navigator.clipboard.writeText(username);
      flash_message("Username copied", "success");
      // avoid propagation for click listeners under it
      e.stopPropagation();
    });

    // if a there is a class selector for .copy-password (password might not be set)
    if (login.querySelector(".copy-passw") !== null) {
      //   if login has password set, clicking on the div.copy-passw starts function for get request for the password to be copied into clipboard
      login
        .querySelector(".copy-passw")
        .addEventListener("click", copy_password.bind(login));
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
    generate_username.addEventListener("click", random_username);
    generate_password.addEventListener(
      "click",
      random_password
    ); /*end event listener for password generator */

    // if user clicks anywhere outside the white box, closes the modal(inset) and reset form inside it
    login_modal.addEventListener("click", close_reset_modal, false);
  });

  //   const search_form = document.querySelector('#search_form')
  //   search_form.addEventListener('enter')

  //   event listener on "+ Folder"

  const new_folder = document.querySelector("#new_folder");
  const folder_modal = document.querySelector("#new_folder_modal");
  new_folder.addEventListener("click", () => {
    folder_modal.style.display = "grid";

    folder_modal.addEventListener("click", close_reset_modal);
  });

  const editFolder_modal = document.querySelector("#edit_folder_modal");
  const edit_btn = editFolder_modal.querySelector('input[value="Edit"]');
  const delete_btn = editFolder_modal.querySelector('input[value="Delete"]');
  const editForm = editFolder_modal.querySelector("form");
  const folderName_field = editFolder_modal.querySelector(
    "#current_folder_name"
  );

  // select <ul#folder> + select all children <li>
  if (document.querySelector("#folders")) {
    const folder_list = document.querySelector("#folders").querySelectorAll("li");

    // GET fetch request to pre fill the edit form with name of the folder
    // + checks if user is allowed or html has been hacked
    folder_list.forEach((folder_item) => {
      folder_item
        .querySelector(".edit-folder")
        .addEventListener("click", (e) => {
          const id = e.currentTarget.getAttribute("data-folder");

          fetch(`/edit_folder/${id}`)
            .then((response) => response.json())
            .then((data) => {
              if (data.success) {
                // if request successful shows div and fills form content with response data
                editFolder_modal.style.display = "grid";
                folderName_field.value = data.name;
                editForm.value = data.id;
              } else if (data.denied) {
                // if request was denied, shows error message containing response message
                flash_message(data.message, "error");
              }
            });
        });
    });

    // click outside modal triggers close
    editFolder_modal.addEventListener("click", close_modal);

    edit_btn.addEventListener("click", (e) => {
      // fetch request to PUT EDIT
      //not preventdefault so it refreshes

      fetch(`/edit_folder/${editForm.value}`, {
        method: "PUT",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-type": "application/json",
        },
        body: JSON.stringify(folderName_field.value),
      })
        .then((response) => response.json())
        .then((data) => {
          // if successful edit, flashes success message
          if (data.success) {
            flash_message(data.success, "success");
          } else {
            console.log(data);
          }
        });
    });

    delete_btn.addEventListener("click", (e) => {
      // fetch request to DELETE
      //not preventdefault so it refreshes

      fetch(`/edit_folder/${editForm.value}`, {
        method: "DELETE",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          // if successful delete, flashes success message
          if (data.success) {
            flash_message(data.message, "success");
          } else {
            console.log(data);
          }
        });
    });
  }
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


  const id = this.getAttribute("id");

  // from HTML data-protection attribute
  const status = this.dataset.protection;

  if (status == "unlocked") {
    var pin = false;
    fetch_password(id, pin);
  }
  // STOP TEMPOARANEO  ===================================================================================
  else if (status == "locked") {
    const pin_modal = document.querySelector("#pin_modal");
    const pin_form = pin_modal.querySelector("form");
    const pin_input = pin_form.querySelector("#pin_input");

    pin_modal.style.display = "grid";
    pin_modal.addEventListener("click", close_reset_modal, false);
    pin_form.addEventListener("submit", (e) => {
      e.preventDefault();
      var pin = pin_input.value;
      pin_form.reset();
      console.log(pin);
      pin_modal.style.display = "none";
      fetch_password(id, pin);
    }, { once: true });
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
    body: JSON.stringify(pin),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // if request successful, adds content to clipboard
        navigator.clipboard.writeText(data.content);
        flash_message("Passw copied", "success");
      } else if (data.denied) {
        flash_message(data.message, "error");
      }
    })
    .catch(function () {
      // catches errors in fetch promise request (only on fail of execution like unavailable service)
      // TODO flash message on page
      flash_message("500 - Error on password request.");
    });
}

// ============= JS TO HANDLE TO USERPAGE HTML & REQUESTS ===========================================================
function login_content_page() {
  const delete_item = document.querySelector("#delete_item");
  const generate_username = document.querySelector("#generate_username");
  const generate_password = document.querySelector("#generate_password");

  // fetch request to external api that generates random person, then getting the login.username field from the request
  generate_username.addEventListener("click", random_username);

  // fetch request to function to generate password from util function
  generate_password.addEventListener(
    "click",
    random_password
  ); /*end event listener for password generator */

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
  }

  delete_item.addEventListener("click", (e) => {
    const id = e.currentTarget.value;
    const confirm_modal = document.querySelector("#delete_item_confirm");
    const dismiss = confirm_modal.querySelector('button[value="dismiss"]');
    const confirm = confirm_modal.querySelector('button[value="confirm"]');

    confirm_modal.style.display = "grid";
    confirm_modal.addEventListener("click", (e) => {
      if (e.target == e.currentTarget || e.target == dismiss) {
        e.currentTarget.style.display = "none";
      } else if (e.target == confirm) {
        fetch(`/delete/${id}`, {
          method: "delete",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-type": "application/json",
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              console.log(data.success);
              window.location = "/";
            } else if (data.denied) {
              console.log(data.message);
            }
          });
      }
    });
    dismiss.addEventListener("click", () => confirm_modal.click());
  });

  //   if login has password history list
  if (document.querySelector("#password_history")) {
    document.querySelectorAll("li").forEach((old_passw) => {
      old_passw.addEventListener("click", () => {
        navigator.clipboard.writeText(old_passw.textContent);
      });
    });
  }

// appends arrow to uri field, arrow.onclick opens URI in the uri_field
  const uri_field = document.querySelector('input[name="uri"]')
  const toggle = document.createElement('span')
// LATER   arrow as HTML code change to icon
  toggle.innerHTML = "&#10551;"
//   tailwind classes
  toggle.classList.add('text-3xl', "font-bold", "text-white", "bg-red-500", "rounded-full", "px-2")
  uri_field.parentElement.append(toggle)
  toggle.addEventListener('click', () =>{
    // check if starts with https else appends to it and open in another blank window
    const page = uri_field.value.includes('https://') ? uri_field.value : "https://" + uri_field.value
    window.open(page, "_blank");

  })

}

// =========== HELPER FUNCTIONS ================================

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
  flash_message("Username created", "success");
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
      if (data.success) {
        flash_message(data.message, "success");
        const password_input = document.querySelector("#id_password");
        password_input.value = data.password;
      } else {
        flash_message(data.message, "error");
      }
    });
}

// ===================================================================================
// toggle password field visibility

function toggle_visibility(e) {
  const pw_input = this.parentNode.querySelector("input");
  if (pw_input.getAttribute("type") == "password") {
    pw_input.setAttribute("type", "text");
    this.src = "/static/icons/hide.svg";
  } else {
    pw_input.setAttribute("type", "password");
    this.src = "/static/icons/show.svg";
  }
}

// ===================================================================================
// flash custom message in the message-box
function flash_message(message, alert) {
  const msgDiv = document.querySelector("#message-box");
  // msgDiv.classList.remove("hidden");

  const popup = create_popup(alert);
  popup.innerText = message;
  msgDiv.append(popup);

  // setTimeout(function() {
  // msgDiv.firstChild.remove()
  // }, 5000);
}
// ===================================================================================
// hide message box
// function timeout_message(){
//     const msgDiv = document.querySelector('#message-box')
//     if( ! msgDiv.classList.contains('hidden')){
//         setTimeout(function(){
//             msgDiv.classList.add("hidden");
//         }, 5000)
//     }

// }

// ===================================================================================

function create_popup(alert) {
  const popup = document.createElement("div");
  popup.classList.add(
    "flex",
    "flex-wrap",
    "items-center",
    "justify-center",
    "p-4",
    "m-2",
    "border-2",
    "border-b-4",
    "border-r-4",
    "rounded-lg"
  );
  console.log(alert);
  if (alert === "success") {
    popup.classList.add("green-popup");
  } else if (alert === "error") {
    popup.classList.add("red-popup");
  }
  setTimeout(function () {
    popup.remove();
  }, 5000);

  return popup;
}
// ===================================================================================

function toggle_darkmode(){
    const body = document.querySelector('body')
    body.classList.contains("dark") ? body.classList.remove('dark') : body.classList.add('dark')
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
