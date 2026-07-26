function axes = worldAxes(cfg)
%WORLDAXES Explicit physical coordinates corresponding to MATLAB array dimensions.

sz = round(cfg.grid.coverage_mm ./ cfg.grid.dx_mm);
dx = cfg.grid.dx_mm;
shift = cfg.grid.world_origin_shift_mm;
axes.x_mm = ((-floor(sz(1)/2)):(ceil(sz(1)/2)-1)) * dx + shift(1);
axes.y_mm = ((-floor(sz(2)/2)):(ceil(sz(2)/2)-1)) * dx + shift(2);
axes.z_mm = ((-floor(sz(3)/2)):(ceil(sz(3)/2)-1)) * dx + shift(3);
end
