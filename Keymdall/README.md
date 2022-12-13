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

## Distinctiveness and Complexity

## Folders and files