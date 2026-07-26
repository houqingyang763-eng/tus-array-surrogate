function run_green_skull_labels(outputDir)
%RUN_GREEN_SKULL_LABELS Generate the frozen 8-train/4-test skull smoke labels.

arguments
    outputDir (1, 1) string
end

repoRoot = fileparts(fileparts(fileparts(mfilename('fullpath'))));
superpositionRoot = fullfile(repoRoot, 'experiments', 'elementwise_superposition');
addpath(superpositionRoot);

cfg = ews.defaultConfig("benchmark_skull", superpositionRoot);
cfg.run.dir = char(outputDir);
cfg.run.overwrite = false;
cfg.output.make_plots = false;
cfg.output.save_monolithic_fields = false;
cfg.array.centres_world_mm = [ ...
    1, -12, -12; 1, -12, 0; 1, -12, 12; 1, 0, -12; ...
    1, 0, 12; 1, 12, -12; 1, 12, 0; 1, 12, 12; ...
    1, -20, -20; 1, -20, 20; 1, 20, -20; 1, 20, 20];
cfg.array.target_world_mm = [64, 0, 0];

if ~isfolder(outputDir); mkdir(outputDir); end
ews.setupPaths(cfg);
mediumData = ews.prepareBenchmarkMedium(cfg);
grid = ews.buildGrid(cfg, mediumData);
sensorDef = ews.buildSensor(cfg, grid);
[geometrySource, ~] = ews.buildSource(cfg, grid, 1:12, ones(1, 12), zeros(1, 12));
geometry = ews.validateGeometry(cfg, mediumData, geometrySource.p_mask, grid);
clear geometrySource
ews.writeJson(fullfile(outputDir, 'geometry.json'), geometry);
ews.writeJson(fullfile(outputDir, 'config.json'), cfg);

for sourceNo = 1:12
    compactFile = fullfile(outputDir, sprintf('source_%02d.mat', sourceNo));
    if isfile(compactFile); continue; end
    caseName = sprintf('kwave_source_%02d', sourceNo);
    [field, meta] = ews.runGpuCase(cfg, mediumData, grid, sensorDef, ...
        caseName, sourceNo, 1, 0);
    field_re_large = real(field.large); %#ok<NASGU>
    field_im_large = imag(field.large); %#ok<NASGU>
    x_mm = field.large_axes_mm.x; %#ok<NASGU>
    y_mm = field.large_axes_mm.y; %#ok<NASGU>
    z_mm = field.large_axes_mm.z; %#ok<NASGU>
    source_centre_mm = cfg.array.centres_world_mm(sourceNo, :); %#ok<NASGU>
    source_normal = cfg.array.target_world_mm - source_centre_mm; %#ok<NASGU>
    source_normal = source_normal ./ norm(source_normal);
    save(compactFile, 'field_re_large', 'field_im_large', 'x_mm', 'y_mm', ...
        'z_mm', 'source_centre_mm', 'source_normal', 'meta', '-v7');
end
end
