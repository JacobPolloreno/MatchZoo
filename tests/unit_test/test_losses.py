import pytest

import numpy as np
from keras import backend as K

from matchzoo import losses


def test_hinge_loss():
    true_value = K.variable(np.array([[1.2], [1],
                                      [1], [1]]))
    pred_value = K.variable(np.array([[1.2], [0.1],
                                      [0], [-0.3]]))
    expected_loss = (0 + 1 - 0.3 + 0) / 2.0
    loss = K.eval(losses.rank_hinge_loss(true_value, pred_value))
    assert np.isclose(expected_loss, loss)
    losses.margin = 2
    expected_loss = (2 + 0.1 - 1.2 + 2 - 0.3 + 0) / 2.0
    loss = K.eval(losses.rank_hinge_loss(true_value, pred_value))
    assert np.isclose(expected_loss, loss)
    true_value = K.variable(np.array([[1.2], [1], [0.8],
                                      [1], [1], [0.8]]))
    pred_value = K.variable(np.array([[1.2], [0.1], [-0.5],
                                      [0], [-2], [-0.3]]))
    losses.margin = 1
    losses.neg_num = 2
    expected_loss = (0 + 1 - 0.3 + 0) / 2.0
    loss = K.eval(losses.rank_hinge_loss(true_value, pred_value))
    assert np.isclose(expected_loss, loss)



def test_rank_crossentropy_loss():
    losses.neg_num = 1
    def softmax(x):
        return np.exp(x)/np.sum(np.exp(x), axis=0)
    true_value = K.variable(np.array([[1.], [0.],
                                      [0.], [1.]]))
    pred_value = K.variable(np.array([[0.8], [0.1],
                                      [0.8], [0.1]]))
    expected_loss = (-np.log(softmax([0.8, 0.1])[0])-np.log(softmax([0.8, 0.1])[1]))/2
    loss = K.eval(losses.rank_crossentropy_loss(true_value, pred_value))
    assert np.isclose(expected_loss, loss)
    true_value = K.variable(np.array([[1.], [0.], [0.],
                                      [0.], [1.], [0.]]))
    pred_value = K.variable(np.array([[0.8], [0.1], [0.1],
                                      [0.8], [0.1], [0.1]]))
    losses.neg_num = 2
    expected_loss = (-np.log(softmax([0.8, 0.1, 0.1])[0])-np.log(softmax([0.8, 0.1, 0.1])[1]))/2
    loss = K.eval(losses.rank_crossentropy_loss(true_value, pred_value))
    assert np.isclose(expected_loss, loss)
