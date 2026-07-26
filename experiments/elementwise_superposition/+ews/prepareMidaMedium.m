function [mediumData, cfg] = prepareMidaMedium(cfg)
%PREPAREMIDAMEDIUM Load, crop, downsample, and map licensed MIDA labels.
%
% The label semantics and crop orientation cannot be inferred safely. They
% are therefore explicit in config/mida_config.json; see the example file.

if ~isfile(cfg.paths.mida_config)
    error('ews:MissingMidaConfig', ...
        ['MIDA configuration was not found at %s. Copy mida_config.example.json ' ...
         'to mida_config.json and fill in the licensed-data path and label IDs.'], ...
        cfg.paths.mida_config);
end
midaCfg = jsondecode(fileread(cfg.paths.mida_config));
labelPath = char(midaCfg.label_file);
if ~isfile(labelPath)
    error('ews:MissingMidaData', 'MIDA label file was not found at %s.', labelPath);
end

[labels, inputVoxelMm] = loadLabels(labelPath, midaCfg);
if isfield(midaCfg, 'input_voxel_mm')
    inputVoxelMm = double(midaCfg.input_voxel_mm);
end
if isscalar(inputVoxelMm)
    inputVoxelMm = repmat(inputVoxelMm, 1, 3);
end
if any(abs(inputVoxelMm - inputVoxelMm(1)) > 1e-6)
    error('ews:MidaVoxel', 'This first implementation requires isotropic MIDA voxels.');
end

cropSize = round(cfg.grid.coverage_mm ./ inputVoxelMm);
startIndex = double(midaCfg.crop_start_index_1based(:).');
stopIndex = startIndex + cropSize - 1;
if any(startIndex < 1) || any(stopIndex > size(labels))
    error('ews:MidaCrop', 'Configured MIDA crop is outside the label volume.');
end
crop = labels(startIndex(1):stopIndex(1), startIndex(2):stopIndex(2), startIndex(3):stopIndex(3));

targetSize = round(cfg.grid.coverage_mm ./ cfg.grid.dx_mm);
if ~isequal(size(crop), targetSize)
    if exist('imresize3', 'file') ~= 2
        error('ews:MissingImresize3', 'Image Processing Toolbox imresize3 is required.');
    end
    crop = imresize3(crop, targetSize, 'nearest');
end

if isfield(midaCfg, 'target_world_mm')
    cfg.array.target_world_mm = double(midaCfg.target_world_mm(:).');
end
if isfield(midaCfg, 'array_centres_world_mm')
    centres = double(midaCfg.array_centres_world_mm);
    if ~isequal(size(centres), [4, 3])
        error('ews:MidaArray', 'array_centres_world_mm must be 4-by-3.');
    end
    cfg.array.centres_world_mm = centres;
end

ids = midaCfg.label_ids;
groups = {'background_water', 'brain', 'soft_tissue', 'cortical_bone', 'trabecular_bone'};
for idx = 1:numel(groups)
    if ~isfield(ids, groups{idx})
        error('ews:MidaLabels', 'Missing label group: %s.', groups{idx});
    end
end

allMapped = [];
for idx = 1:numel(groups)
    allMapped = [allMapped; double(ids.(groups{idx})(:))]; %#ok<AGROW>
end
unknown = setdiff(double(unique(crop(:))), unique(allMapped));
if ~isempty(unknown)
    error('ews:MidaLabels', 'Unmapped MIDA labels in crop: %s', mat2str(unknown(:).'));
end

waterMask = ismember(crop, ids.background_water);
brainMask = ismember(crop, ids.brain);
softMask = ismember(crop, ids.soft_tissue);
corticalMask = ismember(crop, ids.cortical_bone);
trabecularMask = ismember(crop, ids.trabecular_bone);
boneMask = corticalMask | trabecularMask;

sz = size(crop);
c = zeros(sz, 'single');
rho = zeros(sz, 'single');
alpha500 = zeros(sz, 'single');
[c, rho, alpha500] = assign(c, rho, alpha500, waterMask, cfg.material.water);
[c, rho, alpha500] = assign(c, rho, alpha500, brainMask, cfg.material.brain);
[c, rho, alpha500] = assign(c, rho, alpha500, softMask, cfg.material.skin);
[c, rho, alpha500] = assign(c, rho, alpha500, corticalMask, cfg.material.cortical_bone);
[c, rho, alpha500] = assign(c, rho, alpha500, trabecularMask, cfg.material.trabecular_bone);

fMHz = cfg.acoustic.frequency_hz / 1e6;
mediumData.medium.sound_speed = c;
mediumData.medium.density = rho;
mediumData.medium.alpha_coeff = alpha500 ./ single(fMHz ^ cfg.acoustic.alpha_power);
mediumData.medium.alpha_power = cfg.acoustic.alpha_power;
mediumData.brain_mask = brainMask;
mediumData.skull_mask = boneMask;
mediumData.description = 'Licensed MIDA label crop mapped through explicit JSON label groups';
mediumData.source_file = labelPath;
end

function [labels, voxelMm] = loadLabels(path, cfg)
voxelMm = [0.5, 0.5, 0.5];
lowerPath = lower(path);
if endsWith(lowerPath, '.mat')
    data = load(path);
    variable = char(cfg.label_variable);
    if ~isfield(data, variable)
        error('ews:MidaVariable', 'Variable %s is absent from %s.', variable, path);
    end
    labels = data.(variable);
elseif endsWith(lowerPath, '.nii') || endsWith(lowerPath, '.nii.gz')
    info = niftiinfo(path);
    labels = niftiread(info);
    voxelMm = double(info.PixelDimensions(1:3));
else
    error('ews:MidaFormat', 'Supported MIDA inputs are .mat, .nii, and .nii.gz.');
end
if ndims(labels) ~= 3
    error('ews:MidaDimension', 'MIDA labels must be a 3D array.');
end
end

function [c, rho, alpha] = assign(c, rho, alpha, mask, mat)
c(mask) = single(mat.sound_speed_m_s);
rho(mask) = single(mat.density_kg_m3);
alpha(mask) = single(mat.alpha_db_cm_at_500khz);
end
