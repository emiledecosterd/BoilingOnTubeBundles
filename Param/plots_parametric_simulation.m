close all
clear all


%% Datas are read from .txt

directory = uigetdir('./','Choose Folder containing data to process');

files = dir([directory, '/*res.txt']);

Data=cell(length(files),1);

param_1=cell(length(files));
param_2=cell(length(files));


for i = 1:length(files)
    Dat = importdata([directory,'\',getfield(files,{i},'name')]);
    param_2{i} = Dat.textdata(1,1);% gets param_2
    
    index_2=zeros(1,length(Dat.data));
    
    for j = 1:length(Dat.textdata)
        index_2(j)=isequal(param_2{i}, Dat.textdata(j,1));% counts instances of Param_2
    end
    
    n_sim = sum(index_2);% number of instances of Param_2 i equal to nb of simulations
    n_outputs = length(Dat.textdata)/n_sim; % number of outputs per sim if total nb of outputs/ nb of sim
    
    for j = 2:n_outputs:length(Dat.textdata)% reads all param_1 for each simulation
        param_1{j} = Dat.textdata(j,1);
    end
    
    [c1{i}, ia1{i}, ia2{i}] = unique([param_1{:,:}]);
    % counts the number of differents instances of e param_2, gives the
    % number of differents param_1, names are in c1, ia1 contains the
    % coordinate of param_1 changes
    
    Data{i}=reshape(Dat.data, n_outputs, n_sim);
    % reshapes matrix in order to have one simulation per column
    % the order is :
    % Param_2_1  Param_2_1  ... Param_2_2  Param_2_2 ...
    % Param_1_1  Param_1_2  ... Param_1_1  Param_1_2 ...
    % fields     fields         fields     fields
    
    if length(ia1{i}) == 1
        n_points_param_2 = length(unique(Data{i,1}(1,1:end)));
    else
        n_points_param_2 = length(unique(Data{i,1}(1,1:ia1{i}(2)-1)));
        % counts number of points for Param_2
    end
    for j=1:length(ia1{i})
        if j == length(ia1{i})
            n_points_param_1{i}(j) = (n_sim+1-ia1{i}(j))/n_points_param_2;
            
            Data_plot{i,j} = Data{i,1}(:,ia1{i}(j):end);
            
        else
            n_points_param_1{i}(j) = (ia1{i}(j+1)-ia1{i}(j))/n_points_param_2;
            % the number of points for param_1 is total number of simulation for
            % param1/number of points for param_2
            
            Data_plot{i,j} = Data{i,1}(:,ia1{i}(j):ia1{i}(j+1)-1);
            % separates all simulation according to param_1, for each j we
            % change param_1
        end
        
        Data_plot{i,j} = reshape(Data_plot{i,j}, n_outputs,...
            n_points_param_1{i}(j), n_points_param_2);
        % reshapes Data_plots{i,j} to have 3d matrices with each layer is
        % Param_2_1  Param_2_1
        % Param_1_1  Param_1_2
        % fields     fields
        
        % this represents the first layer (Param_2_1<-)
        
    end
    
    
    
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

mkdir(directory,'figures')

plot_error = 0; % option to plot relative error to last term computed 0 when deactivated, 1 to activate
fluids = [{'R134a'},{'Ammonia'},{'Propane'}];
corrPD = [{'Gaddis'},{'Zukauskas'}];
layout = [{'Staggered'},{'In line'}];


for i=1:length(files) % loop on files (lines of Data_plot)
    
    for j=1:length(c1{i}) % loop on diferents param_1
        
        for k=3:n_outputs% loop on field outputs
            
            figure()
            hold on
            Leg={};
            
            for l=1:n_points_param_2 % loops on param_2
                
                if plot_error == 1
                    
                    plot(Data_plot{i,j}(2,:,l),...
                        100*(Data_plot{i,j}(k,:,l)-Data_plot{i,j}(k,end,l))./Data_plot{i,j}(k,end,l),...
                        'x--','Linewidth',width,'Color',color(l,:))
                    Leg=[Leg,strcat('$',param_2{i},'=',num2str(Data_plot{i,j}(1,1,l)),'$')];
                    
                elseif isequal(fields{1}, 'FluidType')
                    plot(Data_plot{i,j}(2,:,l),Data_plot{i,j}(k,:,l),...
                        'x--','Linewidth',width,'Color',color(l,:))
                    Leg=[Leg,strcat('$',fluids(l),'$')];
                    
                elseif isequal(fields{1}, 'corrPD')
                    plot(Data_plot{i,j}(2,:,l),Data_plot{i,j}(k,:,l),...
                        'x--','Linewidth',width,'Color',color(l,:))
                    Leg=[Leg,strcat('$',corrPD(l),'$')];
                    
                elseif isequal(fields{1}, 'layout')
                    plot(Data_plot{i,j}(2,:,l),Data_plot{i,j}(k,:,l),...
                        'x--','Linewidth',width,'Color',color(l,:))
                    Leg=[Leg,strcat('$',layout(l),'$')];
                    
                else
                    plot(Data_plot{i,j}(2,:,l),Data_plot{i,j}(k,:,l),...
                        'x--','Linewidth',width,'Color',color(l,:))
                    Leg=[Leg,strcat('$',param_2{i},'=',num2str(Data_plot{i,j}(1,1,l)),'$')];
                end
                
            end
            
            xlabel(strcat('$', c1{i}(j), '$'))
            
            if plot_error == 1
                ylabel(strcat('$', fields{k}(1:strfind(fields{k}, '[')-1),'\%', '$'))
            else
                ylabel(strcat('$', fields{k}, '$'))
            end
            h=legend(Leg,'Location','best' );
            set(h,'FontSize',10);
            %set(h,'box','off')
            set (gca,'TicklabelInterpreter','LaTex')
            grid on
            
            %removing all problematic signs from figure name
            
            fig_name = regexprep(strcat('Fig_',c1{i}(j),'_',param_2{i},'_',fields{k}),'/','');
            fig_name = regexprep(fig_name,'\','');
            
            print('-f',  '-dpng', fullfile(directory,'figures',cell2mat(fig_name)))
            
        end
    end
end

close all


