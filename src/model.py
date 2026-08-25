import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from colorama import Fore, init
init(autoreset=True)
import time

from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.ensemble import BaggingClassifier
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import TargetEncoder

from xgboost import XGBClassifier
from src.preprocessing import capping


def load_data():
    """
    Load the clean customer churn dataset from the data folder.
    
    Returns:
        pd.DataFrame: Loaded dataset.
    """
    base_dir: Path = Path(__file__).resolve().parent.parent
    df_path = base_dir / 'data' / 'customer_churn_v2.0_clean.csv'
    df = pd.read_csv(df_path)
    return df


def split_data(df: pd.DataFrame):
    """
    Split the dataset into training and testing features (X) and target (y).
    
    Args:
        df (pd.DataFrame): The input dataframe containing customer features and the 'churn' target.
        
    Returns:
        tuple: (x_train, x_test, y_train, y_test) split subsets of the data.
    """
    # Separate independent features from the target variable 'churn'
    x = df.drop('churn', axis=1)
    y = df['churn']
    
    # Split the dataset into 80% training and 20% testing data
    x_train, x_test, y_train, y_test = train_test_split(
        x, y,
        test_size=0.2,
        shuffle=True,
        random_state=42
    )
    return x_train, x_test, y_train, y_test


def model_pipeline():
    """
    Construct the end-to-end preprocessing and model pipeline.
    
    This includes separate pipelines for age, other numerical variables, 
    one-hot encoded categorical variables, target encoded categorical variables,
    and a BaggingClassifier wrapped around an XGBoost model.
    
    Returns:
        Pipeline: Scikit-learn Pipeline containing preprocessing and the classifier.
    """
    # Preprocessing pipeline for the 'age' column:
    # - Impute missing values with the median and add a missing indicator column
    # - Apply log(1 + x) transformation to normalize distribution
    # - Standard scale the features
    age_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median', add_indicator=True)),
        ('transform', FunctionTransformer(np.log1p, validate=True)),
        ('scaler', StandardScaler())
    ])

    # Preprocessing pipeline for standard numerical features (e.g., tenure, charges):
    # - Impute missing values with the mean and add a missing indicator column
    # - Cap outliers using Winsorization (capping function)
    # - Standard scale the features
    numerical_pipe = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean', add_indicator=True)),
        ('capping', FunctionTransformer(capping)),
        ('scale', StandardScaler())
    ])

    # Preprocessing pipeline for low-cardinality categorical features using One-Hot Encoding:
    # - Impute missing values with the most frequent category and add an indicator column
    # - Perform One-Hot Encoding and drop the first category to avoid multicollinearity
    categorical_pipe_for_ohe = Pipeline(steps=[
        ('impute', SimpleImputer(strategy='most_frequent', add_indicator=True)),
        ('OHE', OneHotEncoder(drop='first'))
    ])

    # Preprocessing pipeline for high-cardinality or target-correlated categorical features:
    # - Impute missing values with the most frequent category and add an indicator column
    # - Apply Target Encoding to translate categories into numerical target relationships
    categorical_pipe_for_target_encoding = Pipeline(steps=[
        ('impute', SimpleImputer(strategy='most_frequent', add_indicator=True)),
        ('encode', TargetEncoder(categories='auto',
                                target_type='auto',
                                smooth='auto'))
    ])

    # Combine column-specific transformations using ColumnTransformer
    column_wise_transformers = ColumnTransformer(transformers=[
        # Apply OHE to common categorical columns
        ('categorical_ohe', categorical_pipe_for_ohe, make_column_selector(
            pattern='gender|contract_type|internet_service|phone_service|'
            'online_security|tech_support|email_domain')),

        # Apply Target Encoding to location and payment_method
        ('categorical_target_encode', categorical_pipe_for_target_encoding, make_column_selector(
            pattern='location|payment_method'
        )),

        # Apply specific age transformation pipeline
        ('numerical_transform_age', age_transformer, make_column_selector(
            pattern='age'
        )),

        # Apply numerical pipeline to tenure and charges
        ('numerical_transform', numerical_pipe, make_column_selector(
            pattern='tenure_months|monthly_charge|total_charges'
        ))
    ], remainder='passthrough')

    # Define the ensemble bagging model enclosing XGBoost Classifier
    bagging_model = BaggingClassifier(
        estimator=XGBClassifier(
            max_depth=7,
            colsample_bytree=0.8289096214538103,
            subsample=0.640503362351583,
            n_estimators=118,
            learning_rate=0.04370986966005013,
            grow_policy='lossguide',
            max_leaves=8,
            gamma=0.017614896151937388,
            min_child_weight=3
        ),
        n_estimators=150,
        bootstrap=True,
        oob_score=True,
        n_jobs=1
    )

    # Construct the final pipeline containing preprocessing steps and the model
    model_pipe = Pipeline(steps=[
        ('processors', column_wise_transformers),
        ('model', bagging_model)
    ])

    return model_pipe


def train_model_and_save(model_path=None):
    """
    Train the model pipeline on the training dataset, evaluate it on testing data,
    and save the trained pipeline artifact.
    
    Args:
        model_path (str or Path, optional): The path to save the trained model.
                                           Defaults to 'models/customer_churn_model.joblib'.
    """
    if model_path is None:
        base_dir = Path(__file__).resolve().parent.parent
        model_path = base_dir / 'models' / 'customer_churn_model.joblib'
    """
    Train the model pipeline on the training dataset, evaluate it on testing data,
    and save the trained pipeline artifact.
    
    Args:
        model_path (str): The filename/path to save the trained joblib model.
    """
    print(f'{Fore.GREEN}Loading model pipeline...')
    pipeline = model_pipeline()
    time.sleep(2)

    # Split the dataset
    x_train, x_test, y_train, y_test = split_data(load_data())

    # Fit the pipeline model on training data
    print(f'{Fore.CYAN}Training the model...')
    pipeline.fit(x_train, y_train)
    print(f'{Fore.GREEN}Model training completed.')
    
    # Generate predictions on the test set
    y_pred = pipeline.predict(x_test)

    # Save the trained model pipeline to a serialized joblib file
    joblib.dump(pipeline, model_path)
    
    # Print evaluation metrics
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))


if __name__ == '__main__':
    train_model_and_save()