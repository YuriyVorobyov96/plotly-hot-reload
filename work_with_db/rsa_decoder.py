import rsa

def generate_keys():
	(key_pub, key_priv) = rsa.newkeys(512)

	open('private.pem', 'w').close()
	open('public.pem', 'w').close()

	with open('private.pem', 'a') as the_file:
		the_file.write(key_priv.save_pkcs1().decode('utf-8'))

	with open('public.pem', 'a') as the_file:
		the_file.write(key_pub.save_pkcs1().decode('utf-8'))

def get_private_key():
	with open('private.pem', mode='rb') as privatefile:
		keydata = privatefile.read()

	privkey = rsa.PrivateKey.load_pkcs1(keydata)

	return privkey

def get_pub_key():
	with open('public.pem', mode='rb') as publicfile:
		keydata = publicfile.read()

	pubkey = rsa.PublicKey.load_pkcs1(keydata)

	return pubkey

def encode(data):
	key_pub = get_pub_key()

	return rsa.encrypt((str(data)).encode('utf8'), key_pub)

def decode(data):
	key_priv = get_private_key()

	return (rsa.decrypt(data, key_priv)).decode('utf8')