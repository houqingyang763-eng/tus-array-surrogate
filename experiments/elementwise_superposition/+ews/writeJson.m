function writeJson(path, value)
%WRITEJSON Write human-readable JSON using UTF-8.

text = jsonencode(value, 'PrettyPrint', true);
fid = fopen(path, 'w', 'n', 'UTF-8');
if fid < 0
    error('ews:FileOpen', 'Could not open %s for writing.', path);
end
cleanup = onCleanup(@() fclose(fid));
fwrite(fid, text, 'char');
end
