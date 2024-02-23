from cProfile import label
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


def generate_noise(mean, std, signal):
    noise = np.random.normal(mean, std, len(signal))
    noisy_signal = []
    for i in range(len(signal)):
        noisy_signal.append(signal[i]+noise[i])

    return noisy_signal

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

    # Demodulate received signal
    demodulated_symbols = []

    for i in range(n_symbols):
        sample_index = i * T
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
    
    ber = []
    for i in range(len(demodulated_bits_flat)):
        ber.append(abs(int(transmittedBitstream[i])-int(demodulated_bits_flat[i])))
    ber = sum(ber)/len(demodulated_bits_flat)
    return demodulated_bits_flat,ber

def mpam(koeff):
    t = np.linspace(0,100)
    signal=[]
    for i in range(len(koeff)):
        #making a rect
        signal.append(koeff[i]*sig.square(2*np.pi*0.00001*t))

    flattened_list = [item for sublist in signal for item in sublist]
    return flattened_list

def matched_filter(signal):
    # Define the matched filter coefficients (for simplicity, assuming rectangular pulse shape)
    matched_filter_coeffs = np.ones(len(signal))
    # Apply the matched filter
    filtered_signal = np.convolve(signal, matched_filter_coeffs, mode='same')
    return filtered_signal

trans_signal = demodulatempam(generate_noise(0,0.15,mpam(mpam_koeff(data[int(5600*4):int(5650*4)],16,1))),16,1,data[int(5600*4):int(5650*4)])
print(trans_signal)
#noise_signal = generate_noise(0,0.1,trans_signal)
#print(demodulatempam(noise_signal,16,1,data)[1])
m8 = []
m2 = []
#for i in range(10):
#    m2.append(demodulatempam(generate_noise(0,0.05*i,mpam(mpam_koeff(data,2,1))),2,1,data)[1])
#    m8.append(demodulatempam(generate_noise(0,0.05*i,mpam(mpam_koeff(data,8,1))),8,1,data)[1])
hora = mpam(mpam_koeff(data[:400],8,1))
ejnf = generate_noise(0,0,hora)
ubfeu = matched_filter(ejnf)
print(demodulatempam(ubfeu,8,1,data[:400])[1],demodulatempam(hora,8,1,data[:400])[1])

#print(demodulatempam(ubfeu,8,1,data[:400])[1])
#print(demodulatempam((mpam(mpam_koeff(data,16,1))),16,1,data)[1])
#plt.plot(m8, label="m=8")
#plt.plot(m2,label ="m=2")
plt.legend()
#plt.yscale("log")
#plt.plot(demodulatempam(trans_signal,16,1,data)[0][500:10000])
#plt.plot(trans_signal)
#plt.plot(signal[1])
#plt.plot(np.zeros(len(flattened_list)))
#plt.plot(sig.square(2*np.pi*0.01/2*np.linspace(1,1000)))
plt.show()