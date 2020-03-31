"""
Model definition, loss, and optimization.
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import tensorflow as tf

def get_logits(inputs, params):
    """
    Define the model logits to use in the loss function.
    """
    # TODO: define logits
    hidden = tf.layers.dense(
        inputs=inputs,
        units=3,
        activation=tf.nn.relu)
    logits = tf.layers.dense(
        inputs=hidden,
        units=1,
        activation=None)
    return logits

def get_predictions(logits):
    """
    Define predictions to use with evaluation metrics or TF Serving.
    """
    # TODO: define predictions
    prediction = tf.round(tf.nn.sigmoid(logits))

    predictions = {
        'prediction': prediction
    }

    return predictions

def get_loss(logits, labels, params, mode):
    """
    Define the loss function to use with an optimizer.
    """

    # NOTE: `loss` should be `None` during the "infer" mode
    loss = None
    if mode == tf.contrib.learn.ModeKeys.INFER:
        return loss

    # TODO: define loss
    multi_class_labels = labels['label']
    loss = tf.losses.sigmoid_cross_entropy(
        multi_class_labels=multi_class_labels,
        logits=logits)

    return loss

def get_train_op(loss, params, mode):
    """
    Define the training operation which will be used to optimize the model.
    Uses [`tf.contrib.layers.optimize_loss`](https://goo.gl/z1PswO).
    """

    # NOTE: `train_op` should be `None` outside of the "train" mode
    train_op = None
    if mode != tf.contrib.learn.ModeKeys.TRAIN:
        return train_op

    global_step = tf.contrib.framework.get_or_create_global_step()
    learning_rate = params['learning_rate']

    train_op = tf.contrib.layers.optimize_loss(
        loss=loss,
        global_step=global_step,
        learning_rate=learning_rate,
        optimizer='RMSProp',
        gradient_noise_scale=None,
        gradient_multipliers=None,
        clip_gradients=None,
        learning_rate_decay_fn=None,
        name=None)

    return train_op

def model_fn(features, labels, mode, params):
    """
    Define model and return [tf.contrib.learnModelFnOps](https://goo.gl/lXcvV8)
    for use with [tf.contrib.learn.Estimator](https://goo.gl/Ez2AgV).
    """

    inputs = features['inputs']

    logits = get_logits(inputs, params)
    predictions = get_predictions(logits)
    loss = get_loss(logits, labels, params, mode)
    train_op = get_train_op(loss, params, mode)

    return tf.contrib.learn.ModelFnOps(
        predictions=predictions,
        loss=loss,
        train_op=train_op,
        mode=mode)
