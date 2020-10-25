
iternum = 100;
duration = 360;
output_data = [];
for i = 1 : 15*iternum
    output_data(i) = (1-data1(i,1))*2^0 + (1-data1(i,3))*2^1 + (1-data1(i,5))*2^2;
end
output_data
output_data = categorical(output_data)