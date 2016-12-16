close all
clear all


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

%% alpha_a correlations

files = dir([pwd, '\*_a_nb.txt']);


for i = 1:length(files)
    Dat{i}=importdata([pwd,'\',getfield(files,{i},'name')]);
    
    Data_plot{1,i}(1,:)=Dat{1,i}.data((1:2:end),:);
    Data_plot{1,i}(2,:)=Dat{1,i}.data((2:2:end),:);
end





figure()
hold on

Leg={};

for i=1:length(files)
    plot(log(Data_plot{i}(1,:)), log(Data_plot{i}(2,:)),...
        'x--','Linewidth',width,'Color',color(i,:));
    name=getfield(files,{i},'name');
    Leg=[Leg,strcat('$',name(1:end-9),'$')];
end

xlabel('$ln(q_0)$')
ylabel('$ln(\alpha_{nb})$')
h=legend(Leg);
set(h,'FontSize',10);
set (gca,'TicklabelInterpreter','LaTex')
grid on

%axis([8.5, 10.5, 7.5, 9.5])

%% Feenstra correlation



Dat = importdata('Feenstra_eps.txt');

Dat.data = reshape(Dat.data, 60, 5);

x=Dat.data((1:2:60),1);

figure()

for i = 1:5

    eps(:,i)=Dat.data((2:2:end),i);
    semilogx(x,eps(:,i), '--','Linewidth',width,'Color',color(i,:))
    hold on

end

x = [0.8 0.6];
y = [0.25 0.5];
annotation('textarrow',x,y);
text(0.2, 0.4, 'G')

set (gca,'TicklabelInterpreter','LaTex')

xlabel('$x$')
ylabel('$\varepsilon$')
set (gca,'TicklabelInterpreter','LaTex')
grid on


