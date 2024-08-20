
## Team Members and Team Lead

- **Team Lead**: Sean Sullivan
- **Other Team Members**: N/A


The team lead's GitHub Classroom repository will be used for the project, which can be found [here](https://github.com/nuwebdev/prototype.git).

## Project Goal:

- Comment on Real Estate Listings: A web app built using Flask and Bootstrap, Python and SQL that will allow users to leave comments linked to house listings. 

  ## User Stories:

  - As a user, I want to be able to...
      - Share my opinions on real estate listings and hear others' opinions.
      - Create a user account. 
      - Create/ read/ update/ delete my own posts linked to a house listing URL.
      - Easily read others posts about specific listings, in which all comments about any listing are grouped together.
      - Navigate to the listing itself via a single click of the mouse. 
  - STRETCH GOALS: 
      - Find/ view selected listings in the state of my choice via either search or selection from list. 
      - Add up/down voting buttons to each listing, allowing a user to vote up/down any listing a single time, the value of which will be created/ linked to the SQL db, thereby offering additional grouping display options.
      - Connect a Google Chrome plugin such that users can leave comments on houses via embedded comments box on listing page itself. 


## UI Design:
- The overall design of the site will focus on functionality over aesthetics. Think Craiglist/ Reddit-esque sort of organized message/ posts groupings. A variety of bootstrap5 elements will be used, including but not limited to: 
- [Bootstrap forms](https://getbootstrap.com/docs/4.3/components/forms/) templates will be used for user registration/ login, posts creation and editing.
- [Bootstrap NavBar](https://www.w3schools.com/bootstrap5/bootstrap_navbar.php) to navigate through website.
- [Bootstrap Buttons](https://www.w3schools.com/bootstrap5/bootstrap_buttons.php) 



## Architecture and Technical Requirements:

  This project will be a full-stack web application. It incorporates user authentication, and CRUD Operations for users: creating, reading, updating and deleting comments (posts). 

  This architecture aims to provide a scalable, maintainable, and user-friendly platform for community engagement around house listings, leveraging Flask's flexibility and Bootstrap's design framework for rapid development and deployment.

Front-end:
  -   Bootstrap: Used for front-end design to ensure a responsive and modern user interface. 
  -   HTML: Basic structure of web pages, with Bootstrap managing CSS. 

Back-end:
  -   Flask: Serving as the back-end framework, handling routing, server-side logic, and integration between front-end and    database. Uses Flask to dynamically generate HTML content based on backend data.
  -   Python: Primary language for server-side logic, including user authentication, posts/ data manipulation.
  -   SQLite: Database for storing user info, posts (comments), and metadata like timestamps and listing URLs. 
    
Technical Requirements:
  -   A virtual environment 'venv' has been created for this project and will contain all dependencies to ensure reproducibility. Details can be found in the [environment.yml](environment.yml) file. 
  -   Bootstrap5 classes will be accessed via Bootstrap's CDN to ensure rapid loading for users. 

Acknowledgements:
  -   [Flask 'Blog Blueprint' Tutorial](https://flask.palletsprojects.com/en/3.0.x/tutorial/blog/): This served as the basis for the web applications user auth and posting capabilities.
  -   [W3 Schools Bootstrap5 Tutorials](https://www.w3schools.com/bootstrap5/index.php): Used extensively to access front-end design elements for the application.

Reproducibility:
  -   This project can be reproduced using make commands as found in the Makefile, with explicit instructions avaialble in the [README.md](flaskr/README.md)

Project Management:
  -   This is TBD until a team is formed. 
