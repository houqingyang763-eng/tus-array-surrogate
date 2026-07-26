function setupPaths(cfg)
%SETUPPATHS Add dependencies and fail early when the GPU path is incomplete.

if ~isfolder(cfg.paths.kwave)
    error('ews:MissingKWave', 'k-Wave was not found at %s.', cfg.paths.kwave);
end
addpath(cfg.paths.kwave);

cudaBinary = fullfile(cfg.paths.kwave_binary_dir, 'kspaceFirstOrder-CUDA.exe');
if ~isfile(cudaBinary)
    error('ews:MissingCudaBinary', 'CUDA solver was not found at %s.', cudaBinary);
end

if strcmp(cfg.mode, 'benchmark_skull')
    if ~isfolder(cfg.paths.benchmark_repo)
        error('ews:MissingBenchmark', ...
            ['Clone https://github.com/ucl-bug/transcranial-ultrasound-benchmarks ' ...
             'to %s.'], cfg.paths.benchmark_repo);
    end
    if ~isfolder(cfg.paths.iso2mesh)
        error('ews:MissingIso2Mesh', ...
            'Clone https://github.com/fangq/iso2mesh to %s.', cfg.paths.iso2mesh);
    end
    addpath(genpath(cfg.paths.iso2mesh));
end

if ~isfolder(cfg.paths.cache_dir)
    mkdir(cfg.paths.cache_dir);
end
if ~isfolder(cfg.run.dir)
    mkdir(cfg.run.dir);
end
end
