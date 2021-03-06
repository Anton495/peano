#!/usr/bin/env python3
# coding: utf-8

import unittest

# run script from peano directory
import sys
import os
sys.path.append(os.path.dirname(sys.argv[0]) + '/../lib')

from examples import *
import utils


class TestCurve(unittest.TestCase):
    def test_curve_ratio(self):
        known_bounds = [
            {
                'curve': get_hilbert_curve(),
                'ratio': { 'l2': 6, 'l1': 9, 'linf': 6},
            },
            {
                'curve': get_peano_curve(),
                'ratio': {'l2': 8, 'l1': 32/3, 'linf': 8},
            },
            {
                'curve': get_haverkort_curve_1(),
                'ratio': {'l1': (99 + 5/9)},
            },
            {
                'curve': get_tokarev_curve(),
                'ratio': {'l1': [98.2, 98.4], 'l2': [26.1, 26.3], 'linf': [24.1, 24.3]},
            },
            {
                'curve': get_scepin_bauman_curve(),
                'ratio': {'l1': (10 + 2/3), 'l2': (5 + 2/3), 'linf': (5 + 1/3)},
            },
            {
                'curve': get_meurthe_curve(),
                'ratio': {'l1': (10 + 2/3), 'l2': (5 + 2/3), 'linf': (5 + 1/3)},
            },
            {
                'curve': get_serpentine_curve(),
                'ratio': {'l1': 10, 'l2': 6.25, 'linf': 5.625},
            },
            {
                'curve': get_coil_curve(),
                'ratio': {'l1': (10 + 2/3), 'l2': (6 + 2/3), 'linf': (6 + 2/3)},
            },
            {
                'curve': get_R_curve(),
                'ratio': {'l1': (10 + 2/3), 'l2': (6 + 2/3), 'linf': (6 + 2/3)},
            },
            {   
                'curve': get_haverkort_curve_A26(),
                'ratio': {'l1': (99 + 5/9), 'l2': [22.7,22.9], 'linf': (12 + 4/9)},
            },
            {   
                'curve': get_haverkort_curve_2(),
                'ratio': {'l1': [89.7, 89.8], 'l2': [18,19], 'linf': 14},
            },
        ]
        for data in known_bounds:
            curve = data['curve']
            for metric, ratio in data['ratio'].items():
                if isinstance(ratio, list):
                    ratio_lo, ratio_up = ratio
                else:
                    ratio_lo = ratio * 0.999
                    ratio_up = ratio * 1.001

                if metric == 'l2':
                    func = utils.ratio_l2_squared
                    ratio_lo, ratio_up = ratio_lo**2, ratio_up**2
                elif metric == 'l1':
                    func = utils.ratio_l1
                elif metric == 'linf':
                    func = utils.ratio_linf

                res = curve.estimate_ratio_new(func, rel_tol=0.0001)
                assert res['up'] <= ratio_up, 'metric {} up failed: {} > {}'.format(metric, res['up'], ratio_up)
                assert res['lo'] >= ratio_lo, 'metric {} lo failed: {} < {}'.format(metric, res['lo'], ratio_lo)

    def test_pcurve_ratio(self):
        pcurve = get_peano5_curve().forget(allow_time_rev=True)
        assert pcurve.estimate_ratio(utils.ratio_l2_squared, lower_bound=90, upper_bound=100)


if __name__ == "__main__":
    unittest.main()
