from tkinter import *
import numpy as np

import nltk
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords

from nltk.collocations import BigramCollocationFinder
from langdetect import detect_langs

try:
    from nltk import wordpunct_tokenize
    from nltk.corpus import stopwords
except ImportError:
    print('[!] You need to install nltk (http://nltk.org/index.html)')


# ----------------------------------------------------------------------
def _calculate_languages_ratios(text):
    languages_ratios = {}

    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]

    # Compute per language included in nltk number of unique stopwords appearing in analyzed text
    for language in stopwords.fileids():
        stopwords_set = set(stopwords.words(language))
        words_set = set(words)
        common_elements = words_set.intersection(stopwords_set)

        languages_ratios[language] = len(common_elements)  # language "score"

    return languages_ratios


# ----------------------------------------------------------------------
def detect_language(text):
    ratios = _calculate_languages_ratios(text)

    most_rated_language = max(ratios, key=ratios.get)

    return most_rated_language



                                ######################################
                                ###faire apprendre notre modele ######
                                ######################################

# construire la liste globale des mots de toutes les langues contenues dans le fichier apprentissage
words_list=[]
for line in open('apprentissage.txt'):
    phrase=list(line.split('_'))
    tokens = wordpunct_tokenize(phrase[1])
    words = [word.lower() for word in tokens]
    words_list.append(words)
liste_globale=sum(words_list,[])




class Neural_Network(object):
  def __init__(self,lenght):
    #parameters
    self.inputSize = lenght
    self.outputSize = 1
    self.hiddenSize = 3

    #weights
    self.W1 = np.random.randn(self.inputSize, self.hiddenSize)
    self.W2 = np.random.randn(self.hiddenSize, self.outputSize)

  def forward(self, X):
    #forward propagation through our network
    self.z = np.dot(X, self.W1) # dot product of X (input)
    self.z2 = self.sigmoid(self.z) # activation function
    self.z3 = np.dot(self.z2, self.W2) #
    o = self.sigmoid(self.z3) # final activation function
    return o

  def sigmoid(self, s):
    # activation function
    return 1/(1+np.exp(-s))






tableau={}
def training_neuronne():
    for line in open('apprentissage.txt'):
        NN = Neural_Network(len(liste_globale))
        poid=[]
        X = []
        langue=['por','ita','spa','fra']
        y=[0,0,0,0]    #y= [1, 0, 0, 0]
        phrase = list(line.split('_'))
        y[langue.index(phrase[0])]=1
        tokens = wordpunct_tokenize(phrase[1])
        words = [word.lower() for word in tokens]
        for ele in liste_globale:
            if ele in words:
                X.append(1)
            else:
                X.append(0)


        X = np.array(X, dtype=float) #[1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
        er=NN.W1.tolist()
        et=NN.W2.tolist()
        poid.append(er)
        poid.append(et)

        tableau[float(NN.forward(X))]=list(poid)


# a partir des donnees des test on a recupere les poids qui peuvent nous donner une meilleure prédiction
def meilleur_poids(tableau):
    sorted_key = list(reversed(sorted(tableau.keys())))
    return tableau[sorted_key[0]]

                                    ######################################
                                    ###   la partie graphique       ######
                                    ######################################


# a partir des donnes des test on a recupere les poids qui peuvent nous donner une meilleur prédiction

def essais():
  valeur=sais.get("1.0","end-1c") #<======
  language = detect_language(valeur)
  language1=detect_langs(valeur)
  resultat="le Texte Saisi est : "+str(language)+"\t"+str(language1)
  Texte.set(resultat)

def training():
    training_neuronne()
    meiller_poid=meilleur_poids(tableau)

def sigmoid( s):
    # activation function
    return 1 / (1 + np.exp(-s))
def predire(X):

    inputSize = len(liste_globale)
    outputSize = 1
    hiddenSize = 3

    #weights
    W1 = np.array(meilleur_poids(tableau)[0])
    W2 = np.array(meilleur_poids(tableau)[1])
    #forward propagation through our network
    z = np.dot(X, W1) # dot product of X (input) and first set of 3x2 weights
    z2 = sigmoid(z) # activation function
    z3 = np.dot(z2, W2) #
    o = sigmoid(z3) # final activation function
    return o

def prediction():
    X = []
    langue = ['french', 'spanish', 'italian','portuguese']
    y = [0, 0, 0, 0]
    valeur = sais.get("1.0", "end-1c")
    y[langue.index(detect_language(valeur))] = 1
    tokens = wordpunct_tokenize(sais.get("1.0","end-1c"))
    words = [word.lower() for word in tokens]
    for ele in liste_globale:
        if ele in words:
            X.append(1)
        else:
            X.append(0)
    X=np.array(X)
    predict=predire(X)
    resultat1="la partie prédite par notre modèle est:"+str(predict)+"\n"
    #resultat1+="la partie perdu est : " + str(np.mean(np.square(y - predict)))
    resultat1+="la langue détéctée par le Réseau de Neuronne: "+detect_language(valeur)
    Texte1.set(resultat1)


def tester():
    fichier = open('resultat_.txt', 'w')
    for line in open('test.txt'):
        X = []
        phrase = list(line.split('_'))
        tokens = wordpunct_tokenize(phrase[1])
        for ele in liste_globale:
            if ele in tokens:
                X.append(1)
            else:
                X.append(0)
        X = np.array(X)
        predict = predire(X)
        phras=phrase[1].replace('\n','')

        resultat=''.join(phras)+'.........'+str(detect_language(phrase[1]))+"......"+str(predict)+'\n'
        fichier.write(resultat)




fenetre=Tk()
fenetre.geometry('600x350')
fenetre.title("Projet IA")

saisir=StringVar()
Texte=StringVar()
Texte1=StringVar()


afficher=Label(fenetre, text = "SVP saisir votre TEXTE : ",width=120)
afficher.pack()

sais=Text(fenetre,width=60,height=10)

sais.pack()
bouton= Button(fenetre, text='valider', command= essais)
bouton.pack()
reponse=Label(fenetre, textvariable = Texte,width=200)
reponse.pack()
bouton1= Button(fenetre, width=10,text='TRAINING', bg='turquoise',command= training)
bouton1.pack(side=LEFT)

bouton3= Button(fenetre,width=10, text='Test', command= tester)
bouton3.pack(side=LEFT)

bouton2= Button(fenetre,width=10, text='Prediction', command= prediction)
bouton2.pack(side=LEFT)


reponse1=Label(fenetre, textvariable = Texte1,width=120)
reponse1.pack()

bouton_quitter = Button(fenetre, width=15,text="Quitter", command=fenetre.quit)
bouton_quitter.pack(side=RIGHT)
fenetre.mainloop()

