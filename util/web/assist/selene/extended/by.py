"""
This file extends selene's by.py module
"""

from selene.support.by import *


def class_starts_with(value):
    return xpath(f'.//*[starts-with(@class,"{value}")]')


def class_contains(value):
    return xpath(f'.//*[contains(@class,"{value}")]')
