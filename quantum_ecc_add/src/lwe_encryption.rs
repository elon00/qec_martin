fn main() {
    println!("--- 🛡️ LWE 1-Bit Encryption (Attack Signal) ---");

    let q: i32 = 23;
    let half_q: i32 = q / 2; // This is our 'mountain' (11)

    // 1. Your Secret and Public Key from the previous lesson
    let secret_s: [i32; 3] = [5, 2, 4];
    let matrix_a: [[i32; 3]; 3] = [[12, 4, 15], [3, 19, 8], [10, 6, 21]];
    let public_b: [i32; 3] = [14, 18, 9]; // This is the correct answer of (A*s + e) mod 23

    // 2. The Commander's secret message (Suppose they want to send '1', meaning "Attack")
    let message: i32 = 1;
    println!("Original message (m): {}", message);

    // 3. ENCRYPTION (Done by the Commander)
    // The Commander chooses a random vector 'r' (of 0s and 1s)
    let r: [i32; 3] = [1, 0, 1];

    // Creating u (the clue): r * A
    let mut u: [i32; 3] = [0, 0, 0];
    for j in 0..3 {
        u[j] = (r[0] * matrix_a[0][j] + r[1] * matrix_a[1][j] + r[2] * matrix_a[2][j]) % q;
    }

    // Creating v (the hidden message): r * b + m * (q/2)
    let v_base = (r[0] * public_b[0] + r[1] * public_b[1] + r[2] * public_b[2]) % q;
    let v = (v_base + message * half_q) % q;

    println!("Encrypted data (u, v): ({:?}, {})", u, v);
    println!("--- This data will pass through the internet (exposed to hackers) ---");

    // 4. DECRYPTION (Done by you, the King)
    // You will remove the 'fog' using u and your Secret Key (s)
    let u_dot_s = (u[0] * secret_s[0] + u[1] * secret_s[1] + u[2] * secret_s[2]) % q;

    // Modulo (%) in Rust works differently with negative numbers,
    // so we make sure the math always stays positive.
    let mut decrypted_val = (v - u_dot_s) % q;
    if decrypted_val < 0 {
        decrypted_val += q;
    }

    println!();
    println!("Raw decryption result: {}", decrypted_val);

    // 5. Decision Time (Is it the mountain or the fog?)
    // If the result is around 11 (half_q) (like 9, 10, 11, 12, 13), the message is 1.
    // If the result is around 0 or 23 (like 0, 1, 2, 21, 22), the message is 0.

    let distance_from_half = (decrypted_val - half_q).abs();

    let final_message = if distance_from_half <= 3 {
        1 // Close to 11
    } else {
        0 // Close to 0
    };

    println!("The King has read the message: {}", final_message);
    if final_message == 1 {
        println!("⚔️ The army has received the order to attack!");
    } else {
        println!("🛡️ The army will hold its position.");
    }
}
