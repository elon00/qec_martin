fn main() {
    println!("--- 🛠️ Quantum 3-Qubit Bit-Flip Simulation ---");

    // 1. Encoding
    // Assume our actual data is '1'. We spread it across 3 qubits (Entanglement).
    let mut qubits: [u8; 3] = [1, 1, 1];
    println!("Initial (Encoded) state: {:?}", qubits);

    // 2. Error Injection - Quantum Noise
    // Suppose due to environmental heat, the middle qubit (index 1) flips to 0.
    qubits[1] = 0; 
    println!("State after error (Noise): {:?}", qubits);

    // 3. Syndrome Measurement
    // We don't read the data directly; instead, we compare them in pairs.
    // s1: Are the first and second qubits the same?
    // s2: Are the second and third qubits the same?
    let s1 = qubits[0] ^ qubits[1]; 
    let s2 = qubits[1] ^ qubits[2];
    println!("Syndrome (s1, s2): ({}, {})", s1, s2);

    // 4. Error Correction
    // Based on the syndrome, we will find out where the error occurred and flip it (X-Gate).
    match (s1, s2) {
        (0, 0) => println!("All good! No error."),
        (1, 0) => {
            println!("🚨 Error in the first qubit (Index 0). Fixing it...");
            qubits[0] ^= 1; // Flip it back
        },
        (1, 1) => {
            println!("🚨 Error in the second qubit (Index 1). Fixing it...");
            qubits[1] ^= 1; // Flip it back
        },
        (0, 1) => {
            println!("🚨 Error in the third qubit (Index 2). Fixing it...");
            qubits[2] ^= 1; // Flip it back
        },
        _ => println!("Too many errors! This code can only fix 1 error."),
    }

    // 5. Final Result
    println!("Corrected state: {:?}", qubits);
}