from pydantic import BaseModel,Field,field_validator,EmailStr,computed_field
from typing import Annotated,Literal
from datetime import date
import pandas as pd

class CustomerChurn(BaseModel):

    age:Annotated[int,Field(...,description='enter your age',gt=18,lt=100)]
    gender: Annotated[str,Field(...,description='enter your gender'),Literal['male','female','other']]
    location: Annotated[str,Field(...,description='enter your location',examples=['mumbai','delhi','bangalore'])]
    tenure_months:Annotated[float,Field(...,description='enter your total working months',gt=0,examples=[5,10,20])]
    monthly_charges: Annotated[float,Field(...,description='enter customers monthly charges',gt=0,examples=[40,80,60])]
    total_charges: Annotated[float, Field(...,description='enter customers monthly charges',gt=0,examples=[100,300,1100])]
    contract_type: Annotated[str,Field(...,description='enter customers contract type'),Literal['monthly','1 year','2 year']]
    internet_service : Annotated[str,Field(...,description='enter customers internet service details'),Literal['fiber optic','dsl','no internet service']]
    phone_service: Annotated[str,Field(description='enter yes if  customers using phone service phone service'),Literal['yes','no']]
    online_security: Annotated[str,Field(description='enter yes if customer using online security'),Literal['yes','no']]
    payment_method: Annotated[str,Field(...,description='enter payment method customer using'),Literal['electronic check','credit card (automatic)',
    'mailed check','bank transfer (automatic)','upi','cash']]
    satisfaction_score:Annotated[float,Field(...,description='enter customer satisfaction score',gt=0,lt=15)]
    last_contact_date: Annotated[date,Field(...,description='enter users last contact date',examples=['2023-07-12','2024-03-16'])]
    support_ticket: Annotated[int,Field(description='enter a support tickets by user raised',gt=0,lt=100)]
    email: Annotated[EmailStr,Field(...,description='enter customer email id',examples=['anita19@yahoo.com','yadav31@gmail.com'])]




def test(model:CustomerChurn):
    print(model)

test(CustomerChurn(
        age=15,
        gender='male',
        location='bangalore',
        tenure_months=10,
        monthly_charges=100,
        total_charges=2000,
        contract_type='monthly',
        internet_service='fiber optic',
        phone_service='yes',
        online_security='no',
        payment_method='upi',
        satisfaction_score=10,
        last_contact_date='2020-10-05',
        support_ticket=10,
        email='sachinmasti@gmail.com'
    ))

