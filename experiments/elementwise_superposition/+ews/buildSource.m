function [source, sourceMeta] = buildSource(cfg, grid, geometryIndices, amplitudeMultipliers, phasesRad)
%BUILDSOURCE Build off-grid circular pistons with one waveform per element.

geometryIndices = double(geometryIndices(:).');
amplitudeMultipliers = double(amplitudeMultipliers(:).');
phasesRad = double(phasesRad(:).');
if numel(geometryIndices) ~= numel(amplitudeMultipliers) || ...
        numel(geometryIndices) ~= numel(phasesRad)
    error('ews:SourceSize', 'Geometry, amplitude, and phase vectors must have equal length.');
end

karray = kWaveArray( ...
    'BLITolerance', cfg.array.bli_tolerance, ...
    'UpsamplingRate', cfg.array.upsampling_rate, ...
    'SinglePrecision', true);

shiftM = cfg.grid.world_origin_shift_mm * 1e-3;
targetK = cfg.array.target_world_mm * 1e-3 - shiftM;
for idx = 1:numel(geometryIndices)
    elementNo = geometryIndices(idx);
    positionK = cfg.array.centres_world_mm(elementNo, :) * 1e-3 - shiftM;
    karray.addDiscElement(positionK, cfg.array.element_diameter_mm * 1e-3, targetK);
end

driveAmp = cfg.acoustic.source_peak_pressure_pa .* amplitudeMultipliers;
signals = createCWSignals(grid.kgrid.t_array, cfg.acoustic.frequency_hz, ...
    driveAmp(:), phasesRad(:), cfg.time.ramp_periods);
if isvector(signals) && numel(geometryIndices) > 1
    signals = reshape(signals, numel(geometryIndices), []);
end

source.p_mask = karray.getArrayBinaryMask(grid.kgrid);
source.p = karray.getDistributedSourceSignal(grid.kgrid, signals);
source.p_mode = cfg.acoustic.source_mode;

sourceMeta.geometry_indices = geometryIndices;
sourceMeta.amplitude_multipliers = amplitudeMultipliers;
sourceMeta.phases_rad = phasesRad;
sourceMeta.centres_world_mm = cfg.array.centres_world_mm(geometryIndices, :);
sourceMeta.target_world_mm = cfg.array.target_world_mm;
sourceMeta.diameter_mm = cfg.array.element_diameter_mm;
sourceMeta.source_mask_points = nnz(source.p_mask);
end
