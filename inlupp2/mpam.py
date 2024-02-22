from cgitb import grey
from cmath import pi
from decimal import setcontext
from tokenize import PlainToken
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy import signal as sig

data = open("C:\\Users\\eugen.zovko\\OneDrive - Academedia\\Documents\\digital kommunikation\\hej.csv")
data = data.read().split(",")
data[-1] = "0"

def gray_code(n):
    """Generate Gray code of n bits."""
    if n == 1:
        return ['0', '1']
    else:
        lower = gray_code(n-1)
        upper = lower[::-1]
        return ['0' + code for code in lower] + ['1' + code for code in upper]

def gray_code_converter(m,d):
    result = {}
    x = gray_code(m)
    for i in range(len(x)):
        result[x[i]] = -(d-((1+2*i)*d/(len(x))))
    return result

def mpam_koeff(bitstream, m, es):
    d = math.sqrt(3*es/(m^2-1))

    k = int(np.log2(m))
    num_bits = len(bitstream)

    # Adjust the length of bitstream to ensure a whole number of messages
    num_messages = num_bits // k
    num_needed_bits = num_messages * k
    bitstream = bitstream[:num_needed_bits]

    # Reshape the bitstream into messages of k bits
    messages = np.array(bitstream).reshape(-1, k)
    
    symbols = []
    for message in messages:
        index = ''.join(message)
        symbols.append(gray_code_converter(k,2*d)[index])
    return symbols

def demodulatempam(receivedSignal, M, Es, transmittedBitstream):
    T = 50  # Symbol time
    n_symbols = len(transmittedBitstream) // int(np.log2(M))  # Number of symbols
    
    # Calculate threshold levels for demodulation
    levels = np.linspace(-np.sqrt(3*Es/(M**2 - 1)) * (M-1)/2, np.sqrt(3*Es/(M**2 - 1)) * (M-1)/2, M)
    print(levels)
    # Demodulate received signal
    demodulated_symbols = []
    print(n_symbols)
    print(len(receivedSignal))
    for i in range(n_symbols):
        sample_index = i * T +25
        sample = receivedSignal[sample_index]
        symbol = min(levels, key=lambda x:abs(x-sample))  # Find closest threshold level
        symbol_index = np.where(levels == symbol)[0][0]
        demodulated_symbols.append(symbol_index)
    
    # Convert symbols to bits
    demodulated_bits = []
    gray = gray_code(np.log2(M))

    for symbol in demodulated_symbols:
        demodulated_bits.append(gray[symbol])
    demodulated_bits_flat = [item for sublist in demodulated_bits for item in sublist]
    return demodulated_bits_flat

koeff = mpam_koeff(data,16,1)
t = np.linspace(0,100)
signal=[]
for i in range(len(koeff)):
    signal.append(koeff[i]*sig.square(2*np.pi*0.00001*t))
    
plt.plot(signal[50])
 
flattened_list = [item for sublist in signal for item in sublist]
x= demodulatempam( flattened_list,16,1,data)
print(len(data))
print(len(x))
err = []
for i in range(len(x)):
    err.append(abs(int(data[i])-int(x[i])))
print(sum(err))
#plt.plot(signal[1])
#plt.plot(np.zeros(len(flattened_list)))
#plt.plot(sig.square(2*np.pi*0.01/2*np.linspace(1,1000)))
plt.show()