###############################################################################################################
############################################# INITIAL DATABASES ############################################### 
###############################################################################################################

import pandas as pd
avion = pd.read_csv("path to avion.csv",encoding ='latin')
train = pd.read_csv("path to train.csv",encoding ='latin')
agents = pd.read_csv("path to agents.csv",encoding ='latin')

#agents['idENT_MEN'] = agents['idENT_MEN'].astype(str)

# We will link the nearest train station/airport to the department where the individuals lives.
# Thus, only agents living in departments with a train station and airport will remain in the database.
# For future works, we may also join individuals living in other departments to their nearest station.. 
# On va associer la garre/l'aeroport le plus proche au departement ou habite l'individu:
aeroport = avion[['City_dep','dpt_dep']].drop_duplicates()
agents = agents.merge(aeroport, left_on = 'DEP',right_on = 'dpt_dep')

# Creation des listes d'agents (A), de moyen de transport (O) et de trajet (T) 

A = list(agents['idENT_MEN'].astype(str))
O = ['train','avion'] # 2 moyen de transport

# City list
# Initialisation des villes
T = [] # les trajets # routes
Avion_time = [] # les temps de trajet en avion # time of travel with airplane
Train_time = [] # les temps de trajet en train # time of travel with train

for s in range(len(avion)):
        route = str(avion['dpt_dep'][s]) + '_' + str(avion['dpt_arr'][s])
        if route not in T:
            T.append(route)
            Avion_time.append(avion['Temps_voyage'][s])
            Train_time.append(train['Temps_voyage'][s])
            
            
# Covering all options agent/route/transport mode:
# Toutes les options agent/trajet/moyen de transport:
oat = []
for a in A:
    for t in T:
        for o in O:
            oat.append(a + '_' + t + '_' + o)  

del [route,a,t,s,o]

###############################################################################################################
################################### CHARACTERISTICS ENVIRONMENT ############################################## 
###############################################################################################################

# Caracteristiques de l'environment:

###### Price

def prix(ratio): 
    prix_train = train['Prix'].tolist()
    prix_avion = [item*ratio for item in prix_train] # rapport prix train/avion
    # Relative price of train/airplane. To be modified by the model.
    # Il sera peut être possible de faire varier le ratio du prix train/avion,
    # par exemple avec une taxe de l'état.
    
    prix = []
    for i in range(len(prix_train)):
        prix.append(prix_train[i])
        prix.append(prix_avion[i])   
    prix = prix*len(A)   
    
    cost  = dict(zip(oat, prix))
    
    
    rel_cost = []
    for i in range(0,len(oat),len(O)):
        rel_cost.append(cost[oat[i]] / (cost[oat[i]] + cost[oat[i+1]]))
        rel_cost.append(cost[oat[i+1]] / (cost[oat[i]] + cost[oat[i+1]]))
    return rel_cost

###### Time

def time(in_train = 0, in_avion = 0):
    Time_list=[]
    for i in range(len(Train_time)):
        Time_list.append(Train_time[i] - in_train)
        Time_list.append(Avion_time[i] - in_avion)
    Time_list = Time_list*len(A)
    
    
    time = dict(zip(oat, Time_list))
    
    rel_time = []
    for i in range(0,len(oat),len(O)):
        rel_time.append(time[oat[i]] / (time[oat[i]] + time[oat[i+1]]))
        rel_time.append(time[oat[i+1]] / (time[oat[i]] + time[oat[i+1]]))
    return rel_time

###### Co2 Emissions 

def co2(env_train=0 , env_avion = 0):
    co2_train = train['co2'].tolist()
    co2_avion = avion['co2'].tolist()
    
    co2 = []
    for i in range(len(co2_train)):
        co2.append(co2_train[i] - env_train)
        co2.append(co2_avion[i] - env_avion)   
    co2 = co2*len(A) 
    
    C02 = dict(zip(oat, co2))
    
    rel_C02 = []
    for i in range(0,len(oat),len(O)):
        rel_C02.append(C02[oat[i]] / (C02[oat[i]] + C02[oat[i+1]]))
        rel_C02.append(C02[oat[i+1]] / (C02[oat[i]] + C02[oat[i+1]]))
    return rel_C02

###############################################################################################################
####################################### CHARACTERISTICS AGENTS ################################################ 
###############################################################################################################

def carac_agents(agents):
    agents2 = agents.loc[agents.index.repeat(len(T)*len(O))]
    
    income = agents2['NIVIE10'].tolist()    
    
    time_flex = agents2['V2_OLDMTCH_E'].tolist()
    
    eco_aware = agents2['emission_co2'].tolist()
    #eco_aware = agents2['emission_co2_equi'].tolist()
    
    return income, time_flex,eco_aware

income, time_flex, eco_aware = carac_agents(agents)    

###############################################################################################################
######################################### DESCRIPTIVE STATISTICS ############################################# 
###############################################################################################################

import seaborn as sns

# Population characteristcs (in the paper)

#sns.set(style="darkgrid")
#ax = sns.barplot(x='DEP', y="PONDV1_x", data=agents,estimator=sum).set(title='Population (with ponderation) by department',xlabel='Departments')

#sns.set(style="darkgrid")
#ax = sns.countplot(x="DEP", data=agents).set(title='Population (no ponderation) by department',ylabel = 'Population size',xlabel='Departments')

agents.NIVIE10 = agents.NIVIE10.round(1)

#sns.set(style="darkgrid")
#ax = sns.barplot(x='NIVIE10', y="PONDV1_x", data=agents,estimator=sum, ci=None).set(title='Population (with ponderation) by income',ylabel = 'Population size',xlabel='Income level (decreasing)')


###############################################################################################################
############################################## SIMULATION ##################################################### 
###############################################################################################################

# Preparation of round 1: (3-4mins code)
oat_r1 = []
oat_idx = []
for j in range(len(A)):
    for l in range(len(oat)):
        if A[j] in oat[l] and agents.loc[j]['dpt_dep'].astype(str) in oat[l][12:14]:
            oat_r1.append(oat[l])
            oat_idx.append(l)

ind_idx = {}
for a in A:
    for j in range(len(oat_r1)):
        if a in oat_r1[j]:
            ind_idx[a] = j      

del [j,a,l]

def simulation(repetition, ratio,in_train,in_avion,env_train,env_avion,W_env=1,price_up=0,train_timein=0,avion_envin=0):
    rel_cost = prix(ratio)
    rel_time = time(in_train,in_avion)
    rel_C02 = co2(env_train,env_avion)
    
    rel_cost_r1 = [rel_cost[i] for i in oat_idx] 
    income_r1 = [income[i] for i in oat_idx] 
    rel_time_r1 = [rel_time[i] for i in oat_idx] 
    time_flex_r1 = [time_flex[i] for i in oat_idx] 
    rel_C02_r1 = [rel_C02[i] for i in oat_idx] 
    eco_aware_r1 = [eco_aware[i] for i in oat_idx] 
        
    # Score final du voyage par agent:
    
    # Ponderation des priorites politiques:
    W_cost = 1
    W_time = 1
    W_env = W_env
    
    Soat = []
    for i in range(len(oat_r1)):
        Disutility = W_cost * rel_cost_r1[i] * income_r1[i] + W_time * rel_time_r1[i] * time_flex_r1[i] + W_env * rel_C02_r1[i] * eco_aware_r1[i]
        Soat.append(Disutility)
    
    maxi = []
    choix = []
    for i in A:
        try:
            idx1 = idx2
            idx2 = ind_idx[i]
            maxi.append(min(Soat[idx1:idx2]))
            j+=1
            choix.append(Soat.index(maxi[j]))
        except:
            idx2 = ind_idx[i]
            idx1 = 0
            j = 0
            maxi.append(min(Soat[idx1:idx2]))
            choix.append(Soat.index(maxi[j]))
                    
    # Resultat final:
    choix_final = []
    for i in choix:
        choix_final.append(oat_r1[i])
    
    
    df_choix = pd.DataFrame(choix_final,columns=['trajet'])
    
    df_choix = df_choix.trajet.str.split(pat = '_',expand=True).rename(columns={0: "ident", 1: "dep", 2: "arr", 3: "mdt"})
    
    # Round 2 and more
    df_choix['ponderation'] = agents['PONDV1_x']
    
    nb_train = [round(df_choix.groupby(['mdt']).sum()['ponderation'][1])]
    nb_avion = [round(df_choix.groupby(['mdt']).sum()['ponderation'][0])]
    period = [1]

    ratio_par = 0
    intraintime = 0
    inavionenv = 0    

    
    dic={}
    del i

    for ppp in range(2,repetition):
        rel_cost = prix(ratio + ratio_par)
        rel_cost_r1 = [rel_cost[i] for i in oat_idx] 

        rel_time = time(in_train + intraintime ,in_avion)
        rel_time_r1 = [rel_time[i] for i in oat_idx] 

        rel_C02 = co2(env_train,env_avion + inavionenv)
        rel_C02_r1 = [rel_C02[i] for i in oat_idx] 

       
        Soat2 = []
        for i in range(len(oat_r1)):
            Disutility = Soat[i] + W_cost * rel_cost_r1[i] * income_r1[i] + W_time * rel_time_r1[i] * time_flex_r1[i] + W_env * rel_C02_r1[i] * eco_aware_r1[i]
            Soat2.append(Disutility)        
        
        maxi = []
        choix = []
        for i in A:
            try:
                idx1 = idx2
                idx2 = ind_idx[i]
                maxi.append(min(Soat2[idx1:idx2]))
                j+=1
                choix.append(Soat2.index(maxi[j]))
            except:
                idx2 = ind_idx[i]
                idx1 = 0
                j = 0
                maxi.append(min(Soat2[idx1:idx2]))
                choix.append(Soat2.index(maxi[j]))
                        
        # Resultat final:
        choix_final3 = []
        for i in choix:
            choix_final3.append(oat_r1[i])
    
    
        col_name = 'trajet' + str(ppp)
        id_name = 'ident' + str(ppp)
        dep_name = 'dep' + str(ppp)
        arr_name = 'arr' + str(ppp)
        mdt_name = 'mdt' + str(ppp)  
        df_choix[col_name] = pd.Series(choix_final3)
    
        dic[ppp] = df_choix[col_name].str.split(pat = '_',expand=True).rename(columns={0: id_name, 1: dep_name, 2: arr_name, 3: mdt_name})
        dic[ppp]['ponderation'] = agents['PONDV1_x']
        nb_train.append(round(dic[ppp].groupby([mdt_name]).sum()['ponderation'][1]))
        nb_avion.append(round(dic[ppp].groupby([mdt_name]).sum()['ponderation'][0]))
        period.append(ppp)
        ratio_par = ratio_par + price_up
        intraintime = intraintime + train_timein
        inavionenv = inavionenv + avion_envin

        Soat = Soat2
    return nb_train,nb_avion,period
    
# Scenario 1
nb_train,nb_avion,period = simulation(30,1.5,0,0,0,0,W_env=0.35,price_up=0.05)


count = pd.DataFrame(list(zip(nb_train,nb_avion,period)),columns=['Train','Airplane','period'])
sns.set(style="darkgrid")

df_melted = count.melt("period",var_name="Transport mode",value_name="value")
ax = sns.scatterplot(data=df_melted, x="period", y="value",hue='Transport mode').set(title='Transport choice evolution (scenario 1)',ylabel = 'Population size',xlabel='Period')

# Scenario 2

nb_train2,nb_avion2,period2 = simulation(20,1.5,0,0,0,0,W_env=0.35,train_timein=3)

count2 = pd.DataFrame(list(zip(nb_train2,nb_avion2,period2)),columns=['Train','Airplane','period'])
sns.set(style="darkgrid")

df_melted2 = count2.melt("period",var_name="Transport mode",value_name="value")
ax = sns.scatterplot(data=df_melted2, x="period", y="value",hue='Transport mode').set(xlim=(0,20),title='Transport choice evolution (scenario 2)',ylabel = 'Population size',xlabel='Period')