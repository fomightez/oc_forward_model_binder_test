"""Module responsible for reading in IOP model and IOP LUT data."""

import configparser
import os
import pathlib
import logging
import numpy as np
import glob

def read_iop_params(param_file="IOP_model.ini"):
    resolved_param_file = os.path.join(pathlib.Path(__file__).parent.resolve(), param_file)
    if not os.path.exists(resolved_param_file):
        print("IOP_model.ini file does not exist")
    __params = configparser.ConfigParser()
    __params.read(resolved_param_file)

    return __params

def read_iops(iop_file="IOPs.txt"):
    resolved_iop_file = os.path.join(pathlib.Path(__file__).parent.resolve(), iop_file)
    if not os.path.exists(resolved_iop_file):
        print("IOPS.txt file does not exist")
    __iops = \
        np.genfromtxt(resolved_iop_file, comments="#", delimiter=',', dtype=float)

    __wavelengths = __iops[:,0]
    __abs_coeff_water = __iops[:,1]
    __abs_increment = __iops[:,2]
    __scattering_coefficient = __iops[:,3]

    return __wavelengths, __abs_coeff_water, __abs_increment, __scattering_coefficient

def read_srf_bands(params):

    # read satellite L2 band information and SRFs
    resolved_sensor_path = os.path.join(pathlib.Path(__file__).parent.resolve(), params["Sensors"]["sensor_dir"],'*.txt')
    sensor_files = glob.glob(resolved_sensor_path)
    sensors = {}
    for sensor_file in sensor_files:
        sensor_name = os.path.basename(sensor_file).replace('.txt','')
        __sensor = configparser.ConfigParser()
        __sensor.read(sensor_file)
        sensors[sensor_name] = __sensor

    return sensors