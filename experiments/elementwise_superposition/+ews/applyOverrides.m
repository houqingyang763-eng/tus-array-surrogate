function cfg = applyOverrides(cfg, varargin)
%APPLYOVERRIDES Apply the deliberately small public override surface.

if mod(numel(varargin), 2) ~= 0
    error('ews:InvalidArguments', 'Overrides must be name/value pairs.');
end

for idx = 1:2:numel(varargin)
    name = lower(string(varargin{idx}));
    value = varargin{idx + 1};
    switch name
        case "rundir"
            cfg.run.dir = char(value);
        case "overwrite"
            cfg.run.overwrite = logical(value);
        case "dryrun"
            cfg.run.dry_run = logical(value);
        case "kwavepath"
            cfg.paths.kwave = char(value);
            cfg.paths.kwave_binary_dir = fullfile(cfg.paths.kwave, 'binaries');
        case "midaconfigpath"
            cfg.paths.mida_config = char(value);
        case "gridspacingmm"
            cfg.grid.dx_mm = double(value);
        case "extrasettleperiods"
            cfg.time.extra_settle_periods = double(value);
        otherwise
            error('ews:UnknownOverride', 'Unknown override: %s', name);
    end
end

ratio = cfg.grid.output_spacing_mm / cfg.grid.dx_mm;
if abs(ratio - round(ratio)) > 1e-10
    error('ews:InvalidGrid', 'Output spacing must be an integer multiple of dx.');
end
end
