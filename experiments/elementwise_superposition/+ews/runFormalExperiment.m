function result = runFormalExperiment(cfg)
%RUNFORMALEXPERIMENT Four single-element GPU fields versus three monolithic drives.

switch cfg.mode
    case 'benchmark_skull'
        mediumData = ews.prepareBenchmarkMedium(cfg);
    case 'mida'
        [mediumData, cfg] = ews.prepareMidaMedium(cfg);
    otherwise
        error('ews:FormalMode', 'Unsupported formal mode: %s.', cfg.mode);
end

env = ews.probeEnvironment(cfg);
ews.writeJson(fullfile(cfg.run.dir, 'environment.json'), env);
ews.writeJson(fullfile(cfg.run.dir, 'config.json'), cfg);

grid = ews.buildGrid(cfg, mediumData);
sensorDef = ews.buildSensor(cfg, grid);
[geometrySource, ~] = ews.buildSource(cfg, grid, 1:4, ones(1, 4), zeros(1, 4));
geometry = ews.validateGeometry(cfg, mediumData, geometrySource.p_mask, grid);
clear geometrySource
geometry.grid_points = [grid.kgrid.Nx, grid.kgrid.Ny, grid.kgrid.Nz];
geometry.world_axes_mm = grid.world_axes_mm;
geometry.medium_description = mediumData.description;
ews.writeJson(fullfile(cfg.run.dir, 'geometry.json'), geometry);

library = cell(1, 4);
libraryMeta = cell(1, 4);
for elementNo = 1:4
    caseName = sprintf('element_%d', elementNo);
    [library{elementNo}, libraryMeta{elementNo}] = ews.runGpuCase(cfg, mediumData, ...
        grid, sensorDef, caseName, elementNo, 1, 0);
end

if cfg.run.dry_run
    result.run_dir = cfg.run.dir;
    result.status = 'dry_run_complete';
    return;
end

targetPhase = zeros(1, 4);
for elementNo = 1:4
    targetPhase(elementNo) = phaseAtTarget(library{elementNo}, cfg.array.target_world_mm);
end

cases(1) = driveCase('case1_equal_zero_phase', ones(1, 4), zeros(1, 4));
cases(2) = driveCase('case2_target_phase_aligned', ones(1, 4), wrapToPiLocal(-targetPhase));
cases(3) = driveCase('case3_asymmetric', [1, 0.8, 0.6, 1], [0, pi/2, pi, -pi/2]);

largeMask = mediumData.brain_mask(sensorDef.large_subs{1}, sensorDef.large_subs{2}, sensorDef.large_subs{3});
if ~any(largeMask(:))
    error('ews:EmptyEvaluationMask', 'The brain evaluation mask is empty.');
end

caseResults = repmat(struct(), 1, numel(cases));
for caseNo = 1:numel(cases)
    drive = cases(caseNo);
    summed = ews.superposeFields(library, drive.amplitudes, drive.phases_rad);
    sumFile = fullfile(cfg.run.dir, [drive.name '_sum_field.mat']);
    ews.saveField(sumFile, summed, cfg.output.compression);

    [monolithic, monoMeta] = ews.runGpuCase(cfg, mediumData, grid, sensorDef, ...
        [drive.name '_monolithic'], 1:4, drive.amplitudes, drive.phases_rad);
    metrics = ews.computeMetrics(monolithic, summed, largeMask, ...
        cfg.array.target_world_mm, cfg.grid.output_spacing_mm);
    if cfg.output.make_plots
        ews.makeComparisonPlots(monolithic, summed, metrics, drive.name, cfg.run.dir);
    end

    caseResults(caseNo).name = drive.name;
    caseResults(caseNo).amplitudes = drive.amplitudes;
    caseResults(caseNo).phases_rad = drive.phases_rad;
    caseResults(caseNo).sum_seconds = summed.sum_seconds;
    caseResults(caseNo).monolithic_meta = monoMeta;
    caseResults(caseNo).metrics = metrics;
    ews.writeJson(fullfile(cfg.run.dir, [drive.name '_metrics.json']), caseResults(caseNo));
end

timing = timingSummary(libraryMeta, caseResults);
ews.writeJson(fullfile(cfg.run.dir, 'timing_summary.json'), timing);
writeMetricCsv(fullfile(cfg.run.dir, 'comparison_metrics.csv'), caseResults);

allPass = all(arrayfun(@(x) x.metrics.pass_all_strict, caseResults));
summary.mode = cfg.mode;
summary.run_dir = cfg.run.dir;
summary.all_cases_pass_strict = allPass;
summary.library_target_phase_rad = targetPhase;
summary.cases = caseResults;
summary.timing = timing;
ews.writeJson(fullfile(cfg.run.dir, 'summary.json'), summary);

result.run_dir = cfg.run.dir;
result.status = ternary(allPass, 'passed', 'completed_with_failed_acceptance');
result.summary = summary;
end

function out = driveCase(name, amplitudes, phases)
out.name = name;
out.amplitudes = amplitudes;
out.phases_rad = phases;
end

function value = phaseAtTarget(field, target)
ix = nearest(field.focus_axes_mm.x, target(1));
iy = nearest(field.focus_axes_mm.y, target(2));
iz = nearest(field.focus_axes_mm.z, target(3));
value = angle(field.focus(ix, iy, iz));
end

function idx = nearest(axisValues, value)
[~, idx] = min(abs(axisValues - value));
end

function phases = wrapToPiLocal(phases)
phases = mod(phases + pi, 2*pi) - pi;
end

function timing = timingSummary(libraryMeta, caseResults)
timing.T_library_wrapper_seconds = sum(cellfun(@(x) double(x.gpu_wrapper_seconds), libraryMeta));
timing.T_library_gpu_solver_seconds = sumIgnoringNaN(cellfun(@(x) double(x.gpu_solver_seconds), libraryMeta));
timing.case = repmat(struct(), 1, numel(caseResults));
for idx = 1:numel(caseResults)
    mono = double(caseResults(idx).monolithic_meta.gpu_wrapper_seconds);
    sumTime = double(caseResults(idx).sum_seconds);
    denominator = mono - sumTime;
    timing.case(idx).name = caseResults(idx).name;
    timing.case(idx).T_monolithic_wrapper_seconds = mono;
    timing.case(idx).T_monolithic_gpu_solver_seconds = double(caseResults(idx).monolithic_meta.gpu_solver_seconds);
    timing.case(idx).T_sum_seconds = sumTime;
    if denominator > 0
        timing.case(idx).K_break_even = ceil(timing.T_library_wrapper_seconds / denominator);
    else
        timing.case(idx).K_break_even = Inf;
    end
end
end

function total = sumIgnoringNaN(values)
values = values(~isnan(values));
if isempty(values); total = NaN; else; total = sum(values); end
end

function writeMetricCsv(path, results)
names = string({results.name}).';
complexL2 = arrayfun(@(x) x.metrics.complex_relative_l2, results).';
amplitudeL2 = arrayfun(@(x) x.metrics.amplitude_relative_l2, results).';
phaseMaeDeg = arrayfun(@(x) x.metrics.phase_mae_deg_above_minus20db, results).';
pTargetRelError = arrayfun(@(x) x.metrics.p_target_relative_error, results).';
pPeakRelError = arrayfun(@(x) x.metrics.p_peak_relative_error, results).';
focusErrorMm = arrayfun(@(x) x.metrics.focus_error_mm, results).';
passStrict = arrayfun(@(x) x.metrics.pass_all_strict, results).';
tableOut = table(names, complexL2, amplitudeL2, phaseMaeDeg, pTargetRelError, ...
    pPeakRelError, focusErrorMm, passStrict);
writetable(tableOut, path);
end

function out = ternary(condition, a, b)
if condition; out = a; else; out = b; end
end
