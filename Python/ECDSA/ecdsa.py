import ecdsa

chave_privada = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
chave_publica = chave_privada.get_verifying_key()

with open("private.pem", "wb") as f:
    f.write(chave_privada.to_pem())
with open("public.pem", "wb") as f:
    f.write(chave_publica.to_pem())

assinatura = chave_privada.sign("mensagem aqui".encode("UTF-8"))

assert chave_publica.verify(assinatura, "mensagem aqui".encode("UTF-8"))

print ("Chave privada: " + str(chave_privada.to_pem()))
print ("Chave publica: " + str(chave_publica.to_pem()))