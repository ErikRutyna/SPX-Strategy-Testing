close all
clear
clc
%% PCS Width
PCS15WT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\PCS-0.15delta-width-scaling-balances.csv";
PCS15WT1 = csvread(PCS15WT1, 1, 0);
PCS15WT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\PCS-0.15delta-width-scaling-balances.csv";
PCS15WT2 = csvread(PCS15WT2, 1, 0);
PCS15WT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\PCS-0.15delta-width-scaling-balances.csv";
PCS15WT3 = csvread(PCS15WT3, 1, 0);
PCS15WT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\PCS-0.15delta-width-scaling-balances.csv";
PCS15WT4 = csvread(PCS15WT4, 1, 0);
PCS15WT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\PCS-0.15delta-width-scaling-balances.csv";
PCS15WT5 = csvread(PCS15WT5, 1, 0);
PCS15WT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\PCS-0.15delta-width-scaling-balances.csv";
PCS15WT6 = csvread(PCS15WT6, 1, 0);
PCS15WT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\PCS-0.15delta-width-scaling-balances.csv";
PCS15WT7 = csvread(PCS15WT7, 1, 0);

PCS20WT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\PCS-0.2delta-width-scaling-balances.csv";
PCS20WT1 = csvread(PCS20WT1, 1, 0);
PCS20WT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\PCS-0.2delta-width-scaling-balances.csv";
PCS20WT2 = csvread(PCS20WT2, 1, 0);
PCS20WT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\PCS-0.2delta-width-scaling-balances.csv";
PCS20WT3 = csvread(PCS20WT3, 1, 0);
PCS20WT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\PCS-0.2delta-width-scaling-balances.csv";
PCS20WT4 = csvread(PCS20WT4, 1, 0);
PCS20WT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\PCS-0.2delta-width-scaling-balances.csv";
PCS20WT5 = csvread(PCS20WT5, 1, 0);
PCS20WT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\PCS-0.2delta-width-scaling-balances.csv";
PCS20WT6 = csvread(PCS20WT6, 1, 0);
PCS20WT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\PCS-0.2delta-width-scaling-balances.csv";
PCS20WT7 = csvread(PCS20WT7, 1, 0);

PCS25WT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\PCS-0.25delta-width-scaling-balances.csv";
PCS25WT1 =  csvread(PCS25WT1, 1, 0);
PCS25WT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\PCS-0.25delta-width-scaling-balances.csv";
PCS25WT2 =  csvread(PCS25WT2, 1, 0);
PCS25WT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\PCS-0.25delta-width-scaling-balances.csv";
PCS25WT3 =  csvread(PCS25WT3, 1, 0);
PCS25WT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\PCS-0.25delta-width-scaling-balances.csv";
PCS25WT4 =  csvread(PCS25WT4, 1, 0);
PCS25WT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\PCS-0.25delta-width-scaling-balances.csv";
PCS25WT5 =  csvread(PCS25WT5, 1, 0);
PCS25WT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\PCS-0.25delta-width-scaling-balances.csv";
PCS25WT6 =  csvread(PCS25WT6, 1, 0);
PCS25WT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\PCS-0.25delta-width-scaling-balances.csv";
PCS25WT7 =  csvread(PCS25WT7, 1, 0);

PCS30WT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\PCS-0.3delta-width-scaling-balances.csv";
PCS30WT1 = csvread(PCS30WT1, 1, 0);
PCS30WT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\PCS-0.3delta-width-scaling-balances.csv";
PCS30WT2 = csvread(PCS30WT2, 1, 0);
PCS30WT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\PCS-0.3delta-width-scaling-balances.csv";
PCS30WT3 = csvread(PCS30WT3, 1, 0);
PCS30WT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\PCS-0.3delta-width-scaling-balances.csv";
PCS30WT4 = csvread(PCS30WT4, 1, 0);
PCS30WT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\PCS-0.3delta-width-scaling-balances.csv";
PCS30WT5 = csvread(PCS30WT5, 1, 0);
PCS30WT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\PCS-0.3delta-width-scaling-balances.csv";
PCS30WT6 = csvread(PCS30WT6, 1, 0);
PCS30WT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\PCS-0.3delta-width-scaling-balances.csv";
PCS30WT7 = csvread(PCS30WT7, 1, 0);

PCS35WT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\PCS-0.35delta-width-scaling-balances.csv";
PCS35WT1 = csvread(PCS35WT1, 1, 0);
PCS35WT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\PCS-0.35delta-width-scaling-balances.csv";
PCS35WT2 = csvread(PCS35WT2, 1, 0);
PCS35WT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\PCS-0.35delta-width-scaling-balances.csv";
PCS35WT3 = csvread(PCS35WT3, 1, 0);
PCS35WT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\PCS-0.35delta-width-scaling-balances.csv";
PCS35WT4 = csvread(PCS35WT4, 1, 0);
PCS35WT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\PCS-0.35delta-width-scaling-balances.csv";
PCS35WT5 = csvread(PCS35WT5, 1, 0);
PCS35WT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\PCS-0.35delta-width-scaling-balances.csv";
PCS35WT6 = csvread(PCS35WT6, 1, 0);
PCS35WT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\PCS-0.35delta-width-scaling-balances.csv";
PCS35WT7 = csvread(PCS35WT7, 1, 0);

PCS40WT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\PCS-0.4delta-width-scaling-balances.csv";
PCS40WT1 = csvread(PCS40WT1, 1, 0);
PCS40WT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\PCS-0.4delta-width-scaling-balances.csv";
PCS40WT2 = csvread(PCS40WT2, 1, 0);
PCS40WT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\PCS-0.4delta-width-scaling-balances.csv";
PCS40WT3 = csvread(PCS40WT3, 1, 0);
PCS40WT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\PCS-0.4delta-width-scaling-balances.csv";
PCS40WT4 = csvread(PCS40WT4, 1, 0);
PCS40WT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\PCS-0.4delta-width-scaling-balances.csv";
PCS40WT5 = csvread(PCS40WT5, 1, 0);
PCS40WT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\PCS-0.4delta-width-scaling-balances.csv";
PCS40WT6 = csvread(PCS40WT6, 1, 0);
PCS40WT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\PCS-0.4delta-width-scaling-balances.csv";
PCS40WT7 = csvread(PCS40WT7, 1, 0);

Date = num2str(PCS15WT1(:, 2));
Date = Date(:, 1:4) + "." + Date(:, 5:6) + "." + Date(:, 7:end);
Date = datevec(Date, 'yyyy.mm.dd');
Date = datetime(Date);

figure(1)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('PCS W/ $$\Delta$$ = 0.15 - Width Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, PCS15WT1(:, 1))
plot(Date, PCS15WT2(:, 1))
plot(Date, PCS15WT3(:, 1))
plot(Date, PCS15WT4(:, 1))
plot(Date, PCS15WT5(:, 1))
plot(Date, PCS15WT6(:, 1))
plot(Date, PCS15WT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

figure(2)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('PCS W/ $$\Delta$$ = 0.20 - Width Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, PCS20WT1(:, 1))
plot(Date, PCS20WT2(:, 1))
plot(Date, PCS20WT3(:, 1))
plot(Date, PCS20WT4(:, 1))
plot(Date, PCS20WT5(:, 1))
plot(Date, PCS20WT6(:, 1))
plot(Date, PCS20WT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

figure(3)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('PCS W/ $$\Delta$$ = 0.25 - Width Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, PCS25WT1(:, 1))
plot(Date, PCS25WT2(:, 1))
plot(Date, PCS25WT3(:, 1))
plot(Date, PCS25WT4(:, 1))
plot(Date, PCS25WT5(:, 1))
plot(Date, PCS25WT6(:, 1))
plot(Date, PCS25WT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

figure(4)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('PCS W/ $$\Delta$$ = 0.30 - Width Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, PCS30WT1(:, 1))
plot(Date, PCS30WT2(:, 1))
plot(Date, PCS30WT3(:, 1))
plot(Date, PCS30WT4(:, 1))
plot(Date, PCS30WT5(:, 1))
plot(Date, PCS30WT6(:, 1))
plot(Date, PCS30WT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

figure(5)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('PCS W/ $$\Delta$$ = 0.35 - Width Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, PCS35WT1(:, 1))
plot(Date, PCS35WT2(:, 1))
plot(Date, PCS35WT3(:, 1))
plot(Date, PCS35WT4(:, 1))
plot(Date, PCS35WT5(:, 1))
plot(Date, PCS35WT6(:, 1))
plot(Date, PCS35WT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

figure(6)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('PCS W/ $$\Delta$$ = 0.40 - Width Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, PCS40WT1(:, 1))
plot(Date, PCS40WT2(:, 1))
plot(Date, PCS40WT3(:, 1))
plot(Date, PCS40WT4(:, 1))
plot(Date, PCS40WT5(:, 1))
plot(Date, PCS40WT6(:, 1))
plot(Date, PCS40WT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

%% PCS Contract Scaling
PCS15CT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\PCS-0.15delta-contracts-scaling-balances.csv";
PCS15CT1 = csvread(PCS15CT1, 1, 0);
PCS15CT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\PCS-0.15delta-contracts-scaling-balances.csv";
PCS15CT2 = csvread(PCS15CT2, 1, 0);
PCS15CT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\PCS-0.15delta-contracts-scaling-balances.csv";
PCS15CT3 = csvread(PCS15CT3, 1, 0);
PCS15CT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\PCS-0.15delta-contracts-scaling-balances.csv";
PCS15CT4 = csvread(PCS15CT4, 1, 0);
PCS15CT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\PCS-0.15delta-contracts-scaling-balances.csv";
PCS15CT5 = csvread(PCS15CT5, 1, 0);
PCS15CT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\PCS-0.15delta-contracts-scaling-balances.csv";
PCS15CT6 = csvread(PCS15CT6, 1, 0);
PCS15CT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\PCS-0.15delta-contracts-scaling-balances.csv";
PCS15CT7 = csvread(PCS15CT7, 1, 0);

PCS20CT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\PCS-0.2delta-contracts-scaling-balances.csv";
PCS20CT1 = csvread(PCS20CT1, 1, 0);
PCS20CT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\PCS-0.2delta-contracts-scaling-balances.csv";
PCS20CT2 = csvread(PCS20CT2, 1, 0);
PCS20CT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\PCS-0.2delta-contracts-scaling-balances.csv";
PCS20CT3 = csvread(PCS20CT3, 1, 0);
PCS20CT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\PCS-0.2delta-contracts-scaling-balances.csv";
PCS20CT4 = csvread(PCS20CT4, 1, 0);
PCS20CT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\PCS-0.2delta-contracts-scaling-balances.csv";
PCS20CT5 = csvread(PCS20CT5, 1, 0);
PCS20CT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\PCS-0.2delta-contracts-scaling-balances.csv";
PCS20CT6 = csvread(PCS20CT6, 1, 0);
PCS20CT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\PCS-0.2delta-contracts-scaling-balances.csv";
PCS20CT7 = csvread(PCS20CT7, 1, 0);

PCS25CT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\PCS-0.25delta-contracts-scaling-balances.csv";
PCS25CT1 =  csvread(PCS25CT1, 1, 0);
PCS25CT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\PCS-0.25delta-contracts-scaling-balances.csv";
PCS25CT2 =  csvread(PCS25CT2, 1, 0);
PCS25CT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\PCS-0.25delta-contracts-scaling-balances.csv";
PCS25CT3 =  csvread(PCS25CT3, 1, 0);
PCS25CT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\PCS-0.25delta-contracts-scaling-balances.csv";
PCS25CT4 =  csvread(PCS25CT4, 1, 0);
PCS25CT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\PCS-0.25delta-contracts-scaling-balances.csv";
PCS25CT5 =  csvread(PCS25CT5, 1, 0);
PCS25CT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\PCS-0.25delta-contracts-scaling-balances.csv";
PCS25CT6 =  csvread(PCS25CT6, 1, 0);
PCS25CT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\PCS-0.25delta-contracts-scaling-balances.csv";
PCS25CT7 =  csvread(PCS25CT7, 1, 0);

PCS30CT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\PCS-0.3delta-contracts-scaling-balances.csv";
PCS30CT1 = csvread(PCS30CT1, 1, 0);
PCS30CT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\PCS-0.3delta-contracts-scaling-balances.csv";
PCS30CT2 = csvread(PCS30CT2, 1, 0);
PCS30CT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\PCS-0.3delta-contracts-scaling-balances.csv";
PCS30CT3 = csvread(PCS30CT3, 1, 0);
PCS30CT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\PCS-0.3delta-contracts-scaling-balances.csv";
PCS30CT4 = csvread(PCS30CT4, 1, 0);
PCS30CT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\PCS-0.3delta-contracts-scaling-balances.csv";
PCS30CT5 = csvread(PCS30CT5, 1, 0);
PCS30CT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\PCS-0.3delta-contracts-scaling-balances.csv";
PCS30CT6 = csvread(PCS30CT6, 1, 0);
PCS30CT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\PCS-0.3delta-contracts-scaling-balances.csv";
PCS30CT7 = csvread(PCS30CT7, 1, 0);

PCS35CT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\PCS-0.35delta-contracts-scaling-balances.csv";
PCS35CT1 = csvread(PCS35CT1, 1, 0);
PCS35CT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\PCS-0.35delta-contracts-scaling-balances.csv";
PCS35CT2 = csvread(PCS35CT2, 1, 0);
PCS35CT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\PCS-0.35delta-contracts-scaling-balances.csv";
PCS35CT3 = csvread(PCS35CT3, 1, 0);
PCS35CT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\PCS-0.35delta-contracts-scaling-balances.csv";
PCS35CT4 = csvread(PCS35CT4, 1, 0);
PCS35CT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\PCS-0.35delta-contracts-scaling-balances.csv";
PCS35CT5 = csvread(PCS35CT5, 1, 0);
PCS35CT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\PCS-0.35delta-contracts-scaling-balances.csv";
PCS35CT6 = csvread(PCS35CT6, 1, 0);
PCS35CT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\PCS-0.35delta-contracts-scaling-balances.csv";
PCS35CT7 = csvread(PCS35CT7, 1, 0);

PCS40CT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\PCS-0.4delta-contracts-scaling-balances.csv";
PCS40CT1 = csvread(PCS40CT1, 1, 0);
PCS40CT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\PCS-0.4delta-contracts-scaling-balances.csv";
PCS40CT2 = csvread(PCS40CT2, 1, 0);
PCS40CT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\PCS-0.4delta-contracts-scaling-balances.csv";
PCS40CT3 = csvread(PCS40CT3, 1, 0);
PCS40CT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\PCS-0.4delta-contracts-scaling-balances.csv";
PCS40CT4 = csvread(PCS40CT4, 1, 0);
PCS40CT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\PCS-0.4delta-contracts-scaling-balances.csv";
PCS40CT5 = csvread(PCS40CT5, 1, 0);
PCS40CT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\PCS-0.4delta-contracts-scaling-balances.csv";
PCS40CT6 = csvread(PCS40CT6, 1, 0);
PCS40CT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\PCS-0.4delta-contracts-scaling-balances.csv";
PCS40CT7 = csvread(PCS40CT7, 1, 0);

Date = num2str(PCS15CT1(:, 2));
Date = Date(:, 1:4) + "." + Date(:, 5:6) + "." + Date(:, 7:end);
Date = datevec(Date, 'yyyy.mm.dd');
Date = datetime(Date);

figure(7)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('PCS W/ $$\Delta$$ = 0.15 - Contract Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, PCS15CT1(:, 1))
plot(Date, PCS15CT2(:, 1))
plot(Date, PCS15CT3(:, 1))
plot(Date, PCS15CT4(:, 1))
plot(Date, PCS15CT5(:, 1))
plot(Date, PCS15CT6(:, 1))
plot(Date, PCS15CT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

figure(8)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('PCS W/ $$\Delta$$ = 0.20 - Contract Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, PCS20CT1(:, 1))
plot(Date, PCS20CT2(:, 1))
plot(Date, PCS20CT3(:, 1))
plot(Date, PCS20CT4(:, 1))
plot(Date, PCS20CT5(:, 1))
plot(Date, PCS20CT6(:, 1))
plot(Date, PCS20CT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

figure(9)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('PCS W/ $$\Delta$$ = 0.25 - Contract Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, PCS25CT1(:, 1))
plot(Date, PCS25CT2(:, 1))
plot(Date, PCS25CT3(:, 1))
plot(Date, PCS25CT4(:, 1))
plot(Date, PCS25CT5(:, 1))
plot(Date, PCS25CT6(:, 1))
plot(Date, PCS25CT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

figure(10)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('PCS W/ $$\Delta$$ = 0.30 - Contract Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, PCS30CT1(:, 1))
plot(Date, PCS30CT2(:, 1))
plot(Date, PCS30CT3(:, 1))
plot(Date, PCS30CT4(:, 1))
plot(Date, PCS30CT5(:, 1))
plot(Date, PCS30CT6(:, 1))
plot(Date, PCS30CT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

figure(11)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('PCS W/ $$\Delta$$ = 0.35 - Contract Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, PCS35CT1(:, 1))
plot(Date, PCS35CT2(:, 1))
plot(Date, PCS35CT3(:, 1))
plot(Date, PCS35CT4(:, 1))
plot(Date, PCS35CT5(:, 1))
plot(Date, PCS35CT6(:, 1))
plot(Date, PCS35CT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

figure(12)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('PCS W/ $$\Delta$$ = 0.40 - Contract Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, PCS40CT1(:, 1))
plot(Date, PCS40CT2(:, 1))
plot(Date, PCS40CT3(:, 1))
plot(Date, PCS40CT4(:, 1))
plot(Date, PCS40CT5(:, 1))
plot(Date, PCS40CT6(:, 1))
plot(Date, PCS40CT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

%% CCS Width
CCS15WT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\CCS-0.15delta-width-scaling-balances.csv";
CCS15WT1 = csvread(CCS15WT1, 1, 0);
CCS15WT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\CCS-0.15delta-width-scaling-balances.csv";
CCS15WT2 = csvread(CCS15WT2, 1, 0);
CCS15WT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\CCS-0.15delta-width-scaling-balances.csv";
CCS15WT3 = csvread(CCS15WT3, 1, 0);
CCS15WT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\CCS-0.15delta-width-scaling-balances.csv";
CCS15WT4 = csvread(CCS15WT4, 1, 0);
CCS15WT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\CCS-0.15delta-width-scaling-balances.csv";
CCS15WT5 = csvread(CCS15WT5, 1, 0);
CCS15WT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\CCS-0.15delta-width-scaling-balances.csv";
CCS15WT6 = csvread(CCS15WT6, 1, 0);
CCS15WT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\CCS-0.15delta-width-scaling-balances.csv";
CCS15WT7 = csvread(CCS15WT7, 1, 0);

CCS20WT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\CCS-0.2delta-width-scaling-balances.csv";
CCS20WT1 = csvread(CCS20WT1, 1, 0);
CCS20WT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\CCS-0.2delta-width-scaling-balances.csv";
CCS20WT2 = csvread(CCS20WT2, 1, 0);
CCS20WT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\CCS-0.2delta-width-scaling-balances.csv";
CCS20WT3 = csvread(CCS20WT3, 1, 0);
CCS20WT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\CCS-0.2delta-width-scaling-balances.csv";
CCS20WT4 = csvread(CCS20WT4, 1, 0);
CCS20WT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\CCS-0.2delta-width-scaling-balances.csv";
CCS20WT5 = csvread(CCS20WT5, 1, 0);
CCS20WT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\CCS-0.2delta-width-scaling-balances.csv";
CCS20WT6 = csvread(CCS20WT6, 1, 0);
CCS20WT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\CCS-0.2delta-width-scaling-balances.csv";
CCS20WT7 = csvread(CCS20WT7, 1, 0);

CCS25WT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\CCS-0.25delta-width-scaling-balances.csv";
CCS25WT1 =  csvread(CCS25WT1, 1, 0);
CCS25WT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\CCS-0.25delta-width-scaling-balances.csv";
CCS25WT2 =  csvread(CCS25WT2, 1, 0);
CCS25WT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\CCS-0.25delta-width-scaling-balances.csv";
CCS25WT3 =  csvread(CCS25WT3, 1, 0);
CCS25WT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\CCS-0.25delta-width-scaling-balances.csv";
CCS25WT4 =  csvread(CCS25WT4, 1, 0);
CCS25WT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\CCS-0.25delta-width-scaling-balances.csv";
CCS25WT5 =  csvread(CCS25WT5, 1, 0);
CCS25WT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\CCS-0.25delta-width-scaling-balances.csv";
CCS25WT6 =  csvread(CCS25WT6, 1, 0);
CCS25WT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\CCS-0.25delta-width-scaling-balances.csv";
CCS25WT7 =  csvread(CCS25WT7, 1, 0);

CCS30WT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\CCS-0.3delta-width-scaling-balances.csv";
CCS30WT1 = csvread(CCS30WT1, 1, 0);
CCS30WT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\CCS-0.3delta-width-scaling-balances.csv";
CCS30WT2 = csvread(CCS30WT2, 1, 0);
CCS30WT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\CCS-0.3delta-width-scaling-balances.csv";
CCS30WT3 = csvread(CCS30WT3, 1, 0);
CCS30WT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\CCS-0.3delta-width-scaling-balances.csv";
CCS30WT4 = csvread(CCS30WT4, 1, 0);
CCS30WT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\CCS-0.3delta-width-scaling-balances.csv";
CCS30WT5 = csvread(CCS30WT5, 1, 0);
CCS30WT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\CCS-0.3delta-width-scaling-balances.csv";
CCS30WT6 = csvread(CCS30WT6, 1, 0);
CCS30WT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\CCS-0.3delta-width-scaling-balances.csv";
CCS30WT7 = csvread(CCS30WT7, 1, 0);

CCS35WT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\CCS-0.35delta-width-scaling-balances.csv";
CCS35WT1 = csvread(CCS35WT1, 1, 0);
CCS35WT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\CCS-0.35delta-width-scaling-balances.csv";
CCS35WT2 = csvread(CCS35WT2, 1, 0);
CCS35WT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\CCS-0.35delta-width-scaling-balances.csv";
CCS35WT3 = csvread(CCS35WT3, 1, 0);
CCS35WT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\CCS-0.35delta-width-scaling-balances.csv";
CCS35WT4 = csvread(CCS35WT4, 1, 0);
CCS35WT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\CCS-0.35delta-width-scaling-balances.csv";
CCS35WT5 = csvread(CCS35WT5, 1, 0);
CCS35WT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\CCS-0.35delta-width-scaling-balances.csv";
CCS35WT6 = csvread(CCS35WT6, 1, 0);
CCS35WT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\CCS-0.35delta-width-scaling-balances.csv";
CCS35WT7 = csvread(CCS35WT7, 1, 0);

CCS40WT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\CCS-0.4delta-width-scaling-balances.csv";
CCS40WT1 = csvread(CCS40WT1, 1, 0);
CCS40WT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\CCS-0.4delta-width-scaling-balances.csv";
CCS40WT2 = csvread(CCS40WT2, 1, 0);
CCS40WT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\CCS-0.4delta-width-scaling-balances.csv";
CCS40WT3 = csvread(CCS40WT3, 1, 0);
CCS40WT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\CCS-0.4delta-width-scaling-balances.csv";
CCS40WT4 = csvread(CCS40WT4, 1, 0);
CCS40WT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\CCS-0.4delta-width-scaling-balances.csv";
CCS40WT5 = csvread(CCS40WT5, 1, 0);
CCS40WT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\CCS-0.4delta-width-scaling-balances.csv";
CCS40WT6 = csvread(CCS40WT6, 1, 0);
CCS40WT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\CCS-0.4delta-width-scaling-balances.csv";
CCS40WT7 = csvread(CCS40WT7, 1, 0);

Date = num2str(CCS15WT1(:, 2));
Date = Date(:, 1:4) + "." + Date(:, 5:6) + "." + Date(:, 7:end);
Date = datevec(Date, 'yyyy.mm.dd');
Date = datetime(Date);

figure(1)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('CCS W/ $$\Delta$$ = 0.15 - Width Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, CCS15WT1(:, 1))
plot(Date, CCS15WT2(:, 1))
plot(Date, CCS15WT3(:, 1))
plot(Date, CCS15WT4(:, 1))
plot(Date, CCS15WT5(:, 1))
plot(Date, CCS15WT6(:, 1))
plot(Date, CCS15WT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

figure(2)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('CCS W/ $$\Delta$$ = 0.20 - Width Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, CCS20WT1(:, 1))
plot(Date, CCS20WT2(:, 1))
plot(Date, CCS20WT3(:, 1))
plot(Date, CCS20WT4(:, 1))
plot(Date, CCS20WT5(:, 1))
plot(Date, CCS20WT6(:, 1))
plot(Date, CCS20WT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

figure(3)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('CCS W/ $$\Delta$$ = 0.25 - Width Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, CCS25WT1(:, 1))
plot(Date, CCS25WT2(:, 1))
plot(Date, CCS25WT3(:, 1))
plot(Date, CCS25WT4(:, 1))
plot(Date, CCS25WT5(:, 1))
plot(Date, CCS25WT6(:, 1))
plot(Date, CCS25WT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

figure(4)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('CCS W/ $$\Delta$$ = 0.30 - Width Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, CCS30WT1(:, 1))
plot(Date, CCS30WT2(:, 1))
plot(Date, CCS30WT3(:, 1))
plot(Date, CCS30WT4(:, 1))
plot(Date, CCS30WT5(:, 1))
plot(Date, CCS30WT6(:, 1))
plot(Date, CCS30WT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

figure(5)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('CCS W/ $$\Delta$$ = 0.35 - Width Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, CCS35WT1(:, 1))
plot(Date, CCS35WT2(:, 1))
plot(Date, CCS35WT3(:, 1))
plot(Date, CCS35WT4(:, 1))
plot(Date, CCS35WT5(:, 1))
plot(Date, CCS35WT6(:, 1))
plot(Date, CCS35WT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

figure(6)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('CCS W/ $$\Delta$$ = 0.40 - Width Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, CCS40WT1(:, 1))
plot(Date, CCS40WT2(:, 1))
plot(Date, CCS40WT3(:, 1))
plot(Date, CCS40WT4(:, 1))
plot(Date, CCS40WT5(:, 1))
plot(Date, CCS40WT6(:, 1))
plot(Date, CCS40WT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

%% CCS Contract Scaling
CCS15CT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\CCS-0.15delta-contracts-scaling-balances.csv";
CCS15CT1 = csvread(CCS15CT1, 1, 0);
CCS15CT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\CCS-0.15delta-contracts-scaling-balances.csv";
CCS15CT2 = csvread(CCS15CT2, 1, 0);
CCS15CT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\CCS-0.15delta-contracts-scaling-balances.csv";
CCS15CT3 = csvread(CCS15CT3, 1, 0);
CCS15CT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\CCS-0.15delta-contracts-scaling-balances.csv";
CCS15CT4 = csvread(CCS15CT4, 1, 0);
CCS15CT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\CCS-0.15delta-contracts-scaling-balances.csv";
CCS15CT5 = csvread(CCS15CT5, 1, 0);
CCS15CT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\CCS-0.15delta-contracts-scaling-balances.csv";
CCS15CT6 = csvread(CCS15CT6, 1, 0);
CCS15CT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\CCS-0.15delta-contracts-scaling-balances.csv";
CCS15CT7 = csvread(CCS15CT7, 1, 0);

CCS20CT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\CCS-0.2delta-contracts-scaling-balances.csv";
CCS20CT1 = csvread(CCS20CT1, 1, 0);
CCS20CT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\CCS-0.2delta-contracts-scaling-balances.csv";
CCS20CT2 = csvread(CCS20CT2, 1, 0);
CCS20CT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\CCS-0.2delta-contracts-scaling-balances.csv";
CCS20CT3 = csvread(CCS20CT3, 1, 0);
CCS20CT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\CCS-0.2delta-contracts-scaling-balances.csv";
CCS20CT4 = csvread(CCS20CT4, 1, 0);
CCS20CT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\CCS-0.2delta-contracts-scaling-balances.csv";
CCS20CT5 = csvread(CCS20CT5, 1, 0);
CCS20CT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\CCS-0.2delta-contracts-scaling-balances.csv";
CCS20CT6 = csvread(CCS20CT6, 1, 0);
CCS20CT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\CCS-0.2delta-contracts-scaling-balances.csv";
CCS20CT7 = csvread(CCS20CT7, 1, 0);

CCS25CT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\CCS-0.25delta-contracts-scaling-balances.csv";
CCS25CT1 =  csvread(CCS25CT1, 1, 0);
CCS25CT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\CCS-0.25delta-contracts-scaling-balances.csv";
CCS25CT2 =  csvread(CCS25CT2, 1, 0);
CCS25CT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\CCS-0.25delta-contracts-scaling-balances.csv";
CCS25CT3 =  csvread(CCS25CT3, 1, 0);
CCS25CT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\CCS-0.25delta-contracts-scaling-balances.csv";
CCS25CT4 =  csvread(CCS25CT4, 1, 0);
CCS25CT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\CCS-0.25delta-contracts-scaling-balances.csv";
CCS25CT5 =  csvread(CCS25CT5, 1, 0);
CCS25CT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\CCS-0.25delta-contracts-scaling-balances.csv";
CCS25CT6 =  csvread(CCS25CT6, 1, 0);
CCS25CT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\CCS-0.25delta-contracts-scaling-balances.csv";
CCS25CT7 =  csvread(CCS25CT7, 1, 0);

CCS30CT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\CCS-0.3delta-contracts-scaling-balances.csv";
CCS30CT1 = csvread(CCS30CT1, 1, 0);
CCS30CT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\CCS-0.3delta-contracts-scaling-balances.csv";
CCS30CT2 = csvread(CCS30CT2, 1, 0);
CCS30CT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\CCS-0.3delta-contracts-scaling-balances.csv";
CCS30CT3 = csvread(CCS30CT3, 1, 0);
CCS30CT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\CCS-0.3delta-contracts-scaling-balances.csv";
CCS30CT4 = csvread(CCS30CT4, 1, 0);
CCS30CT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\CCS-0.3delta-contracts-scaling-balances.csv";
CCS30CT5 = csvread(CCS30CT5, 1, 0);
CCS30CT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\CCS-0.3delta-contracts-scaling-balances.csv";
CCS30CT6 = csvread(CCS30CT6, 1, 0);
CCS30CT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\CCS-0.3delta-contracts-scaling-balances.csv";
CCS30CT7 = csvread(CCS30CT7, 1, 0);

CCS35CT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\CCS-0.35delta-contracts-scaling-balances.csv";
CCS35CT1 = csvread(CCS35CT1, 1, 0);
CCS35CT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\CCS-0.35delta-contracts-scaling-balances.csv";
CCS35CT2 = csvread(CCS35CT2, 1, 0);
CCS35CT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\CCS-0.35delta-contracts-scaling-balances.csv";
CCS35CT3 = csvread(CCS35CT3, 1, 0);
CCS35CT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\CCS-0.35delta-contracts-scaling-balances.csv";
CCS35CT4 = csvread(CCS35CT4, 1, 0);
CCS35CT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\CCS-0.35delta-contracts-scaling-balances.csv";
CCS35CT5 = csvread(CCS35CT5, 1, 0);
CCS35CT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\CCS-0.35delta-contracts-scaling-balances.csv";
CCS35CT6 = csvread(CCS35CT6, 1, 0);
CCS35CT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\CCS-0.35delta-contracts-scaling-balances.csv";
CCS35CT7 = csvread(CCS35CT7, 1, 0);

CCS40CT1 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 1\CCS-0.4delta-contracts-scaling-balances.csv";
CCS40CT1 = csvread(CCS40CT1, 1, 0);
CCS40CT2 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 2\CCS-0.4delta-contracts-scaling-balances.csv";
CCS40CT2 = csvread(CCS40CT2, 1, 0);
CCS40CT3 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 3\CCS-0.4delta-contracts-scaling-balances.csv";
CCS40CT3 = csvread(CCS40CT3, 1, 0);
CCS40CT4 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 4\CCS-0.4delta-contracts-scaling-balances.csv";
CCS40CT4 = csvread(CCS40CT4, 1, 0);
CCS40CT5 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 5\CCS-0.4delta-contracts-scaling-balances.csv";
CCS40CT5 = csvread(CCS40CT5, 1, 0);
CCS40CT6 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 6\CCS-0.4delta-contracts-scaling-balances.csv";
CCS40CT6 = csvread(CCS40CT6, 1, 0);
CCS40CT7 = "C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults\Test Run 7\CCS-0.4delta-contracts-scaling-balances.csv";
CCS40CT7 = csvread(CCS40CT7, 1, 0);

Date = num2str(CCS15CT1(:, 2));
Date = Date(:, 1:4) + "." + Date(:, 5:6) + "." + Date(:, 7:end);
Date = datevec(Date, 'yyyy.mm.dd');
Date = datetime(Date);

figure(7)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('CCS W/ $$\Delta$$ = 0.15 - Contract Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, CCS15CT1(:, 1))
plot(Date, CCS15CT2(:, 1))
plot(Date, CCS15CT3(:, 1))
plot(Date, CCS15CT4(:, 1))
plot(Date, CCS15CT5(:, 1))
plot(Date, CCS15CT6(:, 1))
plot(Date, CCS15CT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

figure(8)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('CCS W/ $$\Delta$$ = 0.20 - Contract Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, CCS20CT1(:, 1))
plot(Date, CCS20CT2(:, 1))
plot(Date, CCS20CT3(:, 1))
plot(Date, CCS20CT4(:, 1))
plot(Date, CCS20CT5(:, 1))
plot(Date, CCS20CT6(:, 1))
plot(Date, CCS20CT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

figure(9)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('CCS W/ $$\Delta$$ = 0.25 - Contract Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, CCS25CT1(:, 1))
plot(Date, CCS25CT2(:, 1))
plot(Date, CCS25CT3(:, 1))
plot(Date, CCS25CT4(:, 1))
plot(Date, CCS25CT5(:, 1))
plot(Date, CCS25CT6(:, 1))
plot(Date, CCS25CT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

figure(10)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('CCS W/ $$\Delta$$ = 0.30 - Contract Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, CCS30CT1(:, 1))
plot(Date, CCS30CT2(:, 1))
plot(Date, CCS30CT3(:, 1))
plot(Date, CCS30CT4(:, 1))
plot(Date, CCS30CT5(:, 1))
plot(Date, CCS30CT6(:, 1))
plot(Date, CCS30CT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

figure(11)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('CCS W/ $$\Delta$$ = 0.35 - Contract Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, CCS35CT1(:, 1))
plot(Date, CCS35CT2(:, 1))
plot(Date, CCS35CT3(:, 1))
plot(Date, CCS35CT4(:, 1))
plot(Date, CCS35CT5(:, 1))
plot(Date, CCS35CT6(:, 1))
plot(Date, CCS35CT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')

figure(12)
hold on
xlabel('Date', 'interpreter', 'latex')
ylabel('Profit (\$USD)', 'interpreter', 'latex')
title('CCS W/ $$\Delta$$ = 0.40 - Contract Scaling', 'interpreter', 'latex')
ax = gca;
ax.YAxis.Exponent = 0;
plot(Date, CCS40CT1(:, 1))
plot(Date, CCS40CT2(:, 1))
plot(Date, CCS40CT3(:, 1))
plot(Date, CCS40CT4(:, 1))
plot(Date, CCS40CT5(:, 1))
plot(Date, CCS40CT6(:, 1))
plot(Date, CCS40CT7(:, 1))
legend({'Trial 1','Trial 2','Trial 3','Trial 4','Trial 5','Trial 6','Trial 7'}, 'location', 'northwest')
