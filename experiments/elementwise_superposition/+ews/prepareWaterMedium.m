function mediumData = prepareWaterMedium(cfg)
%PREPAREWATERMEDIUM Uniform water medium for the GPU smoke test.

sz = round(cfg.grid.coverage_mm ./ cfg.grid.dx_mm);
water = cfg.material.water;
mediumData.medium.sound_speed = single(water.sound_speed_m_s);
mediumData.medium.density = single(water.density_kg_m3);
mediumData.medium.alpha_coeff = single(0);
mediumData.medium.alpha_power = cfg.acoustic.alpha_power;
mediumData.brain_mask = true(sz);
mediumData.skull_mask = false(sz);
mediumData.description = 'Uniform lossless water';
end
