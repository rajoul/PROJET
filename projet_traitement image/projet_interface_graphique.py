from tkinter import *
from tkinter import filedialog
import tkFileDialog
from PIL import ImageTk,Image
import string
from Crypto.Cipher import AES

global longueur

key='1234567890abcdef'
def padding(byte):
	if len(byte)<8:
		return (8-(len(byte)))*'0'+str(byte)
	return byte
def padd(message,taille_block=16):
	return message[:taille_block*(len(message)//taille_block)]

def encrypt_AES(data):
	obj = AES.new(key, AES.MODE_ECB)
	#texte=padd(data)
	return obj.encrypt(data[:(len(data)//16)*16])

def decrypt_AES(data):
	obj = AES.new(key, AES.MODE_ECB)
	return obj.decrypt(data)


def encode_in_pixel(byte, pixel):
    """Encodes a byte in the three least significant bits of each channel.
    """
    x=bin(byte)[2:]
    byte=bin(byte)[2:]
    byte=padding(byte)
    r = int(byte[:3],2)
    g = int(byte[3:6],2)
    b = int(byte[6:],2)

    color = (r+(pixel[0]&248),\
             g+(pixel[1]&248),\
             b+(pixel[2]&252))
    return color

def decode_in_pixel(pixel):
	a=padding(bin(pixel[0])[2:])
	b=padding(bin(pixel[1])[2:])
	c=padding(bin(pixel[2])[2:])
	r=a[5:]+b[5:]+c[6:]

	return chr(int(r,2))

def encode_file(image,pixel,data):

	for i in range(len(data)):
	        coords = (i%image.width, i/image.width)

	        byte = ord(data[i])

	        pixel[coords[0], coords[1]] = encode_in_pixel(byte, pixel[coords[0],\
	                                                            coords[1]])
	image.save("image_surcharge_file.png", "PNG")
def encode_image(image,pixel,data):

	for i in range(len(data)):
	        coords = (i%image.width, i/image.width)

	        byte = ord(data[i])

	        pixel[coords[0], coords[1]] = encode_in_pixel(byte, pixel[coords[0],\
	                                                            coords[1]])
	image.save("image_surcharge_img.png", "PNG")



def decode_img(image,pixel,lenght):
	
	data=""
	fau=0
	for i in range(lenght):
	        coords = (i%image.width, i/image.width)

	        valeur=decode_in_pixel(pixel[coords[0], coords[1]])
	        data+=valeur
	return data
def decode_file(image,pixel,lenght=2320):
	
	data=""
	fau=0
	for i in range(lenght):
	        coords = (i%image.width, i/image.width)

	        valeur=decode_in_pixel(pixel[coords[0], coords[1]])
	        data+=valeur
	return data
def enc_dec_file(im,px,file):

	ciphertexte=encrypt_AES(file)
	encode_file(im,px,ciphertexte)
	longueur=len(ciphertexte)
	print longueur
	

def enc_dec_image(im,px,data,im1):
	r=""
	for i in range(len(data)):
		r+=data[i]
	
	ciphertexte=encrypt_AES(r)
	encode_image(im,px,ciphertexte)
	longueur = len(ciphertexte)
	print len(ciphertexte)

	



def UploadAction(event=None):
    filename = tkFileDialog.askopenfilename()
    sais.insert(INSERT,filename)

def valider():
    valeur = sais.get("1.0", "end-1c")
    im = Image.open(valeur)
    px=im.load()
    valeur1 = sais1.get("1.0", "end-1c")
    my_file=open(valeur1).read()
    if '.txt' in valeur1:
    	enc_dec_file(im,px,my_file)
    else:
    	im1 = Image.open(valeur1)
    
    	enc_dec_image(im,px,my_file,im1)

def UploadAction1(event=None):
    filename = tkFileDialog.askopenfilename()
    sais1.insert(INSERT,filename)

def UploadAction2(event=None):
    filename = tkFileDialog.askopenfilename()
    sais2.insert(INSERT,filename)

def valid_dec():
	valeur = sais2.get("1.0", "end-1c")
	print longueur
	if 'file' in valeur:
		im1 = Image.open('image_surcharge_file.png')
		px1 = im1.load()
		t=decode_file(im1,px1)
		plaintexte=decrypt_AES(t)
		t=open('extract_file.txt','w')
		t.write(plaintexte)
	else:
		im1 = Image.open('image_surcharge_img.png')
		print im1.width*im1.height
		px1 = im1.load()
		t=decode_img(im1,px1,63056)

		plaintexte=decrypt_AES(t)
		g=open('recup.png','wb')
		g.write(plaintexte)
	
	
	
longueur=0

fenetre=Tk()
fenetre.geometry('850x480')
fenetre.title("Application Stegano")
#fenetre.configure(bg='dark sea green')
background_image = PhotoImage("/root/Desktop/projet_traitement_image/realisation/dd.jpg")
background_label = Label(fenetre, image=background_image)
background_label.place(x=0,y=0)
afficher=Label(fenetre, text = "SVP inserer Cover: ",width=17)
afficher.place(x=0,y=0)
sais=Text(fenetre,width=30,height=5)
sais.place(x=25,y=24)
button = Button(fenetre, text='Browse', command=UploadAction,bg='dark sea green')
button.place(x=170,y=150)
button1 = Button(fenetre, text='Hide', command=valider,bg='dark sea green')
button1.place(x=360,y=188)

afficher=Label(fenetre, text = "SVP inserer image secrete: ",width=27)
afficher.place(x=370,y=0)
sais1=Text(fenetre,width=30,height=5)
sais1.place(x=410,y=24)
button2= Button(fenetre, text='Browse', command=UploadAction1,bg='dark sea green')
button2.place(x=490,y=150)

afficher=Label(fenetre, text = "Extraction",width=27)
afficher.place(x=200,y=250)
sais2=Text(fenetre,width=40,height=5)
sais2.place(x=220,y=274)
button3= Button(fenetre, text='Browse', command=UploadAction2,bg='dark sea green')
button3.place(x=320,y=405)
button4= Button(fenetre, text='Extract', command=valid_dec,bg='dark sea green')
button4.place(x=480,y=405)



fenetre.mainloop()
