close all
clear all

files = dir([pwd, '\*.txt']);


for i = 1:length(files)
   Dat{i}=importdata([pwd,'\',getfield(files,{i},'name')]);
end
