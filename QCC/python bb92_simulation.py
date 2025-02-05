import random
from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import AerSimulator
from qiskit.visualization import plot_histogram, circuit_drawer
import matplotlib.pyplot as plt

# Number of qubits (number of bits to be exchanged)
n_bits = 100

# Step 1: Alice generates random bits and encodes them
alice_bits = [random.randint(0, 1) for _ in range(n_bits)]

# Alice's encoding:
# If bit is 0: state |0⟩ (Z-basis)
# If bit is 1: state |+⟩ (superposition in X-basis)
alice_states = []
for bit in alice_bits:
    if bit == 0:
        alice_states.append('Z')  # Z-basis state |0⟩
    else:
        alice_states.append('X')  # X-basis state |+⟩

# Step 2: Bob randomly chooses measurement bases
bob_bases = [random.choice(['Z', 'X']) for _ in range(n_bits)]
bob_results = []

# Prepare the quantum circuit
qc = QuantumCircuit(n_bits, n_bits)

# Alice prepares qubits
for i in range(n_bits):
    if alice_states[i] == 'X':
        qc.h(i)
    # No else needed since qubits are initialized to |0⟩ by default

# Bob measures the qubits
for i in range(n_bits):
    if bob_bases[i] == 'X':
        qc.h(i)  # Change to X-basis measurement
    qc.measure(i, i)

# Execute the circuit
backend = AerSimulator()
transpiled_qc = transpile(qc, backend)
job = backend.run(transpiled_qc, shots=1, memory=True)
result = job.result()

# Extract measurement results
memory = result.get_memory()
measurement = memory[0]  # Since shots=1
measurement = measurement[::-1]  # Reverse due to qubit ordering
for bit in measurement:
    bob_results.append(int(bit))

# Key Sifting
sifted_key = []
for i in range(n_bits):
    # Bob's result is only conclusive when he measures in the correct basis
    if (alice_states[i] == 'Z' and bob_bases[i] == 'Z') or (alice_states[i] == 'X' and bob_bases[i] == 'X'):
        sifted_key.append(bob_results[i])

# Display Results
print("BB92 Quantum Key Distribution Simulation")
print("----------------------------------------")
print(f"Number of bits sent: {n_bits}")
print(f"Number of bits received: {len(sifted_key)}")
print(f"Sifted key: {sifted_key}")

# Visualization
counts_0 = bob_results.count(0)
counts_1 = bob_results.count(1)

plt.figure(figsize=(6, 4))
plt.bar(['0', '1'], [counts_0, counts_1], color=['blue', 'red'])
plt.title("Bob's Measurement Results")
plt.xlabel('Bit Value')
plt.ylabel('Counts')
plt.show()

# Save the quantum circuit diagram
qc.draw('mpl', filename='bb92_circuit.png')
print("Quantum circuit diagram saved as 'bb92_circuit.png'")
