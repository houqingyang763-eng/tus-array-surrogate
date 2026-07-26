function metrics = computeMetrics(reference, candidate, evalMask, targetWorldMm, outputSpacingMm)
%COMPUTEMETRICS Compare monolithic reference and elementwise reconstruction.

ref = reference.large;
test = candidate.large;
mask = logical(evalMask);
if ~isequal(size(ref), size(test), size(mask))
    error('ews:MetricSize', 'Fields and evaluation mask must have identical sizes.');
end

refVector = ref(mask);
testVector = test(mask);
metrics.complex_relative_l2 = norm(double(testVector - refVector)) / norm(double(refVector));
metrics.amplitude_relative_l2 = norm(double(abs(testVector) - abs(refVector))) / norm(double(abs(refVector)));

peakReference = max(abs(refVector));
phaseMask = mask & abs(ref) >= 0.1 * peakReference;
phaseDifference = angle(test(phaseMask) .* conj(ref(phaseMask)));
metrics.phase_mae_deg_above_minus20db = mean(abs(rad2deg(double(phaseDifference))));
metrics.phase_points = nnz(phaseMask);

refStats = fieldStats(reference, mask, targetWorldMm, outputSpacingMm);
testStats = fieldStats(candidate, mask, targetWorldMm, outputSpacingMm);
metrics.p_target_reference_pa = refStats.p_target_pa;
metrics.p_target_candidate_pa = testStats.p_target_pa;
metrics.p_target_relative_error = relativeError(refStats.p_target_pa, testStats.p_target_pa);
metrics.p_peak_reference_pa = refStats.p_peak_pa;
metrics.p_peak_candidate_pa = testStats.p_peak_pa;
metrics.p_peak_relative_error = relativeError(refStats.p_peak_pa, testStats.p_peak_pa);
metrics.focus_reference_world_mm = refStats.peak_world_mm;
metrics.focus_candidate_world_mm = testStats.peak_world_mm;
metrics.focus_error_mm = norm(refStats.peak_world_mm - testStats.peak_world_mm);
metrics.focus_index_equal = isequal(refStats.peak_sub, testStats.peak_sub);
metrics.fwhm_reference_mm = refStats.fwhm_mm;
metrics.fwhm_candidate_mm = testStats.fwhm_mm;
metrics.fwhm_abs_difference_mm = abs(refStats.fwhm_mm - testStats.fwhm_mm);
metrics.focal_volume_minus6db_reference_mm3 = refStats.focal_volume_mm3;
metrics.focal_volume_minus6db_candidate_mm3 = testStats.focal_volume_mm3;
metrics.focal_volume_minus6db_relative_error = relativeError(refStats.focal_volume_mm3, testStats.focal_volume_mm3);
metrics.sidelobe_ratio_reference = refStats.sidelobe_ratio;
metrics.sidelobe_ratio_candidate = testStats.sidelobe_ratio;
metrics.sidelobe_ratio_abs_error = abs(refStats.sidelobe_ratio - testStats.sidelobe_ratio);

metrics.pass_complex_l2 = metrics.complex_relative_l2 <= 1e-4;
metrics.pass_amplitude_l2 = metrics.amplitude_relative_l2 <= 1e-4;
metrics.pass_phase = metrics.phase_mae_deg_above_minus20db <= 0.1;
metrics.pass_target_peak = metrics.p_target_relative_error <= 1e-3 && metrics.p_peak_relative_error <= 1e-3;
metrics.pass_focus = metrics.focus_index_equal;
metrics.pass_all_strict = metrics.pass_complex_l2 && metrics.pass_amplitude_l2 && ...
    metrics.pass_phase && metrics.pass_target_peak && metrics.pass_focus;
end

function stats = fieldStats(field, evalMask, targetWorldMm, spacingMm)
amplitude = abs(field.large);
masked = amplitude;
masked(~evalMask) = -inf;
[stats.p_peak_pa, linearPeak] = max(masked(:));
[px, py, pz] = ind2sub(size(masked), linearPeak);
stats.peak_sub = [px, py, pz];
stats.peak_world_mm = [field.large_axes_mm.x(px), field.large_axes_mm.y(py), field.large_axes_mm.z(pz)];

targetSubFocus = [nearest(field.focus_axes_mm.x, targetWorldMm(1)), ...
    nearest(field.focus_axes_mm.y, targetWorldMm(2)), ...
    nearest(field.focus_axes_mm.z, targetWorldMm(3))];
stats.p_target_pa = abs(field.focus(targetSubFocus(1), targetSubFocus(2), targetSubFocus(3)));

stats.fwhm_mm = [ ...
    widthAtHalf(amplitude(:, py, pz), spacingMm), ...
    widthAtHalf(amplitude(px, :, pz), spacingMm), ...
    widthAtHalf(amplitude(px, py, :), spacingMm)];

focalMask = amplitude >= 0.5 * stats.p_peak_pa & evalMask;
componentMask = peakComponent(focalMask, linearPeak);
stats.focal_volume_mm3 = nnz(componentMask) * spacingMm ^ 3;
stats.sidelobe_ratio = sidelobeRatio(amplitude, evalMask, stats.peak_sub, stats.fwhm_mm, spacingMm, stats.p_peak_pa);
end

function component = peakComponent(mask, peakLinear)
component = false(size(mask));
if exist('bwconncomp', 'file') == 2
    cc = bwconncomp(mask, 26);
    for idx = 1:cc.NumObjects
        if any(cc.PixelIdxList{idx} == peakLinear)
            component(cc.PixelIdxList{idx}) = true;
            return;
        end
    end
end
component = mask;
end

function ratio = sidelobeRatio(amplitude, evalMask, peakSub, fwhmMm, spacingMm, peak)
% Exclude an ellipsoid whose semi-axes are 1.5 times the half-maximum widths.
radiusVox = max(1, 0.75 .* fwhmMm ./ spacingMm);
[X, Y, Z] = ndgrid(1:size(amplitude, 1), 1:size(amplitude, 2), 1:size(amplitude, 3));
inside = ((X - peakSub(1)) ./ radiusVox(1)).^2 + ...
    ((Y - peakSub(2)) ./ radiusVox(2)).^2 + ...
    ((Z - peakSub(3)) ./ radiusVox(3)).^2 <= 1;
outside = evalMask & ~inside;
if any(outside(:))
    ratio = max(amplitude(outside)) / peak;
else
    ratio = NaN;
end
end

function width = widthAtHalf(profile, spacing)
profile = squeeze(profile);
threshold = 0.5 * max(profile);
indices = find(profile >= threshold);
if isempty(indices)
    width = NaN;
else
    width = (indices(end) - indices(1) + 1) * spacing;
end
end

function idx = nearest(axisValues, value)
[~, idx] = min(abs(axisValues - value));
end

function value = relativeError(reference, candidate)
value = abs(double(candidate) - double(reference)) / max(abs(double(reference)), eps);
end
