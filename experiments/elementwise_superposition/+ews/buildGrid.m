function grid = buildGrid(cfg, mediumData)
%BUILDGRID Construct an integer-points-per-period k-Wave grid and time axis.

sz = round(cfg.grid.coverage_mm ./ cfg.grid.dx_mm);
dx = cfg.grid.dx_mm * 1e-3;
grid.kgrid = kWaveGrid(sz(1), dx, sz(2), dx, sz(3), dx);

cValues = double(mediumData.medium.sound_speed(:));
cMin = min(cValues);
cMax = max(cValues);
f0 = cfg.acoustic.frequency_hz;
ppp = ceil(cMax / (cfg.grid.cfl_limit * dx * f0));
dt = 1 / (ppp * f0);

worldAxes = ews.worldAxes(cfg);
corners = allCorners(worldAxes);
maxDistanceM = 0;
for idx = 1:size(cfg.array.centres_world_mm, 1)
    delta = corners - cfg.array.centres_world_mm(idx, :);
    maxDistanceM = max(maxDistanceM, max(vecnorm(delta, 2, 2)) * 1e-3);
end
travelPeriods = ceil((maxDistanceM / cMin) * f0);
totalPeriods = travelPeriods + cfg.time.ramp_periods + ...
    cfg.time.extra_settle_periods + cfg.time.record_periods;
Nt = totalPeriods * ppp;
grid.kgrid.setTime(Nt, dt);

grid.ppp = ppp;
grid.dt_s = dt;
grid.Nt = Nt;
grid.total_periods = totalPeriods;
grid.travel_periods = travelPeriods;
grid.cfl_max = cMax * dt / dx;
grid.world_axes_mm = worldAxes;
grid.kgrid_origin_shift_mm = cfg.grid.world_origin_shift_mm;
end

function corners = allCorners(axes)
x = axes.x_mm([1, end]);
y = axes.y_mm([1, end]);
z = axes.z_mm([1, end]);
[X, Y, Z] = ndgrid(x, y, z);
corners = [X(:), Y(:), Z(:)];
end
