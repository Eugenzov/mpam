load train

Vp=2;
N=4;
[quantizedSignal,varLin,varSat,SNqR,qTarget] = MyQuantizer(y,Vp,N);
[bitStream,encoder] = MyGraycode(quantizedSignal,Vp,N);
estimatedBitStream=bitStream;
[estimatedSignal] = MyDAconverter(estimatedBitStream,Vp,N);
time=linspace(0,12880,12880);
subplot(3,1,1)
plot(time(9000:9100),y(9000:9100))
xlabel('Tid')
ylabel('Amplitude')
title('Unquantized Signal')

subplot(3,1,2)
plot(time(9000:9100), quantizedSignal(9000:9100))
xlabel('Tid')
ylabel('Amplitud ')
title('Quantized Signal')

subplot(3,1,3)
hold on
plot(time(9000:9100), estimatedSignal(9000:9100), '--o')
xlabel('Tid')
ylabel('Amplitud ')
title('Estimated Signal')
plot(time(9000:9100), quantizedSignal(9000:9100),'.')
hold off 

res = 0;

%mean square error 
for i =1
    res = res + (quantizedSignal(i)+estimatedSignal(i))^2;
end
[bitStream] = MyGraycode(quantizedSignal,Vp,N);
[estimatedSignal] = MyDAconverter(estimatedBitStream,Vp,N); 
sound(estimatedSignal)
% Save the sound signal to a file
filename = ['sound_sample' num2str(Vp) '.wav'];
audiowrite(filename, estimatedSignal, Fs);
q = Vp/(2^N-1);
varLin_theo = q^2/12;
var_diff = abs(varLin_theo-varLin);