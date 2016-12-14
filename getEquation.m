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
height = 272;
width = 450;
rect = [80, 0, height , width];
map = imcrop(map, rect);
figure('name', 'Re-centered map');
imshow(map);

%% Separate curves in images
center = [225, 90]; % The point where the curves meet
[h, w] = size(map);
map_1 =  map(center(2):end, 1:center(1));
[h1, w1] = size(map_1);
fig1 = figure('name', 'First curve image');
imshow(map_1);

map_2 = map(1:center(2), :);
[h2, w2] = size(map_2);
fig2 = figure('name', 'Second curve image');
imshow(map_2);

map_3 = map(center(2):end, center(1):end);
[h3, w3] = size(map_3);
fig3 = figure('name', 'Third curve image');
imshow(map_3);

%% Find fits

fit_1 = imfit(map_1, 2, fig1)
fit_2 = imfit(map_2, 1, fig2)
fit_3 = imfit(map_3, 1, fig3)

%% Plot the map

[y1o, x1o] = find(map_1==0);
[y2o, x2o] = find(map_2==0);
[y3o, x3o] = find(map_3==0);
y1o = h1-y1o;
% y2o = h-y2o; x2o = w2-x2o;
% y3o = h3-y3o; x3o = w-x3o;
x1 = 0:center(1); y1 = polyval(fit_1, x1);
x2 = center(1):255; y2 = polyval(fit_2,x2)+170;
x3 = center(1):320; y3 = polyval(fit_3, x3)+165;

figure('name', 'Identified map');
xlim([1 width]);
ylim([1 height]);
hold on;
plot([x1,x2,x3], [y1,y2,y3],'.r');
plot(x1o,y1o,'.k');
plot(x2o,y2o,'.k');
plot(x3o,y3o,'.k');
hold off;
