
function [XTest, YTest, XTrain, YTrain] = UUVReqViolation

iternum = 100;
duration = 360;
input_data = [];
for i = 1 : 15*iternum
    uuv = UnmannedUnderwaterVehicle();
    cond_num  = 'condition' + string(i) + '.mat';
    cond = load(cond_num);
    index_name = 'index' + string(i) + '.mat';
    index = load(index_name);
    indextemp = index.index;
    input = zeros(360,15);
    for j = 1:duration
        for k = 1:uuv.N_s
            input(j,k) = uuv.s_accuracy(k);
            input(j,k+uuv.N_s) = uuv.s_energy(k);
            input(j,k+2*uuv.N_s) = uuv.s_speed(k);
        end
    end
    index_cond = 1;
    
    for current_step = 1:duration
        if index_cond > length(indextemp)
            break;
        end
        if current_step == indextemp(index_cond)        
            if cond.condition(index_cond,1) == 1
                sensor_idx = cond.condition(index_cond,2);
                sensor_accuracy = cond.condition(index_cond,3);
                for jj = current_step : duration
                    input(jj,sensor_idx) = sensor_accuracy;
                end
            elseif cond.condition(index_cond,1) == 2
                sensor_idx = cond.condition(index_cond,2);
                sensor_energy = cond.condition(index_cond,3);
                for jj = current_step : duration
                    input(jj,sensor_idx+uuv.N_s) = sensor_energy;
                end
                elseif cond.condition(index_cond,1) == 3
                    sensor_idx = cond.condition(index_cond,2);
                    sensor_speed = cond.condition(index_cond,3);
                    for jj = current_step : duration
                        input(jj,sensor_idx+2*uuv.N_s) = sensor_speed;
                    end
                    elseif cond.condition(index_cond,1) == 4
                        sensor_idx = cond.condition(index_cond,2);
                        for jj = current_step : duration
                            input(jj,sensor_idx) = -1;
                            input(jj,sensor_idx+uuv.N_s) = -1;
                            input(jj,sensor_idx+2*uuv.N_s) = -1;
                        end
            end
            index_cond = index_cond+1;
        end        
    end
    input_data = [input_data;input];
end

data11 = load('data20201014T205752.mat');
data1 = data11.data1;
iternum = 100;
duration = 360;
output_data = [];
for i = 1 : 15*iternum
    output_data(i) = data1(i,1)*2^0 + data1(i,3)*2^1 + data1(i,5)*2^2;
end

end


