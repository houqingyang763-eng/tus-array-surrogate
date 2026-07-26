function env = probeEnvironment(cfg)
%PROBEENVIRONMENT Collect reproducibility and GPU metadata.

env.collected_at = char(datetime('now', 'TimeZone', 'local', ...
    'Format', 'yyyy-MM-dd''T''HH:mm:ssXXX'));
env.matlab_version = version;
env.matlab_release = version('-release');
env.computer = computer;
env.kwave_path = which('kspaceFirstOrder3DG');
env.kwave_array_path = which('kWaveArray');
env.cuda_binary = fullfile(cfg.paths.kwave_binary_dir, 'kspaceFirstOrder-CUDA.exe');

[status, text] = system('nvidia-smi --query-gpu=name,driver_version,memory.total,compute_cap --format=csv,noheader,nounits');
env.nvidia_smi_status = status;
env.nvidia_smi = strtrim(text);

[status, text] = system(sprintf('"%s" --version', env.cuda_binary));
env.cuda_binary_version_status = status;
env.cuda_binary_version = strtrim(text);

env.kwave_contents_timestamp = '';
contentsFile = fullfile(cfg.paths.kwave, 'Contents.m');
if isfile(contentsFile)
    info = dir(contentsFile);
    env.kwave_contents_timestamp = char(datetime(info.datenum, 'ConvertFrom', 'datenum'));
end
end
