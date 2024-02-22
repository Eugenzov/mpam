from decimal import setcontext
import numpy as np
import matplotlib.pyplot as plt
data = open("C:\\Users\\eugen.zovko\\OneDrive - Academedia\\Documents\\digital kommunikation\\hej.csv")
data = data.read().split(",")
data[-1] = "0"

def gray_to_binary(gray_code):
    
    binary_code = gray_code[0]
    for i in range(1, len(gray_code)):
        # XOR operation between current bit of Gray code and previous bit of binary code
        binary_code += str(int(gray_code[i]) ^ int(binary_code[i - 1]))
    return binary_code

def gray_code_converter(m,e):
    result = {}
    x = gray_code(m)
    for i in range(len(x)):
        result[x[i]] = -(e-((1+2*i)*e/(len(x))))
    return result

def gray_code(n):
    """Generate Gray code of n bits."""
    if n == 1:
        return ['0', '1']
    else:
        lower = gray_code(n-1)
        upper = lower[::-1]
        return ['0' + code for code in lower] + ['1' + code for code in upper]


def gray_to_MPAM(bitstream, m, es):
    
    k = int(np.log2(m))
    num_bits = len(bitstream)

    # Adjust the length of bitstream to ensure a whole number of messages
    num_messages = num_bits // k
    num_needed_bits = num_messages * k
    bitstream = bitstream[:num_needed_bits]

    # Reshape the bitstream into messages of k bits
    messages = np.array(bitstream).reshape(-1, k)
    
    gray_mapping = gray_code(k)
    symbols = []
    for message in messages:
        index = ''.join(message)
        symbols.append(gray_code_converter(k,es)[index])
    
    # Normalize symbols to have average energy Es
    #average_symbol_energy = np.mean(np.abs(symbols) ** 2)
    #scaling_factor = np.sqrt(es / average_symbol_energy)
    print(symbols)
    symbols =np.array(symbols)
    average_symbol_energy = np.mean(np.abs(symbols) ** 2)
    scaling_factor = np.sqrt(Es / average_symbol_energy)
    symbols *= scaling_factor
    print(symbols)
    
    # Upsample symbols to get the analog signal
    T = 100  # Symbol time
    analog_signal = np.repeat(symbols, T)
    
    return analog_signal
    
bitstream = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0])  # Example bitstream
M = 16  # M-ary
Es = 1.0  # Average symbol energy
transmitted_signal = gray_to_MPAM(data, M, Es)
plt.plot(transmitted_signal)
plt.show()

