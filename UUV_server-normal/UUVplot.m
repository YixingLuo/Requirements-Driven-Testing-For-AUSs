
global uuv
uuv = UnmannedUnderwaterVehicle();

% k = 1: length(energy_list);
% figure, 
% plot(k, energy_list, 'k')
% axis([0, length(energy_list), 0, 200]);
% 
% k = 1: length(acc_list);
% figure, 
% plot(k, acc_list, 'k')
% axis([0, length(acc_list), 0, 1]);
% 
% for k = 1: length(speed)
%     if(speed(k))<0
%         k, speed(k)
%     end
% end
% k = 1: length(speed);
% figure, 
% plot(k, speed, 'k')
% axis([0, length(speed), 2.6, 3.6])

k = 1: 360;
figure, 
subplot(4,1,4)
plot(k, usage_plan(:,1), 'r','linewidth',1.2)
hold on
plot(k, usage_plan(:,2), 'b--','linewidth',1.2)
hold on
plot(k, usage_plan(:,3), 'g-.','linewidth',1.2)
hold on
plot(k, usage_plan(:,4), 'y','linewidth',1.2)
hold on
plot(k, usage_plan(:,5), 'r:','linewidth',1.2)
axis([0, 360, 0, 1])
hl = legend('S1','S2','S3','S4','S5');
set(hl,'box','off')
% xlabel('Time [100s]','Fontname', 'Times New Roman');
ylabel({'Sensor','usage [%]'},'Fontname', 'Times New Roman');
set(gca,'gridLineStyle', '-.');
set(gca,'fontname','Times');
h = xlabel({'Time [100s]'},'Fontname', 'Times New Roman');
xlim = get(gca,'XLim');
ylim = get(gca,'YLim');
set(gca,'gridLineStyle', '-.');
set(h,'Position',[xlim(2)+(xlim(2)+xlim(1))*0.08,ylim(1)])

distance_list = [];
speed = [];
acc_list = [];
energy_list = [];
pastdistance = 0;
%% distance
for j = 1: 360
    speed_now = 0;
    for i = 1:uuv.N_s
        speed_now = speed_now + usage_plan(j,i)*uuv.s_speed(i);
    end
    speed = [speed, speed_now];
    pastdistance = pastdistance + speed_now * uuv.time_step;
    distance_list = [distance_list, pastdistance];
end
k = 1: length(speed);
% figure, 
subplot(4,1,1)
plot(k, speed, 'k','linewidth',1.2)
% axis([0, length(speed), 2.6, 3.6])
% xlabel('Time [100s]','Fontname', 'Times New Roman');
ylabel({'Scanning', 'speed [m/s]'},'Fontname', 'Times New Roman');
set(gca,'gridLineStyle', '-.');
set(gca,'fontname','Times');
%% accuracy
for j = 1: 360
    acc = 0;
    for i = 1:uuv.N_s
        acc = acc + usage_plan(j,i)*uuv.s_accuracy(i);
    end
    acc_list = [acc_list, acc];      
end
k = 1: length(acc_list);
% figure, 
subplot(4,1,2)
plot(k, acc_list, 'k','linewidth',1.2)
% axis([0, length(acc_list), 0.8, 1]);
% xlabel('Time [100s]','Fontname', 'Times New Roman');
ylabel('Accuracy [%]','Fontname', 'Times New Roman');
set(gca,'gridLineStyle', '-.');
set(gca,'fontname','Times');
%% energy
for j = 1: 360
    engy = 0;
    for i = 1:uuv.N_s
        engy = engy + usage_plan(j,i)*uuv.s_energy(i);
    end
    energy_list = [energy_list, engy];    
end
k = 1: length(energy_list);
% figure, 
subplot(4,1,3)
plot(k, energy_list, 'k','linewidth',1.2)
% axis([0, length(energy_list), 100, 150]);
% xlabel('Time [100s]','Fontname', 'Times New Roman');
ylabel({'Energy', 'consumption [J/s]'},'Fontname', 'Times New Roman');
set(gca,'fontname','Times');
set(gca,'gridLineStyle', '-.');
% set(gca,'linewidth',1.2);
