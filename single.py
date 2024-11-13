from bip_utils import Bip39SeedGenerator, Bip39MnemonicValidator, Bip44, Bip44Coins, Bip44Changes

# Lista delle parole specificate dall'utente (ordine fisso)
word_list = ["asset","trial", "load", "escape", "symbol", "story", "bomb", 
             "picnic", "river", "aerobic", "mystery", "honey"]

# Indirizzo target
target_address = "1K4ezpLybootYF23TM4a8Y4NyP7auysnRo"

# Unisci le parole per creare la frase mnemonica nell'ordine dato
mnemonic = " ".join(word_list)

# Verifica se la frase mnemonica ha un checksum valido
try:
    Bip39MnemonicValidator().Validate(mnemonic)
except Exception:
    print("La frase mnemonica fornita non ha un checksum valido. Programma terminato.")
else:
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
    else:
        print("Checksum valido, ma l'indirizzo non corrisponde all'indirizzo target.")
        print(f"Chiave privata: {private_key}")
        print(f"Chiave pubblica: {bip44_acc.PublicKey().RawCompressed().ToHex()}")
        print(f"Indirizzo generato: {address}")
