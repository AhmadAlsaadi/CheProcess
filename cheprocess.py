#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""CheProcess, Chemical Engineering Process simulator cloned from 
Juan José Gómez Romera <jjgomera@gmail.com> repo pychemqt

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>."""


import argparse
from configparser import ConfigParser
import json
import logging
import os
import shutil
import sys
import urllib.error


# Parse command line options
desc = """CheProcess intended as a free software tool for calculation and \
design of chemical engineering unit operations."""
further = """For any suggestions, comments, bug ... you can contact me at \
https://github.com/ahmadalsaadi/CheProcess or by email al7akeeeem@gmail.com."""

parser = argparse.ArgumentParser(description=desc, epilog=further)
parser.add_argument("-l", "--log", dest="loglevel", default="INFO",
                    help="Set level of report in log file")
parser.add_argument("--debug", action="store_true",
                    help="Enable loglevel to debug, the more verbose option")
parser.add_argument("-n", "--nosplash", action="store_true",
                    help="Don't show the splash screen at start")
parser.add_argument("--style", help="Set qt style")
parser.add_argument("projectFile", nargs="*",
                    help="Optional CheProcess project files to load at startup")
args = parser.parse_args()


# Add CheProcess folder to python path
path = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(path)

# Define CheProcess environment
os.environ["CheProcess"] = path + os.sep
conf_dir = os.path.expanduser("~") + os.sep + ".CheProcess" + os.sep

# Check mandatory external dependences
# PyQt5
try:
    from PyQt5 import QtCore, QtGui, QtWidgets
except ImportError as err:
    print("PyQt5 could not be found, you must install it.")
    raise err

# Qt application definition
app = QtWidgets.QApplication(sys.argv)
app.setOrganizationName("CheProcess")
app.setOrganizationDomain("CheProcess")
app.setApplicationName("CheProcess")


# Qt style definition
if args.style is not None:
    style = QtWidgets.QStyleFactory.create(args.style)
    if style:
        app.setStyle(style)
    else:
        print("Undefined style option, the available options are: %s" %
              QtWidgets.QStyleFactory.keys())

# Add style options
app.setStyleSheet(
    "QDialogButtonBox {dialogbuttonbox-buttons-have-icons: true;}")


# Check qt configuration file
settings = QtCore.QSettings()
if not settings.contains("LastFile"):
    filename = QtCore.QVariant()
    settings.setValue("LastFile", filename)
    recentFiles = QtCore.QVariant()
    settings.setValue("RecentFiles", recentFiles)
    settings.setValue("Geometry", QtCore.QVariant())
    settings.setValue("MainWindow/State", QtCore.QVariant())


# Translation
locale = QtCore.QLocale.system().name()
myTranslator = QtCore.QTranslator()
if myTranslator.load("CheProcess_" + locale, os.environ["CheProcess"] + "i18n"):
    # Note:change spanish translation file name
    app.installTranslator(myTranslator)
qtTranslator = QtCore.QTranslator()
path = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)
if qtTranslator.load("qt_" + locale, path):
    app.installTranslator(qtTranslator)


# scipy
try:
    import scipy
except ImportError as err:
    msg = QtWidgets.QApplication.translate(
        "CheProcess", "scipy could not be found, you must install it.")
    print(msg)
    raise err
else:
    mayor, minor, corr = map(int, scipy.version.version.split("."))
    if mayor == 0 and minor < 14:
        msg = QtWidgets.QApplication.translate(
            "CheProcess",
            "Your version of scipy is too old, you must update it.")
        raise ImportError(msg)

# numpy
try:
    import numpy
except ImportError as err:
    msg = QtWidgets.QApplication.translate(
        "CheProcess", "numpy could not be found, you must install it.")
    print(msg)
    raise err
else:
    mayor, minor, corr = map(int, numpy.version.version.split("."))
    if mayor < 1 or minor < 8:
        msg = QtWidgets.QApplication.translate(
            "CheProcess",
            "Your version of numpy is too old, you must update it.")
        raise ImportError(msg)

# matplotlib
try:
    import matplotlib
except ImportError as err:
    msg = QtWidgets.QApplication.translate(
        "CheProcess", "matplotlib could not be found, you must install it.")
    print(msg)
    raise err
else:
    mayor, minor, corr = map(int, matplotlib.__version__.split("."))
    if mayor < 1 or (mayor == 1 and minor < 4):
        msg = QtWidgets.QApplication.translate(
            "CheProcess",
            "Your version of matplotlib is too old, you must update it.")
        raise ImportError(msg)

# iapws
# Externalized version of iapws, to avoid duple maintenance
try:
    import iapws  # noqa
except ImportError as err:
    msg = QtWidgets.QApplication.translate(
        "CheProcess", "iapws could not be found, you must install it.")
    print(msg)
    raise err
else:
    if iapws.__version__ != "1.4":
        msg = QtWidgets.QApplication.translate(
            "CheProcess",
            "Your version of iapws is too old, you must update it.")
        raise ImportError(msg)


# TODO: Disable python-graph external dependence, functional mock up in
# project yet useless
# python-graph
# try:
    # from pygraph.classes.graph import graph  # noqa
    # from pygraph.algorithms.cycles import find_cycle  # noqa
# except ImportError as err:
    # msg = QtWidgets.QApplication.translate(
    #     "pychemqt", "Python-graph don't found, you need install it")
    # print(msg)
    # raise err


# Check external optional modules
from tools.dependences import optional_modules  # noqa
for module, use in optional_modules:
    try:
        __import__(module)
        os.environ[module] = "True"
    except ImportError:
        print("%s could not be found, %s" % (module, use))
        os.environ[module] = ""
    else:
        # Check required version
        if module == "CoolProp":
            import CoolProp.CoolProp as CP
            version = CP.get_global_param_string("version")
            mayor, minor, rev = map(int, version.split("."))
            if mayor < 6:
                print("Find CoolProp %s but CoolProp 6 required" % version)
                os.environ[module] = ""


# Logging configuration
if args.debug:
    loglevel = "DEBUG"
else:
    loglevel = args.loglevel
loglevel = getattr(logging, loglevel.upper())

# Checking config folder
if not os.path.isdir(conf_dir):
    os.mkdir(conf_dir)

try:
    open(conf_dir + "CheProcess.log", 'x')
except FileExistsError:  # noqa
    pass

fmt = "[%(asctime)s.%(msecs)d] %(levelname)s: %(message)s"
logging.basicConfig(filename=conf_dir+"CheProcess.log", filemode="w",
                    level=loglevel, datefmt="%d-%b-%Y %H:%M:%S", format=fmt)
logging.info(
    QtWidgets.QApplication.translate("CheProcess", "Starting CheProcess"))


# Derive numpy error log to CheProcess log
class NumpyErrorLog(object):
    """Numpy error message catch and send to CheProcess log
    Use debug level for this messages"""
    @staticmethod
    def write(msg):
        logging.debug(msg)


from numpy import seterr, seterrcall  # noqa
seterrcall(NumpyErrorLog)
seterr(all='log')


class SplashScreen(QtWidgets.QSplashScreen):
    """Class to define a splash screen to show loading progress"""
    has_changed = False

    def __init__(self, splash_arg):
        QtWidgets.QSplashScreen.__init__(
            self,
            QtGui.QPixmap(os.environ["CheProcess"] + "/images/splash.jpg"))
        QtWidgets.QApplication.flush()
        if not splash_arg:
            self.show()
        self.file_config(conf_dir)
        self.cost_index(conf_dir)
        self.currency_rate(conf_dir)

    def showMessage(self, msg):
        """Procedure to update message in splash"""
        align = QtCore.Qt.Alignment(QtCore.Qt.AlignBottom |
                                    QtCore.Qt.AlignRight |
                                    QtCore.Qt.AlignAbsolute)
        color = QtGui.QColor(QtCore.Qt.white)
        QtWidgets.QSplashScreen.showMessage(self, msg, align, color)
        QtWidgets.QApplication.processEvents()

    def clearMessage(self):
        QtWidgets.QSplashScreen.clearMessage(self)
        QtWidgets.QApplication.processEvents()

    def file_config(self, path):
        self.showMessage(QtWidgets.QApplication.translate(
            "CheProcess", "Checking config files..."))
        # Checking config file
        default_Preferences = firstrun.Preferences()
        #self.has_changed = False
        if not os.path.isfile(path + "CheProcessrc"):
            default_Preferences.write(open(path + "CheProcessrc", "w"))
            Preferences = default_Preferences
            change = True
        else:
            # Check Preferences options to find set new options
            Preferences = ConfigParser()
            Preferences.read(path + "CheProcessrc")
            for section in default_Preferences.sections():
                if not Preferences.has_section(section):
                    Preferences.add_section(section)
                    self.has_changed = True
                for option in default_Preferences.options(section):
                    if not Preferences.has_option(section, option):
                        value = default_Preferences.get(section, option)
                        Preferences.set(section, option, value)
                        self.has_changed = True
                        logging.warning("Using default configuration option for " +
                                        "%s:%s" % (section, option) +
                                        ", run preferences dialog for configure")
            if self.has_changed:
                Preferences.write(open(path + "CheProcessrc", "w"))

    def cost_index(self, path):
        # Checking costindex
        self.showMessage(QtWidgets.QApplication.translate(
            "CheProcess", "Checking cost index..."))
        if not os.path.isfile(path + "CostIndex.dat"):
            orig = os.path.join(
                os.environ["CheProcess"], "dat", "costindex.dat")
            with open(orig) as cost_index:
                lista = cost_index.readlines()[-1].split(" ")
                with open(conf_dir + "CostIndex.dat", "w") as archivo:
                    for data in lista:
                        archivo.write(data.replace(
                            os.linesep, "") + os.linesep)

    def currency_rate(self, path):
        # Checking currency rates
        self.showMessage(QtWidgets.QApplication.translate(
            "CheProcess", "Checking currency data"))
        currency = False
        if not os.path.isfile(path + "moneda.dat"):
            # Exchange rates file don't available
            currency = True
        else:
            filename = path + "moneda.dat"
            try:
                archivo = open(filename, "r")
                rates = json.load(archivo)
            except urllib.error.URLError:
                # Failed to load json file
                currency = True

            if not isinstance(rates["date"], int):
                # Old version exchange rates format, force upgrade
                currency = True

        if currency:
            # Try to retrieve exchange rates from yahoo
            try:
                firstrun.getrates(path + "moneda.dat")
            except (urllib.error.URLError, urllib.error.HTTPError) as e:
                # Internet error, get hardcoded exchanges from pychemqt distribution
                # Possible outdated file, try to update each some commits
                origen = os.path.join(
                    os.environ["CheProcess"], "dat", "moneda.dat")
                shutil.copy(origen, path + "moneda.dat")
                print(QtWidgets.QApplication.translate("CheProcess",
                                                       "Internet connection error, using archived currency rates"))


""" if not args.nosplash:
    splash.show() """


# Checking config files
from tools import firstrun  # noqa
splash = SplashScreen(args.nosplash)
# splash.showMessage(QtWidgets.QApplication.translate(
#   "CheProcess", "Checking config files..."))
""" splash.file_config(conf_dir)
splash.cost_index(conf_dir)
splash.currency_rate(conf_dir) """
""" # Checking config file
default_Preferences = firstrun.Preferences()
change = False
if not os.path.isfile(conf_dir + "CheProcessrc"):
    default_Preferences.write(open(conf_dir + "CheProcessrc", "w"))
    Preferences = default_Preferences
    change = True
else:
    # Check Preferences options to find set new options
    Preferences = ConfigParser()
    Preferences.read(conf_dir + "CheProcessrc")
    for section in default_Preferences.sections():
        if not Preferences.has_section(section):
            Preferences.add_section(section)
            change = True
        for option in default_Preferences.options(section):
            if not Preferences.has_option(section, option):
                value = default_Preferences.get(section, option)
                Preferences.set(section, option, value)
                change = True
                logging.warning("Using default configuration option for " +
                                "%s:%s" % (section, option) +
                                ", run preferences dialog for configure")
    if change:
        Preferences.write(open(conf_dir + "CheProcessrc", "w")) """

# FIXME: This file might not to be useful but for now I use it to save project
# configuration data
if not os.path.isfile(conf_dir + "CheProcessrc_temporal"):
    Config = firstrun.config()
    Config.write(open(conf_dir + "CheProcessrc_temporal", "w"))

""" # Checking costindex
splash.showMessage(QtWidgets.QApplication.translate(
    "CheProcess", "Checking cost index..."))
if not os.path.isfile(conf_dir + "CostIndex.dat"):
    orig = os.path.join(os.environ["CheProcess"], "dat", "costindex.dat")
    with open(orig) as cost_index:
        lista = cost_index.readlines()[-1].split(" ")
        with open(conf_dir + "CostIndex.dat", "w") as archivo:
            for data in lista:
                archivo.write(data.replace(os.linesep, "") + os.linesep) """

""" # Checking currency rates
splash.showMessage(QtWidgets.QApplication.translate(
    "CheProcess", "Checking currency data"))
currency = False
if not os.path.isfile(conf_dir + "moneda.dat"):
    # Exchange rates file don't available
    currency = True
else:
    filename = conf_dir+"moneda.dat"
    try:
        archivo = open(filename, "r")
        rates = json.load(archivo)
    except urllib.error.URLError:
        # Failed to load json file
        currency = True

    if not isinstance(rates["date"], int):
        # Old version exchange rates format, force upgrade
        currency = True

if currency:
    # Try to retrieve exchange rates from yahoo
    try:
        firstrun.getrates(conf_dir + "moneda.dat")
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        # Internet error, get hardcoded exchanges from pychemqt distribution
        # Possible outdated file, try to update each some commits
        origen = os.path.join(os.environ["CheProcess"], "dat", "moneda.dat")
        shutil.copy(origen, conf_dir + "moneda.dat")
        print(QtWidgets.QApplication.translate("CheProcess",
                                               "Internet connection error, using archived currency rates"))
 """
# Checking database with custom components
splash.showMessage(QtWidgets.QApplication.translate(
    "CheProcess", "Checking custom database..."))
if not os.path.isfile(conf_dir + "databank.db"):
    firstrun.createDatabase(conf_dir + "databank.db")

# Import internal libraries
splash.showMessage(QtWidgets.QApplication.translate(
    "CheProcess", "Importing libraries..."))
from lib import *  # noqa
from UI import *  # noqa
from equipment import UI_equipments, equipments  # noqa
from tools import *  # noqa
from plots import *  # noqa

# Load main program UI
splash.showMessage(QtWidgets.QApplication.translate(
    "CheProcess", "Loading main window..."))
from UI.mainWindow import UI_pychemqt  # noqa
pychemqt = UI_pychemqt()

# Load project files, opened in last CheProcess session and/or specified in
# command line
msg = QtWidgets.QApplication.translate("CheProcess", "Loading project files")
splash.showMessage(msg + "...")
logging.info(msg)

if splash.has_changed:
    config.Preferences = Preferences

filename = []
if config.Preferences.getboolean("General", "Load_Last_Project"):
    filename = pychemqt.lastFile
    if filename is None:
        filename = []
for file in args.projectFile:
    filename.append(file)
for fname in filename:
    if fname and QtCore.QFile.exists(fname):
        msg = QtWidgets.QApplication.translate("CheProcess",
                                               "Loading project files...")
        splash.showMessage(msg + "\n" + fname)
        logging.info(msg + ": " + fname)
        pychemqt.fileOpen(fname)


# Manage error message to avoid print to console
def exceptfunction(error, msg, traceback):
    sys.__excepthook__(error, msg, traceback)


sys.excepthook = exceptfunction  # noqa

# Finish splash and start qt main loop
pychemqt.show()
splash.finish(pychemqt)
sys.exit(app.exec_())
