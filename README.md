# Mybeans: a coffee web app for coffee fanatics
#### Video Demo:
![ezgif com-optimize](https://github.com/pitiao145/CS50-Final-Project-2023/assets/133644618/8b3d5c44-bb91-4676-90fe-f4de9e23f19f)

<img width="40%" alt="Screenshot 2023-07-30 at 20 37 55" src="https://github.com/pitiao145/CS50-Final-Project-2023/assets/133644618/55ce8fc9-cd1b-4a7d-9285-805a010051b9">
<img width="40%" alt="Screenshot 2023-07-30 at 20 38 17" src="https://github.com/pitiao145/CS50-Final-Project-2023/assets/133644618/4941ab35-6576-4f7a-bfec-3318bdd9242f">

#### Description:
This application was designed by a coffee lover, for coffee lovers. With this web app, you can register all the beans you ever bought, keep track of your current stock of beans, leave reviews and write comments for the different types of beans you currently own, or have owned in the past. The app also allows you to track you coffee use, in amount of cups and mass of coffee beans used over time. It also displays your favorite type of beans, favorite origins and favorite brewing methods, according to your usage and brewing methods.
There is also a section that informs you about the different brewing methods. This section will be expanded in the future.

#### Frameworks, libraries and tools used
The web application was designed using a Flask framework for the back-end. SQLite 3 was used as a database. I used [DB Browser for SQLite](https://sqlitebrowser.org/), to access, modify and view the database during development. Front-end was built using HTML, CSS, Bootstrap and Javascript. Furthermore, there are some graphical representations created using chartjs. This web app also integrates an API (the [coffeeAPI](https://coffee.alexflipnote.dev/)), to demonstrate my ability to use other libraries and integrate API's in web applications. In python, I also used the mailconfig library to make a contact form for this website.

The whole web app was designed in a responsive way and in a way that is accessible for anyone.

The main purpose of this application was to expand my acquired knowledge after CS50 and build a meaningfull application that combines the different aspects covered during the course.

#### Usage
##### Registering

<img width="40%" alt="Screenshot 2023-07-30 at 20 44 35" src="https://github.com/pitiao145/CS50-Final-Project-2023/assets/133644618/ff4663f5-8e03-4128-9c0b-67e89aed2ad0">
<img width="40%" alt="Screenshot 2023-07-30 at 20 44 41" src="https://github.com/pitiao145/CS50-Final-Project-2023/assets/133644618/a80de59c-080e-410d-9bd6-85f22f4a36be">

When accessing the web application, the user is prompted to enter a username and password. The program will check that the user inputs a valid username and password, giving feedback the to user about what is missing to achieve a compliant password. Once the user inputs a correct username and password. The username and the hashed password are then stored in a database. The user is then logged in, and redirected to the overview page.

##### Overview page

<img width="1680" alt="Screenshot 2023-07-30 at 20 47 38" src="https://github.com/pitiao145/CS50-Final-Project-2023/assets/133644618/d6c9829d-895d-4bca-83f2-22ef09104f78">

On this page, which acts as a dashboard, the user can see graphs with the amount stock of the different beans he owns, a graph with the daily coffee usage. At first these will be empty, as the user first needs to register some beans on the mybeans page.

Next, the user can see a field to register coffee use. Here, one can input the amount of coffee cups they had on a giving day, specifying the amount of coffee they used, which beans they used, and how they brew the coffee. All this information is stored in the databas, corresponding to the user in this session. All this data is then used to display all the different charts and favorites on the web application.
This section also contains a random image of a coffee cup, which is fetched from the CoffeeAPI. The pogram submits a GET request to the coffeeAPI, and the returned json file is then converted and used as an image on this webpage.

Lastly, at the bottom of this page, the user can see his favorite beans, type of beans and favorite brewing method, according the the data available for this user.

##### My beans page

<img width="1680" alt="Screenshot 2023-07-30 at 20 48 17" src="https://github.com/pitiao145/CS50-Final-Project-2023/assets/133644618/dc61d917-9f9c-46b8-9b10-c4e1d0d41bf4">


On this page, the user can store the different beans he owns, along with a lot of detailed information about these beans. The overview table displays a list of the different beans the users owns, along with some basic information about these beans. If the user wants to see more detailed information, they can click on the 'more info' button, and a modal with more detailed information will pop up. All these information is always up to date as it is fetched directly from the database. Getting the detailed information for the beans from the database happens with an Ajax request function.

On this page are also displayed some graphs for the stockk of the different beans, as some pie charts to see the distribution of the type of beans and their origin. All these graphs are rendered using the chart.js library.

##### Reviews

<img width="1680" alt="Screenshot 2023-07-30 at 20 48 48" src="https://github.com/pitiao145/CS50-Final-Project-2023/assets/133644618/c5b36b77-2a98-4901-83d8-c62f30a84543">


On this page, the user can fill in a form to leave their personal reviews for all the beans they use. This way, they can compare the offcial CR review with their own experience of the coffee beans. Once the user leaves their first review, a table with an overview of all their reviews will also appear on this page.

##### Brewing page

<img width="1680" alt="Screenshot 2023-07-30 at 20 49 23" src="https://github.com/pitiao145/CS50-Final-Project-2023/assets/133644618/4640c2fe-faab-4235-afd0-e11b289f7fb5">


This page contains information about some popular brewing methods, for the users reference. This section will be updated in the future.

##### Contact page

<img width="1680" alt="Screenshot 2023-07-30 at 20 50 15" src="https://github.com/pitiao145/CS50-Final-Project-2023/assets/133644618/d8c7dc47-b788-4e2d-a27d-390212fb5528">

Here's a contact form, to contact me in case of any question. Filling in the form and submitting it will send this form to my email address.

##### My profile tab in navigation bar
Here the user has the option to log out or to change their password.


### Code
The static folder contains all the static files: images, javascript files and CSS files.

The templats folders contains all the HTML documents used to render the web page. Since this was built using the flask framework, the folders contains a layout.html that renders the basic layout of the web application. All the other pages extend this layout, using the jinja2 language.

