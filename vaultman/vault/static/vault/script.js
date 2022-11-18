document.addEventListener('DOMContentLoaded', function() {
    const url = new URL(document.URL);
  const base_path = url.pathname.split("/")[1];

  //   on access if not autheticated, will be redirected to login page
  if (base_path == "") {
    vault_page();
  }/* else if (base_path == "new_element") {
    new_element_page();
  }*/

})

function vault_page(){
    const logins = document.querySelectorAll('.login_box')
    logins.forEach((login) => {
        login.addEventListener('click', view_login, false)
        login.querySelector('.username-copy').addEventListener('click', (e)=>{
            const username = e.currentTarget.firstElementChild.innerText
            console.log(username);
            navigator.clipboard.writeText(username);

            e.stopPropagation();
        })
        if(login.querySelector(".copy-passw") !== null){
            login.querySelector(".copy-passw").addEventListener("click", copy_password.bind(login));
        }

    })
}

function view_login(event){
    id = event.currentTarget.getAttribute('id')

    const url = `login/${id}`
    window.open(url, "_self")
}

function copy_password(e){
    e.stopPropagation()
    console.log(e.currentTarget);
    const id = this.getAttribute('id')
    const status = e.currentTarget.value

    if (status == "clear"){
        pin = false
    }else if (status == "protected"){
        pin = "1111"
    }
    fetch(`password/${id}`, {
        method : "POST",
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
                "Content-type": "application/json",
        },
        mode : "same-origin",
        body : JSON.stringify(pin),
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
    }).catch(function(){
        // catches errors in fetch promise request (only on fail of execution like unavailable service)
        // TODO flash message on page
        console.log("error on password fetch request")
    });

}


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