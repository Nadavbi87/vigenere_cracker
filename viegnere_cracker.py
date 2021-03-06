from itertools import starmap,cycle
from collections import Counter
import numpy as np
import sys


def encryptMsg(plainText ,key ):
	"""encrypting plain text with given key """
	return "".join(starmap(lambda x ,y: chr(((ord(x) + ord(y)) % 26) + ord('A')), zip(plainText, cycle(key))))
	

def decryptMsg(chiperText ,key ):
	"""decrypting chiper text with given key"""
	return "".join(starmap(lambda x ,y: chr(((ord(x) - ord(y)) % 26) + ord('A')), zip(chiperText, cycle(key))))


def letterFreq(chiperText):
	"""Calculate text histogram"""
	return Counter(chiperText)

def indexOfCoincidence(subChiperText):
	"""Calculate index of coincidence in text"""
	N = len(subChiperText)
	C = 26.0
	lF = letterFreq(subChiperText)
	deno = float((N*(N-1))/C)
	
	fSum = 0.0
	for a in lF:
		fSum += float((lF[a]*(lF[a]-1)))
	#if the len of subChiperText is 1 so the deno will be zero 	
	if(deno == 0 ):
		return 0.0
	return fSum/deno

def possibleKeyLenght(chiperText):
	"""Calculate possible key lenght  - with predict value of 1.73"""
	pkl = {}
	possibleKeyLen = []
	for i in range(1,16):
		
		iCAvg = 0.0
		IC = 0.0
		for j in range(i):
			
			subString =''
			for s in range(len(chiperText)):
				if(s%i == j):

					subString+=chiperText[s]
			
			IC +=  indexOfCoincidence(subString)	
		iCAvg = IC/float(i)
		pkl[i] = iCAvg

	
	
	
	predict = 1.73
	for i  in pkl.copy():
		if(abs(pkl[i] - 1.73) < 0.20 ):
			possibleKeyLen.append(i)
	
	
	return possibleKeyLen

def splitForColumns(chiperText  , colLenght):
	"""split the chiper text for rows in size of given key lenght ,and transpose them into columns"""
	subs = []
	n = colLenght
	subs = np.array(["".join(chiperText[i:i+n]) for i in range(0, len(chiperText), n)])
	s =[]
	preLenght = subs[0]
	pieces = []

	for i in range(n):
		piece = ""
		for j in range(len(subs)):
			try:
				piece+=subs[j][i]
			except IndexError:
				piece+=""
		pieces.append(piece)
	return pieces




def possibleKey(cols):
	"""compute possible key for given columns from the chiper text"""

	engLetterFreqs = { 'A' : 8.167 ,'B' : 1.492,'C' : 2.782, 'D' : 4.253, 'E' : 12.702, 'F' : 2.228,'G' : 2.015,'H' : 6.094,'I' : 6.966,'J' : 0.153,'K' : 0.772,'L' : 4.025,'M' : 2.406,'N' : 6.749,'O' : 7.507,'P' : 1.929,'Q' : 0.095,'R' : 5.987,'S' : 6.327,'T' : 9.056,'U' : 2.758,'V' : 0.978,'W' : 2.361,'X' : 0.150,'Y' : 1.974,'Z' : 0.074 }
	letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	key=''
	for i in cols:
		res=[]
		
		for j in letters:
			
			dec = decryptMsg(i ,j)
			freqs = letterFreq(dec)
			X = 0.0
			
			#for k in freqs:
			#	freqs[k] = float(freqs[k] * 100)/float(len(i))
			
			for l in freqs:
				X+= float((freqs[l])*engLetterFreqs[l]*100)/float(len(i))
			res.append((j,X))
		
		
		key+= max(res , key=lambda x: x[1])[0]
	return key
		

def vigenereDecrypt(chiper):
	"""get chiper text and decrypting it"""
	sChiper = ''.join(filter(str.isalpha, chiper)).upper()
	keysLenght = possibleKeyLenght(sChiper)
	print("Possible key lenght are :" , keysLenght)
	for i in keysLenght:
		sCols = splitForColumns(sChiper , i)
		key = possibleKey(sCols)
		decryptMessage = decryptMsg(sChiper , key)
		print('for key in lenght : ' , i)
		print('possible key is :' , key)
		print('message is :' , decryptMessage)


def getMessageFromFile(filePath):
    """read file that contains the chiper message and return the message"""
    with open(filePath, 'r') as f:
        contents = f.read()
    return contents
 
        
if __name__ == '__main__':
    try:
        filePath = sys.argv[1]
        encryptedMessage = getMessageFromFile(filePath)
        if encryptedMessage != None and len(encryptedMessage) > 0 :
            vigenereDecrypt(encryptedMessage)
        else:
            print("Empty message")
    except IndexError:
        print ("Please provide file that contains the chiper")
    except Exception as e :
        print (e)