from pydantic import BaseModel,Field,field_validator,computed_field
from typing import Annotated,Literal
from datetime import date
import regex as re

class CustomerChurn(BaseModel):

    age:Annotated[int,Field(...,description='enter your age',gt=17,lt=100)]
    gender: Annotated[str,Field(...,description='enter your gender'),Literal['male','female','other']]
    location: Annotated[str,Field(...,description='enter your location',examples=['mumbai','delhi','bangalore'])]
    tenure_months:Annotated[float,Field(...,description='enter your total working months',gt=0,examples=[5,10,20])]
    monthly_charges: Annotated[float,Field(...,description='enter customers monthly charges',gt=0,examples=[40,80,60])]
    total_charges: Annotated[float, Field(...,description='enter customers monthly charges',gt=0,examples=[100,300,1100])]
    contract_type: Annotated[str,Field(...,description='enter customers contract type'),Literal['monthly','1 year','2 year']]
    internet_service : Annotated[str,Field(...,description='enter customers internet service details'),Literal['fiber optic','dsl','no internet service']]
    phone_service: Annotated[str,Field(description='enter yes if  customers using phone service phone service'),Literal['yes','no']]
    online_security: Annotated[str,Field(description='enter yes if customer using online security'),Literal['yes','no']]
    tech_support: Annotated[str,Field(description='enter customer tech support'),Literal['yes','no','no internet service']]
    payment_method: Annotated[str,Field(...,description='enter payment method customer using'),Literal['electronic check','credit card (automatic)',
    'mailed check','bank transfer (automatic)','upi','cash']]
    satisfaction_score:Annotated[float,Field(...,description='enter customer satisfaction score',gt=0,lt=16)]
    last_contact_date: Annotated[date,Field(...,description='enter users last contact date',examples=['2023-07-12','2024-03-16'])]
    support_ticket: Annotated[int,Field(description='enter a support tickets by user raised',lt=100)]
    email: Annotated[str,Field(...,description='enter customer email id',examples=['anita19@yahoo.com','yadav31@gmail.com'])]

    @field_validator('gender',mode='before')
    def chek_gender(cls,value):
        if value.lower() not in ['male','female','other']:
            raise ValueError(
                'gender must be ["male","female","other"]'
            )
        else:
            return value.lower()

    @field_validator('location')
    def check_location(cls, value):
        city_lst = ['delhi','mumbai','chennai','bangalore','kolkata','hyderabad','pune']

        return 'other' if value.lower() not in city_lst else value.lower()

    @field_validator('contract_type',mode='before')
    def chek_contract_type(cls,value):
        if value.lower() not in ['monthly','1 year','2 year']:
            raise ValueError(
                'contract type must be "monthly","1 year","2 year"'
            )
        else:
            return value.lower()
    @field_validator('internet_service',mode='before')
    def validate_internet_service(cls,value):
        if value.lower() not in ['fiber optic','dsl','no internet service']:
            raise ValueError(
                f'your {value} must be in \'fiber optic','dsl','no internet service\''
            )
        else:
            return value.lower()
    @field_validator('phone_service',mode='before')
    def valid_phone_service(cls, value):
        return value.lower()

    @field_validator('online_security',mode='before')
    def valid_online_security(cls, value):
        return value.lower()

    @field_validator('tech_support',mode='before')
    def valid_tech_support(cls, value):
        if value.lower() not in ['yes','no','no internet service']:
            raise ValueError(
                f'your {value} must be [\'yes','no','no internet service\']'
            )
        return value.lower()

    @field_validator('payment_method',mode='before')
    def check_payment_method(cls, value):
        payment_list = ['electronic check','credit card (automatic)','mailed check','bank transfer (automatic)','upi','cash']
        if value.lower() not in payment_list:
            raise ValueError(
                f'your {value} must be {payment_list} so retype your input'
            )
        return value.lower()

    @computed_field
    @property
    def last_contact_day(self) -> int:
        return self.last_contact_date.day

    @computed_field
    @property
    def last_contact_month(self) -> int:
        return self.last_contact_date.month

    @computed_field
    @property
    def last_contact_year(self) ->int:
        return self.last_contact_date.year

    @computed_field
    @property
    def last_contact_week(self) -> int:
        return  self.last_contact_date.weekday()

    @computed_field
    @property
    def last_contact_week_of_year(self) -> int:
        return self.last_contact_date.isocalendar().week

    @computed_field
    @property
    def valid_email(self) -> int:
        email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if re.match(email_pattern,self.email.lower()):
            return 1

        return 0

    @computed_field
    @property
    def valid_domain(self)-> str:
        domain_pattern = r'^[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$'
        domain = self.email.split('@')[-1]

        if '@' not in self.email:
            return 'invalid'

        if re.match(domain_pattern,domain):
            return domain
        return 'invalid'

def test(model:CustomerChurn):
    print(model)

test(CustomerChurn(
        age=19,
        gender='Male',
        location='Delhi',
        tenure_months=10,
        monthly_charges=100,
        total_charges=2000,
        contract_type='Monthly',
        internet_service='Fiber Optic',
        phone_service='Yes',
        online_security='No',
        tech_support='NO',
        payment_method='Upi',
        satisfaction_score=10,
        last_contact_date='2020-10-09',
        support_ticket=10,
        email='sachinmasti@gmail.com'
    ))

