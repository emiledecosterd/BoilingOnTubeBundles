% Boiling on tube bundles
% Little script to get a fit for the flow pattern map curves

close all; clear variables; clc;

%%  Get the image
map = imread('FlowPatternMap/flow_pattern_map_filtered.png');
map = rgb2gray(map);
figure('name', 'Grayscale image');
imshow(map);

% Threshold it
map = 1-(map<110);
figure('name', 'Thresholded map');
imshow(map);

% Put origin at the right place
map = imcrop(map);
figure('name', 'Re-centered map');
imshow(map);

%% Separate curves in images
center = [225, 90]; % The point where the curves meet

map_1 =  map(center(2):end, 1:center(1));
fig1 = figure('name', 'First curve image');
imshow(map_1);

map_2 = map(1:center(2), :);
fig2 = figure('name', 'Second curve image');
imshow(map_2);

map_3 = map(center(2):end, center(1):end);
fig3 = figure('name', 'Third curve image');
imshow(map_3);

%% Find fits

fit_1 = imfit(map_1, 2, fig1)
fit_2 = imfit(map_2, 1, fig2)
fit_3 = imfit(map_3, 1, fig3)

