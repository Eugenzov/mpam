function [quantizedSignal,varLin,varSat,SNqR,qTarget] = MyQuantizer(unquantizedSignal,Vp,N)
%% Instructions 
%%% Quantizse a signal using 2^N levels equally spaced on [-Vp, Vp]

%% Definition
quantLevels = 2.^ N ; %kvantiseringsnivåer utefter N- antal bitar
qTarget= linspace(-Vp, Vp, quantLevels); 

quantizedSignal=interp1(qTarget, qTarget, unquantizedSignal, 'nearest', 'extrap'); %avrundar värderna till NN & de värden utanför Vp

%% Beräkning av Varians
qS= unquantizedSignal;
qS(qS < -Vp) = -Vp; % byter ut alla värden utanför saturation till gränsvärdet 
qS(qS > Vp) = Vp; 

eLin=abs(qS-quantizedSignal);     % Linear error 
varLin= mean((eLin-mean(eLin)).^2); % Variance of linear error (empirical estimations) error inom intervallet 

OoB = setdiff(unquantizedSignal,quantizedSignal); % Sparar de värden som är out of bounds 
eSat= abs(abs(OoB)-Vp); %Saturation error
varSat=mean((eSat-mean(eSat)).^2); % Variance of saturation error (empirical estimation) error utanför intervallet 

varSig = mean((unquantizedSignal-mean(unquantizedSignal)).^2); %Variance signal 

SNqR =10*log10(varSig/varLin) ;  % Signal to quantization Noise power Ratio (empitical estimation)in dB

return 


