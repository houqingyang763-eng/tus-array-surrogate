function result = run_elementwise_experiment(mode, varargin)
%RUN_ELEMENTWISE_EXPERIMENT Four-element large-region superposition study.
%
%   run_elementwise_experiment('water_smoke')
%   run_elementwise_experiment('benchmark_skull')
%   run_elementwise_experiment('mida')
%
% Optional name/value pairs:
%   'RunDir'          Existing/new run directory. Enables explicit resume.
%   'Overwrite'       Re-run cases even when their field files exist.
%   'DryRun'          Prepare geometry/medium and write metadata, but do not solve.
%   'KWavePath'       Path to the k-Wave toolbox.
%   'MidaConfigPath'  Path to a MIDA JSON configuration.

% The formal experiments always call kspaceFirstOrder3DG. There is no CPU
% fallback because an unnoticed fallback would invalidate the timing study.

arguments
    mode (1, 1) string {mustBeMember(mode, ["water_smoke", "benchmark_skull", "mida"])}
end
arguments (Repeating)
    varargin
end

experiment_root = fileparts(mfilename('fullpath'));
addpath(experiment_root);

cfg = ews.defaultConfig(mode, experiment_root);
cfg = ews.applyOverrides(cfg, varargin{:});
ews.setupPaths(cfg);

switch mode
    case "water_smoke"
        result = ews.runWaterSmoke(cfg);
    otherwise
        result = ews.runFormalExperiment(cfg);
end
end
