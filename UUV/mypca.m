clear;

%% pca using raw data
x = [149.5 69.5 38.5;
    162.5 77.0 55.5;
    162.7 78.5 50.8;
    162.2 87.5 65.5;
    156.5 74.5 49.0;
    156.1 74.5 45.5;
    172.0 76.5 51.0;
    173.2 81.5 59.5;
    159.5 74.5 43.5;
    157.7 79.0 53.5];
% x = zscore(x); %standardized
[coeff,score,latent,~,explained,mu] = pca(x);
%coeff:coefficient
%latent:eigenvalues
%explained:percentage
%mu:estimated mean of each variable in x

%% pca using covariance matrix
x = [177,179,95,96,53,32,-7,-4,-3;
    0,419,245,131,181,127,-2,1,4;
    0,0,302,60,109,142,4,4,11;
    0,0,0,158,102,42,4,3,2;
    0,0,0,0,137,96,4,5,6;
    0,0,0,0,0,128,2,2,8;
    0,0,0,0,0,0,34,31,33;
    0,0,0,0,0,0,0,39,89;
    0,0,0,0,0,0,0,0,48];
% x = zscore(x); %standardized
xx = x+x'-diag(diag(x));

[COEFF,latent,explained] = pcacov(xx);