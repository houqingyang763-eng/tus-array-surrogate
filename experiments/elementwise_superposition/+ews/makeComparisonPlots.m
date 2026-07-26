function makeComparisonPlots(reference, candidate, metrics, caseName, outputDir)
%MAKECOMPARISONPLOTS Save central/peak slices, error maps, and profiles.

refAmp = abs(reference.large);
testAmp = abs(candidate.large);
[~, peakLinear] = max(refAmp(:));
[px, py, pz] = ind2sub(size(refAmp), peakLinear);

fig = figure('Visible', 'off', 'Color', 'w', 'Position', [100, 100, 1500, 900]);
cleanup = onCleanup(@() close(fig));
planes = {squeeze(refAmp(:, :, pz)), squeeze(refAmp(:, py, :)), squeeze(refAmp(px, :, :)), ...
    squeeze(testAmp(:, :, pz)), squeeze(testAmp(:, py, :)), squeeze(testAmp(px, :, :)), ...
    squeeze(abs(testAmp(:, :, pz) - refAmp(:, :, pz))), ...
    squeeze(abs(testAmp(:, py, :) - refAmp(:, py, :))), ...
    squeeze(abs(testAmp(px, :, :) - refAmp(px, :, :)))};
titles = {'Reference XY', 'Reference XZ', 'Reference YZ', ...
    'Superposition XY', 'Superposition XZ', 'Superposition YZ', ...
    '|Amplitude diff| XY', '|Amplitude diff| XZ', '|Amplitude diff| YZ'};
xCoordinates = {reference.large_axes_mm.x, reference.large_axes_mm.x, reference.large_axes_mm.y, ...
    reference.large_axes_mm.x, reference.large_axes_mm.x, reference.large_axes_mm.y, ...
    reference.large_axes_mm.x, reference.large_axes_mm.x, reference.large_axes_mm.y};
yCoordinates = {reference.large_axes_mm.y, reference.large_axes_mm.z, reference.large_axes_mm.z, ...
    reference.large_axes_mm.y, reference.large_axes_mm.z, reference.large_axes_mm.z, ...
    reference.large_axes_mm.y, reference.large_axes_mm.z, reference.large_axes_mm.z};
xLabels = {'x (mm)', 'x (mm)', 'y (mm)', 'x (mm)', 'x (mm)', 'y (mm)', 'x (mm)', 'x (mm)', 'y (mm)'};
yLabels = {'y (mm)', 'z (mm)', 'z (mm)', 'y (mm)', 'z (mm)', 'z (mm)', 'y (mm)', 'z (mm)', 'z (mm)'};
for idx = 1:9
    subplot(3, 3, idx);
    imagesc(xCoordinates{idx}, yCoordinates{idx}, planes{idx}.');
    axis xy image tight; colorbar;
    xlabel(xLabels{idx}); ylabel(yLabels{idx});
    title(titles{idx}, 'Interpreter', 'none');
end
sgtitle(sprintf('%s: complex L2 %.3g, amplitude L2 %.3g', caseName, ...
    metrics.complex_relative_l2, metrics.amplitude_relative_l2), 'Interpreter', 'none');
exportgraphics(fig, fullfile(outputDir, [caseName '_slices.png']), 'Resolution', 160);
clear cleanup

fig = figure('Visible', 'off', 'Color', 'w', 'Position', [100, 100, 1400, 420]);
cleanup = onCleanup(@() close(fig));
axesNames = {'x', 'y', 'z'};
axisValues = {reference.large_axes_mm.x, reference.large_axes_mm.y, reference.large_axes_mm.z};
refProfiles = {refAmp(:, py, pz), squeeze(refAmp(px, :, pz)), squeeze(refAmp(px, py, :))};
testProfiles = {testAmp(:, py, pz), squeeze(testAmp(px, :, pz)), squeeze(testAmp(px, py, :))};
for idx = 1:3
    subplot(1, 3, idx);
    plot(axisValues{idx}, refProfiles{idx} ./ 1e3, 'k-', 'LineWidth', 1.5); hold on;
    plot(axisValues{idx}, testProfiles{idx} ./ 1e3, 'r--', 'LineWidth', 1.2);
    xlabel([axesNames{idx} ' (mm)']); ylabel('|P| (kPa)'); grid on;
    legend('Monolithic', 'Elementwise sum', 'Location', 'best');
end
exportgraphics(fig, fullfile(outputDir, [caseName '_profiles.png']), 'Resolution', 160);
end
