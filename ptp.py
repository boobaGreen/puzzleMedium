import ecdsa
import hashlib
import base58

# Chiave privata in esadecimale
private_key_hex = "E9873D79C6D87DC0FB6A5778633389F4453213303DA61F20BD67FC233AA33262"

# Converti la chiave privata in byte
private_key_bytes = bytes.fromhex(private_key_hex)

# Usa la curva secp256k1
sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)

# Ottieni la chiave pubblica come oggetto `VerifyingKey`
public_key = sk.verifying_key

# Ottieni le coordinate x e y della chiave pubblica
public_key_bytes = public_key.to_string()
x, y = public_key_bytes[:32], public_key_bytes[32:]

# Crea la chiave pubblica compressa
if y[-1] % 2 == 0:
    compressed_public_key = b'\x02' + x
else:
    compressed_public_key = b'\x03' + x

# Calcola l'hash SHA-256 della chiave pubblica compressa
sha256_hash = hashlib.sha256(compressed_public_key).digest()

# Calcola l'hash RIPEMD-160 dell'hash SHA-256
ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()

# Aggiungi il prefisso per l'indirizzo Bitcoin (0x00 per mainnet)
prefixed_hash = b'\x00' + ripemd160_hash

# Calcola l'hash SHA-256 due volte per il checksum
checksum = hashlib.sha256(hashlib.sha256(prefixed_hash).digest()).digest()[:4]

# Combina il prefisso, l'hash RIPEMD-160 e il checksum
address_bytes = prefixed_hash + checksum

# Converti in Base58 per ottenere l'indirizzo Bitcoin
bitcoin_address = base58.b58encode(address_bytes).decode()

print("Indirizzo Bitcoin:", bitcoin_address)
