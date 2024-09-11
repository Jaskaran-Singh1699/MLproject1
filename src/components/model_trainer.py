import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import Custom_Exception
from src.logger import logging
from src.utils import save_object
from src.utils import evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Split Training and Test input data")

            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models={
                "Random Forest":RandomForestRegressor(),
                "Linear Regression":LinearRegression(),
                "Decision Tree":DecisionTreeRegressor(),
                "Gradient Boosting":GradientBoostingRegressor(),
                # "K-Neighbors Classifiers":KNeighborsRegressor(),
                "XGBRegressor":XGBRegressor(),
                "CatBoost Regressor":CatBoostRegressor(verbose=False),
                "AdaBoost Regressor":AdaBoostRegressor(),
            }


            # giving hyperparameters
            params={
                "Decision Tree":{
                    'criterion':['squared_error','friedman_mse','absolute_error','poisson']
                },
                "Random Forest":{
                    'n_estimators':[8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    'n_estimators':[8,16,32,64,128,256],
                    'learning_rate':[.1,.01,.001,0.05],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9]
                },
                "Linear Regression":{},
                "XGBRegressor":{
                    'learning_rate':[0.1,0.01,0.05,0.001]
                },
                "CatBoost Regressor":{
                    'depth':[6,8,10],
                    'learning_rate':[0.01,0.05,0.1],
                    'iterations':[30,50,100]
                },
                "AdaBoost Regressor":{
                    'n_estimators':[8,16,32,64,128,256],
                    'learning_rate':[0.1,0.01,0.5,0.001]
                }
            }



            model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models,param=params)

            # get best score ffrom dict
            best_model_score=max(sorted(model_report.values()))

            #get best model name
            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model=models[best_model_name]

            if best_model_score<0.6:
                raise Custom_Exception("No Good Model")
            
            logging.info(f"Best model on both training and test dataset is {best_model}")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )


            predicted=best_model.predict(X_test)
            r2score=r2_score(y_test,predicted)
            return r2score

        except Exception as e:
            raise Custom_Exception(e,sys)