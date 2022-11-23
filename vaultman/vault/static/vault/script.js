document.addEventListener("DOMContentLoaded", function () {
  const url = new URL(document.URL);
  const base_path = url.pathname.split("/")[1];

  //   on access if not autheticated, will be redirected to login page
  if (url.pathname == "/") {
    console.log("FUNZIONA ANCORA");
    vault_page();
  } else if (url.pathname.includes('login/')){
    login_content_page()
  }


  /* else if (base_path == "new_element") {
    new_element_page();
  }*/
});

function vault_page() {
  const logins = document.querySelectorAll(".login_box");
  logins.forEach((login) => {
    login.addEventListener("click", view_login, false);
    login.querySelector(".username-copy").addEventListener("click", (e) => {
      const username = e.currentTarget.firstElementChild.innerText;
      console.log(username);
      navigator.clipboard.writeText(username);

      e.stopPropagation();
    });
    // if a there is a class selector for .copy-password
    if (login.querySelector(".copy-passw") !== null) {
      login
        .querySelector(".copy-passw")
        .addEventListener("click", copy_password.bind(login));
    }
  });
  // inserire qui i modal toggles
}

function view_login(event) {
  id = event.currentTarget.getAttribute("id");

  const url = `login/${id}`;
  window.open(url, "_self");
}

function copy_password(e) {
  e.stopPropagation();
  const id = this.getAttribute("id");
  const status = e.currentTarget.value;

  if (status == "clear") {
    var pin = false;
    fetch_password(id, pin);
  }
  // STOP TEMPOARANEO  ===================================================================================
  else if (status == "protected") {
    // TEMP paused, set all to NO PROTECT, adding function later (callback hell, one )
    // le variables sono in modals.html
    pin_modal.style.display = "grid";
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
    body: JSON.stringify(pin),
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
function login_content_page(){
    const delete_item = document.querySelector('#delete_item')
    const generate_username = document.querySelector('#generate_username')
    const generate_password = document.querySelector('#generate_password')
    const see_password_toggle = document.querySelector('#see_password_toggle')


    see_password_toggle.addEventListener('click', () =>{
        const passw_field = document.querySelector('#id_password');
        passw_field.getAttribute('type') == "password" ? passw_field.setAttribute('type', "text") : passw_field.setAttribute('type', "password");
    })

    generate_username.addEventListener('click', () =>{
        const username_field = document.querySelector('#id_username')
    fetch('https://randomuser.me/api/?inc=login')
    .then((response)=>response.json())
    .then((data)=> username_field.value = data.results[0].login.username)
    })
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