use k256::ecdsa::{SigningKey, Signature, VerifyingKey};
use k256::ecdsa::signature::{Signer, Verifier};
use rand_core::OsRng;

fn main() {
    println!("--- 📜 Digital Signature (Royal Seal) Simulation ---");

    // 1. Generating your secret Private Key (Signing Key)
    let private_key = SigningKey::random(&mut OsRng);

    // 2. Extracting the Public Key (Verifying Key) from it to show the world
    let public_key = VerifyingKey::from(&private_key);

    // 3. Our secret message
    let message = b"Move the Quantum Treasure to the North Vault!";
    println!("\nMessage: {:?}", String::from_utf8_lossy(message));

    // 4. SIGNING: You (the King) stamp it with your Private Key
    // This function internally creates a SHA-256 hash and solves the (r, s) math.
    let signature: Signature = private_key.sign(message);
    println!("Your seal (Signature) has been applied!");

    // 5. VERIFICATION: The Commander verifies the seal using your Public Key
    match public_key.verify(message, &signature) {
        Ok(_) => println!("✅ Verification successful! This message was sent by the King and hasn't been tampered with."),
        Err(_) => println!("❌ Fraud! This seal is forged!"),
    }

    // 6. Hacker Attack 
    // Suppose a hacker changed the message from "North" to "South" along the way
    println!("\n--- Hacker tried to alter the message ---");
    let fake_message = b"Move the Quantum Treasure to the South Vault!";
    
    //Now the Commander checks this new (fake) message against the old seal
    match public_key.verify(fake_message, &signature) {
        Ok(_) => println!("✅ Verification successful!"),
        Err(_) => println!("🚨 Alarm! The message was tampered with in transit! The seal doesn't match!"),
    }
}