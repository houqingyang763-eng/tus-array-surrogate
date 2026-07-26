function tests = test_pure_functions
tests = functiontests(localfunctions);
end

function setupOnce(testCase)
root = fileparts(fileparts(mfilename('fullpath')));
addpath(root);
testCase.TestData.root = root;
end

function testSuperposition(testCase)
template.large = complex(single(ones(4, 3, 2)), single(zeros(4, 3, 2)));
template.focus = template.large;
template.large_axes_mm = struct('x', 1:4, 'y', 1:3, 'z', 1:2);
template.focus_axes_mm = template.large_axes_mm;
library = {template, template, template, template};
field = ews.superposeFields(library, [1, 0.8, 0.6, 1], [0, pi/2, pi, -pi/2]);
expected = 1 + 0.8i - 0.6 - 1i;
verifyLessThan(testCase, max(abs(field.large(:) - expected)), 1e-6);
end

function testWorldAxes(testCase)
cfg = ews.defaultConfig("benchmark_skull", testCase.TestData.root);
axes = ews.worldAxes(cfg);
verifyEqual(testCase, axes.x_mm([1, end]), [0, 199]);
verifyEqual(testCase, axes.y_mm([1, end]), [-80, 79]);
verifyEqual(testCase, axes.z_mm([1, end]), [-80, 79]);
end

function testMetricsIdentity(testCase)
field.large = complex(single(rand(10, 8, 6)), single(rand(10, 8, 6)));
field.focus = field.large;
field.large_axes_mm = struct('x', 0:2:18, 'y', -8:2:6, 'z', -6:2:4);
field.focus_axes_mm = field.large_axes_mm;
mask = true(size(field.large));
metrics = ews.computeMetrics(field, field, mask, [8, 0, 0], 2);
verifyEqual(testCase, metrics.complex_relative_l2, 0);
verifyEqual(testCase, metrics.amplitude_relative_l2, 0);
verifyEqual(testCase, metrics.phase_mae_deg_above_minus20db, 0);
verifyTrue(testCase, metrics.pass_all_strict);
end
