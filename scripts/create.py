import os
import re

from sqlalchemy import create_engine
from sqlalchemy.sql import text
import numpy as np
import pandas as pd


DATABASE_URI = os.environ.get('DATABASE_URI')

if not DATABASE_URI:
    raise ValueError('No DATABASE_URI variable was set')

engine = create_engine(DATABASE_URI)
engine.connect()

with open('../database/DDL/DDL.sql') as file:
    ddl = file.read()

for command in ddl.split(';'):
    if command := command.strip():
        engine.execute(text(f'{command};'))
