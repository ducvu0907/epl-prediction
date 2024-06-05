# English Premier League (EPL) Prediction Project

## Overview

This project aims to collect, handle data and predict the outcomes of matches using machine learning models. Multiple models were trained and evaluated on a dataset containing historical EPL match data.

## Dataset

The data used in this project was scraped from [source](https://fbref.com/en/comps/9/Premier-League-Stats). This dataset contains English Premier League (EPL) match data, including match statistics, team performance metrics, and match outcomes.

## Dependencies

This project relies on the following Python libraries:
* Numpy
* Pandas
* Matplotlib
* Scikit-learn
* Requests
* Beautiful Soup

Make sure to install these dependencies using appropriate package manager before running the project. You can install them using the following command:
```bash
pip install numpy pandas matplotlib scikit-learn requests beautifulsoup4
```

## Models

Several machine learning models were trained and fine-tuned on the dataset for predicting match outcomes. The following models were included:
1. Random Forest
2. Logistic Regression
3. XGBoost
4. Support Vector Machine

## Evaluation

The performance of each model was evaluated using various evaluation metrics such as accuracy, precision, recall.

# Future Improvements

This project can be further improved and extended in severals ways, including:
* Gather more data as well as additional features for better predictive performance.
* Employ cross-validation for selections to ensure the robustness of the models.
* Experiment with ensemble methods such as stacking or blending to further enhance generalization.
* Develop a system for real-time prediction of the EPL match outcomes based on live match data.
