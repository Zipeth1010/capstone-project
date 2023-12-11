# Background

## Project Breakdown

This project was developed as the final module of the [IBM Full Stack Software Developer Professional Certificate](https://www.coursera.org/professional-certificates/ibm-full-stack-cloud-developer). I was given tasks to create templates, views, models, urls etc. to build the application up from a very basic initial layout and design. The project was peer-reviewed after submission and I don't plan on spending too much time improving the Front-End design as the biggest learning points from this project were learning Django application development and software developement using serverless and cloud computing.

## Project Aim
The aim of this project is to build a website for a fictional car dealership, to hold dealership, user, review, and car data. Users can sign in, select which dealership they would like information on and if they ended up using the dealership, they can leave a review if logged in so others know if the dealership was good or not. Reviews are automatically analysed using the IBM Watson NLU machine learning service to determine if they were good or not, and will be displayed accordingly. Admins can also be added which have the autority to add different Car Makes (E.g. Audi, Skoda) and models (E.g. R9, Octavia) to a seperate postgreSQL database. These are then saved and are choosable to users when leaving a review about the specific car model they used when at the dealership.

## Running Locally
Firstly, one must clone the project. Open a new terminal and direct the directory towards the area you want it saved. 
- Run 'git clone https://github.com/Zipeth1010/capstone-project.git'.
- Run cd capstone-project/server
- Install the required python packages 'pip install -r requirements.txt'

To run the server, you must do the following:
- In the server directory, run 'python3 manage.py makemigrations'
- Then run 'python3 manage.py migrate'
- Lastly, run 'python3 manage.py runserver'

To create a superuser, which can add car makes:
- Run the command 'python3 manage.py createsuperuser' while in the server directory
- Follow the instructions and you may then use these details to log in on the app, or in the admin site. 

