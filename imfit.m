function [ poly ] = imfit( img, order, fig )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

if nargin <2
   order = 1 ;
end

[h, w] = size(img);

% All the indexes with the points on the curve
[y, x] = find(img==0);
y = h-y;

poly = polyfit(x,y,order);

if nargin >= 2
    figure(fig);
    hold on;
    xlim([1 w]); % Get the right scaling for the function
    ylim([1 h]);
    xval = linspace(1, length(x), length(x));
    yval = h-polyval(poly, xval);
    plot(xval, yval, '.r');
    hold off;
    axis on;
end

end

