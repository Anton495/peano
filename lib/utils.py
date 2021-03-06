# coding: utf-8

import re

from base_map import BaseMap


def ratio_linf(d, dv, dt):
    return (max(abs(x) for x in dv)**d, dt)

def ratio_l1(d, dv, dt):
    return (sum(abs(x) for x in dv)**d, dt)

def ratio_l2_squared(d, dv, dt):
    return (sum(x**2 for x in dv)**d, dt**2)


def chain2proto(chain_code):
    """Convert chain code like 'ijK' to curve prototype."""
    
    dim = len(set(''.join(chain_code).lower()))

    assert dim <= 6
    letters = 'ijklmn'

    vect_dict = {}
    for k in range(dim):
        coord = [0]*dim
        coord[k] = 1
        vect_dict[letters[k]] = coord
        vect_dict[letters[k].upper()] = [-m for m in coord]
        
    def diag_coord(vector):
        arg = [vect_dict[k] for k in vector]
        coord = list(map(sum,zip(*arg)))
        return coord

    proto = [list(map(vect_dict.get,chain_code)) if len(chain_code) == 1 else diag_coord(m) for m in chain_code]
    
    proto = [[0] * dim] + proto
    for l in range(len(proto)-1):
        proto[l+1] = [c + d for c, d in zip(proto[l], proto[l+1])]

    return proto

def basis2base_map(basis):
    
    dim = len(basis)-1 if basis[-1] in ['0','1'] else len(basis)
    
    letters = 'ijklmn'
    assert dim <= 6

    l2i = {l: i for i, l in enumerate(letters)}
    perm = [None]*dim
    flip = [None]*dim
    time_rev = True if basis[-1] =='1' else False
    
    basis = basis[:-1] if basis[-1] in ['0','1'] else basis

    for k, l in enumerate(basis):
        lk = l.lower()
        perm[k] = l2i[lk]
        flip[k] = (l != lk)

    return BaseMap(perm, flip, time_rev)

def bmstr2base_map(bmstr):
    if '1-t' in bmstr:
        time_rev = True
    else:
        time_rev = False
    match = re.match('\(x,y\)->\((.*),(.*)\)', bmstr)
    if not match:
        print('@@@',bmstr)
        
    g1, g2 = match.groups()
    if 'x' in g1:
        perm = [0, 1]
    else:
        perm = [1, 0]
    flip = [False]*2
    flip[0] = ('1-' in g1)
    flip[1] = ('1-' in g2)
    
    return BaseMap(perm, flip, time_rev)
