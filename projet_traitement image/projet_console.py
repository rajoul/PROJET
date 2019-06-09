from PIL import Image
import string
from Crypto.Cipher import AES



key='1234567890abcdef'

def padding(byte):
	if len(byte)<8:
		return (8-(len(byte)))*'0'+str(byte)
	return byte
def padd(message,taille_block=16):
	return message[:taille_block*(len(message)//taille_block)]

def encrypt_AES(data):
	obj = AES.new(key, AES.MODE_ECB)
	texte=padd(data)
	return obj.encrypt(texte)

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

def encode(image,pixel,data):

	for i in range(len(data)):
	        coords = (i%image.width, i/image.width)

	        byte = ord(data[i])

	        pixel[coords[0], coords[1]] = encode_in_pixel(byte, pixel[coords[0],\
	                                                            coords[1]])
	image.save("image_surcharge.png", "PNG")



def decode(image,pixel,lenght):
	
	data=""
	fau=0
	for i in range(lenght):
	        coords = (i%image.width, i/image.width)

	        valeur=decode_in_pixel(pixel[coords[0], coords[1]])
	        data+=valeur
	return data
	
def enc_dec_file(file):

	ciphertexte=encrypt_AES(file)
	encode(im,px,ciphertexte)

	im1 = Image.open('image_surcharge.png')
	px1 = im1.load()

	t=decode(im1,px1,len(ciphertexte))
	plaintexte=decrypt_AES(t)
	t=open('extract_file.txt','w')
	t.write(plaintexte)

def enc_dec_image(data):
	r=""
	for i in range(im.width*im.height):
		r+=data[i]
	ciphertexte=encrypt_AES(r)
	encode(im,px,ciphertexte)
	im1 = Image.open('image_surcharge.png')
	px1 = im1.load()
	t=decode(im1,px1,len(ciphertexte))
	plaintexte=decrypt_AES(t)
	g=open('recup.png','wb')
	g.write(plaintexte)

im = Image.open('image_original.png')
px = im.load()
my_file=open('file.txt').read()
enc_dec_file(my_file)

# data=open('a_cacher.png').read()
# enc_dec_image(data)