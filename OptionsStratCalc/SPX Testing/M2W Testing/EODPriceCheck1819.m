% Checks the difference between the prices of SPX at close
% and at 15 minutes, 10 minutes, 5 minutes, and 1 minute 
% before close
% AYC - All years included, runs the same thing for all years
close all
clear
clc
%% Data Files
Set1 = SPReader('C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData\SPXMinuteData\SANDP-500_180901_190901.csv');

%% Sept 2016 -  Sept 2017
Min15Price = [];
Min10Price = [];
Min5Price = [];
Min1Price = [];
ClosePrice = [];

for i = 1:height(Set1)
    TVal = table2array(Set1(i, 4));
    PVal = table2array(Set1(i, 8));
    if TVal == 160000
        ClosePrice = [ClosePrice PVal];
        for j = i:-1:i-30
            TVal2 = table2array(Set1(j, 4));
            PVal2 =  table2array(Set1(j, 8));
            if TVal2 == 154500
                Min15Price = [Min15Price PVal2];
            elseif TVal2 == 155000
                Min10Price = [Min10Price PVal2];
            elseif TVal2 == 155500
                Min5Price = [Min5Price PVal2];
            elseif TVal2 == 155900
                Min1Price = [Min1Price PVal2];
            end
        end
    end
end

Delta15M = Min15Price - ClosePrice;
Delta10M = Min10Price - ClosePrice;
Delta5M = Min5Price - ClosePrice;
Delta1M = Min1Price - ClosePrice;

%% 15M 
figure()
histogram(Delta15M, 'BinWidth', 1)
xlabel('Difference in Price')
ylabel('Number of occurance')
title('15 Minutes Before Close (Sept 2018 - Sept 2019)')
xlim([-20 20])

figure()
hold on
PD15 = makedist('Normal', 'mu', mean(Delta15M), 'sigma', std(Delta15M));
PDF15= pdf(PD15, sort(Delta15M));
plot(sort(Delta15M), PDF15, 'k', 'linewidth', 2)
plot([mean(Delta15M) - std(Delta15M), mean(Delta15M) - std(Delta15M)], [0 max(PDF15)], '-.b')
plot([mean(Delta15M) + std(Delta15M), mean(Delta15M) + std(Delta15M)], [0 max(PDF15)], '-.b')
plot([mean(Delta15M) - 2*std(Delta15M), mean(Delta15M) - 2*std(Delta15M)], [0 max(PDF15)], '-.r')
plot([mean(Delta15M) + 2*std(Delta15M), mean(Delta15M) + 2*std(Delta15M)], [0 max(PDF15)], '-.r')
xlabel('Difference to Closing Price')
ylabel('% Chance of Occurance')
title('15 Minutes Before Close (Sept 2018 - Sept 2019)')
ylim([0, max(PDF15)])

%% 10M
figure()
histogram(Delta10M, 'BinWidth', 1)
xlabel('Difference in Price')
ylabel('Number of occurance')
title('10 Binutes Before Close (Sept 2018 - Sept 2019)')
xlim([-20 20])

figure()
hold on
PD10 = makedist('Normal', 'mu', mean(Delta10M), 'sigma', std(Delta10M));
PDF10= pdf(PD10, sort(Delta10M));
plot(sort(Delta10M), PDF10, 'k', 'linewidth', 2)
plot([mean(Delta10M) - std(Delta10M), mean(Delta10M) - std(Delta10M)], [0 max(PDF10)], '-.b')
plot([mean(Delta10M) + std(Delta10M), mean(Delta10M) + std(Delta10M)], [0 max(PDF10)], '-.b')
plot([mean(Delta10M) - 2*std(Delta10M), mean(Delta10M) - 2*std(Delta10M)], [0 max(PDF10)], '-.r')
plot([mean(Delta10M) + 2*std(Delta10M), mean(Delta10M) + 2*std(Delta10M)], [0 max(PDF10)], '-.r')
xlabel('Difference to Closing Price')
ylabel('% Chance of Occurance')
title('10 Minutes Before Close (Sept 2018 - Sept 2019)')
ylim([0, max(PDF10)])

%% 5M
figure()
histogram(Delta5M, 'BinWidth', 1)
xlabel('Difference in Price')
ylabel('Number of occurance')
title('5 Minutes Before Close (Sept 2018 - Sept 2019)')
xlim([-15 15])

figure()
hold on
PD5 = makedist('Normal', 'mu', mean(Delta5M), 'sigma', std(Delta5M));
PDF5 = pdf(PD5, sort(Delta5M));
plot(sort(Delta5M), PDF5, 'k', 'linewidth', 2)
plot([mean(Delta5M) - std(Delta5M), mean(Delta5M) - std(Delta5M)], [0 max(PDF5)], '-.b')
plot([mean(Delta5M) + std(Delta5M), mean(Delta5M) + std(Delta5M)], [0 max(PDF5)], '-.b')
plot([mean(Delta5M) - 2*std(Delta5M), mean(Delta5M) - 2*std(Delta5M)], [0 max(PDF5)], '-.r')
plot([mean(Delta5M) + 2*std(Delta5M), mean(Delta5M) + 2*std(Delta5M)], [0 max(PDF5)], '-.r')
xlabel('Difference to Closing Price')
ylabel('% Chance of Occurance')
title('5 Minutes Before Close (Sept 2018 - Sept 2019)')
ylim([0, max(PDF5)])

%% 1M
figure()
histogram(Delta1M, 'BinWidth', 1)
xlabel('Difference in Price')
ylabel('Number of occurance')
title('1 Minutes Before Close (Sept 2018 - Sept 2019)')
xlim([-3 3])

figure()
hold on
PD1 = makedist('Normal', 'mu', mean(Delta1M), 'sigma', std(Delta1M));
PDF1 = pdf(PD1, sort(Delta1M));
plot(sort(Delta1M), PDF1, 'k', 'linewidth', 2)
plot([mean(Delta1M) - std(Delta1M), mean(Delta1M) - std(Delta1M)], [0 max(PDF1)], '-.b')
plot([mean(Delta1M) + std(Delta1M), mean(Delta1M) + std(Delta1M)], [0 max(PDF1)], '-.b')
plot([mean(Delta1M) - 2*std(Delta1M), mean(Delta1M) - 2*std(Delta1M)], [0 max(PDF1)], '-.r')
plot([mean(Delta1M) + 2*std(Delta1M), mean(Delta1M) + 2*std(Delta1M)], [0 max(PDF1)], '-.r')
xlabel('Difference to Closing Price')
ylabel('% Chance of Occurance')
title('1 Minute Before Close (Sept 2018 - Sept 2019)')
ylim([0, max(PDF1)])

function SPImport = SPReader(filename, dataLines)
%IMPORTFILE Import data from a text file
%  SANDP1 = IMPORTFILE(FILENAME) reads data from text file FILENAME for
%  the default selection.  Returns the data as a table.
%
%  SANDP1 = IMPORTFILE(FILE, DATALINES) reads data for the specified row
%  interval(s) of text file FILENAME. Specify DATALINES as a positive
%  scalar integer or a N-by-2 array of positive scalar integers for
%  dis-contiguous row intervals.
%
%  Example:
%  SANDP1 = importfile("C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData\SPXMinuteData\SANDP-500_160901_170901.csv", [2, Inf]);
%
%  See also READTABLE.
%
% Auto-generated by MATLAB on 13-Jul-2021 19:04:04

%% Input handling

% If dataLines is not specified, define defaults
if nargin < 2
    dataLines = [2, Inf];
end

%% Setup the Import Options and import the data
opts = delimitedTextImportOptions("NumVariables", 9);

% Specify range and delimiter
opts.DataLines = dataLines;
opts.Delimiter = ";";

% Specify column names and types
opts.VariableNames = ["TICKER", "PER", "DATE", "TIME", "OPEN", "HIGH", "LOW", "CLOSE", "VOL"];
opts.VariableTypes = ["double", "double", "datetime", "double", "double", "double", "double", "double", "double"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Specify variable properties
opts = setvaropts(opts, "DATE", "InputFormat", "MM/dd/yy");
opts = setvaropts(opts, ["TICKER", "OPEN", "HIGH", "LOW", "CLOSE"], "TrimNonNumeric", true);
opts = setvaropts(opts, ["TICKER", "OPEN", "HIGH", "LOW", "CLOSE"], "ThousandsSeparator", ",");

% Import the data
SPImport = readtable(filename, opts);

end