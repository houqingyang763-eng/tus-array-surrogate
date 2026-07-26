function cfg = defaultConfig(mode, experimentRoot)
%DEFAULTCONFIG Return the versioned experiment configuration.

repoRoot = fileparts(fileparts(experimentRoot));
timestamp = char(datetime('now', 'Format', 'yyyyMMdd_HHmmss'));

cfg.schema_version = 1;
cfg.mode = char(mode);
cfg.paths.repo_root = repoRoot;
cfg.paths.experiment_root = experimentRoot;
cfg.paths.kwave = 'D:\k-wave\k-Wave';
cfg.paths.kwave_binary_dir = fullfile(cfg.paths.kwave, 'binaries');
cfg.paths.benchmark_repo = fullfile(repoRoot, 'external', 'transcranial-ultrasound-benchmarks');
cfg.paths.iso2mesh = fullfile(repoRoot, 'external', 'iso2mesh');
cfg.paths.cache_dir = fullfile(repoRoot, 'data', 'elementwise_superposition');
cfg.paths.mida_config = fullfile(experimentRoot, 'config', 'mida_config.json');
cfg.run.dir = fullfile(repoRoot, 'runs', 'elementwise_superposition', char(mode), timestamp);
cfg.run.overwrite = false;
cfg.run.dry_run = false;

cfg.grid.coverage_mm = [200, 160, 160];
cfg.grid.dx_mm = 1.0;
cfg.grid.output_spacing_mm = 2.0;
cfg.grid.focus_half_width_mm = 20.0;
cfg.grid.pml_size = 10;
cfg.grid.cfl_limit = 0.20;
% World axes are x = 0..199 mm, y = -80..79 mm, z = -80..79 mm.
cfg.grid.world_origin_shift_mm = [100, 0, 0];

cfg.acoustic.frequency_hz = 500e3;
cfg.acoustic.source_peak_pressure_pa = 100e3;
cfg.acoustic.alpha_power = 2;
cfg.acoustic.source_mode = 'additive';

cfg.time.ramp_periods = 4;
cfg.time.record_periods = 4;
% Phase-rotated reuse is sensitive to residual start-up transients. In the
% benchmark skull, 48 periods still left ~1e-3 error, while 400 periods
% reduced a 0/90-degree single-element rotation test to 7.2e-6.
cfg.time.extra_settle_periods = 400;

cfg.array.element_diameter_mm = 10;
cfg.array.pitch_mm = 12;
cfg.array.centres_world_mm = [ ...
    1, -6, -6; ...
    1, -6,  6; ...
    1,  6, -6; ...
    1,  6,  6];
cfg.array.target_world_mm = [64, 0, 0];
cfg.array.bli_tolerance = 0.05;
cfg.array.upsampling_rate = 10;

% Aubry et al., JASA 2022, Table I. alpha_at_500khz is dB/cm.
cfg.material.water = material(1500, 1000, 0.0);
cfg.material.skin = material(1610, 1090, 0.2);
cfg.material.brain = material(1560, 1040, 0.3);
cfg.material.cortical_bone = material(2800, 1850, 4.0);
cfg.material.trabecular_bone = material(2300, 1700, 8.0);

cfg.output.compression = 4;
cfg.output.save_monolithic_fields = true;
cfg.output.make_plots = true;

if mode == "water_smoke"
    cfg.grid.coverage_mm = [64, 48, 48];
    cfg.grid.output_spacing_mm = 1.0;
    cfg.grid.focus_half_width_mm = 12.0;
    cfg.grid.world_origin_shift_mm = [32, 0, 0];
    cfg.array.centres_world_mm(:, 1) = 2;
    cfg.array.target_world_mm = [32, 0, 0];
    cfg.time.extra_settle_periods = 24;
    cfg.output.make_plots = false;
end
end

function out = material(c, rho, alphaAt500kHz)
out.sound_speed_m_s = c;
out.density_kg_m3 = rho;
out.alpha_db_cm_at_500khz = alphaAt500kHz;
end
