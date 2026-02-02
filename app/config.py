# app/config.py
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://test_1b75_user:T42FQWFCiL9G3WGOF8b5vCG4R69i9qhQ@dpg-cv80lfdds78s73crbjag-a.oregon-postgres.render.com/test_1b75'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = timedelta(days=7)