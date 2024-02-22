function [bitStream,encoder] = MyGraycode(quantizedSignal,Vp,N)

%% Instruktion
%Function that uses Gray coded N bits to represent each of the quantization levels.
% Returns a vector of length N · Ns containing the bits representing these values,

%% Encoder 
Ns=length(quantizedSignal); % längden av qvantiserad signal
quantLevels = 2.^ N ;
qTarget= linspace(-Vp, Vp, quantLevels); 
encoder=zeros(2.^N, N);
for i = 0:quantLevels-1
    encoder(i+1, :) = bitget(bitxor(i, bitshift(i, -1)), N:-1:1);
end 
%% Analog till Gray Omvandling
bitStream = [];
   
for i = 1:Ns
 % Find the index of the control value that matches the current signal element
 controlIndex = find(qTarget ==quantizedSignal(i)); %hittar index hos kvantiseringsvärde som den kvantiserade signalen motsvarar
 row = encoder(controlIndex, :); % tar ut den rad ur encodern som det kvantiserade värdet motsvarar i greykod 
 bitStream = [bitStream, row]; %adderar till en array
end 

end




