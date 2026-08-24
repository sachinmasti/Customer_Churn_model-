import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from colorama import Fore,init
init(autoreset=True)
import time

from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer,make_column_selector
from sklearn.metrics import confusion_matrix,classification_report
from sklearn.ensemble import BaggingClassifier
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import TargetEncoder

from xgboost import XGBClassifier
from scipy.stats.mstats import  winsorize


def capping(x):
    cap = winsorize(x,limits=(0.05,0.05))
    return cap

def load_data():
    base_dir: Path = Path(__file__).resolve().parent
    df_path = base_dir/'data'/'customer_churn_v2.0_clean.csv'
    df = pd.read_csv(df_path)
    return df

def split_data(df:pd.DataFrame):
    x = df.drop('churn',axis=1)
    y = df['churn']
    x_train, x_test, y_train, y_test = train_test_split(
        x, y,
        test_size=0.2,
        shuffle=True,
        random_state=42
    )
    return x_train, x_test, y_train, y_test

def model_pipeline():
    age_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median',add_indicator=True)),
        ('transform',FunctionTransformer(np.log1p,validate=True)),
        ('scaler',StandardScaler())
    ])

    numerical_pipe = Pipeline(steps=[
        ('imputer',SimpleImputer(strategy='mean',add_indicator=True)),
        ('capping',FunctionTransformer(capping)),
        ('scale',StandardScaler())
    ])

    categorical_pipe_for_ohe = Pipeline(steps=[
        ('impute',SimpleImputer(strategy='most_frequent',add_indicator=True)),
        ('OHE',OneHotEncoder(drop='first'))
    ])

    categorical_pipe_for_target_encoding = Pipeline(steps=[
        ('impute',SimpleImputer(strategy='most_frequent',add_indicator=True)),
        ('encode',TargetEncoder(categories='auto',
                                target_type='auto',
                                smooth='auto'))
    ])

    column_wise_transformers = ColumnTransformer(transformers=[
        ('categorical_ohe',categorical_pipe_for_ohe,make_column_selector(
            pattern='gender|contract_type|internet_service|phone_service|'
            'online_security|tech_support|email_domain')),

        ('categorical_target_encode',categorical_pipe_for_target_encoding,make_column_selector(
            pattern='location|payment_method'
        )),

        ('numerical_transform_age',age_transformer,make_column_selector(
            pattern='age'
        )),

        ('numerical_transform',numerical_pipe,make_column_selector(
            pattern='tenure_months|monthly_charge|total_charges'
        ))
    ],remainder='passthrough')

    bagging_model = BaggingClassifier(
        estimator=XGBClassifier(
             max_depth = 7,
            colsample_bytree = 0.8289096214538103,
            subsample = 0.640503362351583,
            n_estimators = 118,
            learning_rate = 0.04370986966005013,
            grow_policy = 'lossguide',
            max_leaves = 8,
            gamma= 0.017614896151937388,
            min_child_weight = 3
        ),
        n_estimators=150,
        bootstrap=True,
        oob_score=True,
        n_jobs=1

    )

    model_pipe = Pipeline(steps=[
        ('processors',column_wise_transformers),
        ('model',bagging_model)
    ])

    return model_pipe

def train_model_and_save(model_path = 'customer_churn_model.joblib'):
    print(f'{Fore.GREEN} model pipeline is loading')
    pipeline = model_pipeline()
    time.sleep(2)

    x_train,x_test,y_train,y_test = split_data(load_data())

    print(f'{Fore.CYAN} model is training')
    pipeline.fit(x_train,y_train)
    print(f'{Fore.GREEN} model is trained')
    y_pred = pipeline.predict(x_test)

    joblib.dump(pipeline,model_path)
    print(confusion_matrix(y_test,y_pred))
    print(classification_report(y_test,y_pred))

if __name__ == '__main__':
    train_model_and_save()