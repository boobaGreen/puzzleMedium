from bip_utils import Bip39SeedGenerator, Bip39MnemonicValidator, Bip44, Bip44Coins, Bip44Changes
import itertools

# Lista delle parole specificate dall'utente (prime 10 parole fisse)
fixed_words = ["faint", "lonely", "scale", "gate", "camera", "shoulder", "adult", 
               "game", "medal", "language"]

# Ultime due parole che vuoi variare
variable_words = ["good", "enough", "payment", "border"]

# Indirizzo target
target_address = "1K4ezpLybootYF23TM4a8Y4NyP7auysnRo"

# Crea tutte le combinazioni possibili delle ultime due parole
combinations = list(itertools.product(variable_words, repeat=2))

# Funzione per generare l'indirizzo e confrontarlo con quello target
def check_mnemonic(mnemonic):
    # Verifica se la frase mnemonica ha un checksum valido
    try:
        Bip39MnemonicValidator().Validate(mnemonic)
    except Exception as e:
        print(f"Errore nella validazione della mnemonica: {str(e)}")
        return None  # Frase mnemonica non valida

    # Genera il seed e calcola l'indirizzo pubblico e la chiave privata
    seed_generator = Bip39SeedGenerator(mnemonic)
    seed = seed_generator.Generate()
    bip44_mst = Bip44.FromSeed(seed, Bip44Coins.BITCOIN)
    bip44_acc = bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    address = bip44_acc.PublicKey().ToAddress()
    private_key = bip44_acc.PrivateKey().ToWif()

    # Restituisce l'indirizzo e le chiavi per il log
    return mnemonic, private_key, bip44_acc.PublicKey().RawCompressed().ToHex(), address

# Log per registrare tutte le combinazioni
log_entries = []

# Cicla su tutte le combinazioni delle ultime due parole
for combo in combinations:
    # Unisci le parole fisse con la combinazione delle ultime due parole
    mnemonic = " ".join(fixed_words + list(combo))

    # Aggiungi un log per verificare la combinazione di parole
    print(f"Verifica combinazione: {mnemonic}")
    
    # Verifica la frase mnemonica
    result = check_mnemonic(mnemonic)
    
    if result:
        mnemonic, private_key, public_key, address = result
        log_entry = {
            "mnemonic": mnemonic,
            "private_key": private_key,
            "public_key": public_key,
            "address": address,
        }
        
        # Aggiungi al log
        log_entries.append(log_entry)
        
        # Stampa il log
        print(f"Frase mnemonica: {mnemonic}")
        print(f"Chiave privata: {private_key}")
        print(f"Chiave pubblica: {public_key}")
        print(f"Indirizzo: {address}")
        
        # Verifica se l'indirizzo corrisponde a quello target
        if address == target_address:
            print("Indirizzo CORRISPONDE all'indirizzo target!")
        else:
            print("Indirizzo NON CORRISPONDE all'indirizzo target.")
    print('-' * 50)  # Separatore per rendere più chiara la lettura tra i vari log

# Log finale: stampa tutte le combinazioni e gli indirizzi generati
print("\n--- Log completo delle combinazioni e degli indirizzi generati ---")
for entry in log_entries:
    print(f"Lista parole: {entry['mnemonic']}")
    print(f"Indirizzo calcolato: {entry['address']}")
    print('-' * 50)
