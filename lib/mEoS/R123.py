#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''Pychemqt, Chemical Engineering Process simulator
Copyright (C) 2009-2017, Juan José Gómez Romera <jjgomera@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''


from unittest import TestCase

from lib.meos import MEoS
from lib import unidades


class R123(MEoS):
    """Multiparameter equation of state for R123"""
    name = "2,2-dichloro-1,1,1-trifluoroethane"
    CASNumber = "306-83-2"
    formula = "CHCl2CF3"
    synonym = "R123"
    _refPropName = "R123"
    _coolPropName = "R123"
    rhoc = unidades.Density(550.)
    Tc = unidades.Temperature(456.831)
    Pc = unidades.Pressure(3661.8, "kPa")
    M = 152.93  # g/mol
    Tt = unidades.Temperature(166.0)
    Tb = unidades.Temperature(300.973)
    f_acent = 0.28192
    momentoDipolar = unidades.DipoleMoment(1.356, "Debye")
    id = 1631

    CP1 = {"ao": 17.01154/8.31451,
           "an": [0.4046308/8.31451, -4.644803e-4/8.31451,
                  2.347418e-7/8.31451],
           "pow": [1, 2, 3],
           "ao_exp": [], "exp": [],
           "ao_hyp": [], "hyp": []}

    Fi1 = {"ao_log": [1, 1.046009],
           "pow": [0, 1, -1, -2, -3],
           "ao_pow": [-13.23249393, 10.94800494, -11.1159955, 1.94308183,
                      -0.22430542],
           "ao_exp": [], "titao": [],
           "ao_hyp": [], "hyp": []}

    MBWR = {
        "__type__": "MBWR",
        "__name__": "MBWR equation of state for R-123 of Younglove and "
                    "McLinden (1994)",
        "__doi__": {"autor": "Younglove, B.A. and McLinden, M.O.",
                    "title": "An International Standard Equation of State for "
                             "the Thermodynamic Properties of Refrigerant 123 "
                             "(2,2-Dichloro-1,1,1-trifluoroethane)",
                    "ref": "J. Phys. Chem. Ref. Data, 23(5) (1994) 731-779",
                    "doi":  "10.1063/1.555950"},

        # TODO: The paper include heltmholtz expresion from MBWR equation

        "R": 8.31451,
        "cp": CP1,
        "ref": "IIR",

        "Tmin": Tt, "Tmax": 600.0, "Pmax": 40000.0, "rhomax": 11.60,
        "Pmin": 0.0042, "rhomin": 11.60,

        "b": [None, -0.657453133659e-2, 0.293479845842e1, -0.989140469845e2,
              0.201029776013e5, -0.383566527886e7, 0.227587641969e-2,
              -0.908726819450e1, 0.434181417995e4, 0.354116464954e7,
              -0.635394849670e-3, 0.320786715274e1, -0.131276484299e4,
              -0.116360713718, -0.113354409016e2, -0.537543457327e4,
              0.258112416120e1, -0.106148632128, 0.500026133667e2,
              -0.204326706346e1, -0.249438345685e7, -0.463962781113e9,
              -0.284903429588e6, 0.974392239902e10, -0.637314379308e4,
              0.314121189813e6, -0.145747968225e3, -0.843830261449e7,
              -0.241138441593e1, 0.108508031257e4, -0.106653193965e-1,
              -0.121343571084e2, -0.257510383240e3]}

    tillner = {
        "__type__": "Helmholtz",
        "__name__": "Helmholtz equation of state for R-123 of Baehr and "
                    "Tillner-Roth (1993)",
        "__doi__": {"autor": "Baehr, H.D., Tillner-Roth, R.",
                    "title": "Thermodynamic Properties of Environmentally "
                             "Acceptable Refrigerants: Equations of State and "
                             "Tables for Ammonia, R22, R134a, R152a, and R123",
                    "ref": "Springer-Verlag, Berlin, 1994.",
                    "doi": "10.1007/978-3-642-79400-1"},

        # This MEoS is a transformation of Youglove-McLinden MBWR equation
        "R": 8.31451,
        "cp": Fi1,
        "ref": "IIR",

        "Tmin": Tt, "Tmax": 600.0, "Pmax": 40000.0, "rhomax": 11.60,
        "Pmin": 0.0042, "rhomin": 11.60,

        "nr1": [-0.100242647494e2, -0.280607656419, 0.206814471606e-1,
                -0.284379431451, 0.593928110321e1, -0.936560389528e1,
                0.416660793675e1, -0.174023292951e1, 0.177019905365,
                -0.154721692260e1, 0.161820495590e1, 0.288903529383e1,
                -0.118493874757, 0.130952266209e1, -0.117308103711e1,
                -0.128125131950, -0.786087387513e-1, -0.816000499305e-1,
                0.536451054311e-1, -0.680078211929e-2, 0.701264082191e-2,
                -0.901762397311e-3],
        "d1": [0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 5, 5, 6, 7, 7,
               8],
        "t1": [3, 4, 5, 0, 0.5, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 1, 2, 3, 2, 2, 3,
               3],

        "nr2": [0.100242647494e2, 0.280607656419, -0.206814471606e-1,
                0.798923878145e1, -0.547972072476, -0.206814470584e-1,
                0.249142724365e1, -0.273986034884, 0.236001863614,
                0.540528251211, -0.600457561959e-1, 0.786672874826e-1,
                0.708085874508e-1, -0.150114389748e-1, 0.182205199477e-2,
                0.314978575163e-2, 0.784455573794e-2, 0.364410397155e-3],
        "d2": [0, 0, 0, 2, 2, 2, 4, 4, 4, 6, 6, 6, 8, 8, 8, 10, 10, 10],
        "t2": [3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5],
        "c2": [2]*18,
        "gamma2": [1]*18}

    shortSpan = {
        "__type__": "Helmholtz",
        "__name__": "short Helmholtz equation of state for R-123 of Span and "
                    "Wagner (2003)",
        "__doi__": {"autor": "Span, R., Wagner, W.",
                    "title": "Equations of State for Technical Applications. "
                             "III. Results for Polar Fluids",
                    "ref": "Int. J. Thermophys., 24(1) (2003) 111-162",
                    "doi": "10.1023/A:1022362231796"},

        "R": 8.31451,
        "cp": CP1,
        "ref": "NBP",
        "M": 152.931, "Tc": 456.82, "rhoc": 553/152.931,

        "Tmin": Tt, "Tmax": 600.0, "Pmax": 100000.0, "rhomax": 11.62,
        "Pmin": 0.0041534, "rhomin": 11.613,

        "nr1": [0.1116973e1, -0.3074593e1, 0.51063873, 0.94478812e-1,
                0.29532752e-3],
        "d1": [1, 1, 1, 3, 7],
        "t1": [0.25, 1.25, 1.5, 0.25, 0.875],

        "nr2": [0.66974438, 0.96438575, -0.14865424e-1, -0.49221959,
                -0.22831038e-1, -0.1407486, -0.25117301e-1],
        "d2": [1, 2, 5, 1, 1, 4, 2],
        "t2": [2.375, 2, 2.125, 3.5, 6.5, 4.75, 12.5],
        "c2": [1, 1, 1, 2, 2, 2, 3],
        "gamma2": [1]*7}

    # eq = MBWR, tillner, shortSpan
    eq = tillner, shortSpan

    _surface = {"sigma": [0.056151], "exp": [1.2367]}
    _vapor_Pressure = {
        "eq": 3,
        "n": [-0.74610e1, 0.20293e1, -0.21897e1, -0.34945e1],
        "t": [1.0, 1.5, 2.25, 4.5]}
    _liquid_Density = {
        "eq": 1,
        "n": [0.19996e1, 0.41823, 0.24849, 0.18831, 0.13737],
        "t": [0.345, 0.74, 1.2, 2.6, 7.2]}
    _vapor_Density = {
        "eq": 2,
        "n": [-3.0205, -7.4537, -21.88, -57.43, 11.239, -166.4],
        "t": [0.3905, 1.29, 3.4, 7.0, 12.0, 15.0]}

    visco0 = {"__name__": "Tanaka (1996)",
              "__doi__": {
                  "autor": "Tanaka, Y., Sotani, T.",
                  "title": "Thermal Conductivity and Viscosity of 2,2-"
                           "Dichioro-1,1,1-Trifluoroethane (HCFC-123)",
                  "ref": "Int. J. Thermophys. 17(2) (1996) 293-328",
                  "doi":  "10.1007/BF01443394"},

              "eq": 1, "omega": 0,

              "no": [-2.273638, 5.099859e-2, -2.402786e-5],
              "to": [0, 1, 2],

              "Tref_res": 1, "rhoref_res": 1,
              "nr": [-2.226486e-2, 5.550623e-5, -3.222951e5/1828.263,
                     -0.1009812, 6.161902e-5, -8.84048e-8],
              "tr": [0, -1, 0, 0, 0, 0],
              "dr": [1, 1, 0, 1, 2, 3],

              "nr_num": [-3.222951e5],
              "tr_num": [0],
              "dr_num": [0],
              "nr_den": [1, -1828.263],
              "tr_den": [0, 0],
              "dr_den": [1, 0]}

    _viscosity = visco0,

    thermo0 = {"eq": 1,
               "__name__": "Laesecke (1996)",
               "__doi__": {"autor": "Laesecke, A., Perkins, R.A., and Howley, J.B.",
                           "title": "An improved correlation for the thermal conductivity of HCFC123 (2,2-dichloro-1,1,1-trifluoroethane)",
                           "ref": "Int. J. Refrigeration, 19:231-238, 1996",
                           "doi":  "10.1016/0140-7007(96)00019-9"},
               "__test__": """
                   >>> st=R123(T=180, x=0.5, eq=2)
                   >>> print "%0.0f %0.4g %0.5g %0.4g %0.4g %0.4g" % (st.T, st.P.MPa,\
                    st.Liquido.rho, st.Gas.rho, st.Liquido.k.mWmK, st.Gas.k.mWmK)
                   180 0.00002812 1739.0 0.002873 110.9 1.473
                   >>> st=R123(T=200, x=0.5, eq=2)
                   >>> print "%0.0f %0.4g %0.5g %0.4g %0.4g %0.4g" % (st.T, st.P.MPa,\
                    st.Liquido.rho, st.Gas.rho, st.Liquido.k.mWmK, st.Gas.k.mWmK)
                   200 0.0002494 1694.4 0.02295 105.6 3.610
                   >>> st=R123(T=250, x=0.5, eq=2)
                   >>> print "%0.0f %0.4g %0.5g %0.4g %0.4g %0.4g" % (st.T, st.P.MPa,\
                    st.Liquido.rho, st.Gas.rho, st.Liquido.k.mWmK, st.Gas.k.mWmK)
                   250 0.01007 1581.1 0.7467 90.84 6.437
                   >>> st=R123(T=300, x=0.5, eq=2)
                   >>> print "%0.0f %0.4g %0.5g %0.4g %0.4g %0.4g" % (st.T, st.P.MPa,\
                    st.Liquido.rho, st.Gas.rho, st.Liquido.k.mWmK, st.Gas.k.mWmK)
                   300 0.09778 1458.2 6.258 75.91 9.293
                   >>> st=R123(T=350, x=0.5, eq=2)
                   >>> print "%0.0f %0.4g %0.5g %0.4g %0.4g %0.4g" % (st.T, st.P.MPa,\
                    st.Liquido.rho, st.Gas.rho, st.Liquido.k.mWmK, st.Gas.k.mWmK)
                   350 0.4514 1320.8 26.97 63.34 12.50
                   >>> st=R123(T=400, x=0.5, eq=2)
                   >>> print "%0.0f %0.4g %0.5g %0.4g %0.4g %0.4g" % (st.T, st.P.MPa,\
                    st.Liquido.rho, st.Gas.rho, st.Liquido.k.mWmK, st.Gas.k.mWmK)
                   400 1.372 1146.9 85.31 52.41 16.87
                   >>> st=R123(T=440, x=0.5, eq=1)
                   >>> print "%0.0f %0.4g %0.5g %0.4g %0.4g %0.4g" % (st.T, st.P.MPa,\
                    st.Liquido.rho, st.Gas.rho, st.Liquido.k.mWmK, st.Gas.k.mWmK)
                   440 2.790 924.64 215.3 43.11 23.18
                   """, # Table 2, Pag 237

               "Tref": 1., "kref": 1,
               "no": [-0.00778, 5.695e-5],
               "co": [0, 1],

               "Trefb": 456.831, "rhorefb": 3.596417, "krefb": 1,
               "nb": [0.642894e-1, -0.530474e-1, 0.453522e-4, -0.139928,
                      0.16654, -0.162656e-1, 0.136819, -0.183291, 0.357146e-1,
                      -0.231210e-1, 0.341945e-1, -0.757341e-2],
               "tb": [-1.5, -2, -6, 0, -0.5, -1.5, 0, -0.5, -1.5, 0, -0.5, -1.5],
               "db": [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4],
               "cb": [0]*12,

               "critical": 1,
               "crit_num_Tref": -456.831, "crit_num_rhoref": 3.596417,
               "crit_num_k": 1.,
               "crit_num_n": [0.486742e-2],
               "crit_num_alfa": [0],
               "crit_num_t": [0],
               "crit_num_beta": [0],
               "crit_num_d": [0],
               "crit_num_c": [0],
               "crit_den_n": [-100.0, -7.08535],
               "crit_den_alfa": [-1, 0],
               "crit_den_t": [4, 0],
               "crit_den_beta": [0, -1],
               "crit_den_d": [0, 2],
               "crit_den_c": [0, 0]}

    _thermal = thermo0,

# TODO: Add thermal conductivity correlation from Tanaka


class Test(TestCase):

    # def test_younglove(self):
        # # Selected point from Table C1 pag 759, saturation states
        # st = R123(T=R123.Tt, x=0.5, eq=1)
        # self.assertEqual(round(st.P.MPa, 5), 0)
        # self.assertEqual(round(st.Liquido.rho, 1), 1770.9)
        # self.assertEqual(round(st.Liquido.h.kJkg, 2), 98.81)
        # self.assertEqual(round(st.Liquido.s.kJkgK, 4), 0.5311)
        # self.assertEqual(round(st.Liquido.cv.kJkgK, 3), 0.630)
        # self.assertEqual(round(st.Liquido.cp.kJkgK, 3), 0.929)
        # self.assertEqual(round(st.Liquido.w, 1), 1243.8)
        # self.assertEqual(round(st.Gas.rho, 4), 0.0005)
        # self.assertEqual(round(st.Gas.h.kJkg, 2), 322.50)
        # self.assertEqual(round(st.Gas.s.kJkgK, 4), 1.8786)
        # self.assertEqual(round(st.Gas.cv.kJkgK, 3), 0.419)
        # self.assertEqual(round(st.Gas.cp.kJkgK, 3), 0.474)
        # self.assertEqual(round(st.Gas.w, 1), 101.0)

        # st = R123(T=+273.15, x=0.5)
        # self.assertEqual(round(st.P.MPa, 6), 0)
        # self.assertEqual(round(st.Liquido.rho, 1), )
        # self.assertEqual(round(st.Liquido.h.kJkg, 2), )
        # self.assertEqual(round(st.Liquido.s.kJkgK, 4), )
        # self.assertEqual(round(st.Liquido.cv.kJkgK, 3), )
        # self.assertEqual(round(st.Liquido.cp.kJkgK, 3), )
        # self.assertEqual(round(st.Liquido.w, 1), )
        # self.assertEqual(round(st.Gas.rho, 1), )
        # self.assertEqual(round(st.Gas.h.kJkg, 2), )
        # self.assertEqual(round(st.Gas.s.kJkgK, 4), )
        # self.assertEqual(round(st.Gas.cv.kJkgK, 3), )
        # self.assertEqual(round(st.Gas.cp.kJkgK, 3), )
        # self.assertEqual(round(st.Gas.w, 1), )

    def test_tillner(self):
        # Selected point from pag 166, saturation state
        st = R123(T=-55+273.15, x=0.5, eq="tillner")
        self.assertEqual(round(st.P.MPa, 5), 0.00121)
        self.assertEqual(round(st.Liquido.rho, 1), 1653.9)
        self.assertEqual(round(st.Gas.rho, 4), 0.1020)
        self.assertEqual(round(st.Liquido.h.kJkg, 2), 147.12)
        self.assertEqual(round(st.Hvap.kJkg, 2), 202.30)
        self.assertEqual(round(st.Gas.h.kJkg, 2), 349.42)
        self.assertEqual(round(st.Liquido.s.kJkgK, 4), 0.7842)
        self.assertEqual(round(st.Svap.kJkgK, 4), 0.9273)
        self.assertEqual(round(st.Gas.s.kJkgK, 4), 1.7115)

        st = R123(T=273.15, x=0.5, eq="tillner")
        self.assertEqual(round(st.P.MPa, 5), 0.03265)
        self.assertEqual(round(st.Liquido.rho, 1), 1526.1)
        self.assertEqual(round(st.Gas.rho, 4), 2.2417)
        self.assertEqual(round(st.Liquido.h.kJkg, 2), 200.00)
        self.assertEqual(round(st.Hvap.kJkg, 2), 181.44)
        self.assertEqual(round(st.Gas.h.kJkg, 2), 381.44)
        self.assertEqual(round(st.Liquido.s.kJkgK, 4), 1.0000)
        self.assertEqual(round(st.Svap.kJkgK, 4), 0.6642)
        self.assertEqual(round(st.Gas.s.kJkgK, 4), 1.6642)

        st = R123(T=50+273.15, x=0.5, eq="tillner")
        self.assertEqual(round(st.P.MPa, 5), 0.21246)
        self.assertEqual(round(st.Liquido.rho, 1), 1397.8)
        self.assertEqual(round(st.Gas.rho, 3), 13.031)
        self.assertEqual(round(st.Liquido.h.kJkg, 2), 251.06)
        self.assertEqual(round(st.Hvap.kJkg, 2), 160.44)
        self.assertEqual(round(st.Gas.h.kJkg, 2), 411.50)
        self.assertEqual(round(st.Liquido.s.kJkgK, 4), 1.1711)
        self.assertEqual(round(st.Svap.kJkgK, 4), 0.4965)
        self.assertEqual(round(st.Gas.s.kJkgK, 4), 1.6676)

        st = R123(T=100+273.15, x=0.5, eq="tillner")
        self.assertEqual(round(st.P.MPa, 5), 0.78553)
        self.assertEqual(round(st.Liquido.rho, 1), 1246.9)
        self.assertEqual(round(st.Gas.rho, 3), 46.996)
        self.assertEqual(round(st.Liquido.h.kJkg, 2), 305.76)
        self.assertEqual(round(st.Hvap.kJkg, 2), 134.01)
        self.assertEqual(round(st.Gas.h.kJkg, 2), 439.77)
        self.assertEqual(round(st.Liquido.s.kJkgK, 4), 1.3271)
        self.assertEqual(round(st.Svap.kJkgK, 4), 0.3591)
        self.assertEqual(round(st.Gas.s.kJkgK, 4), 1.6862)

        st = R123(T=150+273.15, x=0.5, eq="tillner")
        self.assertEqual(round(st.P.MPa, 5), 2.09868)
        self.assertEqual(round(st.Liquido.rho, 1), 1036.8)
        self.assertEqual(round(st.Gas.rho, 2), 142.23)
        self.assertEqual(round(st.Liquido.h.kJkg, 2), 367.10)
        self.assertEqual(round(st.Hvap.kJkg, 2), 93.95)
        self.assertEqual(round(st.Gas.h.kJkg, 2), 461.05)
        self.assertEqual(round(st.Liquido.s.kJkgK, 4), 1.4782)
        self.assertEqual(round(st.Svap.kJkgK, 4), 0.2220)
        self.assertEqual(round(st.Gas.s.kJkgK, 4), 1.7003)

        st = R123(T=180+273.15, x=0.5, eq="tillner")
        self.assertEqual(round(st.P.MPa, 5), 3.45057)
        self.assertEqual(round(st.Liquido.rho, 2), 765.91)
        self.assertEqual(round(st.Gas.rho, 2), 341.95)
        self.assertEqual(round(st.Liquido.h.kJkg, 2), 416.22)
        self.assertEqual(round(st.Hvap.kJkg, 2), 40.60)
        self.assertEqual(round(st.Gas.h.kJkg, 2), 456.82)
        self.assertEqual(round(st.Liquido.s.kJkgK, 4), 1.5867)
        self.assertEqual(round(st.Svap.kJkgK, 4), 0.0896)
        self.assertEqual(round(st.Gas.s.kJkgK, 4), 1.6763)

        st = R123(T=183+273.15, x=0.5, eq="tillner")
        self.assertEqual(round(st.P.MPa, 5), 3.62135)
        self.assertEqual(round(st.Liquido.rho, 2), 665.76)
        self.assertEqual(round(st.Gas.rho, 2), 433.97)
        self.assertEqual(round(st.Liquido.h.kJkg, 2), 426.94)
        self.assertEqual(round(st.Hvap.kJkg, 2), 21.52)
        self.assertEqual(round(st.Gas.h.kJkg, 2), 448.46)
        self.assertEqual(round(st.Liquido.s.kJkgK, 4), 1.6097)
        self.assertEqual(round(st.Svap.kJkgK, 4), 0.0472)
        self.assertEqual(round(st.Gas.s.kJkgK, 4), 1.6569)

        st = R123(P=1e3, x=0.5, eq="tillner")
        self.assertEqual(round(st.T.C, 2), -57.38)
        self.assertEqual(round(st.Liquido.rho, 1), 1659.2)
        self.assertEqual(round(st.Gas.rho, 4), 0.0854)
        self.assertEqual(round(st.Liquido.h.kJkg, 2), 144.90)
        self.assertEqual(round(st.Hvap.kJkg, 2), 203.20)
        self.assertEqual(round(st.Gas.h.kJkg, 2), 348.10)
        self.assertEqual(round(st.Liquido.s.kJkgK, 4), 0.7739)
        self.assertEqual(round(st.Svap.kJkgK, 4), 0.9418)
        self.assertEqual(round(st.Gas.s.kJkgK, 4), 1.7157)

        st = R123(P=1e4, x=0.5, eq="tillner")
        self.assertEqual(round(st.T.C, 2), -23.27)
        self.assertEqual(round(st.Liquido.rho, 1), 1581.4)
        self.assertEqual(round(st.Gas.rho, 4), 0.7422)
        self.assertEqual(round(st.Liquido.h.kJkg, 2), 177.25)
        self.assertEqual(round(st.Hvap.kJkg, 2), 190.34)
        self.assertEqual(round(st.Gas.h.kJkg, 2), 367.59)
        self.assertEqual(round(st.Liquido.s.kJkgK, 4), 0.9130)
        self.assertEqual(round(st.Svap.kJkgK, 4), 0.7617)
        self.assertEqual(round(st.Gas.s.kJkgK, 4), 1.6747)

        st = R123(P=1e5, x=0.5, eq="tillner")
        self.assertEqual(round(st.T.C, 2), 27.46)
        self.assertEqual(round(st.Liquido.rho, 1), 1457.6)
        self.assertEqual(round(st.Gas.rho, 4), 6.3918)
        self.assertEqual(round(st.Liquido.h.kJkg, 2), 227.65)
        self.assertEqual(round(st.Hvap.kJkg, 2), 170.34)
        self.assertEqual(round(st.Gas.h.kJkg, 2), 398.00)
        self.assertEqual(round(st.Liquido.s.kJkgK, 4), 1.0963)
        self.assertEqual(round(st.Svap.kJkgK, 4), 0.5667)
        self.assertEqual(round(st.Gas.s.kJkgK, 4), 1.6629)

        st = R123(P=1e6, x=0.5, eq="tillner")
        self.assertEqual(round(st.T.C, 2), 111.15)
        self.assertEqual(round(st.Liquido.rho, 1), 1207.7)
        self.assertEqual(round(st.Gas.rho, 4), 60.445)
        self.assertEqual(round(st.Liquido.h.kJkg, 2), 318.66)
        self.assertEqual(round(st.Hvap.kJkg, 2), 126.78)
        self.assertEqual(round(st.Gas.h.kJkg, 2), 445.45)
        self.assertEqual(round(st.Liquido.s.kJkgK, 4), 1.3607)
        self.assertEqual(round(st.Svap.kJkgK, 4), 0.3299)
        self.assertEqual(round(st.Gas.s.kJkgK, 4), 1.6906)

        # Selected point from Pag 174, single region states
        st = R123(T=273.15, P=1e4, eq="tillner")
        self.assertEqual(round(st.rho, 4), 0.6773)
        self.assertEqual(round(st.h.kJkg, 2), 382.19)
        self.assertEqual(round(st.s.kJkgK, 4), 1.7306)

        st = R123(T=175+273.15, P=2e4, eq="tillner")
        self.assertEqual(round(st.rho, 4), 0.8225)
        self.assertEqual(round(st.h.kJkg, 2), 511.64)
        self.assertEqual(round(st.s.kJkgK, 4), 2.0555)

        st = R123(T=-5+273.15, P=3e4, eq="tillner")
        self.assertEqual(round(st.rho, 1), 1538.2)
        self.assertEqual(round(st.h.kJkg, 2), 195.06)
        self.assertEqual(round(st.s.kJkgK, 4), 0.9818)

        st = R123(T=10+273.15, P=5e4, eq="tillner")
        self.assertEqual(round(st.rho, 4), 3.3352)
        self.assertEqual(round(st.h.kJkg, 2), 387.47)
        self.assertEqual(round(st.s.kJkgK, 4), 1.6633)

        st = R123(T=100+273.15, P=1e5, eq="tillner")
        self.assertEqual(round(st.rho, 4), 5.0265)
        self.assertEqual(round(st.h.kJkg, 2), 451.10)
        self.assertEqual(round(st.s.kJkgK, 4), 1.8209)

        st = R123(T=45+273.15, P=2e5, eq="tillner")
        self.assertEqual(round(st.rho, 1), 1411.4)
        self.assertEqual(round(st.h.kJkg, 2), 245.81)
        self.assertEqual(round(st.s.kJkgK, 4), 1.1548)

        st = R123(T=-25+273.15, P=3e5, eq="tillner")
        self.assertEqual(round(st.rho, 1), 1585.9)
        self.assertEqual(round(st.h.kJkg, 2), 175.70)
        self.assertEqual(round(st.s.kJkgK, 4), 0.9061)

        st = R123(T=80+273.15, P=5e5, eq="tillner")
        self.assertEqual(round(st.rho, 1), 1311.3)
        self.assertEqual(round(st.h.kJkg, 2), 283.35)
        self.assertEqual(round(st.s.kJkgK, 4), 1.2660)

        st = R123(T=120+273.15, P=1e6, eq="tillner")
        self.assertEqual(round(st.rho, 3), 57.583)
        self.assertEqual(round(st.h.kJkg, 2), 453.52)
        self.assertEqual(round(st.s.kJkgK, 4), 1.7114)

        st = R123(T=200+273.15, P=2e6, eq="tillner")
        self.assertEqual(round(st.rho, 3), 95.885)
        self.assertEqual(round(st.h.kJkg, 2), 514.78)
        self.assertEqual(round(st.s.kJkgK, 4), 1.8225)

    def test_shortSpan(self):
        # Table III, Pag 117
        st = R123(T=500, rho=500, eq="shortSpan")
        self.assertEqual(round(st.cp0.kJkgK, 4), 0.8667)
        self.assertEqual(round(st.P.MPa, 3), 6.018)
        self.assertEqual(round(st.cp.kJkgK, 4), 1.9509)

        st2 = R123(T=600, rho=100, eq="shortSpan")
        self.assertEqual(round(st2.h.kJkg-st.h.kJkg, 2), 144.33)
        self.assertEqual(round(st2.s.kJkgK-st.s.kJkgK, 5), 0.29582)

    def test_tanaka(self):
        # Table VII, Pag 316
        # TODO: The paper use the Younglove equation so add when fix MBWR
        pass

        # st = R123(T=260, x=0.5, eq="shortSpan")
        # self.assertEqual(round(st.P.MPa, 3), 0.017)
        # self.assertEqual(round(st.Liquido.rho, 1), 1557.7)
        # self.assertEqual(round(st.Gas.rho, 3), 1.286)
        # self.assertEqual(round(st.Liquido.k.mWmK, 2), 87.42)
        # self.assertEqual(round(st.Gas.k.mWmK, 2), 8.405)
        # self.assertEqual(round(st.Liquido.mu.muPas, 1), 670.0)
        # self.assertEqual(round(st.Gas.mu.muPas, 2), 9.346)

        # st = R123(T=260, x=0.5, eq="MBWR")
        # self.assertEqual(round(st.P.MPa, 3), )
        # self.assertEqual(round(st.Liquido.rho, 1), )
        # self.assertEqual(round(st.Gas.rho, 3), )
        # self.assertEqual(round(st.Liquido.k.mWmK, 2), )
        # self.assertEqual(round(st.Gas.k.mWmK, 2), )
        # self.assertEqual(round(st.Liquido.mu.muPas, 1), )
        # self.assertEqual(round(st.Gas.mu.muPas, 2), )

        # Table IX, Pag 320
        # """
        # >>> st=R123(T=260, P=1e5, eq=2)
        # >>> print "%0.4g" % st.mu.muPas
        # 670.6
        # >>> st=R123(T=280, P=1e6, eq=2)
        # >>> print "%0.4g" % st.mu.muPas
        # 524.5
        # >>> st=R123(T=300, P=2e6, eq=2)
        # >>> print "%0.4g" % st.mu.muPas
        # 419.3
        # >>> st=R123(T=320, P=1e5, eq=2)
        # >>> print "%0.4g" % st.mu.muPas
        # 11.54
        # >>> st=R123(T=360, P=5e5, eq=2)
        # >>> print "%0.4g" % st.mu.muPas
        # 12.87
        # >>> st=R123(T=420, P=1.5e6, eq=2)
        # >>> print "%0.4g" % st.mu.muPas
        # 15.40
        # >>> st=R123(T=400, P=6e6, eq=2)
        # >>> print "%0.4g" % st.mu.muPas
        # 165.0
        # >>> st=R123(T=300, P=5e6, eq=2)
        # >>> print "%0.4g" % st.mu.muPas
        # 435.9
        # >>> st=R123(T=260, P=1e7, eq=2)
        # >>> print "%0.4g" % st.mu.muPas
        # 747.7
        # >>> st=R123(T=420, P=2e7, eq=2)
        # >>> print "%0.4g" % st.mu.muPas
        # 188.7
        # >>> st=R123(T=300, P=1.5e7, eq=2)
        # >>> print "%0.4g" % st.mu.muPas
        # 491.8
        # """,
