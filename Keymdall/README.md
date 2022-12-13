# Capstone
This is my submission for the final project for the cs50-web course.

I've built a web application for storing login credentials for websites.
I took inspiration from BitWarden, a service I use daily and really love, and since it is one of the services that most helped and change my daily life, it became something I got really passionate about and took the chance to re create it in order to better learn about security and user experience.

## Description

This web-app is built using Django in the backend and plain JavaScript in the frontend, styling is managed using Tailwind.
The Django project has 3 apps:
* `dashboard`manages users registration and login/logout using django built-in authenticator and account settings
* `theme` is the django-tailwind app that manages the base template, css classes and darkmode,
* `vault` is the main app that has the models for storing, encrypting and managing saved *Login* informations, folders and history for password changes.

An unautheticated/unregistered user will be redirected to the login/register page;
Upon registration the site will route the user to the index page, where the user's vault content will be displayed.
Each *Login* item an user saved will be displayed in a box preview in the index page where with the title and username an user stored for it, you can click on the username or the key icon in order to copy to clipboard the content instance of it that was saved, while clicking on the box itself will route to the page displaying the Item's content.

Also in the index page an user can create a new Login element or a Folder that can be used to organize the content of the vault by preference.
Folders have the options for a color accent to be visually more appealing, also Logins that belong in a folder will also have a color accent that matches their Folder.

Clicking on the user name in the navbar will open the userpage dashboard, which contains some useful info about the user, like the total number of Login stored, and the last login timestamp.
In the Dashboard a new user can set a 4 digit PIN, that behaves as an added layer of protection to the stored Logins asking for the PIN before being able to interact with them.

User credentials are encrypted using django built in AbstractUser model methods, while sensitive Login fields and user PIN are encrypted in the backend using the `cryptography.fernet` library.


## Distinctiveness and Complexity
This project fundamentally differs from previous psets in this course.
While other projects were built as a platform to enable interactions between user on the app, my submission is instead meant to be a private service for a user to have a personal encrypted database to store sensitive informations and credentials.
First of all the backend ensures an user can only view, save, interact and update only his own submission, any attempt to tamper with requests will result in an error response.
Trying to decrypt other user's fields in the database will also fail since decryption also requires the requesting user to be the same as the original owner.
The project is based around 4 Models, *User, Login, Folder and History* and 2 ModelForms, for the *Login Form* and for the *Folder Form*.

## Folders and files
* **dashboard/**
    * `static/dashboard-script.js` = JavaScript to handle forms and UI in the login/register page and also the userpage where it handles the modals for setting or updating PIN, Master Password, Email or deleting account.
    * `templates/dashboard_modals.html` HTML templates for modals/overlays belonging to userpage
    * `templates/login.html` contains the login and register forms
    * `templates/userpage.html` contains the body of the userpage to display count of saved Logins, user Folders and additional information and Account settings
    * `models.py` contains the User Model inherited from AbstractUser with the addition for PIN field and model related properties
    * `urls.py` handles urls in the dashboard app
    * `views.py` manages the dashboard app, with the logic for registration, login/logout updating Account info or deleting entire Account

* **theme/**
    * `static/` contains static files for custom icons, images and script to handle darktheme and save theme setting in localStorage
    * `static_src/` contains Tailwind settings and configurations
    * `templates/base.html` base html file containing the navbar and popup messages. It gets extended via template inheritance by the other apps
    * `templates/footer.html` Footer containing attribution links for content I used and my personal contact info

* **vault/**
    * `static/script.js` script that handles the Vault app frontend, manages the display for every modal in the index page (for new item, create folder, edit folder) as well as functions to copy username (via external API call) to clipboard and async requests to request Login passwords to the backend after authentication check.
    * `templates/` contains templates and components included in the index page in `index.html` and the template for every Login content page
    * `encrypt_util.py` is a module that handles encryption and decryption of fields using the `cryptography-fernet` library, it enables encryption and decryption across all apps and models.
    * `forms.py` contains Django ModelForms for the *Folder Form* and *Login Form* and their widgets
    * `models.py` defines the models for Login items and its many-to-one relationship with the Folder table and the many-to-many link to the History table
    * `urls.py` routes the traffic between function of the vault app
    * `utils.py` is a custom utility with:
        * a function to generates random password on user request between all alphanumeric + symbol characters and also takes an optional length argument
        * a function to automate the format for Login urls, so that an user doesn't have to manually add "https://"
    * `views.py` manages the vault app logic, defines the content of the index page handling query filters, handles the insertion/ deletion and edit of new Logins and Folders to the database, manages async requests from Js to get password or create random passwords and ensures security, checking for the request.user to be the owner of the content he is trying to access.