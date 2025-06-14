# Nama file: encryptionModule.py
# Versi final dengan perbaikan pada CustomHmac untuk mencegah tabrakan hash.

import os

salt : str = '4c8606f5a10e3895f2e7b929fa331fa1'

# --- Bagian 1: Kelas Lfsr ---
class Lfsr:
    def __init__(self, seed, taps, stateSize):
        binaryString = format(seed, 'b').zfill(stateSize)
        self.state = [int(i) for i in binaryString]
        self.taps = taps

    def step(self):
        feedbackBit = 0
        for tap in self.taps:
            feedbackBit ^= self.state[tap]
        
        self.state.pop()
        self.state.insert(0, feedbackBit)
        
        return self.state[-1]

    def generateKeystreamByte(self):
        byteVal = 0
        for _ in range(8):
            byteVal = (byteVal << 1) | self.step()
        return byteVal

# --- Bagian 2: Kelas CustomHmac (DENGAN PERBAIKAN) ---
class CustomHmac:
    BLOCK_SIZE = 64

    def __init__(self, key: bytes):
        if len(key) > self.BLOCK_SIZE:
            self.key = self.simpleHash(key)
        else:
            self.key = key.ljust(self.BLOCK_SIZE, b'\0')

        self.opad = bytes([x ^ 0x5c for x in self.key])
        self.ipad = bytes([x ^ 0x36 for x in self.key])

    def simpleHash(self, data: bytes) -> bytes:
        """
        Fungsi hash yang lebih kompleks untuk mengurangi kemungkinan tabrakan.
        Menggabungkan rotasi bit dan perkalian dengan bilangan prima.
        """
        # Konstanta bilangan prima besar untuk proses "mixing"
        P1 = 0xff51afd7ed558ccd
        P2 = 0xc4ceb9fe1a85ec53
        
        # Inisialisasi hash
        hashVal = 0xabcdef1234567890
        bitmask = 0xFFFFFFFFFFFFFFFF # Masker untuk operasi 64-bit

        # Proses setiap byte data
        for byte in data:
            hashVal ^= byte
            hashVal = (hashVal * P1) & bitmask
            # Rotasi bit ke kiri sebanyak 23 bit
            hashVal = ((hashVal << 23) | (hashVal >> (64 - 23))) & bitmask
        
        # Proses final mixing untuk meningkatkan efek longsor (avalanche)
        hashVal ^= hashVal >> 33
        hashVal = (hashVal * P2) & bitmask
        hashVal ^= hashVal >> 33

        return hashVal.to_bytes(8, 'big')

    def sign(self, message: bytes) -> bytes:
        innerHash = self.simpleHash(self.ipad + message)
        finalTag = self.simpleHash(self.opad + innerHash)
        return finalTag

# --- Bagian 3: Fungsi Generate Key ---
def generateKeyFromPassword(password: str, salt: bytes, length: int) -> bytes:
    key = password.encode('utf-8')
    for _ in range(1000):
        hasher = CustomHmac(key)
        key = hasher.sign(salt + key)
    return key[:length]

# --- Bagian 4: Fungsi Encrypt ---
def encrypt(password: str, plaintext: str) -> str:
    keyMaterial = generateKeyFromPassword(password, bytes.fromhex(salt), 48)
    lfsrSeedBytes = keyMaterial[:16]
    hmacKey = keyMaterial[16:]

    PREDETERMINED_TAPS = (0, 2, 3, 7, 25, 61, 127)
    lfsrSeed = int.from_bytes(lfsrSeedBytes, 'big')
    
    STATE_SIZE = 128
    cipher = Lfsr(seed=lfsrSeed, taps=PREDETERMINED_TAPS, stateSize=STATE_SIZE)
    
    plaintextBytes = plaintext.encode('utf-8')
    ciphertext = bytearray()
    for byte in plaintextBytes:
        keystreamByte = cipher.generateKeystreamByte()
        encryptedByte = byte ^ keystreamByte
        ciphertext.append(encryptedByte)
    
    ciphertext = bytes(ciphertext)
    
    hmac = CustomHmac(key=hmacKey)
    tag = hmac.sign(ciphertext)

    res = ciphertext.hex() + tag.hex()
    
    return res
        

# --- Bagian 5: Fungsi Decrypt ---
def decrypt(password: str, encryptedData: str) -> str:
    try:
        ciphertext = bytes.fromhex(encryptedData[:-16])
        receivedTag = bytes.fromhex(encryptedData[-16:])
        # salt = bytes.fromhex(encryptedData["salt"])
    except (ValueError, KeyError):
        raise ValueError("Paket terenkripsi tidak valid atau korup.")

    keyMaterial = generateKeyFromPassword(password, bytes.fromhex(salt), 48)
    lfsrSeedBytes = keyMaterial[:16]
    hmacKey = keyMaterial[16:]

    hmac = CustomHmac(key=hmacKey)
    calculatedTag = hmac.sign(ciphertext)

    if calculatedTag != receivedTag:
        raise ValueError("Gagal Dekripsi: Data mungkin telah dirusak atau kunci salah!")

    PREDETERMINED_TAPS = (0, 2, 3, 7, 25, 61, 127)
    lfsrSeed = int.from_bytes(lfsrSeedBytes, 'big')

    STATE_SIZE = 128
    cipher = Lfsr(seed=lfsrSeed, taps=PREDETERMINED_TAPS, stateSize=STATE_SIZE)
    
    decryptedBytes = bytearray()
    for byte in ciphertext:
        keystreamByte = cipher.generateKeystreamByte()
        decryptedByte = byte ^ keystreamByte
        decryptedBytes.append(decryptedByte)

    return bytes(decryptedBytes).decode('utf-8')

if __name__ == "__main__":
    # Skenario 1: Enkripsi dan Dekripsi Berhasil
    print("--- Skenario 1: Sukses ---")
    userPassword = "PasswordSuperRahasia123"
    originalData = "Farhan, CTO, 081234567890, Jalan Ganesha 10"
    
    print(f"Data Asli: {originalData}")
    
    encryptedPackage = encrypt(userPassword, originalData)
    print(f"Paket Terenkripsi: {encryptedPackage}")
    
    try:
        decryptedData = decrypt(userPassword, encryptedPackage)
        print(f"Data Terdekripsi: {decryptedData}")
        assert originalData == decryptedData
        print("✅ Integritas dan kerahasiaan terjaga!")
    except ValueError as e:
        print(f"❌ Terjadi Error Tak Terduga: {e}")

    print("\n" + "="*40 + "\n")

    # Skenario 2: Gagal Dekripsi karena Password Salah
    print("--- Skenario 2: Password Salah ---")
    try:
        print("Mencoba dekripsi dengan password yang salah...")
        decryptedData = decrypt("PasswordSalah", encryptedPackage)
    except ValueError as e:
        print(f"✅ Berhasil! Error yang diharapkan muncul: {e}")

    print("\n" + "="*40 + "\n")

    # Skenario 3: Gagal Dekripsi karena Data Dirusak (Tampering)
    print("--- Skenario 3: Data Dirusak ---")
    tamperedCiphertext = bytearray.fromhex(encryptedPackage)
    # Ubah satu bit saja di tengah ciphertext
    originalByte = tamperedCiphertext[5]
    tamperedByte = originalByte ^ 1 
    tamperedCiphertext[5] = tamperedByte
    encryptedPackage = tamperedCiphertext.hex()
    
    print("Ciphertext telah diubah. Mencoba dekripsi...")
    try:
        decryptedData = decrypt(userPassword, encryptedPackage)
    except ValueError as e:
        print(f"✅ Berhasil! Error yang diharapkan muncul: {e}")