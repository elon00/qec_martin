use k256::{PublicKey, SecretKey};
use rand_core::OsRng; // This provides a secure random number generator for us

fn main() {
    println!("--- 🔐 Generating real ECC Keys ---");

    // 1. Generate Private Key (k)
    // OsRng requests a completely secure random number from the operating system.
    // No hacker can predict this number.
    let secret_key = SecretKey::random(&mut OsRng);

    // 2. Generate Public Key (P)
    // Under the hood, this library performs the complex math (Point Multiplication)
    // of P = k * G in a fraction of a millisecond.
    let public_key = secret_key.public_key();

    // 3. View the keys (in Hexadecimal format)
    // We convert the bytes into a Hex string so that we can read them.

    let secret_hex = hex::encode(secret_key.to_bytes());
    // (Note: If you want to run this, add hex = "0.4" to your Cargo.toml as well)

    // View the compressed Public Key (this saves space)
    let public_hex = hex::encode(public_key.to_sec1_bytes());

    println!("Your Private Key (k) - Always keep this a secret! 🤫");
    println!("{}", secret_hex);

    println!("\nYour Public Key (P) - You can share this with the whole world! 🌍");
    println!("{}", public_hex);
}
