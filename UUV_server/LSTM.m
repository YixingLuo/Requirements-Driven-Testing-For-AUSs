
%%
%加载序列数据
%数据描述：总共270组训练样本共分为9类，每组训练样本的训练样个数不等，每个训练训练样本由12个特征向量组成，
[XTrain,YTrain] = japaneseVowelsTrainData;
%数据可视化
% figure
% plot(XTrain{1}')
% xlabel("Time Step")
% title("Training Observation 1")
% legend("Feature " + string(1:12),'Location','northeastoutside')
%%
%LSTM可以将分组后等量的训练样本进行训练，从而提高训练效率
%如果每组的样本数量不同，进行小批量拆分，则需要尽量保证分块的训练样本数相同
%首先找到每组样本数和总的组数
% numObservations = numel(XTrain);
% for i=1:numObservations
%     sequence = XTrain{i};
%     sequenceLengths(i) = size(sequence,2);
% end
%绘图前后排序的各组数据个数
% figure
% subplot(1,2,1)
% bar(sequenceLengths)
% ylim([0 30])
% xlabel("Sequence")
% ylabel("Length")
% title("Sorted Data")
% %按序列长度对测试数据进行排序
% [sequenceLengths,idx] = sort(sequenceLengths);
% XTrain = XTrain(idx);
% YTrain = YTrain(idx);
% subplot(1,2,2)
% bar(sequenceLengths)
% ylim([0 30])
% xlabel("Sequence")
% ylabel("Length")
% title("Sorted Data")
%%
%设置LSTM训练数据的小批量分组个数
miniBatchSize = 27;
%%
%定义LSTM网络架构：
%将输入大小指定为序列大小 12（输入数据的维度）
%指定具有 100 个隐含单元的双向 LSTM 层，并输出序列的最后一个元素。
%指定九个类，包含大小为 9 的全连接层，后跟 softmax 层和分类层。
inputSize = 12;
numHiddenUnits = 100;
numClasses = 9;
layers = [ ...
    sequenceInputLayer(inputSize)
    bilstmLayer(numHiddenUnits,'OutputMode','last')
    fullyConnectedLayer(numClasses)
    softmaxLayer
    classificationLayer]
%%
%指定训练选项：
%求解器为 'adam'
%梯度阈值为 1，最大轮数为 100。
% 27 作为小批量数。
%填充数据以使长度与最长序列相同，序列长度指定为 'longest'。
%数据保持按序列长度排序的状态，不打乱数据。
% 'ExecutionEnvironment' 指定为 'cpu'，设定为'auto'表明使用GPU。
maxEpochs = 100;
miniBatchSize = 27;
options = trainingOptions('adam', ...
    'ExecutionEnvironment','cpu', ...
    'GradientThreshold',1, ...
    'MaxEpochs',maxEpochs, ...
    'MiniBatchSize',miniBatchSize, ...
    'SequenceLength','longest', ...
    'Shuffle','never', ...
    'Verbose',0, ...
    'Plots','training-progress');
%%
%训练LSTM网络
net = trainNetwork(XTrain,YTrain,layers,options);
%%
%测试LSTM网络
%加载测试集
[XTest,YTest] = japaneseVowelsTestData;
%由于LSTM已经按照相似长度的小批量分组27，测试需要按照相同方式对数据进行排序处理。
numObservationsTest = numel(XTest);
for i=1:numObservationsTest
    sequence = XTest{i};
    sequenceLengthsTest(i) = size(sequence,2);
end
[sequenceLengthsTest,idx] = sort(sequenceLengthsTest);
XTest = XTest(idx);
YTest = YTest(idx);
%使用classify进行分类，指定小批量大小27，指定组内数据按照最长的数据填充
miniBatchSize = 27;
YPred = classify(net,XTest, ...
    'MiniBatchSize',miniBatchSize, ...
    'SequenceLength','longest');
%计算分类准确度
acc = sum(YPred == YTest)./numel(YTest)