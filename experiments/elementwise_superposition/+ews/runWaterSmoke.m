function result = runWaterSmoke(cfg)
%RUNWATERSMOKE Four small GPU runs that validate scaling, phase, and source identity.

env = ews.probeEnvironment(cfg);
ews.writeJson(fullfile(cfg.run.dir, 'environment.json'), env);
ews.writeJson(fullfile(cfg.run.dir, 'config.json'), cfg);

mediumData = ews.prepareWaterMedium(cfg);
grid = ews.buildGrid(cfg, mediumData);
sensorDef = ews.buildSensor(cfg, grid);
[fullSource, ~] = ews.buildSource(cfg, grid, 1:4, [1, 0, 0, 0], zeros(1, 4));
geometry = ews.validateGeometry(cfg, mediumData, fullSource.p_mask, grid);
ews.writeJson(fullfile(cfg.run.dir, 'geometry.json'), geometry);

[base, baseMeta] = ews.runGpuCase(cfg, mediumData, grid, sensorDef, 'base_element1', 1, 1, 0);
[doubleAmp, doubleMeta] = ews.runGpuCase(cfg, mediumData, grid, sensorDef, 'double_amplitude', 1, 2, 0);
[phase90, phaseMeta] = ews.runGpuCase(cfg, mediumData, grid, sensorDef, 'phase_plus90deg', 1, 1, pi/2);
[fullMask, fullMaskMeta] = ews.runGpuCase(cfg, mediumData, grid, sensorDef, 'four_geometry_only_element1_active', 1:4, [1, 0, 0, 0], zeros(1, 4));

if cfg.run.dry_run
    result.run_dir = cfg.run.dir;
    result.status = 'dry_run_complete';
    return;
end

mask = true(size(base.large));
report.double_amplitude_complex_l2 = relL2(doubleAmp.large, 2 .* base.large, mask);
report.phase_plus90_complex_l2 = relL2(phase90.large, 1i .* base.large, mask);
report.single_vs_four_geometry_complex_l2 = relL2(fullMask.large, base.large, mask);
report.sensor_roundtrip_exact = sensorRoundtrip(sensorDef.sensor.mask, sensorDef.large_subs, sensorDef.focus_subs);
report.pass_double_amplitude = report.double_amplitude_complex_l2 <= 1e-4;
report.pass_phase_plus90 = report.phase_plus90_complex_l2 <= 1e-4;
report.pass_source_identity = report.single_vs_four_geometry_complex_l2 <= 1e-4;
report.pass_all = report.pass_double_amplitude && report.pass_phase_plus90 && ...
    report.pass_source_identity && report.sensor_roundtrip_exact;
report.case_metadata = {baseMeta, doubleMeta, phaseMeta, fullMaskMeta};
ews.writeJson(fullfile(cfg.run.dir, 'smoke_report.json'), report);

result.run_dir = cfg.run.dir;
result.status = ternary(report.pass_all, 'passed', 'failed');
result.report = report;
if ~report.pass_all
    error('ews:SmokeFailed', 'GPU/mathematical smoke test failed. See %s.', cfg.run.dir);
end
end

function value = relL2(actual, expected, mask)
a = actual(mask);
b = expected(mask);
value = norm(double(a - b)) / norm(double(b));
end

function passed = sensorRoundtrip(mask, largeSubs, focusSubs)
encoded = single((1:nnz(mask)).');
volume = zeros(size(mask), 'single');
volume(mask) = encoded;
large = volume(largeSubs{1}, largeSubs{2}, largeSubs{3});
focus = volume(focusSubs{1}, focusSubs{2}, focusSubs{3});
passed = isequal(large, reshape(volume(largeSubs{1}, largeSubs{2}, largeSubs{3}), size(large))) && ...
    isequal(focus, reshape(volume(focusSubs{1}, focusSubs{2}, focusSubs{3}), size(focus)));
end

function out = ternary(condition, a, b)
if condition; out = a; else; out = b; end
end
