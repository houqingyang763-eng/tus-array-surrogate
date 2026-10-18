"""Reproducible analytic costs, not a GPU benchmark or peak-memory estimate.

Only Python's standard library is required. Run from any directory:
    python cost_model.py --output ../calculations/costs.json
An explicit output path is resolved against the current working directory.
"""

import argparse
import json
from functools import reduce
from operator import mul
from pathlib import Path


def prod(values):
    return reduce(mul, values, 1)


def tensor(name, elements, bytes_per_element, note):
    size = elements * bytes_per_element
    return dict(name=name, elements=elements, bytes=size,
                MiB=size / 2**20, GiB=size / 2**30, note=note)


def conv(name, voxels, cin, cout, kernel=3, depthwise=False):
    mac = voxels * (kernel**3 * cin + cin * cout if depthwise
                    else kernel**3 * cin * cout)
    return dict(name=name, voxels=voxels, real_cin=cin, real_cout=cout,
                kernel=kernel, depthwise_plus_pointwise=depthwise,
                MAC=mac, GMAC=mac / 1e9, forward_FLOP=2 * mac)


def build_report():
    shape = (352, 352, 192)
    n = prod(shape)
    valid = 5_101_889
    coarse = {str(h): n // factor**3 for h, factor in
              [(0.5, 1), (1.0, 2), (2.0, 4), (4.0, 8)]}
    assert n == 23_789_568 and prod((88, 88, 48)) == coarse['2.0']
    tensors = [
        tensor('ROI complex field FP32', 2*n, 4, 'Two real components'),
        tensor('ROI 8 real channels FP16', 8*n, 2, 'One tensor only'),
        tensor('ROI 16 real channels FP16', 16*n, 2, 'One tensor only'),
        tensor('ROI 16 real channels FP32', 16*n, 4, 'One tensor only'),
        tensor('1mm 16 real channels FP16', 16*coarse['1.0'], 2,
               '8 complex channels; exact packing of one fine complex field'),
        tensor('2mm 48 real channels FP16', 48*coarse['2.0'], 2, '24 complex'),
        tensor('2mm 64 real channels FP16', 64*coarse['2.0'], 2, '32 complex'),
        tensor('Full 8-carrier bank complex FP32', 16*n, 4,
               'Avoid materializing; includes no intermediate activations'),
        tensor('2mm SSM Ccomplex=16 S=4 one direction FP32',
               coarse['2.0']*16*4*2, 4,
               'Complex states, one direction; six separate directions multiply by six'),
        tensor('ROI dense basis rank32 complex FP32', 2*n*32, 4,
               'Basis storage only, no gradients/optimizer'),
        tensor('Mask dense basis rank32 complex FP32', 2*valid*32, 4,
               'Diagnostic mask only; not full output implementation'),
        tensor('ROI trainable rank32 basis FP32 Adam lower bookkeeping',
               2*n*32, 16, 'Weights+gradient+two moments; no activation/master copy'),
        tensor('ROI attention scores 4096 tokens FP16', n*4096, 2,
               'One head dense scores; excludes Q/K/V'),
        tensor('Mask attention scores 4096 tokens FP16', valid*4096, 2,
               'One head; mask output is not the default full ROI contract'),
        tensor('Dense spectral weights 64x64 channels 64^3 complex FP32',
               64*64*64**3*2, 4,
               'One stored block only; implementation may require multiple sign blocks'),
    ]
    operations = [
        conv('ROI dense 8 to 8', n, 8, 8),
        conv('ROI dense 16 to 16', n, 16, 16),
        conv('ROI dense 32 to 32', n, 32, 32),
        conv('ROI depthwise3 plus pointwise 16 to 16', n, 16, 16, depthwise=True),
        conv('2mm dense 64 to 64', coarse['2.0'], 64, 64),
    ]
    # M0 deliberately uses real-channel counts as an upper bound for tied
    # complex arithmetic. Every stated step is counted below, including T=2.
    fine_n, n1, n2, n4 = n, coarse['1.0'], coarse['2.0'], coarse['4.0']
    core = [
        (conv('fine local encoder/decode block 1', fine_n, 8, 8, depthwise=True), 1),
        (conv('fine local encoder/decode block 2', fine_n, 8, 8, depthwise=True), 1),
        (conv('1mm field/mixing block', n1, 16, 16, depthwise=True), 6),
        (conv('2mm field/mixing block', n2, 48, 48, depthwise=True), 6),
        (conv('4mm field/mixing block', n4, 96, 96, depthwise=True), 6),
        (conv('1mm latent A pointwise', n1, 16, 16, kernel=1), 6),
        (conv('2mm latent A pointwise', n2, 48, 48, kernel=1), 6),
        (conv('4mm latent A pointwise', n4, 96, 96, kernel=1), 6),
        # Packed states: 1mm16 -> 2mm128 -> 48; 2mm48 -> 4mm384 -> 96.
        (conv('packed restriction 1mm to 2mm', n2, 128, 48, kernel=1), 3),
        (conv('packed restriction 2mm to 4mm', n4, 384, 96, kernel=1), 3),
        (conv('prolongation 4mm to packed2mm', n4, 96, 384, kernel=1), 3),
        (conv('prolongation 2mm to packed1mm', n2, 48, 128, kernel=1), 3),
        (conv('1mm decoder to packed complex residual', n1, 16, 16, kernel=1), 1),
        (conv('fine output 8 to 2', fine_n, 8, 2, kernel=1), 1),
        (conv('1mm source lift: packedP0+media8+geometry4', n1, 28, 16, kernel=1), 1),
        (conv('fine decode fusion: field2+media8+geometry4', fine_n, 14, 8, kernel=1), 1),
        (conv('fine reference projection 2 to 2', fine_n, 2, 2, kernel=1), 1),
        (conv('1mm media gate from pooled8', n1, 8, 16, kernel=1), 1),
        (conv('2mm media gate from pooled8', n2, 8, 48, kernel=1), 1),
        (conv('4mm media gate from pooled8', n4, 8, 96, kernel=1), 1),
        (conv('4mm post-axis pointwise', n4, 96, 96, kernel=1), 6),
    ]
    core_rows = [dict(op, count=count, total_GMAC=op['GMAC']*count)
                 for op, count in core]
    core_mac = sum(row['MAC']*row['count'] for row in core_rows)
    axis_mac = n4 * 96 * 2 * 8 * 6  # two T cycles, three axes, rank8
    core_rows.append(dict(name='4mm axial low-rank token mixing', rank=8,
                          axes_per_cycle=3, cycles=2, MAC=axis_mac,
                          total_GMAC=axis_mac/1e9))
    core_mac += axis_mac
    baseline = []
    channels = [8, 16, 32, 64, 128, 128]
    for level, cout in enumerate(channels):
        nl = n // 8**level
        cin = 3 if level == 0 else channels[level-1]
        baseline.extend([conv('V9BASE encoder %s first' % level, nl, cin, cout),
                         conv('V9BASE encoder %s second' % level, nl, cout, cout)])
    for level in range(4, -1, -1):
        nl, cout, cin = n // 8**level, channels[level], channels[level+1]
        baseline.extend([conv('V9BASE upconv %s' % level, nl//8, cin, cout, kernel=2),
                         conv('V9BASE decoder %s first' % level, nl, 2*cout, cout),
                         conv('V9BASE decoder %s second' % level, nl, cout, cout)])
    baseline.append(conv('V9BASE output head', n, 8, 2, kernel=1))
    return dict(
        status='ANALYTIC_ONLY',
        dimensions=dict(ROI=shape, ROI_voxels=n, valid_mask_voxels=valid,
                        full_simulation_voxels=384*480*224,
                        voxel_counts_by_spacing_mm=coarse),
        conventions=dict(MAC='one real multiply-accumulate; 2 FLOP',
                         memory='single tensor; excludes liveness, workspace, allocator',
                         timing='No measured V100 time, bandwidth or DDP time',
                         resource='per sample/per GPU; global batch5 on five GPUs'),
        input_evidence=dict(media_channels=1, P0_real_channels=2,
                            source='MISSION-linked T512-V9BASE RESULTS.md ROI hook, line 203',
                            scope='Recorded baseline interface, not a fresh model run'),
        tensors=tensors, operations=operations,
        baseline_backbone=dict(real_channels=channels, input_channels=3,
                               rows=baseline,
                               forward_GMAC=sum(row['MAC'] for row in baseline)/1e9,
                               excluded=['conditioning/fusion/Fourier-FiLM',
                                         'norm/activation/pooling/data movement',
                                         'backward/DDP/optimizer'],
                               note='Analytic conventional backbone only; not total baseline timing'),
        candidate_M0_core=dict(real_channels=[8,16,48,96], shared_updates=2,
                               rows=core_rows, forward_GMAC=core_mac/1e9,
                               forward_TFLOP=2*core_mac/1e12,
                               media_input_lift_GMAC_per_channel=n*8/1e9,
                               full_formula='forward_GMAC + media_input_lift_GMAC_per_channel * C_m',
                               forward_GMAC_for_current_media1=(core_mac+n*8)/1e9,
                               excluded=['elementwise gate/activation/residual operations',
                                         'geometry feature generation',
                                         'interpolation/norm/packing data movement',
                                         'backward/recomputation/DDP/optimizer']),
        query_decoder=dict(hidden_layers=4, width=256,
                           full_ROI_GMAC=n*4*256**2/1e9,
                           valid_mask_GMAC=valid*4*256**2/1e9,
                           note='Four square hidden transforms; excludes input/output transforms'),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = build_report()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(status=report['status'], ROI_voxels=report['dimensions']['ROI_voxels'],
                          M0_forward_GMAC_current_input=report['candidate_M0_core']['forward_GMAC_for_current_media1'],
                          V9BASE_backbone_GMAC=report['baseline_backbone']['forward_GMAC'],
                          output=str(args.output) if args.output else None), ensure_ascii=False))


if __name__ == '__main__':
    main()
