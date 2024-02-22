function [estimatedSignal] = MyDAconverter(estimatedBitStream,Vp,N)
%% Instruction 
%%% Takes a bit stream input and provides the quantized levels of the signal in

%% Encoder
quantLevels = 2.^ N;
Ns = length(estimatedBitStream);
qTarget= linspace(-Vp, Vp, quantLevels); 
bitSize=Ns/N; 

newBitStream=reshape(estimatedBitStream, N, bitSize)'; %delar upp bitstream i en matris där rader =greykod för enskild signal

encoder=zeros(2.^N, N);
for i = 0:quantLevels-1
    encoder(i+1, :) = bitget(bitxor(i, bitshift(i, -1)), N:-1:1);
end 

%% Grey till Analog omvandling 
estimatedSignal=[];

for j = 1:length(newBitStream) 
    index=find(all(repmat(newBitStream(j, :), quantLevels, 1) == encoder, 2)); %hittar respektive index hos den rad i qLevels som bitarnamotsvarar
    estimatedSignal=[estimatedSignal, qTarget(index)]; % sparar det analoga värdet i en array
end 
estimatedSignal=estimatedSignal'; 






