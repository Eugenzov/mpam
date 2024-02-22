N=4;
Vp=1;
quantLevels = 2.^ N;
Ns = length(bitStream);
qTarget= linspace(-Vp, Vp, quantLevels); 
bitSize=Ns/N; 

newBitStream=reshape(bitStream,N, bitSize)';

encoder=zeros(2.^N, N);
for i = 0:quantLevels-1
    encoder(i+1, :) = bitget(bitxor(i, bitshift(i, -1)), N:-1:1);
end 

estimatedSignal=[];

for j = 1:length(newBitStream)
    index=find(all(repmat(newBitStream(j, :), quantLevels, 1) == encoder, 2))
    estimatedSignal=[estimatedSignal, qTarget(index)];
end 
estimatedSignal=estimatedSignal';




