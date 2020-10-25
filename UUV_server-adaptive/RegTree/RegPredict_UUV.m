function f = RegPredict_UUV(XTest) %#codegen
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
% XTest = XTest';
model_num = hour - 1;
for i = 1:3
    model_name = 'Reg_model-'+ string(iter) + '-'+ string(model_num)+ '-'+ string(i);
    model_path = strcat(datafolder, '/', model_name);
    mdl = load(model_path);
    f(i) = predict(mdl.Mdl,XTest);
end

% size(XTest)
% Y_preditct = mdl.net(XTest);
% Y_preditct = float(Y_preditct);
% f = Y_preditct;
end