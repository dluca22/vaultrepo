# Capstone
This is my submission for the final project for the cs50-web course.

I've built a web application for storing login credentials for websites.
I took inspiration from BitWarden, a service I daily use and really love, being one of the services that most helped me and improved my daily life, so much so that it actually motivated me to start a career in coding and web development.
I took the chance to re create it in order gain better knowledge learn about security and user experience, working on it with a professional approach like it was meant to be ready for production.

## Description

This web-app is built using Django in the backend and plain JavaScript in the frontend, styling is managed using Tailwind.
The Django project has 3 apps:
* `dashboard`manages users registration and login/logout using django built-in authenticator and account settings
* `theme` is the django-tailwind app that manages the base template, CSS classes and darkmode,
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
While other projects were built as a platform to enable interactions between user on the website, my submission is instead meant to be a private service for a user to have a personal encrypted database to store sensitive informations and credentials.
First of all the backend ensures an user can only view, save, interact and update only his own submission, any attempt to tamper with requests will result in an error response.
Trying to decrypt other user's fields in the database will also fail since decryption also requires the requesting user to be the same as the original owner.
The project is based around 4 Models, *User, Login, Folder and History* and 2 ModelForms, for the *Login Form* and for the *Folder Form*.

## Models
* **Login** : defines the structure of a Login instance, the only required field is the title (in order to accomodate different types of credentials to be stored, or to add them later if needed), an user can save the username, password, notes and URI related to a specific website he is registered to.
Logins have a foreign key relation with the Folder so that an user can organize them to his preferences.
The model also lets the user flag it as a *Favorite* login (so it can be filtered with a query in the index page), and set the Login as *Protected* that adds a second layer of protection for it, requiring the submission of a PIN to unlock the content of it.
Upon submitting the Login form, the backend saves the request.user as *owner* so that he would be the only one allowed to interact and view any of the content of it.

* **Folder** is a table with a many to one relationship with Login table, so that user can categorize Logins by his preference.
This table also has a row named `color` that allows to choose from a set of 10 colors from Tailwind in order to give each folder and login contained in it a color accent as a visual aid for the user.

* **History** is a table that stores updated Login passwords. Whenever an user edits a Login item's password, if the old one is not empty and is different from the newer one, the old password will be stored in the History table with the Login reference, so that if a user edited the password, he'd still be able to browse to the older password if needed.
Passwords in this table are also encrypted and only accessible by the owner.

## Features
I've focused my work around making this webapp as user friendly as I could, the user in the Index page can see all the items he stored in the database, and can filter them by the folder they belong in, the ones set as favorites and can also search them via the searchbar.
Every item in the index page is previewed in a small box that has the title, username and a key icon for the password;
Clicking on the username or the Key icon will copy to the user's clipboard the intended content, while clicking generally on the box will open the item's page.
Every login box, if set will have an accent color for the folder they belong in and a star if the Login is set as *Favorite*.

While displaying a Login form, the user has the option to generate a random username and password using the related toggles, `generate username` will retrieve a random username from an external API from [https://randomuser.me/](https://randomuser.me/), while `generate password` will generate a random password using the function defined in `vault/utils.py`.

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

    ## Conclusion

    I'm using this project as a canvas to train my skills and reflect more on how features should be designed to be maintainable, scalable and secure.
    I intend to continue building upon it as I go along my learning path, adding features and testing scalability and security.

    I have learned a lot of things while working on it, as a frontend I used JavaScript in order to imporove my skills and knowledge of it, but I plan on switching to another framework better suited to create interactive UI in order to improve the user experience and have more complex features.
