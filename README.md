## Sneaker Investment Deployment

This is Licheng (Ian) Yin's insight project.

Sneaker Investment is a web application that predicts sneakers’ profitability for hobby investors using random forest model on sneakers’ transaction data from StockX. 

### Prerequisites
All packages within requirement.txt needs to be installed. 

### Project Structure
This project has four major parts :
1. sneaker.pkl - This contains pre-trained random forest classifier, which classify sneakers into profitable or not profitable sneakers.
2. app.py - This contains Flask routes that receives upcoming sneaker details through GUI, computes the precited sneaker profitability based on model and returns results as well as the most similar past release sneakers calculated using euclidean distance.
3. templates - This folder contains HTML templates that allow user to enter sneaker details and present predicted result.
4. statics - This folder contains CSS and JS files used for HTML templates.

### Running the project
1. Run app.py using below command to start Flask API
```
python app.py
```
By default, flask will run on port 5000.

2. Navigate to URL http://localhost:5000 

Users should be able to view the homepage as below :
![alt text](https://github.com/ianianing/example/blob/master/home.png)

Users should enter all 7 features for the upcoming sneaker they want to predict.
![alt text](https://github.com/ianianing/example/blob/master/sample_selection.png)

If everything goes well, users should  be able to see results on a new html page as below!
Users can click on "Predict Other Sneakers" button if they want to predict profitability for a different sneaker
![alt text](https://github.com/ianianing/example/blob/master/sample_results.png)


