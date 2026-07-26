function saveField(path, field, compression)
%SAVEFIELD Persist real/imaginary parts in Pa without long-term time series.

field_re_large = real(field.large); %#ok<NASGU>
field_im_large = imag(field.large); %#ok<NASGU>
field_re_focus = real(field.focus); %#ok<NASGU>
field_im_focus = imag(field.focus); %#ok<NASGU>
large_axes_mm = field.large_axes_mm; %#ok<NASGU>
focus_axes_mm = field.focus_axes_mm; %#ok<NASGU>
save(path, 'field_re_large', 'field_im_large', 'field_re_focus', ...
    'field_im_focus', 'large_axes_mm', 'focus_axes_mm', '-v7.3');

% MATLAB does not expose a per-save compression level. Keep this argument
% in metadata/API so changing the storage backend later is non-breaking.
if compression < 0 %#ok<UNRCH>
    error('Invalid compression setting.');
end
end
