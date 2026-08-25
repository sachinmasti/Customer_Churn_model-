from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Annotated, Literal
from datetime import date
import regex as re

class CustomerChurn(BaseModel):
    """
    Pydantic schema representing the data model for Customer Churn Prediction.
    
    This class defines the expected data structure, validation constraints,
    and feature engineering (computed properties) for incoming requests to the API.
    """

    # --- INPUT FIELDS ---

    # Age of the customer (integer, must be between 18 and 99 inclusive)
    age: Annotated[int, Field(..., description='enter your age', gt=17, lt=100)]
    
    # Gender of the customer (must be 'male', 'female', or 'other')
    gender: Annotated[str, Field(..., description='enter your gender'), Literal['male', 'female', 'other']]
    
    # Location of the customer (major city name or generic categories)
    location: Annotated[str, Field(..., description='enter your location', examples=['mumbai', 'delhi', 'bangalore'])]
    
    # Customer tenure in months (float, greater than 0)
    tenure_months: Annotated[float, Field(..., description='enter your total working months', gt=0, examples=[5, 10, 20])]
    
    # Monthly charges billed to the customer (float, greater than 0)
    monthly_charges: Annotated[float, Field(..., description='enter customers monthly charges', gt=0, examples=[40, 80, 60])]
    
    # Cumulative total charges billed to the customer (float, greater than 0)
    total_charges: Annotated[float, Field(..., description='enter customers monthly charges', gt=0, examples=[100, 300, 1100])]
    
    # Type of contract contract billing ('monthly', '1 year', '2 year')
    contract_type: Annotated[str, Field(..., description='enter customers contract type'), Literal['monthly', '1 year', '2 year']]
    
    # Internet service classification ('fiber optic', 'dsl', 'no internet service')
    internet_service: Annotated[str, Field(..., description='enter customers internet service details'), Literal['fiber optic', 'dsl', 'no internet service']]
    
    # Whether the customer uses phone service ('yes', 'no')
    phone_service: Annotated[str, Field(description='enter yes if  customers using phone service phone service'), Literal['yes', 'no']]
    
    # Whether online security is enabled ('yes', 'no')
    online_security: Annotated[str, Field(description='enter yes if customer using online security'), Literal['yes', 'no']]
    
    # Level of technical support used ('yes', 'no', 'no internet service')
    tech_support: Annotated[str, Field(description='enter customer tech support'), Literal['yes', 'no', 'no internet service']]
    
    # Payment method used by the customer
    payment_method: Annotated[str, Field(..., description='enter payment method customer using'), Literal['electronic check', 'credit card (automatic)',
    'mailed check', 'bank transfer (automatic)', 'upi', 'cash']]
    
    # Customer satisfaction score (1 to 15 rating)
    satisfaction_score: Annotated[float, Field(..., description='enter customer satisfaction score', gt=0, lt=16)]
    
    # Date of last contact with customer
    last_contact_date: Annotated[date, Field(..., description='enter users last contact date', examples=['2023-07-12', '2024-03-16'])]
    
    # Number of support tickets raised by customer (must be less than 100)
    support_tickets: Annotated[int, Field(description='enter a support tickets by user raised', lt=100)]
    
    # Email address of the customer
    email: Annotated[str, Field(..., description='enter customer email id', examples=['anita19@yahoo.com', 'yadav31@gmail.com'])]


    # --- VALIDATORS ---

    @field_validator('gender', mode='before')
    def chek_gender(cls, value):
        """
        Validate and standardize the gender input to lowercase.
        """
        if value.lower() not in ['male', 'female', 'other']:
            raise ValueError('gender must be ["male","female","other"]')
        return value.lower()

    @field_validator('location')
    def check_location(cls, value):
        """
        Validate and map the location to recognized major Indian cities.
        If the city is not in the list, maps it to 'other'.
        """
        city_lst = ['delhi', 'mumbai', 'chennai', 'bangalore', 'kolkata', 'hyderabad', 'pune']
        return 'other' if value.lower() not in city_lst else value.lower()

    @field_validator('contract_type', mode='before')
    def chek_contract_type(cls, value):
        """
        Validate and standardize contract type to lowercase.
        """
        if value.lower() not in ['monthly', '1 year', '2 year']:
            raise ValueError('contract type must be "monthly","1 year","2 year"')
        return value.lower()

    @field_validator('internet_service', mode='before')
    def validate_internet_service(cls, value):
        """
        Validate and standardize internet service type to lowercase.
        """
        if value.lower() not in ['fiber optic', 'dsl', 'no internet service']:
            raise ValueError(f"your {value} must be in ['fiber optic', 'dsl', 'no internet service']")
        return value.lower()

    @field_validator('phone_service', mode='before')
    def valid_phone_service(cls, value):
        """
        Standardize phone service value to lowercase.
        """
        return value.lower()

    @field_validator('online_security', mode='before')
    def valid_online_security(cls, value):
        """
        Standardize online security value to lowercase.
        """
        return value.lower()

    @field_validator('tech_support', mode='before')
    def valid_tech_support(cls, value):
        """
        Validate and standardize tech support value to lowercase.
        """
        if value.lower() not in ['yes', 'no', 'no internet service']:
            raise ValueError(f"your {value} must be ['yes', 'no', 'no internet service']")
        return value.lower()

    @field_validator('payment_method', mode='before')
    def check_payment_method(cls, value):
        """
        Validate and standardize payment method value to lowercase.
        """
        payment_list = ['electronic check', 'credit card (automatic)', 'mailed check', 'bank transfer (automatic)', 'upi', 'cash']
        if value.lower() not in payment_list:
            raise ValueError(f"your {value} must be {payment_list} so retype your input")
        return value.lower()


    # --- COMPUTED FIELDS (FEATURE ENGINEERING) ---

    @computed_field
    @property
    def last_contact_day(self) -> int:
        """
        Extract the day of the month from the last contact date.
        """
        return self.last_contact_date.day

    @computed_field
    @property
    def last_contact_month(self) -> int:
        """
        Extract the month from the last contact date.
        """
        return self.last_contact_date.month

    @computed_field
    @property
    def last_contact_year(self) -> int:
        """
        Extract the year from the last contact date.
        """
        return self.last_contact_date.year

    @computed_field
    @property
    def last_contact_week(self) -> int:
        """
        Extract the day of the week (0 = Monday, 6 = Sunday) from the last contact date.
        """
        return self.last_contact_date.weekday()

    @computed_field
    @property
    def last_contact_week_of_year(self) -> int:
        """
        Extract the ISO week number of the year from the last contact date.
        """
        return self.last_contact_date.isocalendar().week

    @computed_field
    @property
    def valid_email(self) -> int:
        """
        Validate email format using a regular expression.
        Returns 1 if valid, 0 otherwise.
        """
        email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if re.match(email_pattern, self.email.lower()):
            return 1
        return 0

    @computed_field
    @property
    def email_domain(self) -> str:
        """
        Extract and return the domain name of the customer's email.
        Returns 'invalid' if the email is not valid or domain not in training data.
        """
        known_domains = {'gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com', 'company.in', 'invalid'}
        domain_pattern = r'^[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$'
        domain = self.email.split('@')[-1].lower()

        if '@' not in self.email:
            return 'invalid'

        if re.match(domain_pattern, domain) and domain in known_domains:
            return domain
        return 'invalid'

