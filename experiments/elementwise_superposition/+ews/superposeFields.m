function field = superposeFields(library, amplitudes, phases)
%SUPERPOSEFIELDS Coherently combine cached single-element complex fields.

if numel(library) ~= numel(amplitudes) || numel(library) ~= numel(phases)
    error('ews:SuperpositionSize', 'Library and drive vectors must have equal length.');
end
weights = double(amplitudes(:)) .* exp(1i .* double(phases(:)));

start = tic;
field = library{1};
field.large = complex(zeros(size(library{1}.large), 'single'));
field.focus = complex(zeros(size(library{1}.focus), 'single'));
for idx = 1:numel(library)
    field.large = field.large + single(weights(idx)) .* library{idx}.large;
    field.focus = field.focus + single(weights(idx)) .* library{idx}.focus;
end
field.sum_seconds = toc(start);
end
