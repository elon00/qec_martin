fn main() {
    println!("--- 🛡️ Post-Quantum LWE (Lattice) Simulation ---");

    // 1. Modulo (q) - Our math will not exceed 23
    let q: i32 = 23;

    // 2. Your Secret Key (s) - The real treasure map!
    let secret_s: [i32; 3] = [5, 2, 4];
    println!("Secret Key (s): {:?}", secret_s);

    // 3. Public Matrix (A) - A web of random numbers
    let matrix_a: [[i32; 3]; 3] = [[12, 4, 15], [3, 19, 8], [10, 6, 21]];

    // 4. Error (e) - Our 'magic fog' (small numbers like 1, 0, 2)
    // If we don't add this, even a school kid could solve the equation!
    let error_e: [i32; 3] = [1, 2, 1];

    // 5. Generating Public Key (b)
    let mut public_b: [i32; 3] = [0, 0, 0];

    println!("\nGenerating Public Key (b): b = (A * s) + e mod {}", q);

    for i in 0..3 {
        let mut sum = 0;

        // Multiplication of A and s (Dot Product)
        for j in 0..3 {
            sum += matrix_a[i][j] * secret_s[j];
        }

        // Adding the fog (Error)
        sum += error_e[i];

        // Modulo (clock math)
        public_b[i] = sum % q;
    }

    println!("Public Key (b): {:?}", public_b);

    println!("\n🎩 Magic: Now the hacker has A and b. But because of 'e' (Error), they will never find 's', and even a quantum computer will fail!");
}
