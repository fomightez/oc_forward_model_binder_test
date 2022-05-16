"""Module responsible for the core logic of the forward model."""

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from forward_model.read_params import read_iop_params, read_iops
from forward_model.read_samples import *
from forward_model.model_plots import *
from forward_model.jupyter_widgets import build_widgets
from forward_model.components import *
import os

def make_box_layout():
     return widgets.Layout(
        border='solid 1px black',
        margin='0px 10px 10px 0px',
        padding='5px 5px 5px 5px'
     )

class ForwardModel(widgets.HBox):
     
    def __init__(self):
        super().__init__()

        # read static values
        self.conditions = {}
        self.conditions["params"] = read_iop_params()
        self.conditions["wavelengths"], self.conditions["abs_coeff_water"], self.conditions["abs_increment"], self.conditions["scattering_coefficient"] = read_iops()
        self.conditions["sample_files"], self.conditions["rrs_samples"] = read_rrs_samples(self.conditions["params"])
        self.conditions["user_files"], self.conditions["user_samples"] = read_rrs_user(self.conditions["params"])
        self.conditions["chl_default"] = 1
        self.conditions["nap_default"] = 1
        self.conditions["cdom_default"] = 1

        # setup output streams for plots
        self.output_vals = widgets.Output()
        self.output_spectral_rrs = widgets.Output()
        self.output_spectral_absorption = widgets.Output()
        self.output_spectral_backscatter = widgets.Output()

        # define initial conditions
        components = calc_components(
            self.conditions["wavelengths"],
            self.conditions["params"],
            self.conditions["abs_coeff_water"],
            self.conditions["abs_increment"],
            self.conditions["scattering_coefficient"],
            self.conditions["chl_default"],
            self.conditions["nap_default"],
            self.conditions["cdom_default"])

        # define parameters for "inputs" plot
        set_input_plot(self)
  
        # define parameters for "spectral" plots
        set_spectral_rrs_plot(self, self.conditions["wavelengths"], components)
        set_spectral_absorption_plot(self, self.conditions["wavelengths"], components)
        set_spectral_backscatter_plot(self, self.conditions["wavelengths"], components)

        # define widgets
        chl_slider, nap_slider, cdom_slider, rrs_samples, user_samples, \
            saved_samples, options_fQ, options_two_species = build_widgets(self)

        # set control panel
        self.controls = widgets.VBox([
            chl_slider, 
            nap_slider, 
            cdom_slider,
            self.output_vals,
            rrs_samples,
            user_samples,
            saved_samples,
            options_fQ,
            options_two_species
        ])

        self.spectral_plots = widgets.VBox([self.output_spectral_rrs, self.output_spectral_absorption, self.output_spectral_backscatter])

        # define layouts
        self.controls.layout = make_box_layout()
        out_box = widgets.Box([self.spectral_plots])
        self.spectral_plots.layout = make_box_layout()
        
        # add to children
        self.children = [self.controls, self.spectral_plots]
      
        # observe spectra
        chl_slider.observe(self.update_model, 'value')
        nap_slider.observe(self.update_model, 'value')
        cdom_slider.observe(self.update_model, 'value')

        # show sample spectra
        rrs_samples.observe(self.show_sample_plots, 'value')

        # show user spectra
        user_samples.observe(self.show_user_plots, 'value')

    def update_model(self, change):
        """Draw line in plot"""
        chl_val = self.children[0].children[0].value
        nap_val = self.children[0].children[1].value
        cdom_val = self.children[0].children[2].value
        TSM = nap_val + chl_val * float(self.conditions["params"]["Constituents"]["Chl2DW"])

        components = calc_components(
            self.conditions["wavelengths"],
            self.conditions["params"],
            self.conditions["abs_coeff_water"],
            self.conditions["abs_increment"],
            self.conditions["scattering_coefficient"],
            chl_val,
            nap_val,
            cdom_val)

        self.line1a.set_ydata([np.log10(chl_val), np.log10(nap_val), np.log10(cdom_val)])
        self.line1b.set_ydata(np.log10(TSM))

        self.line2a.set_ydata(components["rrs"])

        self.line3a.set_ydata(components["total_absorption"])
        self.line3b.set_ydata(components["aw"])
        self.line3c.set_ydata(components["aph"])
        self.line3d.set_ydata(components["aCDOM"])
        self.line3e.set_ydata(components["aNAP"])

        self.line4a.set_ydata(np.log10(components["total_backscatter"]))
        self.line4b.set_ydata(np.log10(components["bbw"]))
        self.line4c.set_ydata(np.log10(components["bbph"]))
        self.line4d.set_ydata(np.log10(components["bbpNAP"]))

    def show_sample_plots(self, change):

        if change.new:
            self.rrs_samples = [None] * np.shape(self.conditions["rrs_samples"])[0]
            for ii in range(np.shape(self.conditions["rrs_samples"])[0]):
                self.rrs_samples[ii], = self.ax2.plot(
                    self.conditions["rrs_samples"][ii,:,0],
                    self.conditions["rrs_samples"][ii,:,1],
                    color='b', linestyle='--')
        else:
            for item in self.rrs_samples:
                item.set_ydata(None)

    def show_user_plots(self, change):

        if change.new:
            self.user_samples = [None] * np.shape(self.conditions["user_samples"])[0]
            for ii in range(np.shape(self.conditions["user_samples"])[0]):
                self.user_samples[ii] = self.ax2.scatter(
                    self.conditions["user_samples"][ii,:,0],
                    self.conditions["user_samples"][ii,:,1],
                    color='r')
        else:
            for item in self.user_samples:
                item.set_visible(False)