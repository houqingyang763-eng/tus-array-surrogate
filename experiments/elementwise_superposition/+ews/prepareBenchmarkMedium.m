function mediumData = prepareBenchmarkMedium(cfg)
%PREPAREBENCHMARKMEDIUM Rasterize the public V1 skull STL and assign Table I properties.

dx = cfg.grid.dx_mm;
sz = round(cfg.grid.coverage_mm ./ dx);
cacheName = sprintf('aubry_v1_%dx%dx%d_dx_%gmm.mat', sz(1), sz(2), sz(3), dx);
cacheFile = fullfile(cfg.paths.cache_dir, cacheName);

if isfile(cacheFile)
    loaded = load(cacheFile);
    skullMask = loaded.skullMask;
    brainMask = loaded.brainMask;
else
    [skullMask, brainMask] = rasterizeV1(cfg, sz, dx);
    save(cacheFile, 'skullMask', 'brainMask', 'dx', '-v7.3');
end

if ~isequal(size(skullMask), sz)
    error('ews:BenchmarkSize', 'Cached skull size does not match the configured grid.');
end

water = cfg.material.water;
brain = cfg.material.brain;
bone = cfg.material.cortical_bone;

c = repmat(single(water.sound_speed_m_s), sz);
rho = repmat(single(water.density_kg_m3), sz);
alpha500 = zeros(sz, 'single');

c(brainMask) = single(brain.sound_speed_m_s);
rho(brainMask) = single(brain.density_kg_m3);
alpha500(brainMask) = single(brain.alpha_db_cm_at_500khz);

c(skullMask) = single(bone.sound_speed_m_s);
rho(skullMask) = single(bone.density_kg_m3);
alpha500(skullMask) = single(bone.alpha_db_cm_at_500khz);

% k-Wave alpha_coeff is dB/(MHz^y cm). Convert Table I's value at 0.5 MHz.
fMHz = cfg.acoustic.frequency_hz / 1e6;
alphaCoeff = alpha500 ./ single(fMHz ^ cfg.acoustic.alpha_power);

mediumData.medium.sound_speed = c;
mediumData.medium.density = rho;
mediumData.medium.alpha_coeff = alphaCoeff;
mediumData.medium.alpha_power = cfg.acoustic.alpha_power;
mediumData.brain_mask = brainMask;
mediumData.skull_mask = skullMask;
mediumData.cache_file = cacheFile;
mediumData.description = 'Aubry V1 STL: water + brain + uniform cortical skull';
end

function [skullCrop, brainCrop] = rasterizeV1(cfg, targetSize, dx)
benchmarkDir = fullfile(cfg.paths.benchmark_repo, 'intercomparison');
stlDir = fullfile(benchmarkDir, 'skull-stl');
outerFile = fullfile(stlDir, 'skull_outer.stl');
innerFile = fullfile(stlDir, 'skull_inner.stl');
affineFile = fullfile(stlDir, 'affine_transform_v1.mat');

if ~isfile(outerFile) || ~isfile(innerFile) || ~isfile(affineFile)
    error('ews:BenchmarkFiles', 'The benchmark STL or V1 affine transform is missing.');
end
if exist('surf2vol', 'file') ~= 2
    error('ews:MissingSurf2Vol', 'iso2mesh surf2vol is not on the MATLAB path.');
end

fprintf('Rasterizing Aubry V1 skull at %.3g mm (first run only)...\n', dx);
outerTri = stlread(outerFile);
innerTri = stlread(innerFile);
affineData = load(affineFile, 'affine_transform');
A = affineData.affine_transform;

outerPoints = transformPoints(outerTri.Points, A);
innerPoints = transformPoints(innerTri.Points, A);

% surf2vol must see a grid that encloses the complete surface. These are
% the public benchmark rasterization bounds, in millimetres.
xi = -180:dx:180;
yi = -180:dx:180;
zi = 0:dx:300;

outerVolume = surf2vol(outerPoints, outerTri.ConnectivityList, xi, yi, zi, 'fill', 1) > 0;
brainVolume = surf2vol(innerPoints, innerTri.ConnectivityList, xi, yi, zi, 'fill', 1) > 0;

% Published code permutes [x,y,z] -> [z,y,x] so propagation is along +x.
xWorld = (0:targetSize(1)-1) * dx;
yWorld = ((0:targetSize(2)-1) - targetSize(2)/2) * dx;
zWorld = ((0:targetSize(3)-1) - targetSize(3)/2) * dx;
ixOld = nearestIndices(xi, zWorld);
iyOld = nearestIndices(yi, yWorld);
izOld = nearestIndices(zi, xWorld);

outerCrop = permute(outerVolume(ixOld, iyOld, izOld), [3, 2, 1]);
brainCrop = permute(brainVolume(ixOld, iyOld, izOld), [3, 2, 1]);
skullCrop = outerCrop & ~brainCrop;

clear outerVolume brainVolume outerCrop
skullCrop = logical(skullCrop);
brainCrop = logical(brainCrop);
end

function points = transformPoints(points, A)
homogeneous = [double(points), ones(size(points, 1), 1)] * A.';
points = homogeneous(:, 1:3);
end

function ind = nearestIndices(axisValues, requested)
ind = round((requested - axisValues(1)) ./ (axisValues(2) - axisValues(1))) + 1;
if any(ind < 1) || any(ind > numel(axisValues))
    error('ews:RasterBounds', 'Requested crop extends beyond the rasterization bounds.');
end
actual = axisValues(ind);
if any(abs(actual - requested) > 1e-6)
    error('ews:RasterAlignment', 'Crop coordinates are not aligned to the raster grid.');
end
end
