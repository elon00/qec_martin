use aes_gcm::{
    aead::{Aead, KeyInit},
    Aes256Gcm, Nonce, Key
};
use rand::RngCore;

fn main() {
    println!("\n--- 🚀 AES-256-GCM Superfast Encryption ---");

    // 1. Generate a 256-bit (32 bytes) Key
    // (In reality, this key comes from Kyber, but here we generate secure random bytes)
    let mut key_bytes = [0u8; 32];
    rand::thread_rng().fill_bytes(&mut key_bytes);
    
    // Convert bytes into AES Key format
    let key = Key::<Aes256Gcm>::from_slice(&key_bytes);
    println!("🔑 256-bit Key (First 5 bytes): {:?}", &key[..5]);

    // Initialize the AES machine with the key
    let cipher = Aes256Gcm::new(key);

    // 2. Generate a 96-bit (12 bytes) Nonce (Number Used Once)
    let mut nonce_bytes = [0u8; 12];
    rand::thread_rng().fill_bytes(&mut nonce_bytes);
    
    // Convert bytes into Nonce format
    let nonce = Nonce::from_slice(&nonce_bytes);

    // 3. Your top-secret message (The Treasure)
    let secret_message = b"Attack the enemy base at dawn with 1000 troops!";
    println!("\n📜 Original Message: {:?}", String::from_utf8_lossy(secret_message));

    // 4. ENCRYPTION (Locking the data)
    // Note: The '&' before nonce is strictly required here
    let ciphertext = cipher.encrypt(&nonce, secret_message.as_ref())
        .expect("Encryption failed!");
    
    println!("🔒 Encrypted Ciphertext: {:?}", ciphertext);

    // 5. DECRYPTION (Unlocking the data)
    let decrypted_message = cipher.decrypt(&nonce, ciphertext.as_ref())
        .expect("Decryption failed! Either the key is wrong or the data was tampered with.");

    println!("\n✅ Decrypted Message: {:?}", String::from_utf8_lossy(&decrypted_message));
    println!("--------------------------------------------------\n");
}
