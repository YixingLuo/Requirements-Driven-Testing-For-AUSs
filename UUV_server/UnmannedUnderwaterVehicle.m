classdef UnmannedUnderwaterVehicle
    properties 
s_energy = [170, 135, 118, 100, 78];
s_speed = [2.6, 3.6, 2.6, 3.0, 3.6];
s_accuracy = [0.97, 0.89, 0.83, 0.74, 0.49];
s_work = [1,1,1,1,1];
k = 360;

distance_budget = 0;
distance_target = 100*1000;
time_budget = 10*60*60;
time_target = 10*60*60;
time_step = 100;
energy_budget = 170*2*100*360;
energy_target = 5.4*1e6;
acc_budget = 0;
acc_target = 1;

N = 5;
N_s = 5;
    end
 methods
        function uuv = UnmannedUnderwaterVehicle(uuv)
            uuv.N_s = length(uuv.s_accuracy);
        end
        function uuv = SensorFailure(uuv, no)
            uuv.s_accuracy(no) = 0;
            uuv.s_energy(no) = 0;
            uuv.s_speed(no) = 0;
            uuv.s_work(no) = 0;
            uuv.N_s = length(uuv.s_accuracy);   
        end
        function uuv = EnergyDisturbance(uuv, no, energy)
            uuv.s_energy(no) = energy;
        end 
        function uuv = SpeedDisturbance(uuv, no, speed)
            uuv.s_speed(no) = speed;
        end 
        function uuv = SensorError(uuv, no, acc)
            uuv.s_accuracy(no) = acc;
        end
        function uuv = EnergyBudget(uuv, energy_target)
            uuv.energy_target = energy_target;
%             uuv.energy_budget = energy_target * 1.05;
        end 
        function uuv = DistanceBudget(uuv, distance_target)
            uuv.distance_target = distance_target;
%             uuv.distance_budget = distance_target * 0.95;
        end 
        function uuv = AccuracyBudget(uuv, accuracy_target)
            uuv.acc_target = accuracy_target;
%             uuv.acc_budget = accuracy_target*0.9;
%             uuv.acc_target = min(max(uuv.s_accuracy),accuracy_target);
        end 
 end
end


        