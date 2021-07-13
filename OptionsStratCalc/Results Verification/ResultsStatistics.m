close all
clear
clc
% I very much understand this code is incredibly inefficient, and
% there is a lot that could of been done to automate it, but I was
% lazy and took the brute force approach. I'm only doing this once,
% so I can't be asked to automate it.
%% PCS - Width Scaling

% Final profit
PCS15.P_W = [162410.21, 157103.01, 175131.26, 187510.83, 162162.8, 197015.56, 173376.3];
PCS15.P_Wavg = mean(PCS15.P_W);
PCS15.P_Wstd = std(PCS15.P_W);

PCS20.P_W = [207064.77, 232788.9, 231630.9, 212718.95, 223076.61,  217155.77, 233842.58];
PCS20.P_Wavg = mean(PCS20.P_W);
PCS20.P_Wstd = std(PCS20.P_W);

PCS25.P_W = [232292.41, 184393.65, 173715.65, 188956.6, 153053.55, 139764.67, 166117.72];
PCS25.P_Wavg = mean(PCS25.P_W);
PCS25.P_Wstd = std(PCS25.P_W);

PCS30.P_W = [186449.16, 138027.2, 182656.49, 189081.62, 196692.94, 186037.71, 125032.95];
PCS30.P_Wavg = mean(PCS30.P_W);
PCS30.P_Wstd = std(PCS30.P_W);

PCS35.P_W = [177806.39, 138163.79, 183899.21, 162133.14, 181197.7, 173803.2, 168864.14];
PCS35.P_Wavg = mean(PCS35.P_W);
PCS35.P_Wstd = std(PCS35.P_W);

PCS40.P_W = [24377.34, 67687.04, 59003.07, 41850.54, 60979.45, 46451.36, 105866.39];
PCS40.P_Wavg = mean(PCS40.P_W);
PCS40.P_Wstd = std(PCS40.P_W);


% Percent returns
PCS15.PR_W = [7.7852, 7.8232, 7.7967, 7.9009, 7.8531, 7.8809, 7.8886];
PCS15.PR_Wavg = mean(PCS15.PR_W);
PCS15.PR_Wstd = std(PCS15.PR_W);

PCS20.PR_W = [9.966, 9.966, 9.8545, 10.084, 10.0077, 10.037, 9.886];
PCS20.PR_Wavg = mean(PCS20.PR_W);
PCS20.PR_Wstd = std(PCS20.PR_W);

PCS25.PR_W = [12.2709, 12.5768, 12.902, 12.6481, 12.9682, 12.9561, 12.8744];
PCS25.PR_Wavg = mean(PCS25.PR_W);
PCS25.PR_Wstd = std(PCS25.PR_W);

PCS30.PR_W = [15.7759, 16.2162, 15.876, 15.5036, 15.7727, 15.8489, 16.0377];
PCS30.PR_Wavg = mean(PCS30.PR_W);
PCS30.PR_Wstd = std(PCS30.PR_W);

PCS35.PR_W = [19.8793,  21.9659, 19.9216, 21.0927, 19.6766, 20.3921, 20.9306];
PCS35.PR_Wavg = mean(PCS35.PR_W);
PCS35.PR_Wstd = std(PCS35.PR_W);

PCS40.PR_W = [31.6962, 27.6268, 26.5701, 30.3029, 28.0786, 29.4299, 25.6296];
PCS40.PR_Wavg = mean(PCS40.PR_W);
PCS40.PR_Wstd = std(PCS40.PR_W);


% Spreads traded
PCS15.ST_W = [1102, 1100, 1149, 1185, 1109, 1221, 1147];
PCS15.ST_Wavg = mean(PCS15.ST_W);
PCS15.ST_Wstd = std(PCS15.ST_W);

PCS20.ST_W = [1203, 1267, 1275, 1229, 1233, 1232, 1241];
PCS20.ST_Wavg = mean(PCS20.ST_W);
PCS20.ST_Wstd = std(PCS20.ST_W);

PCS25.ST_W = [1371, 1182, 1129, 1168, 1093, 1055, 1119];
PCS25.ST_Wavg = mean(PCS25.ST_W);
PCS25.ST_Wstd = std(PCS25.ST_W);

PCS30.ST_W = [1211, 1085, 1136, 1153, 1219, 1138, 1003];
PCS30.ST_Wavg = mean(PCS30.ST_W);
PCS30.ST_Wstd = std(PCS30.ST_W);

PCS35.ST_W = [1268, 1066, 1248, 1155, 1234, 1219, 1168];
PCS35.ST_Wavg = mean(PCS35.ST_W);
PCS35.ST_Wstd = std(PCS35.ST_W);

PCS40.ST_W = [1006, 1050, 1071, 1012, 1037, 1040, 1173];
PCS40.ST_Wavg = mean(PCS40.ST_W);
PCS40.ST_Wstd = std(PCS40.ST_W);


% Full wins
PCS15.FW_W = [709, 707, 710, 713, 709, 715, 709];
PCS15.FW_Wavg = mean(PCS15.FW_W);
PCS15.FW_Wstd = std(PCS15.FW_W);

PCS20.FW_W = [670, 677, 677, 671, 675, 672, 678];
PCS20.FW_Wavg = mean(PCS20.FW_W);
PCS20.FW_Wstd = std(PCS20.FW_W);

PCS25.FW_W = [640, 633, 629, 631, 625, 624, 628];
PCS25.FW_Wavg = mean(PCS25.FW_W);
PCS25.FW_Wstd = std(PCS25.FW_W);

PCS30.FW_W = [607, 604, 612, 608, 610, 610, 602];
PCS30.FW_Wavg = mean(PCS30.FW_W);
PCS30.FW_Wstd = std(PCS30.FW_W);

PCS35.FW_W = [569, 564, 572, 566, 572, 569, 570];
PCS35.FW_Wavg = mean(PCS35.FW_W);
PCS35.FW_Wstd = std(PCS35.FW_W);

PCS40.FW_W = [531, 532, 540, 529, 537, 535, 541];
PCS40.FW_Wavg = mean(PCS40.FW_W);
PCS40.FW_Wstd = std(PCS40.FW_W);


% Partial wins
PCS15.PW_W = [2, 2, 2, 2, 2, 2, 2];
PCS15.PW_Wavg = mean(PCS15.PW_W);
PCS15.PW_Wstddev = std(PCS15.PW_W);

PCS20.PW_W = [10, 10, 10, 10, 10, 10, 10];
PCS20.PW_Wavg = mean(PCS20.PW_W);
PCS20.PW_Wstd = std(PCS20.PW_W);

PCS25.PW_W = [18, 16, 15, 16, 15, 15, 14];
PCS25.PW_Wavg = mean(PCS25.PW_W);
PCS25.PW_Wstd = std(PCS25.PW_W);

PCS30.PW_W = [16, 14, 15, 16, 15, 15, 14];
PCS30.PW_Wavg = mean(PCS30.PW_W );
PCS30.PW_Wstd = std(PCS30.PW_W );

PCS35.PW_W = [33, 31, 33, 31, 34, 33, 31];
PCS35.PW_Wavg = mean(PCS35.PW_W);
PCS35.PW_Wstd = std(PCS35.PW_W);

PCS40.PW_W = [31, 37, 38, 36, 37, 37, 39];
PCS40.PW_Wavg = mean(PCS40.PW_W);
PCS40.PW_Wstd = std(PCS40.PW_W);


% Partial losses
PCS15.PL_W = [69, 71, 68, 65, 69, 63, 69];
PCS15.PL_Wavg = mean(PCS15.PL_W);
PCS15.PL_Wstd = std(PCS15.PL_W);

PCS20.PL_W = [100, 93, 93, 99, 95, 98, 92];
PCS20.PL_Wavg = mean(PCS20.PL_W);
PCS20.PL_Wstd = std(PCS20.PL_W);

PCS25.PL_W = [122, 131, 136, 133, 140, 141, 138];
PCS25.PL_Wavg = mean(PCS25.PL_W);
PCS25.PL_Wstd = std(PCS25.PL_W);

PCS30.PL_W = [157, 162, 153, 156, 155, 155, 164];
PCS30.PL_Wavg = mean(PCS30.PL_W);
PCS30.PL_Wstd = std(PCS30.PL_W);

PCS35.PL_W = [178, 185, 175, 183, 174, 178, 179];
PCS35.PL_Wavg = mean(PCS35.PL_W);
PCS35.PL_Wstd = std(PCS35.PL_W);

PCS40.PL_W = [218, 211, 202, 215, 206, 208, 200];
PCS40.PL_Wavg = mean(PCS40.PL_W);
PCS40.PL_Wstd = std(PCS40.PL_W);

% Taxes and comissions are based on mean values

%% PCS - Contract Scaling

% Final profit
PCS15.P_C = [410575.48, 412821.45, 404786.81, 413639.56, 422723.29, 425039.8, 397937.38];
PCS15.P_Cavg = mean(PCS15.P_C);
PCS15.P_Cstd = std(PCS15.P_C);

PCS20.P_C = [581849.21, 559228.58, 544715.17, 556125.1, 538304.22, 529844.7, 573624.55];
PCS20.P_Cavg = mean(PCS20.P_C);
PCS20.P_Cstd = std(PCS20.P_C);

PCS25.P_C = [546825.76, 603259.58, 580098.72, 527551.37, 581275.08, 580930.39, 573508.08];
PCS25.P_Cavg = mean(PCS25.P_C);
PCS25.P_Cstd = std(PCS25.P_C);

PCS30.P_C = [439656.67, 592654.2, 653182.11, 555346.67, 505368.68, 595682.37, 550266.04];
PCS30.P_Cavg = mean(PCS30.P_C);
PCS30.P_Cstd = std(PCS30.P_C);

PCS35.P_C = [169537.92, 401896.38, 222619.71,348526.65, 142725.2, 314271.42, 285837.48];
PCS35.P_Cavg = mean(PCS35.P_C);
PCS35.P_Cstd = std(PCS35.P_C);

PCS40.P_C = [186.0, 100.45, 15280.76, 5519.54, 8635.19, 393.95, 5091.49];
PCS40.P_Cavg = mean(PCS40.P_C);
PCS40.P_Cstd = std(PCS40.P_C);


% Percent returns
PCS15.PR_C = [9.3601, 9.2999, 9.3345, 9.2999, 9.3024, 9.2537, 9.3345];
PCS15.PR_Cavg = mean(PCS15.PR_C);
PCS15.PR_Cstd = std(PCS15.PR_C);

PCS20.PR_C = [13.5466, 13.5248, 13.5543, 13.5594, 13.5953, 13.5299, 13.585];
PCS20.PR_Cavg = mean(PCS20.PR_C);
PCS20.PR_Cstd = std(PCS20.PR_C);

PCS25.PR_C = [18.3672, 18.4672, 18.4364, 18.4339, 18.4121, 18.4005, 18.4339];
PCS25.PR_Cavg = mean(PCS25.PR_C);
PCS25.PR_Cstd = std(PCS25.PR_C);

PCS30.PR_C = [23.9545, 23.9993, 23.9647, 24.0019, 23.9301, 23.9468, 23.9493];
PCS30.PR_Cavg = mean(PCS30.PR_C);
PCS30.PR_Cstd = std(PCS30.PR_C);

PCS35.PR_C = [30.807, 30.8403, 30.8403, 30.8224, 30.866, 30.7942, 30.8236];
PCS35.PR_Cavg = mean(PCS35.PR_C);
PCS35.PR_Cstd = std(PCS35.PR_C);

PCS40.PR_C = [38.2512, 38.1961, 38.2717, 38.1743, 38.273, 38.2486, 38.2512];
PCS40.PR_Cavg = mean(PCS40.PR_C);
PCS40.PR_Cstd = std(PCS40.PR_C);


% Spreads traded
PCS15.ST_C = [15976, 16001, 15716, 15770, 16333, 16155, 15478];
PCS15.ST_Cavg = mean(PCS15.ST_C);
PCS15.ST_Cstd = std(PCS15.ST_C);

PCS20.ST_C = [21905, 22092, 22017, 21744, 21596, 21509, 22203];
PCS20.ST_Cavg = mean(PCS20.ST_C);
PCS20.ST_Cstd = std(PCS20.ST_C);

PCS25.ST_C = [24071, 25151, 24871, 24884, 24800, 24180, 24545];
PCS25.ST_Cavg = mean(PCS25.ST_C);
PCS25.ST_Cstd = std(PCS25.ST_C);

PCS30.ST_C = [21719, 26769, 28532, 26112, 23614, 27029, 26517];
PCS30.ST_Cavg = mean(PCS30.ST_C);
PCS30.ST_Cstd = std(PCS30.ST_C);

PCS35.ST_C = [19441, 28213, 26715, 28128, 20453, 26319, 27050];
PCS35.ST_Cavg = mean(PCS35.ST_C);
PCS35.ST_Cstd = std(PCS35.ST_C);

PCS40.ST_C = [1464, 2351, 7426, 3145, 4722, 3147, 3878];
PCS40.ST_Cavg = mean(PCS40.ST_C);
PCS40.ST_Cstd = std(PCS40.ST_C);


% Full wins
PCS15.FW_C = [711, 711, 709, 712, 714, 715, 707];
PCS15.FW_Cavg = mean(PCS15.FW_C);
PCS15.FW_Cstd = std(PCS15.FW_C);

PCS20.FW_C = [677, 674, 672, 673, 670, 670, 677];
PCS20.FW_Cavg = mean(PCS20.FW_C);
PCS20.FW_Cstd = std(PCS20.FW_C);

PCS25.FW_C = [626, 632, 631, 624, 630, 631, 629];
PCS25.FW_Cavg = mean(PCS25.FW_C);
PCS25.FW_Cstd = std(PCS25.FW_C);

PCS30.FW_C = [597, 610, 615, 607, 604, 608, 606];
PCS30.FW_Cavg = mean(PCS30.FW_C);
PCS30.FW_Cstd = std(PCS30.FW_C);

PCS35.FW_C = [567, 576, 564, 571, 565, 569, 569];
PCS35.FW_Cavg = mean(PCS35.FW_C);
PCS35.FW_Cstd = std(PCS35.FW_C);

PCS40.FW_C = [528, 528, 545, 535, 536, 531, 537];
PCS40.FW_Cavg = mean(PCS40.FW_C);
PCS40.FW_Cstd = std(PCS40.FW_C);


% Partial wins
PCS15.PW_C = [0, 0, 0, 0, 0, 0, 0];
PCS15.PW_Cavg = mean(PCS15.PW_C);
PCS15.PW_Cstddev = std(PCS15.PW_C);

PCS20.PW_C = [1, 1, 1, 1, 1, 1, 1];
PCS20.PW_Cavg = mean(PCS20.PW_C);
PCS20.PW_Cstd = std(PCS20.PW_C);

PCS25.PW_C = [7, 7, 7, 7, 7, 7, 7];
PCS25.PW_Cavg = mean(PCS25.PW_C);
PCS25.PW_Cstd = std(PCS25.PW_C);

PCS30.PW_C = [5, 5, 5, 5, 5, 5, 5];
PCS30.PW_Cavg = mean(PCS30.PW_C );
PCS30.PW_Cstd = std(PCS30.PW_C );

PCS35.PW_C = [10, 10, 10, 10, 10, 10, 10];
PCS35.PW_Cavg = mean(PCS35.PW_C);
PCS35.PW_Cstd = std(PCS35.PW_C);

PCS40.PW_C = [14, 14, 14, 14, 14, 14, 14];
PCS40.PW_Cavg = mean(PCS40.PW_C);
PCS40.PW_Cstd = std(PCS40.PW_C);


% Partial losses
PCS15.PL_C = [69, 69, 71, 68, 66, 65, 73];
PCS15.PL_Cavg = mean(PCS15.PL_C);
PCS15.PL_Cstd = std(PCS15.PL_C);

PCS20.PL_C = [102, 105, 107, 106, 109, 109, 102];
PCS20.PL_Cavg = mean(PCS20.PL_C);
PCS20.PL_Cstd = std(PCS20.PL_C);

PCS25.PL_C = [147, 141, 142, 149, 143, 142, 144];
PCS25.PL_Cavg = mean(PCS25.PL_C);
PCS25.PL_Cstd = std(PCS25.PL_C);

PCS30.PL_C = [178, 165, 160, 168, 171, 167, 169];
PCS30.PL_Cavg = mean(PCS30.PL_C);
PCS30.PL_Cstd = std(PCS30.PL_C);

PCS35.PL_C = [203, 194, 206, 199, 205, 201, 201];
PCS35.PL_Cavg = mean(PCS35.PL_C);
PCS35.PL_Cstd = std(PCS35.PL_C);

PCS40.PL_C = [238, 238, 221, 231, 230, 235, 229];
PCS40.PL_Cavg = mean(PCS40.PL_C);
PCS40.PL_Cstd = std(PCS40.PL_C);

% Taxes and comissions are based on mean values

%% CCS - Width Scaling
% Final profit
CCS15.P_W = [81070.21 ];
CCS15.P_Wavg = mean(CCS15.P_W);
CCS15.P_Wstd = std(CCS15.P_W);

CCS20.P_W = [61667.68];
CCS20.P_Wavg = mean(CCS20.P_W);
CCS20.P_Wstd = std(CCS20.P_W);

CCS25.P_W = [28943.28];
CCS25.P_Wavg = mean(CCS25.P_W);
CCS25.P_Wstd = std(CCS25.P_W);

CCS30.P_W = [];
CCS30.P_Wavg = mean(CCS30.P_W);
CCS30.P_Wstd = std(CCS30.P_W);

CCS35.P_W = [];
CCS35.P_Wavg = mean(CCS35.P_W);
CCS35.P_Wstd = std(CCS35.P_W);

CCS40.P_W = [];
CCS40.P_Wavg = mean(CCS40.P_W);
CCS40.P_Wstd = std(CCS40.P_W);


% Percent returns
CCS15.PR_W = [7.7896 ];
CCS15.PR_Wavg = mean(CCS15.PR_W);
CCS15.PR_Wstd = std(CCS15.PR_W);

CCS20.PR_W = [9.2003 ];
CCS20.PR_Wavg = mean(CCS20.PR_W);
CCS20.PR_Wstd = std(CCS20.PR_W);

CCS25.PR_W = [13.4814 ];
CCS25.PR_Wavg = mean(CCS25.PR_W);
CCS25.PR_Wstd = std(CCS25.PR_W);

CCS30.PR_W = [];
CCS30.PR_Wavg = mean(CCS30.PR_W);
CCS30.PR_Wstd = std(CCS30.PR_W);

CCS35.PR_W = [];
CCS35.PR_Wavg = mean(CCS35.PR_W);
CCS35.PR_Wstd = std(CCS35.PR_W);

CCS40.PR_W = [];
CCS40.PR_Wavg = mean(CCS40.PR_W);
CCS40.PR_Wstd = std(CCS40.PR_W);


% Spreads traded
CCS15.ST_W = [863 ];
CCS15.ST_Wavg = mean(CCS15.ST_W);
CCS15.ST_Wstd = std(CCS15.ST_W);

CCS20.ST_W = [834];
CCS20.ST_Wavg = mean(CCS20.ST_W);
CCS20.ST_Wstd = std(CCS20.ST_W);

CCS25.ST_W = [812];
CCS25.ST_Wavg = mean(CCS25.ST_W);
CCS25.ST_Wstd = std(CCS25.ST_W);

CCS30.ST_W = [];
CCS30.ST_Wavg = mean(CCS30.ST_W);
CCS30.ST_Wstd = std(CCS30.ST_W);

CCS35.ST_W = [];
CCS35.ST_Wavg = mean(CCS35.ST_W);
CCS35.ST_Wstd = std(CCS35.ST_W);

CCS40.ST_W = [];
CCS40.ST_Wavg = mean(CCS40.ST_W);
CCS40.ST_Wstd = std(CCS40.ST_W);


% Full wins
CCS15.FW_W = [655];
CCS15.FW_Wavg = mean(CCS15.FW_W);
CCS15.FW_Wstd = std(CCS15.FW_W);

CCS20.FW_W = [613 ];
CCS20.FW_Wavg = mean(CCS20.FW_W);
CCS20.FW_Wstd = std(CCS20.FW_W);

CCS25.FW_W = [553];
CCS25.FW_Wavg = mean(CCS25.FW_W);
CCS25.FW_Wstd = std(CCS25.FW_W);

CCS30.FW_W = [];
CCS30.FW_Wavg = mean(CCS30.FW_W);
CCS30.FW_Wstd = std(CCS30.FW_W);

CCS35.FW_W = [];
CCS35.FW_Wavg = mean(CCS35.FW_W);
CCS35.FW_Wstd = std(CCS35.FW_W);

CCS40.FW_W = [];
CCS40.FW_Wavg = mean(CCS40.FW_W);
CCS40.FW_Wstd = std(CCS40.FW_W);


% Partial wins
CCS15.PW_W = [1];
CCS15.PW_Wavg = mean(CCS15.PW_W);
CCS15.PW_Wstddev = std(CCS15.PW_W);

CCS20.PW_W = [10 ];
CCS20.PW_Wavg = mean(CCS20.PW_W);
CCS20.PW_Wstd = std(CCS20.PW_W);

CCS25.PW_W = [20];
CCS25.PW_Wavg = mean(CCS25.PW_W);
CCS25.PW_Wstd = std(CCS25.PW_W);

CCS30.PW_W = [];
CCS30.PW_Wavg = mean(CCS30.PW_W );
CCS30.PW_Wstd = std(CCS30.PW_W );

CCS35.PW_W = [];
CCS35.PW_Wavg = mean(CCS35.PW_W);
CCS35.PW_Wstd = std(CCS35.PW_W);

CCS40.PW_W = [];
CCS40.PW_Wavg = mean(CCS40.PW_W);
CCS40.PW_Wstd = std(CCS40.PW_W);


% Partial losses
CCS15.PL_W = [124];
CCS15.PL_Wavg = mean(CCS15.PL_W);
CCS15.PL_Wstd = std(CCS15.PL_W);

CCS20.PL_W = [157];
CCS20.PL_Wavg = mean(CCS20.PL_W);
CCS20.PL_Wstd = std(CCS20.PL_W);

CCS25.PL_W = [207];
CCS25.PL_Wavg = mean(CCS25.PL_W);
CCS25.PL_Wstd = std(CCS25.PL_W);

CCS30.PL_W = [];
CCS30.PL_Wavg = mean(CCS30.PL_W);
CCS30.PL_Wstd = std(CCS30.PL_W);

CCS35.PL_W = [];
CCS35.PL_Wavg = mean(CCS35.PL_W);
CCS35.PL_Wstd = std(CCS35.PL_W);

CCS40.PL_W = [];
CCS40.PL_Wavg = mean(CCS40.PL_W);
CCS40.PL_Wstd = std(CCS40.PL_W);

% Taxes and comissions are based on mean values

%% CCS - Contract Scaling

% Final profit
CCS15.P_C = [155265.55 ];
CCS15.P_Cavg = mean(CCS15.P_C);
CCS15.P_Cstd = std(CCS15.P_C);

CCS20.P_C = [254529.73 ];
CCS20.P_Cavg = mean(CCS20.P_C);
CCS20.P_Cstd = std(CCS20.P_C);

CCS25.P_C = [22202.74 ];
CCS25.P_Cavg = mean(CCS25.P_C);
CCS25.P_Cstd = std(CCS25.P_C);

CCS30.P_C = [-3035.1 ];
CCS30.P_Cavg = mean(CCS30.P_C);
CCS30.P_Cstd = std(CCS30.P_C);

CCS35.P_C = [];
CCS35.P_Cavg = mean(CCS35.P_C);
CCS35.P_Cstd = std(CCS35.P_C);

CCS40.P_C = [];
CCS40.P_Cavg = mean(CCS40.P_C);
CCS40.P_Cstd = std(CCS40.P_C);


% Percent returns
CCS15.PR_C = [8.5156  ];
CCS15.PR_Cavg = mean(CCS15.PR_C);
CCS15.PR_Cstd = std(CCS15.PR_C);

CCS20.PR_C = [12.1399 ];
CCS20.PR_Cavg = mean(CCS20.PR_C);
CCS20.PR_Cstd = std(CCS20.PR_C);

CCS25.PR_C = [16.2817 ];
CCS25.PR_Cavg = mean(CCS25.PR_C);
CCS25.PR_Cstd = std(CCS25.PR_C);

CCS30.PR_C = [20.3446 ];
CCS30.PR_Cavg = mean(CCS30.PR_C);
CCS30.PR_Cstd = std(CCS30.PR_C);

CCS35.PR_C = [];
CCS35.PR_Cavg = mean(CCS35.PR_C);
CCS35.PR_Cstd = std(CCS35.PR_C);

CCS40.PR_C = [];
CCS40.PR_Cavg = mean(CCS40.PR_C);
CCS40.PR_Cstd = std(CCS40.PR_C);


% Spreads traded
CCS15.ST_C = [10120 ];
CCS15.ST_Cavg = mean(CCS15.ST_C);
CCS15.ST_Cstd = std(CCS15.ST_C);

CCS20.ST_C = [14218 ];
CCS20.ST_Cavg = mean(CCS20.ST_C);
CCS20.ST_Cstd = std(CCS20.ST_C);

CCS25.ST_C = [3123 ];
CCS25.ST_Cavg = mean(CCS25.ST_C);
CCS25.ST_Cstd = std(CCS25.ST_C);

CCS30.ST_C = [591];
CCS30.ST_Cavg = mean(CCS30.ST_C);
CCS30.ST_Cstd = std(CCS30.ST_C);

CCS35.ST_C = [];
CCS35.ST_Cavg = mean(CCS35.ST_C);
CCS35.ST_Cstd = std(CCS35.ST_C);

CCS40.ST_C = [];
CCS40.ST_Cavg = mean(CCS40.ST_C);
CCS40.ST_Cstd = std(CCS40.ST_C);


% Full wins
CCS15.FW_C = [645 ];
CCS15.FW_Cavg = mean(CCS15.FW_C);
CCS15.FW_Cstd = std(CCS15.FW_C);

CCS20.FW_C = [623 ];
CCS20.FW_Cavg = mean(CCS20.FW_C);
CCS20.FW_Cstd = std(CCS20.FW_C);

CCS25.FW_C = [564];
CCS25.FW_Cavg = mean(CCS25.FW_C);
CCS25.FW_Cstd = std(CCS25.FW_C);

CCS30.FW_C = [389 ];
CCS30.FW_Cavg = mean(CCS30.FW_C);
CCS30.FW_Cstd = std(CCS30.FW_C);

CCS35.FW_C = [];
CCS35.FW_Cavg = mean(CCS35.FW_C);
CCS35.FW_Cstd = std(CCS35.FW_C);

CCS40.FW_C = [];
CCS40.FW_Cavg = mean(CCS40.FW_C);
CCS40.FW_Cstd = std(CCS40.FW_C);


% Partial wins
CCS15.PW_C = [1 ];
CCS15.PW_Cavg = mean(CCS15.PW_C);
CCS15.PW_Cstddev = std(CCS15.PW_C);

CCS20.PW_C = [5 ];
CCS20.PW_Cavg = mean(CCS20.PW_C);
CCS20.PW_Cstd = std(CCS20.PW_C);

CCS25.PW_C = [8];
CCS25.PW_Cavg = mean(CCS25.PW_C);
CCS25.PW_Cstd = std(CCS25.PW_C);

CCS30.PW_C = [7 ];
CCS30.PW_Cavg = mean(CCS30.PW_C );
CCS30.PW_Cstd = std(CCS30.PW_C );

CCS35.PW_C = [];
CCS35.PW_Cavg = mean(CCS35.PW_C);
CCS35.PW_Cstd = std(CCS35.PW_C);

CCS40.PW_C = [];
CCS40.PW_Cavg = mean(CCS40.PW_C);
CCS40.PW_Cstd = std(CCS40.PW_C);


% Partial losses
CCS15.PL_C = [134];
CCS15.PL_Cavg = mean(CCS15.PL_C);
CCS15.PL_Cstd = std(CCS15.PL_C);

CCS20.PL_C = [152 ];
CCS20.PL_Cavg = mean(CCS20.PL_C);
CCS20.PL_Cstd = std(CCS20.PL_C);

CCS25.PL_C = [208];
CCS25.PL_Cavg = mean(CCS25.PL_C);
CCS25.PL_Cstd = std(CCS25.PL_C);

CCS30.PL_C = [190 ];
CCS30.PL_Cavg = mean(CCS30.PL_C);
CCS30.PL_Cstd = std(CCS30.PL_C);

CCS35.PL_C = [];
CCS35.PL_Cavg = mean(CCS35.PL_C);
CCS35.PL_Cstd = std(CCS35.PL_C);

CCS40.PL_C = [];
CCS40.PL_Cavg = mean(CCS40.PL_C);
CCS40.PL_Cstd = std(CCS40.PL_C);

% Taxes and comissions are based on mean values

%% IC - Width Scaling
% Final profit
IC15.P_W = [];
IC15.P_Wavg = mean(IC15.P_W);
IC15.P_Wstd = std(IC15.P_W);

IC20.P_W = [];
IC20.P_Wavg = mean(IC20.P_W);
IC20.P_Wstd = std(IC20.P_W);

IC25.P_W = [];
IC25.P_Wavg = mean(IC25.P_W);
IC25.P_Wstd = std(IC25.P_W);

IC30.P_W = [];
IC30.P_Wavg = mean(IC30.P_W);
IC30.P_Wstd = std(IC30.P_W);

IC35.P_W = [];
IC35.P_Wavg = mean(IC35.P_W);
IC35.P_Wstd = std(IC35.P_W);

IC40.P_W = [];
IC40.P_Wavg = mean(IC40.P_W);
IC40.P_Wstd = std(IC40.P_W);


% Percent returns
IC15.PR_W = [];
IC15.PR_Wavg = mean(IC15.PR_W);
IC15.PR_Wstd = std(IC15.PR_W);

IC20.PR_W = [];
IC20.PR_Wavg = mean(IC20.PR_W);
IC20.PR_Wstd = std(IC20.PR_W);

IC25.PR_W = [];
IC25.PR_Wavg = mean(IC25.PR_W);
IC25.PR_Wstd = std(IC25.PR_W);

IC30.PR_W = [];
IC30.PR_Wavg = mean(IC30.PR_W);
IC30.PR_Wstd = std(IC30.PR_W);

IC35.PR_W = [];
IC35.PR_Wavg = mean(IC35.PR_W);
IC35.PR_Wstd = std(IC35.PR_W);

IC40.PR_W = [];
IC40.PR_Wavg = mean(IC40.PR_W);
IC40.PR_Wstd = std(IC40.PR_W);


% Spreads traded
IC15.ST_W = [];
IC15.ST_Wavg = mean(IC15.ST_W);
IC15.ST_Wstd = std(IC15.ST_W);

IC20.ST_W = [];
IC20.ST_Wavg = mean(IC20.ST_W);
IC20.ST_Wstd = std(IC20.ST_W);

IC25.ST_W = [];
IC25.ST_Wavg = mean(IC25.ST_W);
IC25.ST_Wstd = std(IC25.ST_W);

IC30.ST_W = [];
IC30.ST_Wavg = mean(IC30.ST_W);
IC30.ST_Wstd = std(IC30.ST_W);

IC35.ST_W = [];
IC35.ST_Wavg = mean(IC35.ST_W);
IC35.ST_Wstd = std(IC35.ST_W);

IC40.ST_W = [];
IC40.ST_Wavg = mean(IC40.ST_W);
IC40.ST_Wstd = std(IC40.ST_W);


% Full wins
IC15.FW_W = [];
IC15.FW_Wavg = mean(IC15.FW_W);
IC15.FW_Wstd = std(IC15.FW_W);

IC20.FW_W = [];
IC20.FW_Wavg = mean(IC20.FW_W);
IC20.FW_Wstd = std(IC20.FW_W);

IC25.FW_W = [];
IC25.FW_Wavg = mean(IC25.FW_W);
IC25.FW_Wstd = std(IC25.FW_W);

IC30.FW_W = [];
IC30.FW_Wavg = mean(IC30.FW_W);
IC30.FW_Wstd = std(IC30.FW_W);

IC35.FW_W = [];
IC35.FW_Wavg = mean(IC35.FW_W);
IC35.FW_Wstd = std(IC35.FW_W);

IC40.FW_W = [];
IC40.FW_Wavg = mean(IC40.FW_W);
IC40.FW_Wstd = std(IC40.FW_W);


% Partial wins
IC15.PW_W = [];
IC15.PW_Wavg = mean(IC15.PW_W);
IC15.PW_Wstddev = std(IC15.PW_W);

IC20.PW_W = [];
IC20.PW_Wavg = mean(IC20.PW_W);
IC20.PW_Wstd = std(IC20.PW_W);

IC25.PW_W = [];
IC25.PW_Wavg = mean(IC25.PW_W);
IC25.PW_Wstd = std(IC25.PW_W);

IC30.PW_W = [];
IC30.PW_Wavg = mean(IC30.PW_W );
IC30.PW_Wstd = std(IC30.PW_W );

IC35.PW_W = [];
IC35.PW_Wavg = mean(IC35.PW_W);
IC35.PW_Wstd = std(IC35.PW_W);

IC40.PW_W = [];
IC40.PW_Wavg = mean(IC40.PW_W);
IC40.PW_Wstd = std(IC40.PW_W);


% Partial losses
IC15.PL_W = [];
IC15.PL_Wavg = mean(IC15.PL_W);
IC15.PL_Wstd = std(IC15.PL_W);

IC20.PL_W = [];
IC20.PL_Wavg = mean(IC20.PL_W);
IC20.PL_Wstd = std(IC20.PL_W);

IC25.PL_W = [];
IC25.PL_Wavg = mean(IC25.PL_W);
IC25.PL_Wstd = std(IC25.PL_W);

IC30.PL_W = [];
IC30.PL_Wavg = mean(IC30.PL_W);
IC30.PL_Wstd = std(IC30.PL_W);

IC35.PL_W = [];
IC35.PL_Wavg = mean(IC35.PL_W);
IC35.PL_Wstd = std(IC35.PL_W);

IC40.PL_W = [];
IC40.PL_Wavg = mean(IC40.PL_W);
IC40.PL_Wstd = std(IC40.PL_W);

% Taxes and comissions are based on mean values

%% IC - Contract Scaling

% Final profit
IC15.P_C = [];
IC15.P_Cavg = mean(IC15.P_C);
IC15.P_Cstd = std(IC15.P_C);

IC20.P_C = [];
IC20.P_Cavg = mean(IC20.P_C);
IC20.P_Cstd = std(IC20.P_C);

IC25.P_C = [];
IC25.P_Cavg = mean(IC25.P_C);
IC25.P_Cstd = std(IC25.P_C);

IC30.P_C = [];
IC30.P_Cavg = mean(IC30.P_C);
IC30.P_Cstd = std(IC30.P_C);

IC35.P_C = [];
IC35.P_Cavg = mean(IC35.P_C);
IC35.P_Cstd = std(IC35.P_C);

IC40.P_C = [];
IC40.P_Cavg = mean(IC40.P_C);
IC40.P_Cstd = std(IC40.P_C);


% Percent returns
IC15.PR_C = [];
IC15.PR_Cavg = mean(IC15.PR_C);
IC15.PR_Cstd = std(IC15.PR_C);

IC20.PR_C = [];
IC20.PR_Cavg = mean(IC20.PR_C);
IC20.PR_Cstd = std(IC20.PR_C);

IC25.PR_C = [];
IC25.PR_Cavg = mean(IC25.PR_C);
IC25.PR_Cstd = std(IC25.PR_C);

IC30.PR_C = [];
IC30.PR_Cavg = mean(IC30.PR_C);
IC30.PR_Cstd = std(IC30.PR_C);

IC35.PR_C = [];
IC35.PR_Cavg = mean(IC35.PR_C);
IC35.PR_Cstd = std(IC35.PR_C);

IC40.PR_C = [];
IC40.PR_Cavg = mean(IC40.PR_C);
IC40.PR_Cstd = std(IC40.PR_C);


% Spreads traded
IC15.ST_C = [];
IC15.ST_Cavg = mean(IC15.ST_C);
IC15.ST_Cstd = std(IC15.ST_C);

IC20.ST_C = [];
IC20.ST_Cavg = mean(IC20.ST_C);
IC20.ST_Cstd = std(IC20.ST_C);

IC25.ST_C = [];
IC25.ST_Cavg = mean(IC25.ST_C);
IC25.ST_Cstd = std(IC25.ST_C);

IC30.ST_C = [];
IC30.ST_Cavg = mean(IC30.ST_C);
IC30.ST_Cstd = std(IC30.ST_C);

IC35.ST_C = [];
IC35.ST_Cavg = mean(IC35.ST_C);
IC35.ST_Cstd = std(IC35.ST_C);

IC40.ST_C = [];
IC40.ST_Cavg = mean(IC40.ST_C);
IC40.ST_Cstd = std(IC40.ST_C);


% Full wins
IC15.FW_C = [];
IC15.FW_Cavg = mean(IC15.FW_C);
IC15.FW_Cstd = std(IC15.FW_C);

IC20.FW_C = [];
IC20.FW_Cavg = mean(IC20.FW_C);
IC20.FW_Cstd = std(IC20.FW_C);

IC25.FW_C = [];
IC25.FW_Cavg = mean(IC25.FW_C);
IC25.FW_Cstd = std(IC25.FW_C);

IC30.FW_C = [];
IC30.FW_Cavg = mean(IC30.FW_C);
IC30.FW_Cstd = std(IC30.FW_C);

IC35.FW_C = [];
IC35.FW_Cavg = mean(IC35.FW_C);
IC35.FW_Cstd = std(IC35.FW_C);

IC40.FW_C = [];
IC40.FW_Cavg = mean(IC40.FW_C);
IC40.FW_Cstd = std(IC40.FW_C);


% Partial wins
IC15.PW_C = [];
IC15.PW_Cavg = mean(IC15.PW_C);
IC15.PW_Cstddev = std(IC15.PW_C);

IC20.PW_C = [];
IC20.PW_Cavg = mean(IC20.PW_C);
IC20.PW_Cstd = std(IC20.PW_C);

IC25.PW_C = [];
IC25.PW_Cavg = mean(IC25.PW_C);
IC25.PW_Cstd = std(IC25.PW_C);

IC30.PW_C = [];
IC30.PW_Cavg = mean(IC30.PW_C );
IC30.PW_Cstd = std(IC30.PW_C );

IC35.PW_C = [];
IC35.PW_Cavg = mean(IC35.PW_C);
IC35.PW_Cstd = std(IC35.PW_C);

IC40.PW_C = [];
IC40.PW_Cavg = mean(IC40.PW_C);
IC40.PW_Cstd = std(IC40.PW_C);


% Partial losses
IC15.PL_C = [];
IC15.PL_Cavg = mean(IC15.PL_C);
IC15.PL_Cstd = std(IC15.PL_C);

IC20.PL_C = [];
IC20.PL_Cavg = mean(IC20.PL_C);
IC20.PL_Cstd = std(IC20.PL_C);

IC25.PL_C = [];
IC25.PL_Cavg = mean(IC25.PL_C);
IC25.PL_Cstd = std(IC25.PL_C);

IC30.PL_C = [];
IC30.PL_Cavg = mean(IC30.PL_C);
IC30.PL_Cstd = std(IC30.PL_C);

IC35.PL_C = [];
IC35.PL_Cavg = mean(IC35.PL_C);
IC35.PL_Cstd = std(IC35.PL_C);

IC40.PL_C = [];
IC40.PL_Cavg = mean(IC40.PL_C);
IC40.PL_Cstd = std(IC40.PL_C);

% Taxes and comissions are based on mean values



