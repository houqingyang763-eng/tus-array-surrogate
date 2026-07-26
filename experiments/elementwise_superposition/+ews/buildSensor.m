function sensorDef = buildSensor(cfg, grid)
%BUILDSENSOR Sample the large region at 2 mm plus a 1 mm focal cube.

sz = [grid.kgrid.Nx, grid.kgrid.Ny, grid.kgrid.Nz];
stride = round(cfg.grid.output_spacing_mm / cfg.grid.dx_mm);
largeSubs = {1:stride:sz(1), 1:stride:sz(2), 1:stride:sz(3)};

axes = grid.world_axes_mm;
target = cfg.array.target_world_mm;
focusSubs = { ...
    rangeAround(axes.x_mm, target(1), cfg.grid.focus_half_width_mm), ...
    rangeAround(axes.y_mm, target(2), cfg.grid.focus_half_width_mm), ...
    rangeAround(axes.z_mm, target(3), cfg.grid.focus_half_width_mm)};

mask = false(sz);
mask(largeSubs{1}, largeSubs{2}, largeSubs{3}) = true;
mask(focusSubs{1}, focusSubs{2}, focusSubs{3}) = true;

sensorDef.sensor.mask = mask;
sensorDef.sensor.record = {'p'};
sensorDef.sensor.record_start_index = grid.Nt - cfg.time.record_periods * grid.ppp + 1;
sensorDef.large_subs = largeSubs;
sensorDef.focus_subs = focusSubs;
sensorDef.large_axes_mm.x = axes.x_mm(largeSubs{1});
sensorDef.large_axes_mm.y = axes.y_mm(largeSubs{2});
sensorDef.large_axes_mm.z = axes.z_mm(largeSubs{3});
sensorDef.focus_axes_mm.x = axes.x_mm(focusSubs{1});
sensorDef.focus_axes_mm.y = axes.y_mm(focusSubs{2});
sensorDef.focus_axes_mm.z = axes.z_mm(focusSubs{3});
sensorDef.sensor_points = nnz(mask);
end

function indices = rangeAround(axisMm, centreMm, halfWidthMm)
indices = find(axisMm >= centreMm - halfWidthMm & axisMm <= centreMm + halfWidthMm);
if isempty(indices)
    error('ews:FocusOutsideGrid', 'Focus evaluation cube is outside the grid.');
end
end
