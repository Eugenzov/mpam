function decimalToBinaryNumber(x, n)
    binaryNumber = zeros(1, x);
    i = 1;
    while (x > 0)
        binaryNumber(i) = mod(x, 2);
        x = floor(x / 2);
        i = i + 1;
    end

    % leftmost digits are filled with 0
    for j = 1:(n - i)
        fprintf('0');
    end

    for j = i - 1:-1:1
        fprintf('%d', binaryNumber(j));
    end
end

function generateGrayarr(n)
    N = 2^n;
    for i = 0:(N - 1)
        % generate gray code of corresponding binary
        % number of integer i.
        x = bitxor(i, bitshift(i, -1));

        % printing gray code
        decimalToBinaryNumber(x, n);
        fprintf('\n');
    end
end
