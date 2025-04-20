"""Map a flat dimension with points of rank N, according to the Hilbert curve."""

import numpy as np
import tensorflow as tf

import densecurves.hilbert
import mlable.shapes

# 1D PERMUTATION ###############################################################

def permutation(order: int, rank: int) -> list:
    # 1D dimension of the curve: 2 ** (order * rank)
    __dim = 1 << (order * rank)
    # target shape: (2 ** order, 2 ** order, ...) rank times
    __shape = rank * [1 << order]
    # the whole list of vertexes
    __curve = [densecurves.hilbert.point(__i, order=order, rank=rank) for __i in range(__dim)]
    # match the format of numpy: one row per dimension (!= one row per point)
    __indices = list(zip(*__curve))
    # permutation: __flat[i] contains the destination index of i
    __flat = np.ravel_multi_index(__indices, dims=__shape, mode='wrap', order='C')
    # mapping between destination and origin indices
    __map = {__d: __o for __o, __d in enumerate(__flat.tolist())}
    # match the format of gather: __perm[i] contains the origin of index i
    return [__map[__d] for __d in sorted(__map.keys())]

# 1D => ND #####################################################################

def fold(data: tf.Tensor, order: int, rank: int, axis: int) -> tf.Tensor:
    # only integer dimension (0 for None)
    __shape = mlable.shapes.normalize(data.shape)
    # avoid negative indices => axis + 1 != 0
    __axis = axis % len(__shape)
    # insert the new axes
    __shape = __shape[:__axis] + rank * [1 << order] + __shape[__axis + 1:]
    # 1D reordering of the indexes according to the Hilbert curve
    __perm = permutation(order=order, rank=rank)
    # actually swap the elements along the target axis
    __data = tf.gather(data, indices=__perm, axis=__axis)
    # split the sequence axis
    return tf.reshape(__data, shape=__shape)

# ND => 1D #####################################################################

def unfold() -> tf.Tensor:
    pass
