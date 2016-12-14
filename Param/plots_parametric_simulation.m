close all
clear all


%% Datas are read from .txt
files = dir([pwd, '\*.txt']);

Data=cell(length(files));

param=cell(length(files));
for i = 1:length(files)
    Dat = importdata(getfield(files,{i},'name'));
    param{i} = Dat.textdata(1,1);
    
    index=zeros(1,length(Dat.data));
    
    for j = 1:length(Dat.textdata)
        index(j)=isequal(param{i}, Dat.textdata(j,1));
    end
    
    n_sim = sum(index);
    n_outputs = length(Dat.textdata)/n_sim;
    
    Data{i} = reshape(Dat.data, n_outputs, n_sim);
    
end

fields = Dat.textdata(1:n_outputs,1);

%% results are plotted and saved

color=[0.874, 0.392, 0.04;...
    0.317, 0.850, 0.070;...
    0.027, 0.529, 0.929;...
    0.807, 0.133, 0.141;...
    0.133, 0.564, 0.807;...
    0.976, 0.625, 0.519;...
    0.929, 0.027, 0.737];

width=1.7;
set(0,'DefaultAxesFontSize',20);

set(groot, 'DefaultTextInterpreter', 'LaTex')
set(groot, 'DefaultLegendInterpreter', 'LaTex')

for i=1:length(files)
    
    for j=2:n_outputs
        
        figure()
        plot(Data{i,1}(1,:), Data{i,1}(j,:),'x--','Linewidth',width,'Color',color(1,:));
        xlabel(strcat('$', param{i}, '$'))
        ylabel(strcat('$', fields{j}, '$'))
        set (gca,'TicklabelInterpreter','LaTex')
        grid on
        % removing all problematic signs from figure name
        
        fig_name = regexprep(strcat(param{i,1}{1,1},fields{j}),'/','');
        fig_name = regexprep(fig_name,'\','');
        fig_name = strcat('.\figures\Fig_',fig_name);
        
        print('-f',fig_name,'-depsc')
                
    end
end
        
        
        
        
        
