close all
clear all


%% Datas are read from .txt

directory = uigetdir('./','Choose Folder containing data to process');

files = dir([directory, '\*res.txt']);

Data=cell(length(files),1);

param_1=cell(length(files));
param_2=cell(length(files));


for i = 1:length(files)
    Dat = importdata([directory,'\',getfield(files,{i},'name')]);
    param_2{i} = Dat.textdata(1,1);
    
    index_2=zeros(1,length(Dat.data));
    
    for j = 1:length(Dat.textdata)
        index_2(j)=isequal(param_2{i}, Dat.textdata(j,1));
    end
    
    n_sim = sum(index_2);
    n_outputs = length(Dat.textdata)/n_sim;
    
    for j = 2:n_outputs:length(Dat.textdata)
        param_1{j} = Dat.textdata(j,1);
    end
    
    [c1{i}, ia1{i}, ia2{i}] = unique([param_1{:,1}]); % ia1 contains the coordinate of param_1 changes
    
    Data{i}=reshape(Dat.data, n_outputs, n_sim);
    
    length_param2{i} = length(unique(Data{i,1}(1,1:ia1{i}-1)));
    
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
    
    for j=3:n_outputs
        

        for k=1:length(c1{i})
            figure()
            hold on
            if k == length(c1{i})
                plot(Data{i,1}(2,ia1{i}(k):end),Data{i,1}(j,ia1{i}(k):end),'x--','Linewidth',width,'Color',color(k,:));  
            else
                plot(Data{i,1}(2,ia1{i}(k):ia1{i}(k+1)-1),Data{i,1}(j,ia1{i}(k):ia1{i}(k+1)-1),'x--','Linewidth',width,'Color',color(k,:));
            end
            
            xlabel(strcat('$', c1{i}(k), '$'))
            ylabel(strcat('$', fields{j}, '$'))
            set (gca,'TicklabelInterpreter','LaTex')
            grid on
            
            % removing all problematic signs from figure name
            
            %             fig_name = regexprep(strcat(param{i,1}{1,1},fields{j}),'/','');
            %             fig_name = regexprep(fig_name,'\','');
            %             fig_name = strcat('.\figures\Fig_',fig_name);
            %
            %             print('-f',fig_name,'-depsc')
            
        end
    end
    
end




