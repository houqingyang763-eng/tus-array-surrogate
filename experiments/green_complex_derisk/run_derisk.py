"""Run the gated V1/V2/V3 Green complex-response derisk study."""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import time
from contextlib import nullcontext
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import scipy.io
import torch

from analytic_data import finite_disc_pressure, make_source_split, sample_queries
from green_model import GreenComplexNet, GreenModelConfig, parameter_count
from metrics import complex_metrics


EXPERIMENT_DIR = Path(__file__).resolve().parent
REPO_ROOT = EXPERIMENT_DIR.parents[1]
DEFAULT_RUN_ROOT = REPO_ROOT / "runs" / "green_complex_derisk"
CHUNKS = (8192, 32768, 131072)
FULL_VOLUME_QUERIES = 160 ** 3


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")


def autocast_context(device: torch.device):
    if device.type == "cuda":
        return torch.autocast(device_type="cuda", dtype=torch.bfloat16)
    return nullcontext()


def sync(device: torch.device) -> None:
    if device.type == "cuda":
        torch.cuda.synchronize(device)


def random_geometry(count: int, device: torch.device) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    centre = torch.empty(count, 3, device=device)
    centre[:, 0] = 1.0
    centre[:, 1:].uniform_(-25.0, 25.0)
    focus = torch.empty(count, 3, device=device)
    focus[:, 0].uniform_(60.0, 120.0)
    focus[:, 1:].uniform_(-25.0, 25.0)
    normal = torch.nn.functional.normalize(focus - centre, dim=-1)
    query = torch.empty(count, 3, device=device)
    query[:, 0].uniform_(10.0, 199.0)
    query[:, 1:].uniform_(-79.0, 79.0)
    return centre, normal, query


def run_probe(run_dir: Path, device: torch.device) -> dict[str, Any]:
    model = GreenComplexNet().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=3.0e-4)
    results: list[dict[str, Any]] = []

    for chunk in CHUNKS:
        row: dict[str, Any] = {"chunk": chunk}
        try:
            centre, normal, query = random_geometry(chunk, device)
            # V1 inference is one element queried at many points: cache one source
            # embedding and broadcast it, rather than encoding a source per query.
            centre = centre[:1].expand(chunk, -1)
            normal = normal[:1].expand(chunk, -1)
            with torch.no_grad(), autocast_context(device):
                source_embedding = model.encode_source(centre[:1], normal[:1]).expand(chunk, -1)
                for _ in range(3):
                    model.forward_from_embedding(source_embedding, centre, normal, query)
                sync(device)
                if device.type == "cuda":
                    torch.cuda.reset_peak_memory_stats(device)
                start = time.perf_counter()
                repeats = max(5, math.ceil(524288 / chunk))
                for _ in range(repeats):
                    model.forward_from_embedding(source_embedding, centre, normal, query)
                sync(device)
                elapsed = time.perf_counter() - start
            row["inference_queries_per_second"] = chunk * repeats / elapsed
            row["inference_peak_mib"] = (
                torch.cuda.max_memory_allocated(device) / (1024 ** 2) if device.type == "cuda" else None
            )

            optimizer.zero_grad(set_to_none=True)
            target = torch.randn(chunk, 2, device=device) * 100_000.0
            if device.type == "cuda":
                torch.cuda.reset_peak_memory_stats(device)
            with autocast_context(device):
                prediction, _ = model(centre, normal, query)
                loss = torch.mean((prediction.float() - target.float()) ** 2) / torch.mean(target.float() ** 2)
            loss.backward()
            optimizer.step()
            sync(device)
            row["training_peak_mib"] = (
                torch.cuda.max_memory_allocated(device) / (1024 ** 2) if device.type == "cuda" else None
            )
            row["training_loss"] = float(loss.item())
            row["oom"] = False
            del centre, normal, query, source_embedding, target, prediction, loss
            if device.type == "cuda":
                torch.cuda.empty_cache()
        except torch.cuda.OutOfMemoryError:
            row["oom"] = True
            optimizer.zero_grad(set_to_none=True)
            if device.type == "cuda":
                torch.cuda.empty_cache()
        results.append(row)

    usable = [
        row for row in results
        if not row.get("oom")
        and (row.get("inference_peak_mib") or 0.0) < 4096.0
        and (row.get("training_peak_mib") or 0.0) < 6656.0
    ]
    fastest = max(usable, key=lambda row: row["inference_queries_per_second"]) if usable else None
    if fastest:
        qps = fastest["inference_queries_per_second"]
        one_element_seconds = FULL_VOLUME_QUERIES / qps
        array_32_seconds = one_element_seconds * 32
        array_128_seconds = one_element_seconds * 128
    else:
        one_element_seconds = array_32_seconds = array_128_seconds = float("inf")

    if array_128_seconds < 60.0:
        speed_status = "pass"
    elif array_128_seconds <= 180.0:
        speed_status = "conditional_pass"
    else:
        speed_status = "fail"
    gate_pass = bool(usable) and array_128_seconds <= 180.0
    report = {
        "gate": "V1_resource",
        "status": "pass" if gate_pass else "fail",
        "speed_status": speed_status,
        "device": torch.cuda.get_device_name(device) if device.type == "cuda" else "cpu",
        "torch_version": torch.__version__,
        "bf16_supported": bool(torch.cuda.is_bf16_supported()) if device.type == "cuda" else False,
        "parameter_count": parameter_count(model),
        "model_config": vars(model.config),
        "chunks": results,
        "selected_chunk": fastest["chunk"] if fastest else None,
        "estimated_seconds": {
            "one_element_160_cubed": one_element_seconds,
            "32_elements_160_cubed": array_32_seconds,
            "128_elements_160_cubed": array_128_seconds,
        },
        "scope_note": "Compute-only coordinate batches; excludes disk I/O and skull-volume label generation.",
    }
    write_json(run_dir / "v1_probe.json", report)
    return report


def train_analytic_seed(seed: int, device: torch.device) -> dict[str, Any]:
    torch.manual_seed(seed)
    if device.type == "cuda":
        torch.cuda.manual_seed_all(seed)
    split = make_source_split(device)
    model = GreenComplexNet().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=3.0e-4)
    generator = torch.Generator(device=device).manual_seed(seed + 1000)
    batch_size = 8192
    start = time.perf_counter()
    final_loss = float("nan")

    model.train()
    for _ in range(600):
        source_index = torch.randint(0, 64, (batch_size,), generator=generator, device=device)
        centre = split["train_centres"][source_index]
        normal = split["train_normals"][source_index]
        query = sample_queries(centre, normal, generator)
        with torch.no_grad():
            target = finite_disc_pressure(centre, normal, query)
        optimizer.zero_grad(set_to_none=True)
        with autocast_context(device):
            prediction, _ = model(centre, normal, query)
            numerator = torch.mean(torch.sum((prediction.float() - target.float()) ** 2, dim=-1))
            denominator = torch.mean(torch.sum(target.float() ** 2, dim=-1)).clamp_min(1.0e-12)
            loss = numerator / denominator
        loss.backward()
        optimizer.step()
        final_loss = float(loss.item())

    model.eval()
    predictions: list[torch.Tensor] = []
    targets: list[torch.Tensor] = []
    eval_generator = torch.Generator(device=device).manual_seed(99173)
    with torch.no_grad():
        for source_no in range(16):
            centre = split["test_centres"][source_no:source_no + 1].expand(4096, -1)
            normal = split["test_normals"][source_no:source_no + 1].expand(4096, -1)
            query = sample_queries(centre, normal, eval_generator)
            target = finite_disc_pressure(centre, normal, query)
            with autocast_context(device):
                prediction, _ = model(centre, normal, query)
            predictions.append(prediction.float().cpu())
            targets.append(target.float().cpu())
    metrics = complex_metrics(torch.cat(predictions), torch.cat(targets))
    passed = metrics["complex_relative_l2"] < 0.02 and metrics["phase_mae_deg_above_minus20db"] < 5.0
    return {
        "seed": seed,
        "steps": 600,
        "batch_size": batch_size,
        "final_training_loss": final_loss,
        "training_and_eval_seconds": time.perf_counter() - start,
        "metrics": metrics,
        "passed": passed,
        "model_state": model.state_dict(),
    }


def run_analytic(run_dir: Path, device: torch.device) -> dict[str, Any]:
    seed_results = [train_analytic_seed(seed, device) for seed in (0, 1)]
    for result in seed_results:
        torch.save(result.pop("model_state"), run_dir / f"v2_model_seed_{result['seed']}.pt")
    gate_pass = all(result["passed"] for result in seed_results)
    report = {
        "gate": "V2_analytic_finite_aperture",
        "status": "pass" if gate_pass else "fail",
        "teacher": {
            "frequency_hz": 500_000.0,
            "sound_speed_m_s": 1500.0,
            "element_diameter_mm": 10.0,
            "quadrature_points": 32,
            "train_sources": 64,
            "held_out_sources": 16,
        },
        "acceptance": {"complex_relative_l2_max": 0.02, "strong_phase_mae_deg_max": 5.0},
        "seeds": seed_results,
    }
    write_json(run_dir / "v2_analytic.json", report)
    return report


def generate_skull_labels(label_dir: Path) -> None:
    label_dir.mkdir(parents=True, exist_ok=True)
    if len(list(label_dir.glob("source_*.mat"))) >= 12:
        return
    matlab_call = (
        f"addpath('{EXPERIMENT_DIR.as_posix()}'); "
        f"run_green_skull_labels('{label_dir.as_posix()}')"
    )
    subprocess.run(["matlab", "-batch", matlab_call], cwd=REPO_ROOT, check=True)


def load_skull_labels(label_dir: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(label_dir.glob("source_*.mat")):
        value = scipy.io.loadmat(path, squeeze_me=True)
        field = np.stack((value["field_re_large"], value["field_im_large"]), axis=-1).astype(np.float32)
        records.append({
            "path": str(path),
            "field": field,
            "centre": np.asarray(value["source_centre_mm"], dtype=np.float32).reshape(3),
            "normal": np.asarray(value["source_normal"], dtype=np.float32).reshape(3),
            "axes": tuple(np.asarray(value[key], dtype=np.float32).reshape(-1) for key in ("x_mm", "y_mm", "z_mm")),
        })
    if len(records) != 12:
        raise RuntimeError(f"Expected 12 skull labels, found {len(records)} in {label_dir}")
    return records


def field_queries(record: dict[str, Any]) -> np.ndarray:
    x, y, z = record["axes"]
    query = np.stack(np.meshgrid(x, y, z, indexing="ij"), axis=-1).reshape(-1, 3)
    if query.shape[0] != record["field"].reshape(-1, 2).shape[0]:
        raise RuntimeError("Coordinate and field shapes do not match")
    return query.astype(np.float32)


def predict_record(
    model: GreenComplexNet, record: dict[str, Any], device: torch.device, chunk: int = 32768
) -> np.ndarray:
    queries = field_queries(record)
    centre_one = torch.from_numpy(record["centre"]).to(device).unsqueeze(0)
    normal_one = torch.from_numpy(record["normal"]).to(device).unsqueeze(0)
    output: list[np.ndarray] = []
    model.eval()
    with torch.no_grad(), autocast_context(device):
        source_embedding_one = model.encode_source(centre_one, normal_one)
        for start in range(0, len(queries), chunk):
            query = torch.from_numpy(queries[start:start + chunk]).to(device)
            count = len(query)
            prediction, _ = model.forward_from_embedding(
                source_embedding_one.expand(count, -1), centre_one.expand(count, -1),
                normal_one.expand(count, -1), query,
            )
            output.append(prediction.float().cpu().numpy())
    return np.concatenate(output).reshape(record["field"].shape)


def coherent_metrics(records: list[dict[str, Any]], predictions: list[np.ndarray], indices: list[int]) -> dict[str, float]:
    true_fields = [records[index]["field"][..., 0] + 1j * records[index]["field"][..., 1] for index in indices]
    pred_fields = [predictions[index][..., 0] + 1j * predictions[index][..., 1] for index in indices]
    axes = records[indices[0]]["axes"]
    target_index = tuple(int(np.argmin(np.abs(axis - target))) for axis, target in zip(axes, (64.0, 0.0, 0.0)))
    phases = np.asarray([-np.angle(field[target_index]) for field in true_fields])
    weights = np.exp(1j * phases)
    true_sum = sum(weight * field for weight, field in zip(weights, true_fields))
    pred_sum = sum(weight * field for weight, field in zip(weights, pred_fields))
    relative_l2 = np.linalg.norm(pred_sum - true_sum) / max(np.linalg.norm(true_sum), 1.0e-12)
    p_target_true = abs(true_sum[target_index])
    p_target_pred = abs(pred_sum[target_index])
    p_peak_true = np.max(np.abs(true_sum))
    p_peak_pred = np.max(np.abs(pred_sum))
    return {
        "complex_relative_l2": float(relative_l2),
        "p_target_true_pa": float(p_target_true),
        "p_target_pred_pa": float(p_target_pred),
        "p_target_relative_error": float(abs(p_target_pred - p_target_true) / max(p_target_true, 1.0e-12)),
        "p_peak_true_pa": float(p_peak_true),
        "p_peak_pred_pa": float(p_peak_pred),
        "p_peak_relative_error": float(abs(p_peak_pred - p_peak_true) / max(p_peak_true, 1.0e-12)),
    }


def run_skull(run_dir: Path, device: torch.device, max_minutes: float = 20.0) -> dict[str, Any]:
    label_dir = run_dir / "skull_labels"
    generate_skull_labels(label_dir)
    records = load_skull_labels(label_dir)
    model = GreenComplexNet().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=3.0e-4)
    rng = np.random.default_rng(20260719)
    train_records = records[:8]
    train_samples = []
    for record in train_records:
        queries_np = field_queries(record)
        valid_np = np.linalg.norm(queries_np - record["centre"], axis=1) >= 6.0
        train_samples.append({
            "queries": torch.from_numpy(queries_np).to(device),
            "field": torch.from_numpy(record["field"].reshape(-1, 2)).to(device),
            "valid_indices": np.flatnonzero(valid_np),
            "centre": torch.from_numpy(record["centre"]).to(device).unsqueeze(0),
            "normal": torch.from_numpy(record["normal"]).to(device).unsqueeze(0),
        })
    batch_size = 32768
    start_time = time.perf_counter()
    last_loss = float("nan")
    steps = 0
    model.train()
    while steps < 4000 and (time.perf_counter() - start_time) < max_minutes * 60.0:
        source_no = int(rng.integers(0, 8))
        sample = train_samples[source_no]
        choice_np = rng.choice(sample["valid_indices"], size=batch_size, replace=True)
        choice = torch.from_numpy(choice_np).to(device)
        centre = sample["centre"].expand(batch_size, -1)
        normal = sample["normal"].expand(batch_size, -1)
        query = sample["queries"][choice]
        target = sample["field"][choice]
        optimizer.zero_grad(set_to_none=True)
        with autocast_context(device):
            prediction, _ = model(centre, normal, query)
            loss = torch.mean(torch.sum((prediction.float() - target.float()) ** 2, dim=-1)) / torch.mean(
                torch.sum(target.float() ** 2, dim=-1)
            ).clamp_min(1.0e-12)
        loss.backward()
        optimizer.step()
        last_loss = float(loss.item())
        steps += 1

    training_seconds = time.perf_counter() - start_time
    predictions = [predict_record(model, record, device) for record in records]
    test_metrics = []
    for index in range(8, 12):
        pred = torch.from_numpy(predictions[index].reshape(-1, 2))
        target = torch.from_numpy(records[index]["field"].reshape(-1, 2))
        test_metrics.append({"source": index + 1, **complex_metrics(pred, target)})
    combined_pred = torch.from_numpy(np.concatenate([predictions[index].reshape(-1, 2) for index in range(8, 12)]))
    combined_true = torch.from_numpy(np.concatenate([records[index]["field"].reshape(-1, 2) for index in range(8, 12)]))
    report = {
        "gate": "V3_skull_smoke",
        "status": "completed_no_formal_pass_threshold",
        "labels": 12,
        "train_sources": list(range(1, 9)),
        "held_out_sources": list(range(9, 13)),
        "steps": steps,
        "batch_size": batch_size,
        "training_seconds": training_seconds,
        "last_training_loss": last_loss,
        "held_out_combined_metrics": complex_metrics(combined_pred, combined_true),
        "held_out_per_source": test_metrics,
        "coherent_sums": {
            "one_held_out": coherent_metrics(records, predictions, [8]),
            "four_held_out": coherent_metrics(records, predictions, [8, 9, 10, 11]),
            "eight_mixed_4_train_4_held_out": coherent_metrics(records, predictions, [0, 1, 2, 3, 8, 9, 10, 11]),
        },
        "interpretation_boundary": "Eight-element case is mixed because the fixed 12-label split has only four held-out sources.",
    }
    torch.save(model.state_dict(), run_dir / "v3_skull_model.pt")
    write_json(run_dir / "v3_skull.json", report)
    return report


def write_summary(run_dir: Path, reports: dict[str, Any], elapsed: float) -> None:
    lines = [
        "# Green 复声场路线排雷结果",
        "",
        f"运行目录：`{run_dir}`  ",
        f"总用时：{elapsed / 60.0:.2f} 分钟",
        "",
    ]
    for name, report in reports.items():
        lines.extend((f"## {name}", "", f"状态：**{report['status']}**", ""))
        if name == "V1":
            est = report["estimated_seconds"]
            lines.append(f"参数量：{report['parameter_count']:,}；估计 160³×128 查询：{est['128_elements_160_cubed']:.2f} 秒。")
        elif name == "V2":
            for seed in report["seeds"]:
                metric = seed["metrics"]
                lines.append(
                    f"Seed {seed['seed']}：复场 L2={metric['complex_relative_l2']:.4g}，"
                    f"强场相位 MAE={metric['phase_mae_deg_above_minus20db']:.3f}°。"
                )
        elif name == "V3":
            metric = report["held_out_combined_metrics"]
            lines.append(
                f"未见位置复场 L2={metric['complex_relative_l2']:.4g}，"
                f"强场相位 MAE={metric['phase_mae_deg_above_minus20db']:.3f}°。"
            )
        lines.append("")
    (run_dir / "SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("probe", "analytic", "skull", "all"), default="all")
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--time-budget-min", type=float, default=120.0)
    parser.add_argument("--skull-max-min", type=float, default=20.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for the planned V1/V2/V3 gates")
    device = torch.device("cuda")
    run_dir = args.run_dir or DEFAULT_RUN_ROOT / datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    reports: dict[str, Any] = {}
    # Preserve earlier gate results when stages are resumed into one run directory.
    for name, filename in (("V1", "v1_probe.json"), ("V2", "v2_analytic.json"), ("V3", "v3_skull.json")):
        existing = run_dir / filename
        if existing.is_file():
            reports[name] = json.loads(existing.read_text(encoding="utf-8"))

    if args.stage in ("probe", "all"):
        reports["V1"] = run_probe(run_dir, device)
        if args.stage == "all" and reports["V1"]["status"] != "pass":
            write_summary(run_dir, reports, time.perf_counter() - started)
            return 2
    if args.stage in ("analytic", "all"):
        reports["V2"] = run_analytic(run_dir, device)
        if args.stage == "all" and reports["V2"]["status"] != "pass":
            write_summary(run_dir, reports, time.perf_counter() - started)
            return 3
    if args.stage in ("skull", "all"):
        elapsed_minutes = (time.perf_counter() - started) / 60.0
        if elapsed_minutes >= args.time_budget_min:
            raise TimeoutError("Time budget exhausted before V3")
        remaining = args.time_budget_min - elapsed_minutes
        reports["V3"] = run_skull(run_dir, device, min(args.skull_max_min, max(1.0, remaining - 45.0)))

    write_summary(run_dir, reports, time.perf_counter() - started)
    print(run_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
