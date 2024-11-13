import itertools
from bip_utils import Bip39SeedGenerator, Bip39MnemonicValidator, Bip44, Bip44Coins, Bip44Changes

# Lista delle parole specificate dall'utente
word_list = ["witch","collapse", "practice", "feed", "shame", "open", "despair", 
             "creek", "road", "again", "ice", "least"]
# 22 - 1206 
# Indirizzo target
target_address = "1K4ezpLybootYF23TM4a8Y4NyP7auysnRo"

# Numero massimo di tentativi (fattoriale di 12 parole per tutte le permutazioni)
max_attempts = 479001600
found = False
attempt = 0

# Genera tutte le permutazioni di frasi mnemoniche (12 parole)
for mnemonic_permutation in itertools.permutations(word_list, 12):
    attempt += 1
    if attempt > max_attempts:
        break

    # Unisci le parole per creare la frase mnemonica
    mnemonic = " ".join(mnemonic_permutation)

    # Verifica se la frase mnemonica ha un checksum valido
    try:
        Bip39MnemonicValidator().Validate(mnemonic)
    except Exception:
        # Scarta le frasi non valide e continua con la prossima
        continue

    # Genera il seed e calcola l'indirizzo pubblico e la chiave privata
    seed_generator = Bip39SeedGenerator(mnemonic)
    seed = seed_generator.Generate()
    bip44_mst = Bip44.FromSeed(seed, Bip44Coins.BITCOIN)
    bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    address = bip44_acc.PublicKey().ToAddress()
    private_key = bip44_acc.PrivateKey().ToWif()

    # Controlla se l'indirizzo corrisponde a quello target
    if address == target_address:
        print(f"Frase mnemonica trovata: {mnemonic}")
        print(f"Chiave privata: {private_key}")
        print(f"Chiave pubblica: {bip44_acc.PublicKey().RawCompressed().ToHex()}")
        print(f"Indirizzo: {address}")
        found = True
        break
    else:
        # Loggare solo ogni 10,000 tentativi per evitare troppa stampa
        if attempt % 5000 == 0:
            progress_percentage = (attempt / max_attempts) * 100
            print(f"Tentativo {attempt}/{max_attempts} ({progress_percentage:.2f}% completato):")
            print(f" - Parole nell'ordine: {mnemonic_permutation}")
            print(f" - Indirizzo generato: {address} - NO MATCH")
            print(f" - Chiave privata campione: {private_key}")

if not found:
    print("Indirizzo target non trovato nei tentativi effettuati.")
