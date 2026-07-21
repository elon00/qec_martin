fn main() {
    let secret_message = "HI"; // H and I
    
    println!("Message: {}", secret_message);
    println!("--- Starting bitwise encryption ---");

    // Pick each character (Byte) one by one
    for byte in secret_message.bytes() {
        println!("Binary of character '{}':", byte as char);
        
        // A character has 8 bits, let's extract them
        for i in (0..8).rev() {
            let bit = (byte >> i) & 1; // This bit will be either 0 or 1
            
            // 🚨 Here we would call our previous LWE encryption!
            // let encrypted_bit = encrypt_lwe(bit, public_key);
            print!("{} ", bit); 
        }
        println!(); // New line
    }
}