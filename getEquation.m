% Boiling on tube bundles
% Little script to get a fit for the flow pattern map curves

% Get the image
map = imread('FlowPatternMap/flow_pattern_map.png');
map = rgb2gray(map);
figure();
imshow(map);

% Threshold it
map = 1-(map<100);
figure();
imshow(map)


