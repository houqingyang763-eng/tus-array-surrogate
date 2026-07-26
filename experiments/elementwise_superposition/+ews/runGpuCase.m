function [field, meta] = runGpuCase(cfg, mediumData, grid, sensorDef, caseName, geometryIndices, amplitudes, phases)
%RUNGPUCASE Run or resume one GPU simulation and extract absolute complex pressure.

fieldFile = fullfile(cfg.run.dir, [caseName '_field.mat']);
metaFile = fullfile(cfg.run.dir, [caseName '_meta.json']);
if isfile(fieldFile) && isfile(metaFile) && ~cfg.run.overwrite
    field = ews.loadField(fieldFile);
    meta = jsondecode(fileread(metaFile));
    meta.resumed = true;
    return;
end

prepStart = tic;
[source, sourceMeta] = ews.buildSource(cfg, grid, geometryIndices, amplitudes, phases);
prepSeconds = toc(prepStart);

if cfg.run.dry_run
    field = struct();
    meta.case_name = caseName;
    meta.dry_run = true;
    meta.source = sourceMeta;
    meta.preparation_seconds = prepSeconds;
    ews.writeJson(metaFile, meta);
    return;
end

consoleFile = fullfile(cfg.run.dir, [caseName '_console.txt']);
if isfile(consoleFile)
    delete(consoleFile);
end
diary(consoleFile);
diaryCleanup = onCleanup(@() diary('off'));

inputArgs = { ...
    'PMLSize', cfg.grid.pml_size, ...
    'PMLInside', false, ...
    'PlotPML', false, ...
    'DisplayMask', 'off', ...
    'BinaryPath', cfg.paths.kwave_binary_dir};

fprintf('\n=== GPU CASE %s ===\n', caseName);
solveStart = tic;
sensorData = kspaceFirstOrder3DG(grid.kgrid, mediumData.medium, source, ...
    sensorDef.sensor, inputArgs{:});
wrapperSeconds = toc(solveStart);
diary('off');
clear diaryCleanup

postStart = tic;
[amp, phase, extractedFrequency] = extractAmpPhase(sensorData.p, 1 / grid.dt_s, ...
    cfg.acoustic.frequency_hz, 'Dim', 2, 'Window', 'Rectangular', 'FFTPadding', 1);
pSensor = single(amp) .* exp(1i .* single(phase));
clear sensorData amp phase source

fullField = complex(zeros(grid.kgrid.Nx, grid.kgrid.Ny, grid.kgrid.Nz, 'single'));
fullField(sensorDef.sensor.mask) = pSensor;
field.large = fullField(sensorDef.large_subs{1}, sensorDef.large_subs{2}, sensorDef.large_subs{3});
field.focus = fullField(sensorDef.focus_subs{1}, sensorDef.focus_subs{2}, sensorDef.focus_subs{3});
field.large_axes_mm = sensorDef.large_axes_mm;
field.focus_axes_mm = sensorDef.focus_axes_mm;
clear fullField pSensor
postSeconds = toc(postStart);

saveStart = tic;
ews.saveField(fieldFile, field, cfg.output.compression);
saveSeconds = toc(saveStart);
fileInfo = dir(fieldFile);

consoleText = '';
if isfile(consoleFile)
    consoleText = fileread(consoleFile);
end
meta.case_name = caseName;
meta.resumed = false;
meta.source = sourceMeta;
meta.extracted_frequency_hz = extractedFrequency;
meta.preparation_seconds = prepSeconds;
meta.gpu_wrapper_seconds = wrapperSeconds;
meta.postprocess_seconds = postSeconds;
meta.save_seconds = saveSeconds;
meta.output_bytes = fileInfo.bytes;
meta.gpu_solver_seconds = parseNumber(consoleText, 'Total execution time:\s*([0-9.eE+-]+)s');
meta.peak_gpu_memory_mb = parseNumber(consoleText, 'Peak device memory in use:\s*([0-9.eE+-]+)MB');
meta.grid_points = [grid.kgrid.Nx, grid.kgrid.Ny, grid.kgrid.Nz];
meta.Nt = grid.Nt;
meta.dt_s = grid.dt_s;
meta.points_per_period = grid.ppp;
meta.sensor_points = sensorDef.sensor_points;
ews.writeJson(metaFile, meta);
end

function value = parseNumber(text, expression)
token = regexp(text, expression, 'tokens', 'once');
if isempty(token)
    value = NaN;
else
    value = str2double(token{1});
end
end
