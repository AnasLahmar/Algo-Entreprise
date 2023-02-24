import streamlit as st
import json
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 
import allfunction as all
import random


#==============================================Start=============================================================
#=======================================define All function needed=========================================
def FT2(inp):
    return (inp[0]**2 + inp[1]**2)
def Easom(x):
    y = -np.cos(x[0]) * np.cos(x[1]) * np.exp(-(x[0]-np.pi)**2 - (x[1]-np.pi)**2)
    return y
def Eggholder(x):
    term1 = -(x[1] + 47) * np.sin(np.sqrt(abs(x[1] + x[0]/2 + 47)))
    term2 = -x[0] * np.sin(np.sqrt(abs(x[0] - (x[1] + 47))))
    y = (term1 + term2) / 100
    # optimum at (512, 404.2319), cost value -959.6407
    return y
def Rosenbrock(x):
    y = (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2
    # optimum at (1, 1), cost value 0
    return y
def Rastrigin(x):
    y = 20 + (x[0]**2 - 10*np.cos(2*np.pi*x[0])) + (x[1]**2 - 10*np.cos(2*np.pi*x[1]))
    # optimum at (0, 0), cost value 0
    return y





# Interface Application------------------------------------------------------------------------------------------
st.write(""" ## Algorithmes pour la décision en entreprise""")

selected=option_menu(
    menu_title="Main Menu",
    options=["Home","Essaims Particuliers","Recuit simulé"],
    icons=["house","bar-chart"],
    menu_icon="cast",  # optional
    default_index=0,
    orientation="horizontal",  
    styles={
        "nav-link-selected": {"background-color": "#4B9DFF"},
    } 

     )
   

#========================================================Accueil===========================================
if selected=="Home":
    # creer une animation
    def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)
    lottie_coding = load_lottiefile("pc.json")  # replace link to local lottie file
    st_lottie(
    lottie_coding,
    speed=1,
    reverse=False,
    loop=True,
    quality="low", # medium ; high

    height=None,
    width=None,
    key=None,
)
#======================================================Data Overview=======================================
if selected=="Recuit simulé":
    with st.sidebar:
    # creer une animation
    # Creer un slider
        def load_lottiefile(filepath: str):
                with open(filepath, "r") as f:
                    return json.load(f)
        lottie_coding = load_lottiefile("data.json")  # replace link to local lottie file
        st_lottie(lottie_coding,speed=1,reverse=False,loop=True,quality="high",height=150, width=None, key=None,)
    # Declarer les variables------------------------------------------------------------------------------------------
    
    
    st.sidebar.write("Nombre de villes")
    N = st.sidebar.number_input("N", min_value=1, value=50)

    st.sidebar.write("Choix de la forme")
    forme=st.sidebar.selectbox("Forme",["Select","Cercle","Carré"])
    random.seed(10)

    # Choice of city typology *****************************************************
    # Arranged on a circle if Cercle = True, otherwise random on a square Cercle = False
    Cercle="Cercle"
    Caree="Carré"
    if Cercle==forme:
        st.success("Vous avez sélectionné la forme {} avec un nombre de villes égale à {}".format(forme,N))
        rad = [random.random() * 2 *np.pi for i in range(N)]
        xpos = [np.cos(r) for r in rad]
        ypos = [np.sin(r) for r in rad]
    elif Caree==forme:
        st.success("Vous avez sélectionné la forme {} avec un nombre de villes égale à {}".format(forme,N))
        # x and y coordinates of city positions on a square -1,1
        xpos = [2 * random.random() - 1 for i in range(N)]
        ypos = [2 * random.random() - 1 for i in range(N)]
    else: 
         st.info("Selectionné une forme pour tester !")
    # Calculate Euclidean distances between cities
    if Cercle==forme or Caree==forme:
        dx2 = np.square(np.subtract.outer(xpos, xpos))
        dy2 = np.square(np.subtract.outer(ypos, ypos))
        distance = np.sqrt(dx2 + dy2)
        col1, col2 = st.columns(2)
    
        if col1.checkbox("Régler les parametres du RS :"):
        
            Temp = col1.slider("Temp : ", 0, 100, 10)
            TempGel = col1.slider("TempGel : ", 0.0001, 10.0,step=0.0001, format="%.4f")
            alpha = col1.slider("alpha : ", 0.0, 10.0, 0.99)
            kEquil = col1.slider("kEquil : ", 0, 100, 20)
             #====================================================================
            # define Button style
            m = st.markdown("""
                <style>
                div.stButton > button:first-child {
                    background-color: #0099ff;
                    color:#ffffff;
                }
                div.stButton > button:hover {
                    background-color: #00ff00;
                    color:#ff0000;
                    }
                </style>""", unsafe_allow_html=True)
        #=====================================================================
            button=col2.button("Run")
            if button:
                cas=6
                np.random.seed(cas)
                Cycle = np.linspace(1, N, N, dtype=int).reshape(-1,1)
                a=all.Eval(distance,Cycle,N)
                cycleV=all.Voisin(Cycle,N)
                V=all.Prendre(5,4,1)
                T=all.palier(3,6)
            
                CoutCourant = all.Eval(distance,Cycle,N)
                CoutMeilleur=CoutCourant
                CycleMeilleur=Cycle
                #all.plotGraf(CycleMeilleur,xpos,ypos)
                import time
                start = time.time()
                ci = 1
                cp = 1
                Tabcout = []
                Tabtemp = []
                Tabaccep = []

                while Temp > TempGel:
                    drap = 0
                    for g in range(kEquil): # Boucle sur l'équilibre
                        Candidat = all.Voisin(Cycle, N)
                        CoutCandidat = all.Eval(distance, Candidat, N)
                        if all.Prendre(CoutCandidat, CoutCourant, Temp) == True:
                            Cycle = Candidat
                            CoutCourant = CoutCandidat
                            drap = drap + 1
                        if CoutCourant < CoutMeilleur:
                            CoutMeilleur = CoutCourant
                            CycleMeilleur = Cycle
                            #all.plotGraf(CycleMeilleur, xpos, ypos)
                        Tabcout.append(CoutCourant)
                        Tabtemp.append(Temp)
                        ci = ci + 1
                    Tabaccep.append(drap / kEquil)
                    cp = cp + 1
                    Temp = all.palier(Temp, alpha)

                temps_calcul = time.time() - start
                cycle=CycleMeilleur            
                graf = np.concatenate((cycle, [cycle[0]]))
                xpos_=np.array(xpos)
                ypos_=np.array(ypos)
                fig=plt.figure(figsize=(5,5))
                plt.plot(xpos_[graf[:,0]-1], ypos_[graf[:,0]-1])
                plt.title('Chemin le meilleur obtenu')
                st.set_option('deprecation.showPyplotGlobalUse', False)
                col2.pyplot(fig)
                st.success("Le temps de calcul est : {}s".format(round(temps_calcul,2)))
                st.success("Distance optimisée est : {} (unité)".format(round(CoutMeilleur[0],2)))
                st.write(''' ### Visualisez les courbes suivantes''')
                cl1,cl2=st.columns(2)
                fig=plt.figure(figsize=(6,6))
                plt.plot(Tabaccep)
                plt.xlabel('PALIERS')
                plt.ylabel('TAUX')
                plt.title('Evolution du taux d''acceptation')
                st.set_option('deprecation.showPyplotGlobalUse', False)
                cl1.pyplot(fig)
                
                fig=plt.figure(figsize=(5,4))
                plt.plot(Tabtemp)
                plt.xlabel('ITERATIONS')
                plt.ylabel('TEMPERATURE')
                plt.title('Evolution de la température')
                st.set_option('deprecation.showPyplotGlobalUse', False)
                cl2.pyplot(fig)
                
                fig=plt.figure(figsize=(10,6))
                plt.plot(Tabcout)
                plt.xlabel('ITERATIONS')
                plt.ylabel('COÛT')
                plt.title('Evolution de la fonction coût')
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot(fig)


#========================================================================================
#============================================ESSAIMS======================================

if selected=="Essaims Particuliers":
    with st.sidebar:
        # creer une animation
        def load_lottiefile(filepath: str):
                with open(filepath, "r") as f:
                    return json.load(f)
        lottie_coding = load_lottiefile("data.json")  # replace link to local lottie file
        st_lottie(lottie_coding,speed=1,reverse=False,loop=True,quality="high",height=150, width=None, key=None,)
    st.write("Sélectionnez une fonction")
    function_dict = {
    "FT2": FT2,
    "Easom": Easom,
    "Rastrigin": Rastrigin,
    "Rosenbrock": Rosenbrock,
    "Eggholder": Eggholder
            }
    # Finally, you can use the function names in the selectbox to retrieve the corresponding function object from the dictionary:
    function_name = st.selectbox("Select", ["Select function","FT2", "Easom", "Rastrigin", "Rosenbrock", "Eggholder"])
    if function_name!="Select function":
        selected_function = function_dict[function_name]
        #function=st.selectbox("Select",["FT2","Easom","Rastrigin","Rosenbrock","Eggholder"])
        st.success("Parfait, vous avez choisi la fonction {}".format(function_name))
        # Define the list of options for the radio button
        options = ['Fonction', 'Déplacement des particules']

        # Display the radio button
        selected_option = st.sidebar.radio('Visualisez :', options)
        def Cout(in_):
            return selected_function(in_)

        def vis3D(DemiLongueur, num_points):
            fig=plt.figure(figsize=(10,6))
            ax = plt.axes(projection='3d')
            x = np.linspace(-DemiLongueur, DemiLongueur, num_points)
            y = np.linspace(-DemiLongueur, DemiLongueur, num_points)
            X, Y = np.meshgrid(x, y)
            Z = Cout([X, Y])
            ax.contour3D(X, Y, Z, 100, cmap='jet')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            st.set_option('deprecation.showPyplotGlobalUse', False)
            c2.pyplot(fig)
        if selected_option=='Fonction':
            c1,c2=st.columns(2)
            c1.write(" ")
            c1.write(" ")
            c1.write(" ")
            DemiLongueur=c1.number_input("DemiLongueur",min_value=0,max_value=1000,value=10)
            num_points=c1.number_input("num_points",min_value=0,max_value=1000,value=100)
            vis3D(DemiLongueur, num_points)
        if selected_option=='Déplacement des particules':
            def plotF(DemiLongueur, nb_points):
                x = np.linspace(-DemiLongueur, DemiLongueur, nb_points)
                y = np.linspace(-DemiLongueur, DemiLongueur, nb_points)
                X, Y = np.meshgrid(x, y)
                Z = Cout([X, Y])
                plt.contourf(X, Y, Z, cmap='turbo')
                plt.colorbar()
            
            # Constants
            c1,c2=st.columns(2)
            N = c1.slider("Number of particles",min_value=0,max_value=200,value=10)  # number of particles
            TF = c1.slider("Number of generations",min_value=0,max_value=200,value=5)  # number of generations
            I=c1.slider("Inertie",min_value=0.0,max_value=1.0,value=0.5)
            i=c2.slider("Individualist partition",min_value=0,max_value=20,value=2)
            g=c2.slider("Social partition",min_value=0,max_value=20,value=2)
            DemiLongueur1=c2.slider("DemiLongueur",min_value=0,max_value=1000,value=10)
            
            Vmax = DemiLongueur1 / 2  # maximum admissible speed
            # Initialize particle swarm parameters
            inertia = I #np.random.uniform(0.2, 1)  # randomly chosen between 0 and 1
            a_best_i = i  # 2  # individualist partition
            a_best_g = g  #2  # social partition
            fig=plt.figure(figsize=(12,8))
            plotF(DemiLongueur1, 100)
            # Initialize positions and velocities and calculate cost
            # = DemiLongueur * (2 * np.random.rand(N, 2) - 1)
            # = Vmax * np.random.rand(N, 2) / 4
            X = np.random.uniform(low=-8, high=8, size=(N, 2))
            V = np.zeros((N, 2))
            F = np.array([Cout(x) for x in X])  # calculate initial cost
            Fi = F
            Xi = X
            best_fit_index = np.argmin(Fi)
            best_fit = Fi[best_fit_index]
            XG = np.ones((N, 2)) * X[best_fit_index, :]
            FG = best_fit

            # Plot initial values
            plt.scatter(X[:,0], X[:,1], color='red', s=50, edgecolors='red', facecolors='white', marker='o')
            plt.plot(XG[0, 0], XG[0, 1], '.r')
            c01,c02=st.columns(2)
            df = pd.DataFrame(columns=['X','Y','FG'])
            # Loop over generations
            for t in range(TF):
            
                ri = np.random.rand()
                rg = np.random.rand()
                V = inertia * V + a_best_i * ri * (Xi - X) + a_best_g * rg * (XG - X) # Calcul vitesse
                V[:,0] = np.sign(V[:,0]) * np.minimum(np.abs(V[:,0]), np.ones((1, N)).T[0] * Vmax)
                V[:,1] = np.sign(V[:,1]) * np.minimum(np.abs(V[:,1]), np.ones((1, N)).T[0] * Vmax)
                D = DemiLongueur1 * np.sign(V) - X
                X = X + D + (V - D) * np.sign(D - V) * np.sign(V)
                V = V * np.sign(D - V) * np.sign(V)
                proba = 0
                for i in range(N):
                    F[i] = Cout(X[i,:])
                    if F[i] < Fi[i]:
                        Fi[i] = F[i]
                        Xi[i,:] = X[i,:]
                        proba = proba + 1/N
                    if F[i] < FG:
                        FG = F[i]
                        XG = np.ones((N,2)) * X[i,:]
                #inertia = proba
                #inertia = inertia * (1.0002)**(-t)
                plt.scatter(X[:,0], X[:,1], color='red', s=50, edgecolors='red', facecolors='white', marker='o')
                plt.plot(XG[0], XG[1], '.r')
                df = df.append({'X': XG[0,0],'Y':XG[0,1],'FG':FG}, ignore_index=True)
               
            c01.write(df)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            c02.pyplot(fig)
            st.write(""" #### Variation de la fonction coût""")
            fig=plt.figure(figsize=(10,6))
            plt.plot(df['FG'])
            plt.title("Evolution de la fonction coût en fonction des générations")
            plt.ylabel('FG')
            plt.xlabel('Nombre de génération')
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot(fig)


          








        #============================================FIN=========================================================
       