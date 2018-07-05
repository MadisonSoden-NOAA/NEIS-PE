#!/Users/soden/ python

"""mcb0_7 Ecoforecast prototype goal is to implement rules base from http://ecoforecast.coral.noaa.gov/index/0/MLRF1/model-detail&name=MASS-CORAL-BLEACHING and 'print' a forecast"""

from pyknow import *
import numpy as np

__author__ = "Madison Soden"
__date__ = "Thu Dec 28 13:04:31 2017"
__license__ = "NA?"
__version__ = "mcb0_7"
__email__ = "madison.soden@gmail.com"
__status__ = "Production"

"""Fact Definition Documentation""" #rRange is a string containing a fuzzy (i.e. proxy) values for sst #key = 'rRange' / 0
    #fuzzy values can be 'uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh',
    # 'High', 'vHigh', 'dHigh', 'uHigh'
    #tod is a string indicating a fuzzy time of day values for the-
    # time rRange was recorded. Taken in eight 3 hour, then four 6 hour, then
    # two 12 hour , and one 24 hour time increments
    #key = 'tod' and/or 1
    #fuzzy values can be 
    # 'evening' - 'even' - 0000 to 0300
    # 'midnight' - 'midn' - 0300 to 0600
    # 'pre-dawn' - 'pdaw' - 0600 to 0900
    # 'dawn' - 'dawn' - 0900 to 1200
    # 'morning' - 'morn' - 1200 to 1500
    # 'mid-day' - 'midd' - 1500 to 1800
    # 'pre-sunset' - 'psun' - 2100 to 2400
    # 'sunset' - 'suns' - 2100 to 2400
    # 
    # 'night-hours' - 'nite' - 0000 to 0900
    # 'dawn-morning' - 'dayb' - 0900 to 1500
    # 'afternoon' - 'aftn' - 1800 to 2400
    # 'daylight-hours' - 'dayl' - 0900 to 2400
    # 'all-day' - 'all' - 0300 to 0300
    
    #date is a string containing the date that rRange was calculated on in DDMMYYYY
    #key = 'dateR' and/or 4

"""Fact declarations"""
class parsurf(Fact):
    #photosynthetically active radiation at ocean surface
    pass

class sst(Fact):
    #Remss 'misst' Blended Microwave/infrared sst (surface sea temperature)
    pass

class windsp(Fact):
    #hourly average wind speed
    pass

class tide1m(Fact):
    #tide level at ~1m depth
    pass

class seandbc(Fact):
    #depth-averaged sea temperature
    pass

class sea1m(Fact):
    #sea temperature at ~1m depth
    pass

class curveB(Fact):
    #Berkelmans Temperature-Duration Bleaching Curve
    pass

class sea1mM(Fact):
    #Monthly mean sea temperature at ~1m depth
    pass

class seandbcM(Fact):
    #Monthly Mean Depth-Averaged Sea Temperature
    pass

class windsp3day(Fact):
    #3-day average wind speed
    pass

class MCB(KnowledgeEngine):
#Mass Coral Bleaching Forecast
#initial instruction output
    print("""\n
        ----------------------------------------------------------------------
        To declare Knowledge Engine:
        >> e = mcb0_7.MCB()
        >> e.reset()
        \n
        To add facts to fact list call:
        >> e.declare_facts()
        \n
        To view current rule base call:
        >> e.get_rules()
        \n
        To view current fact base call:
        >> e.facts
        \n
        To run Knowledge Engine call:
        >> e.run()
        ----------------------------------------------------------------------
        \n \n \n""")

#test functions to initialize specific combinations of facts
    def declare_facts(self):
        done='n'
        while(done=='n'):
            print("""Which fact would you like to declare?('windsp3day', 'seandbcM', 'sea1mM', 'curveB', 'sea1m', 'seandbc', 'tide1m', 'windsp', 'sst', or 'parsurf').""")
            x = input('  ')
            print("""What is the rRange?('uLow', 'dLow', 'vLow', 'Low', 'sLow','average', 'sHigh', 'High', 'vHigh', 'dHigh', or 'uHigh').""")
            y = input('  ')
            print("""What is the tod?( 'even'(0000-0300), 'midn'(0300-0600), 'pdaw'(0600-0900), 'dawn'(0900-1200), 'morn'(1200-1500), 'midd'(1500-1800), 'psun'(2100-2400), 'suns'(2100-2400), 'nite'(0000-0900), 'dayb'(0900-1500), 'aftn'(1800-2400), 'dayl'(0900-2400), 'all'(0300-0300).""")
            z = input('  ')
            exec("self.declare(%s(rRange=y, tod=z))" % (x))
            print("""Are you finished declaring facts? (y/n)""")
            done = input('  ')

#Rule production & alert printing

#example/reference rules
#@Rule(sst(rRange='dLow'))
#    def sst0(self):
#        print("sst is drastically Low")
#
#    @Rule(sst(rRange='High'), salience=1)
#    def sst6(self):
#        print("sst is high")
#
#    @Rule(sst(rRange='High'), windsp(rRange='Low'))
#    def c1(self):
#        print(" Coral bleaching is likely")

#other cases
    @Rule(OR(sst(rRange='uLow'), sst(rRange='uHigh')))
    def u1(self):
        print("sst values in unbelievable range")

    @Rule(OR(windsp(rRange='uLow'), windsp(rRange='uHigh')))
    def u2(self):
        print("wind scalar values in unbelievable range")

    @Rule(NOT(sst(rRange= L('uLow') | L('dLow') | L('vLow') | L('Low') | L('sLow') |
        L('average') | L('sHigh') | L('High') | L('vHigh') | L('dHigh') |
        ('uHigh'))))
    def m1(self):
        print("missing or unreadable value for sst rRange")

    @Rule(NOT(windsp(rRange= L('uLow') | L('dLow') | L('vLow') | L('Low') | L('sLow') |
        L('average') | L('sHigh') | L('High') | L('vHigh') | L('dHigh') |
        L('uHigh'))))
    def m2(self):
        print("missing or unreadable value for windsp rRange")

#MCB MASS-CORAL-BLEACHING implementation
#Description: Mass bleaching of hard corals
#forecast has 24 distinct rules

#Ecoforecast Rule #1: Coral-Bleaching-Itlwt
#Description: Mass coral bleaching (high in-situ sea temperature + high light + low wind + low tide)
    @Rule(parsurf(rRange=L('High') | L('vHigh') | L('dHigh')),
            parsurf(tod=L('midd') | L('psun') | L('dayl') | L('aftn') | L('all')),
            tide1m(rRange=L('dLow') | L('vLow') | L('Low')),
            tide1m(tod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            windsp(rRange=L('dLow') | L('vLow') | L('Low')),
            windsp(tod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all'),
            seandbc(rRange=L('High') | L('vHigh') | L('dHigh')),
            seandbc(tod=W()))
    def mcb1(self):
        print("Coral-Bleaching-Itlwt fired")

#Ecoforecast Rule #2: Coral-Bleaching-Stlwt
#Description: Mass coral bleaching (high 'shallow' sea temperature + high light + low wind + low tide)
    @Rule(parsurf(rRange=L('High') | L('vHigh') | L('dHigh')), 
            parsurf(tod=L('midd') | L('dayl') | L('all')),
            tide1m(rRange=L('dLow') | L('vLow') | L('Low')),
            tide1m(tod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            windsp(rRange=L('dLow') | L('vLow') | L('Low')),
            windsp(tod=L('morn') | L('midd') | L ('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            sea1m(rRange=L('High') | L('vHigh') | L('dHigh')),
            sea1m(tod=W()))
    def mcb2(self):
        print("Coral-Bleaching-Stlwt fired")

#Ecoforecast Rule #3: Coral-Bleaching-Tlwt
#Description: Mass coral bleaching (high SST + high light + low wind + low tide)
    @Rule(parsurf(rRange=L('High') | L('vHigh') | L('dHigh'),
            parsurf(tod=L('midd') | L('dayl') | L('all')),
            tide1m(rRange=L('dLow') | L('vLow') | L('Low')),
            tide1m(tod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            windsp(rRange=L('dLow') | L('vLow') | L('Low')),
            windsp(tod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('aftn') | L('all')),
            sst(rRange=L('High') | L('vHigh') | L('dHigh')),
            sst(tod=W()))
    def mcb3(self):
        print("Coral-Bleaching-Tlwt fired")

#Ecoforecast Rule #4: Coral-Bleaching-Itlw
# Description: Mass coral bleaching (high in-situ sea temperature + high light + low wind)
    @Rule(parsurf(rRange=L('High') | L('vHigh') | L('dHigh'),
            parsurf(tod=L('midd') | L('psun') | L('dayl') | L('aftn') |
                L('all')),
            windsp(rRange=L('dLow') | L('vLow') | L('Low')),
            windsp(tod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            seandbc(rRange=L('High') | L('vHigh') | L('dHigh')),
            seandbc(tod=W()))
    def mcb4(self):
        print("Coral-Bleaching-Itlw fired")

#Ecoforecast Rule #5: Coral-Bleaching-Itwt
#Description: Mass coral bleaching (high in-situ sea temperature + low wind + low tide)
    @Rule(tide1m(rRange=L('dLow') | L('vLow') | L('low')),
            tide1m(tod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            windsp(rRange=L('dLow') | L('vLow') | L('Low')),
            windsp(tod=L('morn') | L('midd') | L('psun') | L('day') | L('dayb')
                | L('aftn') | L('all')),
            seandbc(rRange=L('High') | L('vHigh') | L('dHigh')),
            seandbc(tod=W()))
    def mcb5(self):
        print("Coral-Bleaching-Itwt")

#Ecoforecast Rule #6: Coral-Bleaching-Stlw
#Description: Mass coral bleaching (high 'shallow' sea temperature + high light + low wind)
    @Rule(parsurf(rRange=L('High') | L('vHigh') | L('dHigh')),
            parsurf(tod=L('midd') | L('dayl') | L('all'))
            windsp(rRange=L('dLow') | L('vLow') | L('Low')),
            windsp(tod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            sea1m(rRange=L('High') | L('vHigh') | L('dHigh')),
            sea1m(tod=W()))
    def mcb6(self):
        print("Coral-Bleaching-Stlw fired")

#Ecoforecast Rule #7: Coral-Bleaching-Stwt
#Description: Mass coral bleaching (high 'shallow' sea temperature + low wind + low tide)
    @Rule(tide1m(rRange=L('dLow') | L('vLow') | L('Low')),
            tide1m(tod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            windsp(rRange=L('dLow') | L('vLow') | L('Low')),
            windsp(tod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            sea1m(rRange=L('High') | L('vHigh') | L('dHigh')),
            sea1m(tod=W()))
    def mcb7(self):
        print("Coral-Bleaching-Stwt fired")


#Ecoforecast Rule #8: Coral-Bleaching-Tlw
#Description: Mass coral bleaching (high SST + high light + low wind)
    @Rule(parsurf(rRange=L('High') | L('vHigh') | L('dHigh')),
            parsurf(tod=L('midd') | L('dayl') | L('all')),
            windsp(rRange=L('dLow') | L('vLow') | L('Low')),
            windsp(rRange=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            sst(rRange=L('High') | L('vHigh') | L('dHigh')),
            sst(tod=W()))
    def mcb8(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #9: Coral-Bleaching-Twt
# Description: Mass coral bleaching (high SST + low wind + low tide)
    @Rule(tide1m(rRange=L('dLow') | L('vLow') | L('Low')),
            tide1m(tod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            windsp(rRange=L('dLow') | L('vLow') | L('Low')),
            windsp(tod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            sst(rRange=L('High') | L('vHigh') | L('dHigh')),
            sst(tod=W()))
    def mcb9(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #10: Coral-Bleaching-Itd
#Description: Mass coral bleaching (high in-situ sea temperature + doldrums)
    @Rule(windsp3day(rRange=L('dLow') | L('vLow') | L('Low')),
            windsp3day(tod=W()),
            seandbc(rRange=L('High') | L('vHigh') | L('dHigh')),
            seandbc(tod=W()))
    def mcb10(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #11: Coral-Bleaching-Itl
#Description: Mass coral bleaching (very high in-situ sea temperature + very high light)
    @Rule(parsurf(rRange=L('vHigh') | L('dHigh')),
            parsurf(tod=L('midd') | L('psun') | L('dayl') | L('aftn') |
                L('all')),
            seandbc(rRange=L('vHigh') | L('dHigh')),
            seandbc(tod=W()))
    def mcb11(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #12: Coral-Bleaching-Itw
#Description: Mass coral bleaching (very high in-situ sea temperature + very low wind)
    @Rule(windsp(rRange=L('dLow') | L('vLow')),
            windsp(tod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            seandbc(rRange=L('vHigh') | L('dHigh')),
            seandbc(tod=W()))
    def mcb12(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #13: Coral-Bleaching-Std
#Description: Mass coral bleaching (high 'shallow' sea temperature + doldrums)
    @Rule(windsp3day(rRange=L('dLow') | L('vLow') | L('Low')),
            windsp3day(tod=W()),
            sea1m(rRange=L('High') | L('dHigh') | L('vHigh')),
            sea1m(tod=W()))
    def mcb13(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #14: Coral-Bleaching-Stl
#Description: Mass coral bleaching (very high 'shallow' sea temperature + very high light)
    @Rule(parsurf(rRange=L('vHigh') | L('dHigh')),
            parsurf(tod=L('midd') | L('dayl') | L('all')),
            sea1m(rRange=L('vHigh') | L('dHigh')),
            sea1m(tod=W())))
    def mcb14(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #15: Coral-Bleaching-Stw
#Description: Mass coral bleaching (very high 'shallow' sea temperature + very low wind)
    @Rule(windsp(rRange=L('dLow') | L('vLow')),
            windsp(tod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            sea1m(rRange=L('vHigh') | L('dHigh')),
            sea1m(tod=W()))
    def mcb15(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #16: Coral-Bleaching-Tl
#Description: Mass coral bleaching (very high SST + very high light)
    @Rule(parsurf(rRange=L('vHigh') | L('dHigh')),
            parsurf(tod=L('midd') | L('dayl') | L('all')),
            sst(rRange=L('vHigh') | L('dHigh')),
            ssst(tod=W()))
    def mcb16(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #17: Coral-Bleaching-Tw
#Description: Mass coral bleaching (very high SST + very low wind)
    @Rule(windsp(rRange=L('dLow') | L('vLow')),
            windsp(tod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            sst(rRange=L('vHigh') | L('dHigh')),
            sst(tod=W()))
    def mcb17(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #18: Coral-Bleaching-B
#Description: Mass coral bleaching (Berkelmans bleaching curve)
    @Rule(curveB(rRange=L('Conductive') | L('vConductive')),
            curveB(tod=W()))
    def mcb18(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #19: Coral-Bleaching-It
#Description: Mass coral bleaching (drastic high in-situ sea temperature)
    @Rule(seandbc(rRange=L('dHigh')),
            seandbc(tod=W()))
    def mcb19(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #20: Coral-Bleaching-Mort
#Description: Mass coral mortality (>50%) for local sensitive species (Berkelmans)
    @Rule(curveB(rRange=L('Mortality') | L('hMortality')),
            curveB(tod=W()))
    def mcb20(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #21: Coral-Bleaching-Mst
#Description: Mass coral bleaching (high monthly mean 'shallow' sea temperature)
    @Rule(sea1mM(rRange=L('High') | L('vHigh') | L('dHigh')),
            sea1mM(tod=W()))
    def mcb21(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #22: Coral-Bleaching-Mwt
#Description: Mass coral bleaching (high monthly mean in situ sea temperature)
    @Rule(seandbcM(rRange=L('High') | L('vHigh') | L('dHigh')),
            seandbcM(tod=W()))
    def mcb22(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #23: Coral-Bleaching-St
#Description: Mass coral bleaching (drastic high 'shallow' sea temperature)
    @Rule(sea1m(rRange=L('dHigh')),
            sea1m(tod=W()))
    def mcb23(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #24: Coral-Bleaching-T
#Description: Mass coral bleaching (drastic high SST)
    @Rule(sst(rRange=L('dHigh')),
            sst(tod=W()))
    def mcb24(self):
        print("Coral-Bleaching-Stwt fired")


#import mcb0_7 as a
#e = a.MCB()
#e.reset()
#e.missing_facts()
#e.facts() """displays current fact list in working memory"""
#e.run()
#"""expected output: 'sst is Some what Low'"""

