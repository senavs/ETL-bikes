import os
import re

from sqlalchemy import create_engine
import numpy as np
import pandas as pd


DATABASE_URI = os.environ.get('DATABASE_URI')

if not DATABASE_URI:
    raise ValueError('No DATABASE_URI variable was set')

engine = create_engine(DATABASE_URI)
engine.connect()


def to_upper(text: str) -> str:
    """To upper case non null text"""
    if text is not None:
        return text.upper()

    
def to_lower(text: str) -> str:
    """To lower case non null text"""
    if text is not None:
        return text.lower()


def id_to_captilize(text: str) -> str:
    """Replace string non null text that ends with ID to Id"""
    if text is not None:
        return re.sub(r'(^.*)ID', r'\1Id', text)



def to_snake_case(text: str) -> str:
    """To snake case non null text"""
    if text is not None:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', text)



def to_float(text: str) -> float:
    """String to float format"""
    if text is not None:
        return float(text.replace(',', '.'))

    
# Person

dataframe = pd.read_csv('../dataset/Person.Person.csv', sep=';')

dataframe.columns = [to_upper((to_snake_case(id_to_captilize(column)))) for column in dataframe.columns]
dataframe.rename({'BUSINESS_ENTITY_ID': 'PERSON_ID'}, axis=1, inplace=True)
dataframe.TITLE.replace({'Ms': 'Ms.'}, inplace=True)


dataframe.to_sql('PERSON', engine, if_exists='append', index=False)


# Customer

dataframe = pd.read_csv('../dataset/Sales.Customer.csv', sep=';')

dataframe.columns = [to_upper((to_snake_case(id_to_captilize(column)))) for column in dataframe.columns]

dataframe.to_sql('CUSTOMER', engine, if_exists='append', index=False)


# Sales Order Header

dataframe = pd.read_csv('../dataset/Sales.SalesOrderHeader.csv', sep=';')

dataframe.columns = [to_upper((to_snake_case(id_to_captilize(column)))) for column in dataframe.columns]
dataframe.replace({np.nan: None}, inplace=True)
dataframe.SUB_TOTAL = dataframe.SUB_TOTAL.apply(to_float)
dataframe.TAX_AMT = dataframe.TAX_AMT.apply(to_float)
dataframe.FREIGHT = dataframe.FREIGHT.apply(to_float)
dataframe.TOTAL_DUE = dataframe.TOTAL_DUE.apply(to_float)

dataframe.to_sql('SALES_ORDER_HEADER', engine, if_exists='append', index=False)


# Product

dataframe = pd.read_csv('../dataset/Production.Product.csv', sep=';')

dataframe.columns = [to_upper((to_snake_case(id_to_captilize(column)))) for column in dataframe.columns]
dataframe.STANDARD_COST = dataframe.STANDARD_COST.apply(to_float)
dataframe.LIST_PRICE = dataframe.LIST_PRICE.apply(to_float)

dataframe.to_sql('PRODUCT', engine, if_exists='append', index=False)


# Special Offer Product

dataframe = pd.read_csv('../dataset/Sales.SpecialOfferProduct.csv', sep=';')

dataframe.columns = [to_upper((to_snake_case(id_to_captilize(column)))) for column in dataframe.columns]

dataframe.to_sql('SPECIAL_OFFER_PRODUCT', engine, if_exists='append', index=False)


# Sales Order Detail

dataframe = pd.read_csv('../dataset/Sales.SalesOrderDetail.csv', sep=';')

dataframe.columns = [to_upper((to_snake_case(id_to_captilize(column)))) for column in dataframe.columns]
dataframe.UNIT_PRICE = dataframe.UNIT_PRICE.apply(to_float)
dataframe.UNIT_PRICE_DISCOUNT = dataframe.UNIT_PRICE_DISCOUNT.apply(to_float)

dataframe.to_sql('SALES_ORDER_DETAIL', engine, if_exists='append', index=False)
