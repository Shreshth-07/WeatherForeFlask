# WeatherForeFlask
This personal project consists of a website that displays the weather forecast for the current day for a specific city (Puerto Madryn, Chubut, Argentina). 
The project is divided into three main parts:
 1) Data adquisition: the data has been collected from my own weather station (placed in Puerto Madryn, Argentina). The data from the last 9 years is stored in wunderground.com from whose API the data has been obtained.
Further pre-processing is needed to make the data feasible for Machine Learning (ML) and Deep Learning (DL) model predictions.
 2) Weather variables predictions: by means of ML and DL models, the maximum and minimum temprature, and the rain probability is predicted one day in advance. Further improvements are on the way.
 3) Deployment: the way to comunicate the predictions is via a website developed in Flask. The website presents also few more features, such as: users registration and tasks reminder.
 
 The current repository contains the code that concerns the deployment task (3). 
