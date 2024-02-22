from scipy.io import loadmat
mat_data = loadmat('/Users/jenny/Documents/MATLAB/Additional Files/assign1_variables.mat')

# Access variables in Python
# Variables in matlab file 'bitStream', 'estimatedBitStream', 'estimatedSignal', 'N', 'qTarget', 'quantizedSignal', 'Vp'

bitStream = mat_data['bitStream']
estimatedBitStream = mat_data['estimatedBitStream']
N = mat_data['N']
qTarget=mat_data['qTarget']
quantizedSignal=mat_data['quantizedSignal']
Vp=mat_data['Vp']
print(bitStream)