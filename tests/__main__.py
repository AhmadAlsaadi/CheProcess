#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Main script for unit testing


from test_lib import TestLib
from unittest import TextTestRunner, TestSuite
import warnings
from numpy import seterr
import os

# Define pychemqt environment
os.environ["CheProcess"] = os.path.abspath('.')
os.environ["freesteam"] = "False"
os.environ["pybel"] = "False"
os.environ["CoolProp"] = "False"
os.environ["refprop"] = "False"
os.environ["ezodf"] = "False"
os.environ["openpyxl"] = "False"
os.environ["xlwt"] = "False"
os.environ["icu"] = "False"
os.environ["reportlab"] = "False"
os.environ["PyQt5.Qsci"] = "False"


# Don't print the numpy RuntimeWarning
seterr("ignore")

warnings.simplefilter("ignore")


suite = TestSuite()
suite.addTest(TestLib)

runner = TextTestRunner(failfast=True)
results = runner.run(suite)
