#!/usr/bin/env python3

# create table users (
#     -> id int primary key not null auto_increment,
#     -> username varchar(320),
#     -> password varchar(60),
#     -> NaCl varchar(30)
#     -> );

import mysql.connector
from config import MYSQL
from Crypto.Cipher import AES
from Crypto import Random

dbEntries = []		# User objects
decryptHashes = []  # To Decrypt
encryptedPW = []	# Final product

cnx = mysql.connector.connect (
	user = MYSQL.user,
	password = MYSQL.password,
	host = MYSQL.host,
	database = MYSQL.database)

cursor = cnx.cursor()

class Scramble:
	"""	Every row on the database is passed througinh this scrambled object.
	Uname and Pword length are taken. Each character is then rotated in a
	caesar cipher fasion, correlating to the UTF-8 character codes. 
	The iv is generated using the Crypto random module. """

	def __init__(self, uname, pword, salt):
		self.new_uname = []
		self.new_pword = []

		self.uname = uname
		self.pword = pword
		self.key  = salt
		self.ulen = len(uname)
		self.plen = len(pword)
		self.iv = Random.new().read(AES.block_size)

	# Takes the unicode number for the password and username, adds length to it
	def caesar(self):
		for x in self.uname:
			self.new_uname.append(chr(ord(x) + self.ulen))

		for y in self.pword:
			self.new_pword.append(chr(ord(y) + self.plen))

	# Converts the respective arrays to strings
		self.mystring = ''.join(self.new_uname)
		self.mypass = ''.join(self.new_pword)

query = ("SELECT * FROM users")

cursor.execute(query)
i = cursor.fetchall()

#	Converts each entry to a Scramble object
for w, x, y, z in i:
	dbEntries.append(Scramble(x, y, z))

count = 0
while count < len(dbEntries):
	dbEntries[count].caesar()
	print(dbEntries[count].__dict__)
	print('\n')
	count += 1 


# count = 0 
# while count < len(dbEntries):
# 	# print(dbEntries[count].__dict__)
# 	cipher = AES.new(dbEntries[count].key, AES.MODE_CFB, dbEntries[count].iv)

# 	msg = cipher.encrypt(dbEntries[count].pword)
# 	print(msg)

# 	encryptedPW.append(msg)
# 	count += 1 

# count = 0

#	Function to decipher the encrypted part
# while count < len(dbEntries):
# 	decipher = AES.new(dbEntries[count].key, AES.MODE_CFB, dbEntries[count].iv)
# 	print(decipher.decrypt(encryptedPW[count]))
# 	count += 1 

#	It is imperative that the same cipher string is NOT reused 
#	~ Encrypt and decrypt 
# 		key = b'Sixteen byte key'
# 		iv = Random.new().read(AES.block_size)
# 		cipher = AES.new(key, AES.MODE_CFB, iv)
# 		msg = cipher.encrypt(b' To be encrypted ')
# 		print(msg)
# decipher = AES.new(key, AES.MODE_CFB, iv)
# print(decipher.decrypt(msg))
