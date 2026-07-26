function report = validateGeometry(cfg, mediumData, sourceMask, grid)
%VALIDATEGEOMETRY Check source/skull/target placement before a long solve.

axes = grid.world_axes_mm;
targetIndex = nearestSub(axes, cfg.array.target_world_mm);
report.target_index = targetIndex;
report.target_in_brain = logical(mediumData.brain_mask(targetIndex(1), targetIndex(2), targetIndex(3)));
report.source_overlaps_skull_points = nnz(sourceMask & mediumData.skull_mask);

report.element = repmat(struct('centre_world_mm', [], 'ray_skull_points', 0, ...
    'normal_dot_target_direction', 0), size(cfg.array.centres_world_mm, 1), 1);
for elementNo = 1:size(cfg.array.centres_world_mm, 1)
    centre = cfg.array.centres_world_mm(elementNo, :);
    direction = cfg.array.target_world_mm - centre;
    direction = direction ./ norm(direction);
    samples = centre + linspace(0, 1, 400).' .* (cfg.array.target_world_mm - centre);
    subs = nearestSubs(axes, samples);
    lin = sub2ind(size(mediumData.skull_mask), subs(:, 1), subs(:, 2), subs(:, 3));
    report.element(elementNo).centre_world_mm = centre;
    report.element(elementNo).ray_skull_points = nnz(mediumData.skull_mask(lin));
    report.element(elementNo).normal_dot_target_direction = dot(direction, direction);
end

if ~strcmp(cfg.mode, 'water_smoke')
    if ~report.target_in_brain
        error('ews:TargetNotBrain', 'The configured target is not inside the brain mask.');
    end
    if report.source_overlaps_skull_points > 0
        error('ews:SourceInSkull', 'The source mask overlaps %d skull points.', report.source_overlaps_skull_points);
    end
    if any([report.element.ray_skull_points] == 0)
        error('ews:RayMissesSkull', 'At least one element-to-target ray does not cross the skull.');
    end
end
end

function sub = nearestSub(axes, point)
subs = nearestSubs(axes, point);
sub = subs(1, :);
end

function subs = nearestSubs(axes, points)
subs = zeros(size(points));
for dim = 1:3
    names = {'x_mm', 'y_mm', 'z_mm'};
    axisValues = axes.(names{dim});
    subs(:, dim) = round((points(:, dim) - axisValues(1)) / (axisValues(2) - axisValues(1))) + 1;
    subs(:, dim) = min(max(subs(:, dim), 1), numel(axisValues));
end
end
