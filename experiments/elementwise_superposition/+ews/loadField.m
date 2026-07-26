function field = loadField(path)
%LOADFIELD Reconstruct complex pressure from persisted Re/Im arrays.

data = load(path);
field.large = complex(data.field_re_large, data.field_im_large);
field.focus = complex(data.field_re_focus, data.field_im_focus);
field.large_axes_mm = data.large_axes_mm;
field.focus_axes_mm = data.focus_axes_mm;
end
