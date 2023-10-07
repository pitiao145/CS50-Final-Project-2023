# Mybeans: a coffee web app for coffee fanatics
#### Video Demo:

![ezgif com-optimize](https://github.com/pitiao145/CS50-Final-Project-2023/blob/main/static/readmeImages/webappdemoGIF.gif)

<img width="40%" alt="img1" src="https://github.com/pitiao145/CS50-Final-Project-2023/blob/main/static/readmeImages/webappimage1.png">

<img width="40%" alt="img2" src="https://github.com/pitiao145/CS50-Final-Project-2023/blob/main/static/readmeImages/webappimage2.png">

#### Description:
This application was designed by a coffee lover, for coffee lovers. With this web app, you can register all the beans you ever bought, keep track of your current stock of beans, leave reviews and write comments for the different types of beans you currently own, or have owned in the past. The app also allows you to track your coffee use, in the amount of cups and mass of coffee beans used over time. It also displays your favorite type of beans, favorite origins and favorite brewing methods, according to your usage and brewing methods.
There is also a section that informs you about the different brewing methods. This section will be expanded in the future.

#### Frameworks, libraries and tools used
The web application was designed using a Flask framework for the back-end. SQLite 3 was used for the database. I used [DB Browser for SQLite](https://sqlitebrowser.org/), to access, modify and view the database during development. Front-end was built using HTML, CSS, Bootstrap and Javascript. Furthermore, there are some graphical representations created using chartjs. This web app also integrates an API (the [coffeeAPI](https://coffee.alexflipnote.dev/)), to demonstrate my ability to use other libraries and integrate API's in web applications. In python, I also used the mailconfig library to make a contact form for this website, which send out an email when the user fills in the form.

The whole web app was designed in a responsive way.

The main purpose of this application was to expand my acquired knowledge after CS50 and build a meaningful application that combines the different aspects covered during the course.

#### Usage
##### Registering

<img width="40%" alt="img3" src="https://github.com/pitiao145/CS50-Final-Project-2023/blob/main/static/readmeImages/webappimage3.png">
<img width="40%" alt="img4" src="https://github.com/pitiao145/CS50-Final-Project-2023/blob/main/static/readmeImages/webappimage4.png">

When accessing the web application, the user is prompted to enter a username and password. The program will check that the user inputs a valid username and password, giving feedback the to user about what is missing to achieve a compliant password. Once the user inputs the correct username and password, the username and the hashed password are stored in a database. The user is then logged in and redirected to the overview page.

##### Overview page

<img width="1680" alt="img5" src="https://github.com/pitiao145/CS50-Final-Project-2023/blob/main/static/readmeImages/webappimage5.png">

On this page, which acts as a dashboard, the user can see graphs with the amount of stock of the different beans he owns, and a graph with the daily coffee usage. At first, these will be empty, as the user first needs to register some beans on the mybeans page.

Next, the user can see a field to register coffee use. Here, one can input the amount of coffee cups they had on a given day, specifying the amount of coffee they used, which beans they used, and how they brew the coffee. All this information is stored in the database, corresponding to the user in this session. All this data is then used to display all the different charts and favorites on the web application.
This section also contains a random image of a coffee cup, which is fetched from the CoffeeAPI. The program submits a GET request to the coffeeAPI, and the returned json file is then converted and used as an image on this webpage.

Lastly, at the bottom of this page, the user can see his favorite beans, type of beans and favorite brewing method, according to the the data available for this user.

##### My beans page

<img width="1680" alt="img6" src="https://github.com/pitiao145/CS50-Final-Project-2023/blob/main/static/readmeImages/webappimage6.png">


On this page, the user can store the different beans he owns, along with a lot of detailed information about these beans. The overview table displays a list of the different beans the user owns, along with some basic information about these beans. If the user wants to see more detailed information, they can click on the 'more info' button, and a modal with more detailed information will pop up. All this information is always up to date as it is fetched directly from the database.

Getting the detailed information for the beans from the database happens was implemented with an Ajax request function. This way, not the whole page is refreshed, but only part of the page is updated with the required information from the database.

This page also displays some graphs for the stokk of the different beans, as well as some pie charts to see the distribution of the type of beans and their origin. All these graphs are rendered using the chart.js library.

##### Reviews

<img width="1680" alt="review" src="https://github.com/pitiao145/CS50-Final-Project-2023/blob/main/static/readmeImages/webappimagereviews.png">


On this page, the user can fill in a form to leave their personal reviews for all the beans they use. This way, they can compare the official CR review with their own experience of the coffee beans. Once the user leaves their first review, a table with an overview of all their reviews will also appear on this page.

##### Brewing page

<img width="1680" alt="brewing" src="https://github.com/pitiao145/CS50-Final-Project-2023/blob/main/static/readmeImages/webappimagebrewing.png">


This page contains information about some popular brewing methods, for the user's reference. This section will be updated in the future.

##### Contact page

<img width="1680" alt="contact" src="https://github.com/pitiao145/CS50-Final-Project-2023/blob/main/static/readmeImages/webappimage7.png">

Here's a contact form, to contact me in case of any questions. Filling in the form and submitting it will send this form to my email address.

##### My profile tab in the navigation bar
Here the user has the option to log out or to change their password.


### Code
<img width="163" alt="Code structure" src="https://github.com/pitiao145/CS50-Final-Project-2023/blob/main/static/readmeImages/codestruct.png">


  * The static folder contains all the static files: images, javascript files and CSS files.
  * _main.js_
  Contains some JS functions, used in HTML pages. One function gets the name of the available beans in the my beans table. The other function assigns the names of the beans to the different `<select> <option>` tags in the different forms across the web pages.
  * _charts.js_
  This script is used to render the  different charts on the pages. It fetches the data, which has been selected in the _app.py_ file using db queries, converts it to a json file, which is then used to populate the charts.
  *  The _templates_ folder contains all the HTML documents used to render the web page. Since this was built using the Flask framework, the folders contain a layout.html that renders the basic layout of the web application. All the other pages extend this layout, using the jinja2 language.
  *  _app.py_ contains all the code with the different routes for navigating the web app.
  *  _APIcall_ is a different file that contains the function that performs a get request from the coffeeAPI. The response of the API contains a JSON file with a random image file. This function is called anytime the relevant page of the web app refreshes.
  *  _helpers.py_ contains the helpers functions. These are the functions that check if a user is logged in a session and get the user_id of the user in the current session.
  *  _mailconfig_ contains the constants for the _mailconfig_ configuration in the _app.py_ file.

### Database
The database for this project contains 4 tables: users, coffee_use, mybeans and reviews.
*  _users_ 
In this table, the different users and their hashed passwords are stored
*  _coffee use_
This table stores data for every user about the amount of coffees registered and when they were registered, the amount of coffee grounds used, how many times each brewing method was used
*  _my beans_
This table contains the data about the beans for each user: name, roast date, expiry date, origin, retailer, stock, bean type, roasting level, notes, acidity, official CR review, description and comments
*  _reviews_
This contains the reviews the user adds from the review page.


