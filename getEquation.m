% Boiling on tube bundles
% Little script to get a fit for the flow pattern map curves

% Get the image
map = imread('FlowPatternMap/flow_pattern_map_filtered.png');
map = rgb2gray(map);
figure();
imshow(map);

% Threshold it
map = 1-(map<110);
figure();
imshow(map)

% Separate image
[width, height] = size(map);
first_map = map(1:width-215, height-75:height);


% Get coordinates
[x, y] = find(map);
curve = polyfit
