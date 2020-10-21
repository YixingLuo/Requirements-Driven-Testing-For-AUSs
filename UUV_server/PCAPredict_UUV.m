function f = PCAPredict_UUV(XTest) %#codegen
global coeff
global mu
global idx
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
model_num = hour - 1;
model_name = 'myMdl-iter'+ string(iter) + '-'+ string(model_num);
mdl = loadLearnerForCoder(strcat(datafolder, '/', model_name));
scoreTest95 = (XTest-mu)*coeff(:,1:idx);
f = predict(mdl,scoreTest95);
