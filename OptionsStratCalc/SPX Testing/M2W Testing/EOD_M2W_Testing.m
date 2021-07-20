 % Checks the difference between the prices of SPX at close
% and at 15 minutes, 10 minutes, 5 minutes, and 1 minute 
% before close
% AYC - All years included, runs the same thing for all years
close all
clear
clc
%% Data Files
Set1 = SPReader('C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData\SPXMinuteData\SANDP-500_160901_170901.csv');
Set2 = SPReader('C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData\SPXMinuteData\SANDP-500_170901_180901.csv');
Set3 = SPReader('C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData\SPXMinuteData\SANDP-500_180901_190901.csv');
Set4 = SPReader('C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData\SPXMinuteData\SANDP-500_190901_200901.csv');
Set5 = SPReader('C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData\SPXMinuteData\SANDP-500_200901_210701.csv');

%% Data manipulation
Min15Price = [];
Min10Price = [];
Min5Price = [];
Min4Price = [];
Min3Price = [];
Min2Price = [];
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
            elseif TVal2 == 155600
                Min4Price = [Min4Price TVal2];
            elseif TVal2 == 155700
                Min3Price = [Min3Price TVal2];
            elseif TVal2 == 155800
                Min2Price = [Min2Price TVal2];
            end
        end
    end
end

for i = 1:height(Set2)
    TVal = table2array(Set2(i, 4));
    PVal = table2array(Set2(i, 8));
    if TVal == 160000
        ClosePrice = [ClosePrice PVal];
        for j = i:-1:i-30
            TVal2 = table2array(Set2(j, 4));
            PVal2 =  table2array(Set2(j, 8));
            if TVal2 == 154500
                Min15Price = [Min15Price PVal2];
            elseif TVal2 == 155000
                Min10Price = [Min10Price PVal2];
            elseif TVal2 == 155500
                Min5Price = [Min5Price PVal2];
            elseif TVal2 == 155900
                Min1Price = [Min1Price PVal2];
            elseif TVal2 == 155600
                Min4Price = [Min4Price TVal2];
            elseif TVal2 == 155700
                Min3Price = [Min3Price TVal2];
            elseif TVal2 == 155800
                Min2Price = [Min2Price TVal2];
            end
        end
    end
end

for i = 1:height(Set3)
    TVal = table2array(Set3(i, 4));
    PVal = table2array(Set3(i, 8));
    if TVal == 160000
        ClosePrice = [ClosePrice PVal];
        for j = i:-1:i-30
            TVal2 = table2array(Set3(j, 4));
            PVal2 =  table2array(Set3(j, 8));
            if TVal2 == 154500
                Min15Price = [Min15Price PVal2];
            elseif TVal2 == 155000
                Min10Price = [Min10Price PVal2];
            elseif TVal2 == 155500
                Min5Price = [Min5Price PVal2];
            elseif TVal2 == 155900
                Min1Price = [Min1Price PVal2];
            elseif TVal2 == 155600
                Min4Price = [Min4Price TVal2];
            elseif TVal2 == 155700
                Min3Price = [Min3Price TVal2];
            elseif TVal2 == 155800
                Min2Price = [Min2Price TVal2];
            end
        end
    end
end

for i = 1:height(Set5)
    TVal = table2array(Set5(i, 4));
    PVal = table2array(Set5(i, 8));
    if TVal == 160000
        ClosePrice = [ClosePrice PVal];
        for j = i:-1:i-30
            TVal2 = table2array(Set5(j, 4));
            PVal2 =  table2array(Set5(j, 8));
            if TVal2 == 154500
                Min15Price = [Min15Price PVal2];
            elseif TVal2 == 155000
                Min10Price = [Min10Price PVal2];
            elseif TVal2 == 155500
                Min5Price = [Min5Price PVal2];
            elseif TVal2 == 155900
                Min1Price = [Min1Price PVal2];
            elseif TVal2 == 155600
                Min4Price = [Min4Price TVal2];
            elseif TVal2 == 155700
                Min3Price = [Min3Price TVal2];
            elseif TVal2 == 155800
                Min2Price = [Min2Price TVal2];
            end
        end
    end
end

for i = 1:height(Set5)
    TVal = table2array(Set5(i, 4));
    PVal = table2array(Set5(i, 8));
    if TVal == 160000
        ClosePrice = [ClosePrice PVal];
        for j = i:-1:i-30
            TVal2 = table2array(Set5(j, 4));
            PVal2 =  table2array(Set5(j, 8));
            if TVal2 == 154500
                Min15Price = [Min15Price PVal2];
            elseif TVal2 == 155000
                Min10Price = [Min10Price PVal2];
            elseif TVal2 == 155500
                Min5Price = [Min5Price PVal2];
            elseif TVal2 == 155900
                Min1Price = [Min1Price PVal2];   
             elseif TVal2 == 155600
                Min4Price = [Min4Price TVal2];
            elseif TVal2 == 155700
                Min3Price = [Min3Price TVal2];
            elseif TVal2 == 155800
                Min2Price = [Min2Price TVal2];
            end
        end
    end
end

%% Loading function
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