import cv2
import traceback
import neuralgym as ng
import numpy as np
from inpaint_model import InpaintCAModel
from Utils import HiddenPrints
import logging
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # FATAL
logging.getLogger('tensorflow').setLevel(logging.FATAL)
import tensorflow as tf


def inpaint_all_frames(videoPath):

    base_dir = "output/" + videoPath.split(".")[0].split('/')[-1] + "/"
    checkpoint_dir = "model_logs/release_places2_256"
    i = 0
    while True:
        input_path = base_dir + videoPath.split(".")[0].split('/')[-1] + str(i) + "_input.png"
        mask_path = base_dir + videoPath.split(".")[0].split('/')[-1] + str(i) + "_mask.png"
        output_path = base_dir + videoPath.split(".")[0].split('/')[-1] + str(i) + "_out.png"
        i = i+1
        try:
            inpaint_single_frame(input_path, mask_path, output_path, checkpoint_dir)
        except Exception:

            track = traceback.format_exc()
            #print(track)
            if not track == traceback.format_exc():
                print(track)
            break


def inpaint_single_frame(input_path, mask_path, output_path, checkpoint_dir):

    image = cv2.imread(input_path)
    mask = cv2.imread(mask_path)

    with HiddenPrints():
        FLAGS = ng.Config('inpaint.yml')
    model = InpaintCAModel()

    assert image.shape == mask.shape

    h, w, _ = image.shape
    grid = 8
    image = image[:h // grid * grid, :w // grid * grid, :]
    mask = mask[:h // grid * grid, :w // grid * grid, :]
    # print('Shape of image: {}'.format(image.shape))

    image = np.expand_dims(image, 0)
    mask = np.expand_dims(mask, 0)
    input_image = np.concatenate([image, mask], axis=2)

    tf.reset_default_graph()
    sess_config = tf.ConfigProto()
    sess_config.gpu_options.allow_growth = True
    with tf.Session(config=sess_config) as sess:
        input_image = tf.constant(input_image, dtype=tf.float32)
        output = model.build_server_graph(FLAGS, input_image, reuse=False)
        output = (output + 1.) * 127.5
        output = tf.reverse(output, [-1])
        output = tf.saturate_cast(output, tf.uint8)
        # load pretrained model
        vars_list = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)
        assign_ops = []
        for var in vars_list:
            vname = var.name
            from_name = vname
            var_value = tf.contrib.framework.load_variable(checkpoint_dir, from_name)
            assign_ops.append(tf.assign(var, var_value))
        sess.run(assign_ops)
        # print('Model loaded.')
        result = sess.run(output)
        cv2.imwrite(output_path, result[0][:, :, ::-1])