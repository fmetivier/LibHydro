import matplotlib.pyplot as plt
import matplotlib.dates as md
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from datetime import datetime, timedelta
import time
from sqlalchemy import create_engine
from getpass import getpass
import glob

from scipy.interpolate import RegularGridInterpolator


def weatherDB_connect(fname=None):
    """Connect to weather database


    Parameters
    ----------
    fname : string, optional
        fichier de connexion, by default None

    Returns
    -------
    connexion object
        connexion à la base
    """

    if fname:
        f = open(fname, "r")
        mylogin = f.readline().strip("\n")
        mypass = f.readline().strip("\n")
        f.close()
    else:
        mylogin = input("login:")
        mypass = getpass("password:")

    engine = create_engine(
        "mysql://%s:%s@localhost/weatherDB" % (mylogin, mypass))
    conn = engine.connect()

    return conn

def piezo_connect(fname=None):
    """Connexion to piezometric database


    Parameters
    ----------
    fname : string, optional
        fichier de connexion, by default None

    Returns
    -------
    connexion object
        connexion à la base 
    """
    if fname:
        f = open(fname, "r")
        mylogin = f.readline().strip("\n")
        mypass = f.readline().strip("\n")
        f.close()
    else:
        mylogin = "root"
        mypass = "iznogod01"
        # mylogin = input("login:")
        # mypass = getpass("password:")

    engine = create_engine(
        "mysql://%s:%s@localhost/piezo" % (mylogin, mypass))
    conn = engine.connect()

    return conn

def DB_connect(fname=None, mybase='Mayotte'):
    """Connect to database extends the previous two base connections


    Parameters
    ----------
    fname : string, optional
        file with connection info, by default None
    mybase: string, optional
        database name, by default Mayotte

    Returns
    -------
    connexion object
        connexion à la base
    """

    if fname:
        f = open(fname, "r")
        mylogin = f.readline().strip("\n")
        mypass = f.readline().strip("\n")
        f.close()
    else:
        mylogin = input("login:")
        mypass = getpass("password:")

    engine = create_engine(
        "mysql://%s:%s@localhost/%s" % (mylogin, mypass, mybase))
    conn = engine.connect()

    return conn


def load_piezo(fname="",idp="",idi="",type='p',base='piezo'):
    """Load piezometric files from Diver  sounders to a mariadb (mysql) database

    Parameters
    ----------
    fname : str, optional
        file containig data to load, by default ""
    idp : str, optional
        piezometer id, by default ""
    idi : str, optional
        instrument code, by default ""
    type : str, optional
        measurement type (piezometric or barometric), by default 'p'
    base : str optional
        database, by default 'piezo'
    """

    conn = piezo_connect()

    f=open(fname)
    lines=f.readlines()
    f.close()

    # virer la partie entête
    l_count = 0;
    while "Date/time;Pression[cmH2O];Température[°C]" not in lines[l_count]:
        l_count += 1

    l_count+=1
    
    for line in lines[l_count:]:
        if line[0:4] in ['2023','2024','2025']:
            print(line)
            data = line.strip("\n").replace(',','.').split(';')
            if type=="p":
                sql = "insert into piezo values (NULL,%s,'%s',%s,%s,%s)" % (idp,data[0],data[1],data[2],idi)
            elif type=="b":
                sql = "insert into baro values (NULL,%s,'%s',%s,%s,%s)" % (idp,data[0],data[1],data[2],idi)
            conn.execute(sql,)

    conn.close()

def load_weather_records(station_code="AV01", fname="Station_1.txt", dir="/home/metivier/Nextcloud/cours/TRH/stage/Fontainebleau/data/meteo/"):
    """Reads a meteolog file and loads  THP data into the corresponding tables

    .. warning: Do not  import the data twice or more...

    Parameters
    ----------
    station_code : str, optional
        code of the meteorologic station, by default "AV01"
    fname : str, optional
        name of the file to be parsed, by default "Station_1.txt"
    dir : str, optional
        path to the file, by default "/home/metivier/Nextcloud/cours/TRH/stage/Fontainebleau/data/meteo/"
    """
    

    conn = weatherDB_connect()
    f = open(dir + fname, "r")
    lines = f.readlines()
    for line in lines:
        data = line.strip("\n").split(",")
        if "w" in data[0]:
            try:
                sql = "insert into BME values (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                conn.execute(
                    sql,
                    [
                        data[1],
                        data[2],
                        data[3],
                        data[4],
                        data[5],
                        data[6],
                        data[7],
                        data[9],
                        data[8],
                        data[10],
                        station_code,
                    ],
                )    
            except:
                print("record registration failed for line %s" % (line))
    conn.close()

def load_precipitation_records(station_code="AV01", fname="Station_1.txt", dir="/home/metivier/Nextcloud/cours/TRH/stage/Fontainebleau/data/meteo/"):
    """Reads a meteolog file and loads  Precip
    data into the corresponding tables

    .. warning:: not to import the data twice or more...



    Parameters
    ----------
    station_code : str, optional
        code of the meteorologic station, by default "AV01"
    fname : str, optional
        name of the file to be parsed, by default "Station_1.txt"
    dir : str, optional
        path to the data file, by default "/home/metivier/Nextcloud/cours/TRH/stage/Fontainebleau/data/meteo/"
    """
    conn = weatherDB_connect()
    f = open(dir + fname, "r")
    lines = f.readlines()
    for line in lines:
        data = line.strip("\n").split(",")
        if "p" in data[0]:
            try:
                sql = "insert into Precipitation values (NULL,%s,%s,%s,%s,%s,%s,%s,%s)"
                conn.execute(
                    sql,
                    [
                        data[1],
                        data[2],
                        data[3],
                        data[4],
                        data[5],
                        data[6],
                        data[7],
                        station_code,
                    ],
                )
            except:
                print("record registration failed for line %s" % (line))
    conn.close()

def load_records(station_code="AV01", fname="Station_1.txt", dir="/home/metivier/Nextcloud/cours/TRH/stage/Fontainebleau/data/meteo/"):
    """Reads a meteolog file and loads TH and P
    data into the corresponding tables

    .. note::
        
        BEWARE not to import the data twice or more...

    Parameters:
    -----------
        station_code: str 
            code of the meteorologic station
        fname: str 
            name of the file to be parsed
    """
    conn = weatherDB_connect()
    f = open(dir + fname, "r")
    lines = f.readlines()
    for line in lines:
        data = line.strip("\n").split(",")
        if "w" in data[0]:
            sql = "insert into BME values (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            conn.execute(
                sql,
                [
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    data[5],
                    data[6],
                    data[7],
                    data[9],
                    data[8],
                    data[10],
                    station_code,
                ],
            )
        if "p" in data[0]:
            try:
                sql = "insert into Precipitation values (NULL,%s,%s,%s,%s,%s,%s,%s,%s)"
                conn.execute(
                    sql,
                    [
                        data[1],
                        data[2],
                        data[3],
                        data[4],
                        data[5],
                        data[6],
                        data[7],
                        station_code,
                    ],
                )
            except:
                print("record registration failed for line %s" % (line))
    conn.close()


def TH_record(station_code="PA01", save=False):
    """    temperature record of the station
    the record is stored in a mysql database

    Parameters:
    -----------
        station_code: str
            Station code, defaults to 'PA01'
        save: boolean
            save to file, defaults to False
    """

    conn = weatherDB_connect()

    sql = "select * from BME where station = '%s' " % (station_code)

    res = conn.execute(sql).fetchall()
    temps = []
    temperature = []
    humidity = []

    for r in res:
        temps.append(datetime(r[1], r[2], r[3], r[4], r[5], int(r[6])))
        temperature.append(r[7])
        humidity.append(r[8])

    fig, ax = plt.subplots(1, figsize=(15, 10))
    ax.plot(temps, temperature, "-", color="C1", label="Air temperature")
    ax.legend(loc=1)
    ax2 = ax.twinx()
    ax2.plot(temps, humidity, "-", color="C0", label="Humidity")
    ax2.legend(loc=2)

    # myFmt = md.DateFormatter("%m-%d")
    # ax.xaxis.set_major_formatter(myFmt)
    ax.xaxis.set_major_locator(md.DayLocator())

    ax.set_ylabel("Temperature ($^o$C)")
    ax2.set_ylabel("Humidity ($\%$)")
    ax.set_xlabel("Date")

    fig.autofmt_xdate()

    if save:
        plt.savefig("TH.pdf", bbox_inches="tight")

    conn.close()


def pressure_record(station_code="PA01", save=False, baro=False):
    """
    pressure record of the station
    the record is stored in a mysql database
    if baro then plots the pressure given by the baro diver
    """
    conn = weatherDB_connect()
    sql = "select * from BME where station = '%s' " % (station_code)
    res = conn.execute(sql).fetchall()
    conn.close()

    temps = []
    pressure = []

    for r in res:
        temps.append(datetime(r[1], r[2], r[3], r[4], r[5], int(r[6])))
        pressure.append(float(r[9])/1000)




    fig, ax = plt.subplots(1, figsize=(15, 10))
    ax.plot(temps, pressure, "-", color="C1", label="Pression Station")


    if baro:
        temps_b = []
        pressure_b = []
        conn = piezo_connect()
        sql = "select year(mdate), month(mdate), day(mdate), hour(mdate), minute(mdate), second(mdate), p from baro "
        res = conn.execute(sql).fetchall()
        conn.close()
        for r in res:
            print(r)
            md = datetime(r[0], r[1], r[2], r[3], r[4], int(r[5]))
            # md = datetime.strptime(str(r[0]),"%%Y-%%mo-%%da %%H:%%M:%%S")
            print(md)
            temps_b.append(md)
            pressure_b.append(float(r[6])/10)
        ax.plot(temps_b, pressure_b, color = 'C2', label = "Sonde Baro")


    ax.legend(loc=1)

    # myFmt = md.DateFormatter("%m-%d")
    # ax.xaxis.set_major_formatter(myFmt)
    # ax.xaxis.set_major_locator(md.DayLocator())

    ax.set_ylabel("Pression ($kPa$)")
    ax.set_xlabel("Date")

    fig.autofmt_xdate()

    if save:
        plt.savefig("Pression_meteo_baro.pdf", bbox_inches="tight")

    x = []
    for t in temps:
        x.append(datetime.timestamp(t))
    f = interp1d(x, pressure)
    xmax = max(x)

    diff=[]
    t = []
    for i in range( len( temps_b) ):
        try:
            diff.append( pressure_b[i] - f(datetime.timestamp(temps_b[i]) ) )
            t.append(temps_b[i])
        except:
            pass
    fig2, ax2 = plt.subplots(1)
    ax2.plot(t,diff,label = "Différence de pression baro-station")
    ax2.set_xlabel("date")
    ax2.set_ylabel("pression (kPa)")
    ax2.legend(loc=1)
    if save:
        plt.savefig("diff_p_barro_station.pdf",bbox_inches='tight')

def temperature_hour_avg(station_code="PA01"):
    """
    Hourly temperature plot from the database record
    """
    conn = weatherDB_connect()

    sql = (
        "select Ye, Mo, Da, Ho, avg(Temperature) as Tm from BME  where station = '%s' group by Ye, Mo, Da, Ho"
        % (station_code)
    )

    res = conn.execute(sql).fetchall()
    temps = []
    temperature = []

    for r in res:
        temps.append(datetime(r[0], r[1], r[2], r[3]))
        temperature.append(r[4])

    plt.figure(figsize=(15, 10))

    plt.plot(temps, temperature, color="C1")

    conn.close()


def precip_new(station_code="PA01", stdate=[], edate=[], save=False):
    """
    Calculation fo the rainfall intensity
    """
    conn = weatherDB_connect()

    if len(stdate) > 1 and len(edate) > 1:
        sql = """select * from Precipitation  where station = '%s' and Ye between %s and %s and Mo between %s and %s and Da between %s and %s """ % (
            station_code, stdate[0], edate[0], stdate[1], edate[1], stdate[2], edate[2])
    else:
        sql = """select * from Precipitation  where station = '%s' """ % (
            station_code)

    res = conn.execute(sql).fetchall()
    temps = []
    precip = []

    for r in res:
        temps.append(datetime(r[1], r[2], r[3], r[4], r[5], int(r[6])))
        precip.append(r[7])

    tts = [0]  # arbitrary first timestamp
    for t in temps:
        tts.append(t.timestamp())

    I = np.ones(len(precip)) * 0.25 / np.diff(np.array(tts)) * 3600

    c = 0
    tbar = [temps[0]]
    pbar = [I[0]]
    while c < len(I) - 1:
        tbar.append(temps[c])
        tbar.append(temps[c + 1])
        pbar.append(I[c + 1])
        pbar.append(I[c + 1])
        c += 1

    fig, ax = plt.subplots(1, figsize=(15, 10))
    ax.plot(tbar, pbar, "-")
    myFmt = md.DateFormatter("%d:%h")
    ax.xaxis.set_major_formatter(myFmt)
    ax.set_ylabel("Rainfall rate (mm/h)")
    ax.set_xlabel("Date")
    if save:
        plt.savefig("precip_new.pdf", bbox_inches="tight")

    conn.close()


def daily_rain(station_code='AV01'):
    
    conn = weatherDB_connect()
    sql = """select * from daily_rain where station = '%s' """ % (station_code)

    f = open('daily_rain.csv', 'w')
    f.write("Date;precip (mm);station\n")
    res = conn.execute(sql).fetchall()
    for r in res:
        f.write(str(r[0])+';'+str(r[1])+';'+str(r[2]+'\n'))
        print(r)

    f.close()
    conn.close()

def extract_daily_for_comparison():

    conn = weatherDB_connect()
    sql = """select date(str_to_date(concat(ye,'-',mo,'-',da," ",ho,':',mi,':',se), '%%Y-%%m-%%d %%H:%%i:%%s') + interval -10 hour), count(*)*0.3 
    from Precipitation 
    where station='AV01' 
    group by date(str_to_date(concat(ye,'-',mo,'-',da," ",ho,':',mi,':',se), '%%Y-%%m-%%d %%H:%%i:%%s') + interval -10 hour)"""

    f = open('daily_rain_offset.csv', 'w')
    f.write("Date;precip (mm)\n")
    res = conn.execute(sql).fetchall()
    for r in res:
        f.write(str(r[0])+';'+str(r[1])+'\n')
        print(r)

    f.close()
    conn.close()

def export_csv(station_code='AV01', edate=()):

    conn = weatherDB_connect()

    # Précipitations

    if edate:
        fname = station_code + '-%s-%s-%s_P_.csv' % edate
        sql = """select concat(ye,'-',mo,'-',da,' ',ho,':',mi,':',se) as mdate,  P*0.3, station from  Precipitation where ye=%s and mo = %s and da=%s and station='%s';""" % (edate[0],edate[1],edate[2],station_code)
        res = conn.execute(sql).fetchall()

    else:
        fname = station_code + '_P_.csv'
        sql = """select concat(ye,'-',mo,'-',da,' ',ho,':',mi,':',se) as mdate,  P*0.3, station from  Precipitation where station='%s';""" % (station_code)

        res = conn.execute(sql).fetchall()

    f = open(fname, 'w')
    f.write("""################################################################
# Précipitation en mm.
# Chaque date correspond à l'instant de bascule du pluviomètre
# mdate: date et heure de mesure Y-M-D hh:mmm:ss
# P: valeur de précipitation ici 0.3 mm par bascule
################################################################\n""")
    f.write("mdate;P\n")
    for r in res:
        f.write(str(r[0])+";"+str(r[1])+'\n')
    f.close()

    if edate:
        fname = station_code+'-%s-%s-%s_TPHG_.csv' % edate
        sql = """select concat(ye,'-',mo,'-',da,' ',ho,':',mi,':',se) as mdate,  Temperature, Humidity,Pressure, Gaz, station from  BME where ye=%s and mo = %s and da=%s and station='%s';""" % (edate[0],edate[1],edate[2],station_code)
        res = conn.execute(sql).fetchall()
    else:
        fname = station_code+'_TPHG_.csv'
        sql = """select concat(ye,'-',mo,'-',da,' ',ho,':',mi,':',se) as mdate,  Temperature, Humidity,Pressure, Gaz, station from  BME where station='%s';""" % (station_code)
        res = conn.execute(sql).fetchall()
    f = open(fname, 'w')
    f.write("""##########################################
# Météo capteur BME680
# mdate: date et heure de mesure Y-M-D hh:mmm:ss
# T: Température en °C
# H:  Humidité en %%
# P: Pression en Pas
# G: contenu en gaz (Ohm)
##########################################\n""")
    f.write("mdate;T;H;P;G\n")
    for r in res:
        f.write(str(r[0])+";"+str(r[1])+";"+str(r[2])
                + ";"+str(r[3])+";"+str(r[4])+'\n')
    f.close()

    conn.close()

def compute_piezo():
    #
    # ATTENTION P EN CM H20
    #
    temps_b = []
    pressure_b = []
    conn = piezo_connect()
    # sql = "select year(mdate), month(mdate), day(mdate), hour(mdate), minute(mdate), second(mdate), p from baro "


    #
    #  Récupération des données barométrique et création d'une fonction d'interpolation
    #  pour la correction ultérieure
    #
    sql = "select mdate, p from baro "
    res = conn.execute(sql).fetchall()
    for r in res:
        # print(r)
        mdate=r[0]
        # md = datetime(r[0], r[1], r[2], r[3], r[4], int(r[5]))
        # md = datetime.strptime(str(r[0]),"%%Y-%%mo-%%da %%H:%%M:%%S")
        print(md)
        temps_b.append(mdate)
        pressure_b.append(float(r[1]))

    tb=[]
    for t in temps_b:
        tb.append(datetime.timestamp(t))
    tba = np.array(tb)
    pb = np.array(pressure_b)
    f = interp1d(tba, pb)


    fig,ax = plt.subplots()
    ax.plot(tb, pb, color = 'C2', label = "Sonde Baro")


    #
    # Récupération des données piézométriques
    # correction de la pression du baromètre
    # 

    # myFmt = md.DateFormatter("%d:%h")
    # ax.xaxis.set_major_formatter(myFmt)
    # ax.set_ylabel("Pression ($Pa$)")
    # ax.set_xlabel("Date")

    # Récupère les infos de site
    sql = "select *  from info where id_p !=4 "
    res = conn.execute(sql).fetchall()
    idp = []
    site = []
    elev = []

    for r in res:
        idp.append(r[0])
        site.append(r[1])
        elev.append(r[5])

    # statique = np.array([2.9,21.57,21.01,7.6]) avec bois le roi mais fini
    statique = np.array([2.9,21.57,21.01])

        # pour chaque site récupère les données piézo
        # corrige de la pression
        # ajoute au graphique

    fig2,ax2 = plt.subplots(1)
    for i in range(len(idp)):
        sql = "select * from piezo where id_p = %s" % (i+1)
        res = conn.execute(sql).fetchall()
        tp = []
        hp = []
        pp = []
        for r in res:
            t = datetime.timestamp(r[2])
            p = float(r[3])
            try:
                pa = f(t)
                tp.append(t)
                hp.append((p-pa)/100)
                pp.append(p)

            except Exception as inst:
                print("echec: ", inst)

        tp = np.array(tp)
        hp = np.array(hp)
        # hp = hp - hp[-10] + offset[i] # pourquoi -10 ??
        # on attend 4 valeur histoire d'etre certain que la sonde est dans l'eau et au calme pour retirer l'offset.
        offset = np.array(elev)  - statique
        print("altitude orthométrique des piézomètres", elev)
        print("offest pour le calcul de nappe", offset)
        hp = np.around(hp - hp[4] + offset[i],2) 

        mt = []
        for t in tp:
            mt.append(datetime.fromtimestamp(t))

        fname = 'piezo_%s.txt' % (site[i])
        np.savetxt(fname, np.array((mt,hp)).T,delimiter=';', fmt='%s', header='date;cote piezometrique', newline='\n')
         
        ax2.plot(mt[4:-4],hp[4:-4],'-',label = site[i])
        # ax2.plot(tp,pp,'o-',label = site[i])
    ax2.legend(loc=0)
    ax2.set_xlabel("Date de mesure")
    ax2.set_ylabel("Hauteur de la surface libre (m NGF) ")

    plt.savefig("Piezo_fontainebleau.pdf", bbox_inches='tight')

    conn.close()

def compute_piezo_1(idp=[1], dmin = '', export = False ):

    temps_b = []
    pressure_b = []
    conn = piezo_connect()
    if dmin == '':
        sql = "select mdate, p from baro "
    else:
        sql = "select mdate, p from baro where mdate > '%s'" % (dmin)

    res = conn.execute(sql).fetchall()

    for r in res:
        # print(r)
        mdate=r[0]
        # md = datetime(r[0], r[1], r[2], r[3], r[4], int(r[5]))
        # md = datetime.strptime(str(r[0]),"%%Y-%%mo-%%da %%H:%%M:%%S")
        print(md)
        temps_b.append(mdate)
        pressure_b.append(float(r[1])*100)

    tb=[]
    for t in temps_b:
        tb.append(datetime.timestamp(t))
    tba = np.array(tb)
    pb = np.array(pressure_b)
    f = interp1d(tba, pb)


    # fig,ax = plt.subplots()
    # ax.plot(temps_b, pb, color = 'C2', label = "Sonde Baro")
    # fig.autofmt_xdate()

#
    # myFmt = md.DateFormatter("%d:%h")
    # ax.xaxis.set_major_formatter(myFmt)
    # ax.set_ylabel("Pression ($Pa$)")
    # ax.set_xlabel("Date")

    # plt.savefig("sonde_baro_ndef.pdf", bbox_inches='tight')
    # on trace la pluvio
    conn2 = weatherDB_connect()

    if dmin == '':
        sql = "select date(dateLocale), sum(Pluie) from sencrop group by date(dateLocale) order by date(dateLocale);" 
    else:
        sql = "select date(dateLocale), sum(Pluie) from sencrop where date(dateLocale) >= '%s' group by date(dateLocale) order by date(dateLocale);" % (dmin)

    print(sql)
    res = conn2.execute(sql).fetchall()
    conn2.close()

    pd, pp = [],[]
    for  r in res:
        pd.append(r[0])
        pp.append(float(r[1]))

    fig,ax = plt.subplots(1, figsize=(20/2.54,10/2.54))

    ax.bar(pd,pp,width=1, color='C0', label='Pluviomètre de Perthes', zorder=1)
    ax.set_ylabel("Précipitations quotidiennes (mm)")
    ax2 = ax.twinx()
    
    col = 0
    for val in idp:
        sql = "select *  from info where id_p = %i " %(val)
        res = conn.execute(sql).fetchall()
        site = []
        des = []
        elev = []
        lat = []
        lon = []

        for r in res:
            site = r[1]
            des = r[2]
            lat = r[3]
            lon = r[4]
            elev = r[5]   # récupère les infos de site
    
        # statique = np.array([2.9,21.57,21.01,7.6])
        statique = np.array([2.9,21.57,21.01,0,9.1,4.98,7.05])
        offset = elev  - statique[val-1]
        print("altitude orthométrique des piézomètres", elev)
        print("offest pour le calcul de nappe", offset)

        # pour chaque site récupère les données piézo
        # corrige de la pression
        # ajoute au graphique


        if dmin == '':
            sql = "select * from piezo where id_p = %i and mdate <= (select max(mdate) from baro)" % (val)
        else:
            sql = "select * from piezo where id_p = %i and mdate > '%s' and  mdate <= (select max(mdate) from baro)" % (val, dmin)

        res = conn.execute(sql).fetchall()
        tp = []
        hp = []
        pp = []
        for r in res:
            t = datetime.timestamp(r[2])
            p = float(r[3])*100
            try:
                pa = f(t)
                tp.append(t)
                hp.append((p-pa)/1000/9.81)
                pp.append(p)

            except:
                print("echec")

        tp = np.array(tp)
        hp = np.array(hp)
        hp = hp - hp[5] + offset # ok hp[-10] c'est le 0
        prof =  elev - (statique[val-1] - (hp - hp[5])) 

        mt = []
        for t in tp:
            mt.append(datetime.fromtimestamp(t))

        mt = mt[10:-10]
        h = hp[10:-10]
        prof = prof[10:-10]


        col += 1
        ax2.plot(mt,prof,'-',label = 'Sonde de %s' % (site), zorder=2, color = 'C%i' % (col))

        if export:
            ofname = "piezo_%s.txt" % (site)
            f = open(ofname, "w")
            f.write("#Nom: %s\n" % (site))
            f.write("#Description: %s\n" % (des))
            f.write("#Localisation: %f, %f, %f\n" % (lat,lon, elev))
            f.write("#Cote NGF en mètres\n")
            f.write("#date, cote\n")
            for i in range(len(mt)):
                f.write('%s,%f\n' % (mt[i],prof[i]))
            f.close()
 
    ax2.xaxis_date()
    ax2.set_ylabel("Hauteur d'eau (m, cote NGF) ")
    
    fig.autofmt_xdate()
    # ax.plot(t, np.nanmean(h*t**(1/4))/t**(1/4.),'-')

        # ax2.plot(tp,pp,'o-',label = site[i])
    ax.legend(loc=1)
    ax2.legend(loc=2)

    ax.set_xlabel("Date de mesure")

    fig.autofmt_xdate()
 
    oname  = "Piezo_"
    for v in idp:
        oname += "%i_" % (v)
    oname += ".pdf"

    plt.savefig(oname, bbox_inches='tight')

    conn.close()


def compute_piezo_rel(idp=[1], dmin = '', vol=False ):
    temps_b = []
    pressure_b = []
    conn = piezo_connect()
    if dmin == '':
        sql = "select mdate, p from baro "
    else:
        sql = "select mdate, p from baro where mdate > '%s'" % (dmin)

    res = conn.execute(sql).fetchall()

    for r in res:
        # print(r)
        mdate=r[0]
        # md = datetime(r[0], r[1], r[2], r[3], r[4], int(r[5]))
        # md = datetime.strptime(str(r[0]),"%%Y-%%mo-%%da %%H:%%M:%%S")
        print(md)
        temps_b.append(mdate)
        pressure_b.append(float(r[1])*100)

    tb=[]
    for t in temps_b:
        tb.append(datetime.timestamp(t))
    tba = np.array(tb)
    pb = np.array(pressure_b)
    f = interp1d(tba, pb)


    # on trace la pluvio
    conn2 = weatherDB_connect()

    if dmin == '':
        sql = "select date(dateLocale), sum(Pluie) from sencrop group by date(dateLocale) order by date(dateLocale);" 
    else:
        sql = "select date(dateLocale), sum(Pluie) from sencrop where date(dateLocale) >= '%s' group by date(dateLocale) order by date(dateLocale);" % (dmin)

    print(sql)
    res = conn2.execute(sql).fetchall()
    conn2.close()

    pd, pp = [],[]
    for  r in res:
        pd.append(r[0])
        pp.append(float(r[1]))

    fig,ax = plt.subplots(1, figsize=(20/2.54,10/2.54))

    ax.bar(pd,pp,width=1, color='C0', label='Pluviomètre de Perthes', zorder=1)
    ax.set_ylabel("Précipitations quotidiennes (mm)")
    ax2 = ax.twinx()
    

    # on récupère les infos de site
    col = 0
    for val in idp:
        sql = "select *  from info where id_p = %i " %(val)
        res = conn.execute(sql).fetchall()
        site = []
        elev = []

        for r in res:
            site = r[1]
            elev = r[5]

    # statique = np.array([2.9,21.57,21.01,7.6])
        # pour chaque site récupère les données piézo
        # corrige de la pression
        # ajoute au graphique


        if dmin == '':
            sql = "select * from piezo where id_p = %i  mdate <= (select max(mdate) from baro)" % (val)
        else:
            sql = "select * from piezo where id_p = %i and mdate > '%s' and  mdate <= (select max(mdate) from baro)" % (val, dmin)

        res = conn.execute(sql).fetchall()
        tp = []
        hp = []
        pp = []
        for r in res:
            t = datetime.timestamp(r[2])
            p = float(r[3])*100
            try:
                pa = f(t)
                tp.append(t)
                hp.append((p-pa)/1000/9.81)
                pp.append(p)

            except:
                print("echec")

        tp = np.array(tp)
        hp = np.array(hp)
        hp = hp - hp[5] # ok hp[-10] c'est le 0
        prof =    (hp - hp[5])

        mt = []
        for t in tp:
            mt.append(datetime.fromtimestamp(t))

        mt = mt[10:-10]
        h = hp[10:-10]
        prof = prof[10:-10]
        print(mt[0:10])


        
        col += 1

        if vol:
            a = [np.pi/4, np.pi* 1.5**2  / 4]
            ax2.plot(mt,(prof-prof[0])*a[col-1],'-',label = 'Sonde de %s' % (site), zorder=2, color = 'C%i' % (col))
        else:
            ax2.plot(mt,prof,'-',label = 'Sonde de %s' % (site), zorder=2, color = 'C%i' % (col))
    
    ax2.xaxis_date()

    if vol:
        ax2.set_ylabel("Volume d'eau (m$^3$) ")
    else:
        ax2.set_ylabel("Hauteur d'eau (m) ")

    fig.autofmt_xdate()
    # ax.plot(t, np.nanmean(h*t**(1/4))/t**(1/4.),'-')

        # ax2.plot(tp,pp,'o-',label = site[i])
    ax.legend(loc=1)
    ax2.legend(loc=2)

    ax.set_xlabel("Date de mesure")

    

    # plt.savefig("Piezo_%s_ndef.pdf" % (idp), bbox_inches='tight')

    conn.close()

def load_pluvio_sencrop(fname):

    df = pd.read_excel(fname)
    df["dateLocale"] = pd.to_datetime(df["dateLocale"], infer_datetime_format = True)
    sname = ["PERTHES"]*len(df)
    df["Station"] = sname
    print(df.dtypes)
    print(df.head())
    conn = weatherDB_connect()
    df.to_sql('sencrop',conn,if_exists='append',index=False)
    conn.close()



def load_piezos():
    piez_dic={"chailly":[2,2], "villiers":[1,2],"13-01":[3,2],"13-01b":[3,7],'MC':[5,2],'MJ':[6,2], "Perthes": [7,2]}
    # # chailly idp=2, idi=2 #fini
    # Perthes sonde de Chailly redéployée
    load_piezo("/home/metivier/Nextcloud/cours/TRH/stage/Fontainebleau/data/piezo/CSV/exportDiver/CSV/PERTHES_251010095454_DR512.CSV",7,2)
    # #villiers idp=1, idi=2
    load_piezo("/home/metivier/Nextcloud/cours/TRH/stage/Fontainebleau/data/piezo/CSV/exportDiver/CSV/VILLIERS_251010095701_DT084.CSV",1,2)
    # #
    # # #13-01 idp=3, idi=2
    load_piezo("/home/metivier/Nextcloud/cours/TRH/stage/Fontainebleau/data/piezo/CSV/exportDiver/CSV/VEI_DR524_251010095921_DR524.CSV",3,2)
    # # #13-01 idp=3, idi=7
    load_piezo("/home/metivier/Nextcloud/cours/TRH/stage/Fontainebleau/data/piezo/CSV/exportDiver/CSV/VEI_DS262_251010095740_DS262.CSV",3,7,"b")
    # MC
    load_piezo("/home/metivier/Nextcloud/cours/TRH/stage/Fontainebleau/data/piezo/CSV/exportDiver/CSV/Montaquoy cour_251010095616_DR533.CSV",5,2,"p")
   # MJ
    # load_piezo("/home/metivier/Nextcloud/cours/TRH/stage/Fontainebleau/data/piezo/CSV/Montaqoy_250513133006_DR536.CSV",6,2,"p")

def get_meteo_stations():
    """liste les stations météo du 77
    """
    fname="data/meteo/H_77_latest-2023-2024.csv"
    f = open(fname,'r')
    entete=f.readline()
    lines = f.readlines()
    num_list, nom, lat, lon = [], [], [], []
    for line in lines:
        data = line.split(';')
        if data[0] not in num_list:
            num_list.append(data[0])
            nom.append(data[1])
            lat.append(float(data[2]))
            lon.append(float(data[3]))

    f.close()
    f = open('stations_mete_77.txt','w')
    for i in range(len(num_list)):
        f.write("%s;%s;%s;%s\n" % (num_list[i],nom[i],lat[i],lon[i]))
    f.close()

def rr(station = '77186002'):
    """Extrait les données de pluie d'une station donnée

    Parameters
    ----------
    station : str, optional
        code de la station à extraire, by default '77186002'
    """
    fname="data/meteo/H_77_latest-2023-2024.csv"
    f = open(fname,'r')
    entete=f.readline()
    lines = f.readlines()
    f.close()
    mdate=[]
    RR=[]
    i=0
    f = open('Pluvio_station_Fontainebleau_Meteo_France.txt','w')
    for line in lines:
        data = line.strip('\n').split(';')
        # print(data[0])
        if int(data[0]) ==  int(station):
            print(station)
            try:
                RR.append(float(data[6]))
                mdate.append(datetime(int(data[5][0:4]),int(data[5][4:6]),int(data[5][6:8]),int(data[5][8:10])))
            except Exception as inst:
                print(inst)

    for md, r in zip(mdate,RR):
        f.write(md.strftime("%d/%m/%Y %H:%M:%S")+";"+str(r)+"\n")
    f.close()
    print(RR)
    plt.plot(mdate,RR,'-')
    
def compare_rain():

    md, rr = [], []
    f = open('Pluvio_station_Fontainebleau_Meteo_France.txt','r')

    lines = f.readlines()
    f.close()

    for line in lines:
        data = line.strip('\n').split(';')
        md.append(datetime.strptime(data[0],"%d/%m/%Y %H:%M:%S"))
        rr.append(float(data[1]))

    sql = "select ye, mo, da, ho, count(*)*0.4 from Precipitation where station='AV01' group by ye, mo, da, ho;"

    conn = weatherDB_connect()
    res = conn.execute(sql).fetchall()

    print(res)

    mds, rrs = [], []
    avon_dic={}
    for r in res:
        # mds.append(datetime(r[0],r[1],r[2],r[3]))
        # rrs.append(float(r[4])) 
        avon_dic[datetime(r[0],r[1],r[2],r[3])] = float(r[4])

    
    for i in range(len(md)):
        if md[i] in avon_dic.keys():
            rrs.append(avon_dic[md[i]])
        else:
            rrs.append(0)

    plt.plot(md,rr,'-', color='C0')
    plt.plot(md,rrs,'-', color='C1')

def loadMeteoFrance(fname = "/home/metivier/Téléchargements/H_77_previous-2020-2023.csv", type='H'):

    df = pd.read_csv(fname, delimiter=";")
    print(df.head())
    print(df.columns)
    print(df["PSTAT"])

    conn = weatherDB_connect()
    df.to_sql('horaire', conn, if_exists = 'append')

def compute_piezo_from_files(pfile="", mfile="",ctd=False):

    # csv diver file
    #
    f=open(pfile,'r')
    lines = f.readlines()
    f.close()
    t_diver,P_diver,T_diver = [],[],[]
    if ctd:
        c_diver=[]
    for line in lines:
        if line[0] == '2':
            data = line.strip("\r\n").split(";")
            t_diver.append(datetime.strptime(data[0],"%Y/%m/%d %H:%M:%S"))
            P_diver.append(float(data[1]))
            T_diver.append(float(data[2]))
            if ctd:
                c_diver.append(float(data[3]))


    # csv meteo file
    f=open(mfile,'r')
    lines = f.readlines()
    f.close()
    t_meteo, P_meteo, T_meteo = [],[],[]
    for line in lines:
        data = line.strip("\r\n").split(',')
        t_meteo.append(datetime.strptime(data[4],"%Y-%m-%d %H:%M:%S"))
        P_meteo.append(float(data[2]))
        T_meteo.append(float(data[1]))

    # create interpolator
    tb=[]
    for t_val in t_meteo:
        tb.append(datetime.timestamp(t_val))
    tba = np.array(tb)
    pb = np.array(P_meteo)
    f = interp1d(tba, pb)

    # Repositionnement à partir du 04/12
    # 
    ztot= - 13.336 + 20.997 - 0.64 # référence de map_topo mesures 11/2023
    Ns = 5.8 # idem référence de map_topo
    Ps=1080.342*0.98/100
    Pm=1013.55/100
    z_sonde = ztot-Ns-Ps+Pm
    print(z_sonde)

    dp = np.diff(P_diver)
    t_fil, p_fil= [], []
    # correct from pressure
    for i in range(len(P_diver)):
        P_diver[i] = z_sonde + (P_diver[i] *0.98 - f(datetime.timestamp(t_diver[i])))/100

    # manque une mesure de ref et l'altitude de la margelle
    
    print(np.min(P_diver))

    fig,ax = plt.subplots(1,figsize=(20,10))
    # ax.plot(t_fil,p_fil,color='C0')
    # ax.plot(t_diver[1:],np.diff(P_diver)*P_diver[1:],marker='o', color='C1')
    ax.plot(t_diver, P_diver, label="Niveau piézométrique (m asl)", color='C1')
    ax.set_xlabel("Date")
    ax.set_ylabel("Niveau pizeométrique (m au dessus de la mer)", color='C1')
    ax.legend(loc=1)
    ax2=ax.twinx()
    ax2.plot(t_diver,c_diver,color='C2', label='Conductivité (mS/cm)')
    ax2.set_ylabel("Conductivité (mS/cm)", color='C2')
    # ax2.set_xticklabels(color='C2')
    ax2.legend(loc=2)
    # plt.plot(t_meteo,P_meteo,color='C1')
    plt.savefig("Sonde_Ibrahim.pdf")



if __name__ == "__main__":
    # load_records(fname='DATALOG12.TXT')
    # load_precipitation_records(fname='DATALOG11.TXT')
    # TH_record(station_code="AV01", save=True)
    # temperature_hour_avg(station_code='AV01')
    # precip_new(station_code="AV01", save=True)
    # pressure_record(station_code="AV01", save=True, baro=True)
    # daily_rain()
    # for i in (20,21,22):
    # export_csv(edate = (2024,8,15))

    # load_piezos()

    # extract_daily_for_comparison()
    # get_meteo_stations()

    # load sencrop data
    # files = glob.glob('../data/meteo/2024-11-PERTHES/*.xlsx')
    # for file in files:
    #     load_pluvio_sencrop(file)

    # for i in range(1):
    #     compute_piezo_1(idp=[i+1])
    # compute_piezo_rel(idp=[5,6],dmin='2024-06-01',vol=True)
    # rr()
    # compare_rain()
    
    # loadMeteoFrance(fname = "/home/metivier/Téléchargements/H_91_latest-2024-2025.csv")

    pfile="../../../Recherche/GroundWater/islands/data/Mayotte/PIEZO/JARDIN_IBRAHIM_260418142654_X8718.CSV"
    mfile="../../../Recherche/GroundWater/islands/data/Mayotte/METEO/DATAFILE_IBRAHIM.TXT"
    compute_piezo_from_files(pfile,mfile,ctd=True)
    plt.show()
