function f = NNPredict_UUV(XTest) %#codegen
global hour
global num_incidents
global iter
global datafolder
[m,n] = size(XTest);
for i = 1:m
    for j = 1:num_incidents
        XTest(i,(j-1)*4+1) = round(XTest(i,(j-1)*4+1));
        XTest(i,(j-1)*4+2) = round(XTest(i,(j-1)*4+2));
        XTest(i,(j-1)*4+3) = round(XTest(i,(j-1)*4+3));
        XTest(i,(j-1)*4+4) = XTest(i,(j-1)*4+4);
    end
end
XTest = XTest';
model_num = hour - 1;
model_name = 'NN_fit_net'+ string(iter) + '-'+ string(model_num);
model_path = strcat(datafolder, '/', model_name);
mdl = load(model_path);
Y_preditct = mdl.net(XTest);
% Y_preditct = float(Y_preditct);
f = Y_preditct;