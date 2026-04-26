######################################
#
# Most of the functions below 
# deal with Mayotte and
# uses the Mayotte sql database
#
######################################


from map_topo import *
from grande_terre import *
import sys
import pyproj 

sys.path.append('../Data/')
sys.path.append('/home/metivier/Nextcloud/cours/TRH/stage/Fontainebleau/src')

import meteo_piezo as mp 


def db_connect(dbname='Mayotte', user="me", passwd ="you"):
    """connexion to sql database using sqlalchemy

    Parameters
    ----------
    dbname : str, optional
        database name, by default 'Mayotte'
    user : str, optional
        user name, by default "me"
    passwd : str, optional
        passwd, by default "you"

    Returns
    -------
    connexion object
        connexion object to the database
    """

    engine = create_engine(
            "mysql://%s:%s@localhost/%s" % (user, passwd,dbname)
            )
    conn = engine.connect()

    return conn    

def get_piezo(code = '12307X0011', conn=[]):
    """get piezometric chronicles from an ANDES piezometer and plots the result

    .. note:: 
    
        uses chronicles from piezometric network run by BRGM. data tables and names are standard


    Parameters
    ----------
    code : str, optional
        piezometer code in the database, by default '12307X0011'
    conn : list, optional
        connexion object, by default []
    """


    sql = "select datemes, cote_ngf from chroniques where An_code_nat_BSS regexp %s" 
    data = conn.execute(sql,(code,)).fetchall()
    d = np.array(data).T
    
    fig, ax = plt.subplots(1)
    ax.plot(d[0],d[1],'-', color='C0')
    ax.set_xlabel("Date")
    ax.set_ylabel("Cote NGF (m)")
    plt.title("Piézomètre %s" % (code))


    sql = "select avg(cote_ngf), std(cote_ngf) from chroniques where An_code_nat_BSS regexp %s" 
    res = conn.execute(sql,(code,)).fetchall()
    for r in res:
        m = float(r[0])
        s = float(r[1])
    ax.plot([min(d[0]),max(d[0])],[m,m],'--',color='C0')
    plt.savefig('./figures/Piezo_%s.pdf' % (code), bbox_inches='tight')


def piezo_an(conn):

    sql = """select distinct id_nat_bss from chroniques;"""
    res=conn.execute(sql).fetchall()
    for r in res:
        sql = "select datemes, cote_ngf from chroniques where id_nat_bss = %s" 
        data = conn.execute(sql,(r[0],)).fetchall()
        d=np.array(data).T
        fig,ax=plt.subplots(1)
        ax.plot(d[0],d[1])
        ax.set_xlabel("Date")
        ax.set_ylabel("Cote NGF (m)")
        plt.title("Piézomètre %s" % r[0])

    """
    select id_nat_bss, year(datemes), max(cote_ngf)-min(cote_ngf), count(*) as battement from chroniques group by id_nat_bss,year(datemes) having count(*) > 300;
    select id_nat_bss, avg(battement), std(battement), count(*) from (select id_nat_bss, year(datemes), max(cote_ngf)-min(cote_ngf) as battement, count(*) as N from chroniques group by id_nat_bss,year(datemes) having count(*) > 300) as Q group by id_nat_bss;

    """

def load_data(fname, tab_name, conn):
    """Load data into the database specified by `connn` using the `panda to_sql` function

    Parameters:
    -----------
        fname: datafile name (format csv)
        tab_name: table name in Mayotte base in which to load the data
    """

    df = pd.read_csv(fname,delimiter="|")
    print(df.head())
    print(df.columns)
    
    df.to_sql(tab_name,conn,if_exists='append')


def correl_pm(conn):
    """Find the weather station closest to each of the piezometers

    Returns
    -------
    list
        List of piezo-weather station pairs
    """

    # récupère les localisations des piézos
    sql = "select distinct Id_nat_BSS , An_code_nat_BSS, X_WGS84 , Y_WGS84 from chroniques"
    p_loc = conn.execute(sql).fetchall()

    # récupère les localisations des stations météo
    sql = "select distinct NUM_POSTE, Lon, Lat from MeteoQ"
    m_loc = conn.execute(sql).fetchall()

    #cherche la station météo la plus proche de chaque piézo 
    wgs84_geod = pyproj.Geod(ellps='WGS84')

    my_crs = ccrs.UTM(zone=38, southern_hemisphere=True)
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111, projection=my_crs)
    ax.coastlines(resolution='10m')
    gl = ax.gridlines(draw_labels=True, x_inline=False, y_inline=False, zorder=2)
    gl.xlabels_top = False
    gl.ylabels_right = False
    ax.set_ylabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_extent([45, 45.3, -13.1, -12.6], crs=ccrs.PlateCarree())

    c_tab = []
    for p in p_loc:
        d=1e10
        id_p, aid_p, lon_p, lat_p = p
        for m in m_loc:
            id_m, lon_m, lat_m = m 
            az12, az21, dist = wgs84_geod.inv(lon_p,lat_p,lon_m,lat_m)
            if dist < d:
                d = dist
                station = id_m
                lon_s = lon_m
                lat_s = lat_m
        c_tab.append([aid_p,station])
        ax.plot([lon_p,lon_s],[lat_p,lat_s],'k-', transform=ccrs.Geodetic())
        ax.plot(lon_p,lat_p,'s', color='C0', transform=ccrs.Geodetic())
        ax.plot(lon_s,lat_s,'d', color='C1', transform=ccrs.Geodetic())

    print(c_tab)

    return c_tab

def get_recharge(conn):
    """Calculates annual groundwater recharge based on annual precipitation and an estimate
    of evaporation using Turc (1955) for each couple piezo-weather station. 
    Returns the result and writes to file

    Parameters:
    -----------
        conn: connexion object to Mayotte database

    Returns:
    --------
        List: list of yearly recharge, precipitation and temp
    """

    c_tab = correl_pm()

    sql="""select avg(A), std(A), count(A)  from (select year(datemes), max(cote_ngf)-min(cote_ngf) as A 
    from chroniques where An_code_nat_BSS regexp %s group by year(datemes)) as Q;"""

    sql2 = """select avg(P), std(P), count(P), avg(T), std(T), count(T) from 
        (select substr(AAAAMMJJ,1,4) as a, sum(RR) as P, avg(TM) as T 
        from MeteoQ where NUM_POSTE = %s and substr(AAAAMMJJ,1,4) <
        2024 group by a having P > 200) as Q"""

    tp_pm = []
    
    f = open('GT_recharge.txt','w')
    for c in c_tab:
        d = conn.execute(sql,(c[0],)).fetchall()[0]
        pt = conn.execute(sql2,(c[1],)).fetchall()[0]
        try:
            ETR = Turc(pt[0],pt[3])/1000
            tp_pm.append([c[0],c[1],d[0],pt[0]/1000,pt[3],ETR,(pt[0]/1000-ETR)/d[0]*100])
            st = "%s&%s&%4.2f&%4.2f&%4.2f&%4.2f&%4.2f\\\\ \n" % (c[0],c[1],d[0],pt[0]/1000,pt[3],ETR,(pt[0]/1000-ETR)/d[0]*100)
            f.write(st)
        except:
            pass

        
    f.close()
    
    print(tp_pm)




def plot_p_r(conn):
    """Comparison of daily rainfall in terms of intensity and total accumulation
    """

    c_tab = correl_pm(conn)

    sql="""select date(datemes), avg(cote_NGF), RR 
        from chroniques c, MeteoQ m 
        where year(datemes)=substr(AAAAMMJJ,1,4) and month(datemes)=substr(AAAAMMJJ,5,2) 
        and day(datemes)=substr(AAAAMMJJ,7,2) and c.Id_nat_BSS=%s 
        and m.NUM_Poste=%s and year(datemes) between 2018 and 2022
        group by date(datemes);
        """ 
    sql="""select date(datemes), avg(cote_NGF), RR 
        from chroniques c, MeteoQ m 
        where year(datemes)=substr(AAAAMMJJ,1,4) and month(datemes)=substr(AAAAMMJJ,5,2) 
        and day(datemes)=substr(AAAAMMJJ,7,2) and c.Id_nat_BSS=%s 
        and m.NUM_Poste=%s 
        group by date(datemes);
        """ 

    for i in [0,1]:
        co = c_tab[i]
        print(co)
        res=conn.execute(sql,(co[0], co[1])).fetchall()   

        md = []
        c = []
        p = []
        for r in res:
            md.append(r[0])
            c.append(r[1])
            p.append(r[2])

        c = np.array(c)*1000
        p = np.array(p)
        print(len(md), len(c), len(p))

        if len(md) > 0:
            fig, ax = plt.subplots(1)
            ax.plot(md,np.array(p), color='C1', label=c_tab[0][1])
            ax2 = ax.twinx()
            ax2.plot(md[1:],np.diff(c), color='C0', label=str(c_tab[0][0]))
            ax.set_ylim(min(np.diff(c)), max(np.diff(c)))
            ax2.set_ylim(min(np.diff(c)), max(np.diff(c)))
            ax.plot([],[],'-', color='C0', label=str(c_tab[0][0]))
            ax.legend()

            fig, ax = plt.subplots(1)
            ax.plot(md,np.cumsum(p), color='C1', label=c_tab[0][1])
            ax2 = ax.twinx()
            ax2.plot(md,c-min(c), color='C0', label=str(c_tab[0][0]))
            ax.plot([],[],'-', color='C0', label=str(c_tab[0][0]))
            ax.legend()



def Mayotte_K(fname="", conn=[]):
    """Calculate the mean K using data from the file fname 
    inserted into the database

    Parameters
    ----------
    fname : str, optional
        file containing K's data, by default ""
    """


    if fname != "": 
        try:
            f = open(fname,'r',encoding='utf-8-sig')
            lines = f.readlines()
            # print(lines)
            f.close()
            K_list = []
            val = []
            ref_puits = []
            for line in lines:
                if len(line) > 1:
                    if line[0] == '#':
                        puits = line[1:].strip("\n").split(":")
                        ref_puits.append([puits[0],puits[1]])
                        val.append([])
                    else:
                        kh = line.strip("\n").split(";")
                        print(kh)
                        val[-1].append([float(kh[0]),float(kh[1]),float(kh[2]),float(kh[3])]) 
            print(ref_puits)
            print(val)
            k_dic={}
            for i in range(len(ref_puits)):
                kh_min = 0
                kh_max = 0
                h_tot = 0
                for d in val[i]:
                    h = d[3]-d[2]
                    h_tot += h
                    kh_min += d[0]*h
                    kh_max += d[1]*h
                sql = "insert into K values (%s,%s,NULL)"
                conn.execute(sql, (ref_puits[i][1], kh_min/h_tot))
                conn.execute(sql, (ref_puits[i][1], kh_max/h_tot))

        except Exception as inst:
            print(inst)
    else:
        print ("Aucun nom de fichier")


    print ("Fin Mayotte K")


def output_K(conn):

    entete = """\begin{tabular}{llllllllll}\\hline\n
    Code piézomètre & Nom & Profondeur Forage (m) & K (m/s) & Cote NGF moy (m)& distance mer (m) & $\\|\nabla h_{mer}\\|$ & distance rivière (m) & cote NGF rivière (m) & $\\|\nabla h_{riviere}\\|$ \\\\ \\hline\n
    """
    closure = """ \\hline\end{tabular}\n """
    

    sql = """
    select code_bss, nom, profondeur, 
    kval, cote_ngf_m, dmer, abs(cote_ngf_m /dmer) as Jm,      
    driviere , zrivier, abs(cote_ngf_m - zrivier)/driviere      
    from DataPiezo d left join 
    (select An_code_nat_BSS , avg(kval) as kval from K group by An_code_nat_BSS  ) as K 
    on d.code_bss=K.An_code_nat_BSS;
    """

    res= conn.execute(sql).fetchall()

    f = open( 'output_k.tex' , 'w')
    f.write(entete)
    k=[]
    for r in res:
        print(r)
        st = "%s" % (r[0]) 
        for i in range(len(r)-1): 
            if type(r[i+1]) is str:
                st += "&%s" % (r[i+1])
            elif type(r[i+1]) is float and i+1 not in [3,6,9]:
                st += "&%4.1f" % (r[i+1])
            elif type(r[i+1]) is float and i+1  in [3,6,9]:
                st += "&%4.1e" % (r[i+1])
            else:
                st += "& "
            
        st+="\\\\ \n"        
        
        print(st)
        f.write(st)


    f.write(closure)
    f.close()


def Turc(P=1200,T=26.9):
    """Calculates Evaporation according to Turc (1955)


    Parameters
    ----------
    P : int, optional
        Annual precipitation, default 1200
    T : float, optional
        Mean annual temperature, by default 26.9

    Returns
    -------
    float
        Evaporation calculated
    """

    L = 0.05*T**3+25*T+300
    Ev = P / (0.9+P**2/L**2)**(1/2)
    print(T,P,L,Ev)


    return Ev 

def conducti():
    """Plot conductivity from BRGM report data
    """

    z0 = {'P1': 3.86+38.54, 'P2': 1.07+21.68 }

    ns_1 = np.array([38.54, 37.75, 37.80])

    

    c = [np.array([[38,470],[47,450],[55,460],[60,440],[65,510]])]
    c.append(np.array([[38,490],[40,492],[50,428]]))
    c.append(np.array([[40,490],[50,520]]))
    c.append(np.array([[38,734],[40,734],[45,735],[49,742]]))

    md = ['14/02/1990','03/04/1990','02/07/1990','08/03/1991']

    c2 = [np.array([[21,325],[33,585],[40,623],[50,922]])]
    c2.append(np.array([[21,802],[30,1015],[40,1170],[50,1728]]))
    c2.append(np.array([[21,450],[30,543],[40,970],[50,2000]]))
    c2.append(np.array([[22,486],[25,539],[30,679],[35,877],[40,888],[45,1070],[49,4160]]))

    md2 = ["22/02/1990","03/04/1190","02/07/1990","08/03/1991"]
    
    fig,ax  = plt.subplots(1,2, figsize=(15/2.54,10/2.54))

    
    for p,d in zip(c,md):
        ax[0].plot(p[:,1],z0['P1']-p[:,0],'o-', label=d)
    ax[0].set_xlabel('Conductivité (micro S/cm)')
    ax[0].set_ylabel('côte NGM (m)')
    ax[0].set_title('Pamandzi 1')
    ax[0].legend(loc='lower right')
    for p,d in zip(c2,md2):
        ax[1].plot(p[:,1],z0['P2']-p[:,0],'o-', label=d)
    ax[1].set_xlabel('Conductivité (micro S/cm)')
    ax[1].set_title('Pamandzi 2')
    ax[1].legend(loc='upper right')

    plt.savefig("figures/profils_conducti_pt.pdf",bbox_inches='tight')

if __name__ == '__main__':
    
    # conn = db_connect('Guadeloupe')
    # load_data("/home/metivier/Nextcloud/Recherche/GroundWater/islands/data/Guadeloupe/ades_export/Quantite/chroniques.txt",'chroniques',conn)

    etr = Turc(1086,24.5)
    print(1086-etr)

    # conn.close()
