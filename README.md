# Molecular Biology Automation (molbio.ai)

The molbio.ai application is a full-stack application aimed at automating molecular biology workflows. The application allows users to enter specific biology research project parameters, which it then processes and returns a detailed breakdown of the necessary steps to automate the project, along with OpenTrons API code to automate relevant steps.

## Backend

The backend of this application is built using Flask and served by Gunicorn. It has two main dependencies: the `flask` package to set up the web server, and `flask_cors` to handle Cross-Origin Resource Sharing (CORS), allowing the frontend and backend to communicate.

The application's backend contains an API endpoint (`/reverse`), which accepts POST requests. When the server receives data from the client, it calls a function `main()` imported from `molbio.py` to process the user input. The processed data is then returned to the frontend.

Exception handling is implemented to catch and report any errors that may occur during the processing of the user input. 

The server is set to run on host '0.0.0.0' and port 5000.

## Frontend

The frontend is built using React. The main component `App` handles the user input and communicates with the backend using the `axios` library to send a POST request.

A loading message is displayed to the user while waiting for the response from the server, with the message changing every 10 seconds. Once the server response is received, it is displayed on the page.

The UI includes an input field for user input and a submit button, which changes its text based on whether the user input has been submitted or not.

## Server

The reverse proxy server is built on Nginx. The Flask server listens on port 5000, the React frontend listens on port 3000, and the Nginx server listens on port 80. The Nginx server acts as a reverse proxy, forwarding requests to the Flask server or the React frontend as appropriate.   

## Containers

The project is divided into three directories, each corresponding to a Docker container which are built and run together according to docker-compose.yaml 

frontend/: Contains all the React components and related frontend code.
backend/: Houses the Flask server and related backend code.
nginx/: Contains the configuration file for the Nginx reverse proxy server.

## Getting Started

This website can be accessed at my domain, molbio.ai

To host this on your machine, make sure you have Docker and Docker compose. Then, clone the repository and run:

```bash
$ docker-compose up --build -d
```

## Testing

The molbio.py driver has a test() function, and app.js can be easily modified to call this upon submission. This test() function will wait thirty seconds, allowing for three loading messages to be displayed, and then returns the user input and some text.

To test the driver main() function, run the following to call the main() function with a preset project for user_input and with output directed to the terminal:

```bash
$ python3 molbio.py
```