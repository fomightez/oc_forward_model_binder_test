"""Module responsible for the core logic of the forward model."""

import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from forward_model.read_params import *
from forward_model.read_samples import *
from forward_model.model_plots import *
from forward_model.jupyter_widgets import build_widgets
from forward_model.components import *
from forward_model.sensors import *
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
        self.sensors = read_srf_bands(self.conditions["params"])
        self.conditions["wavelengths"], self.conditions["abs_coeff_water"], self.conditions["abs_increment"], self.conditions["scattering_coefficient"] = read_iops()
        self.conditions["sample_files"], self.conditions["rrs_samples"] = read_rrs_samples(self.conditions["params"])
        self.conditions["user_files"], self.conditions["user_samples"] = read_rrs_user(self.conditions["params"])
        self.conditions["chl_default"] = 1
        self.conditions["eff_default"] = 20
        self.conditions["ddf_default"] = 1
        self.conditions["nap_default"] = 1
        self.conditions["cdom_default"] = 1

        self.OLCI_A_bands = None
        self.OLCI_B_bands = None
        self.MSI_A_bands = None
        self.MSI_B_bands = None
        self.OLI_bands = None

        # calculate spectral response functions on supplied wavelength basis
        self.srfs = calculate_srfs(self.sensors, self.conditions["wavelengths"])

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

        self.rrs = components["rrs"]

        # define parameters for "inputs" plot
        set_input_plot(self)

        # define parameters for "spectral" plots
        set_spectral_rrs_plot(self, self.conditions["wavelengths"], components)
        set_spectral_absorption_plot(self, self.conditions["wavelengths"], components)
        set_spectral_backscatter_plot(self, self.conditions["wavelengths"], components)

        # define widgets
        chl_slider, eff_slider, ddf_slider, nap_slider, cdom_slider, rrs_samples, user_samples, \
            saved_samples, options_fQ, options_EAP, options_show_OLCI_A, options_show_OLCI_B, \
            options_show_MSI_A, options_show_MSI_B, options_show_OLI = build_widgets(self)

        # set control panel
        self.controls = widgets.VBox([
            chl_slider,
            eff_slider,
            ddf_slider,
            nap_slider, 
            cdom_slider,
            self.output_vals,
            rrs_samples,
            user_samples,
            saved_samples,
            options_fQ,
            options_EAP,
            options_show_OLCI_A,
            options_show_OLCI_B,            
            options_show_MSI_A,
            options_show_MSI_B,
            options_show_OLI
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
        options_EAP.observe(self.update_model, 'value')

        # show sample spectra
        rrs_samples.observe(self.show_sample_plots, 'value')

        # show user spectra
        user_samples.observe(self.show_user_plots, 'value')

        # show OLCI bands/spectra
        options_show_OLCI_A.observe(self.show_sensor_spectra_OLCI_A, 'value')
        options_show_OLCI_B.observe(self.show_sensor_spectra_OLCI_B, 'value')
        options_show_MSI_A.observe(self.show_sensor_spectra_MSI_A, 'value')
        options_show_MSI_B.observe(self.show_sensor_spectra_MSI_B, 'value')
        options_show_OLI.observe(self.show_sensor_spectra_OLI, 'value')

    def update_model(self, change):
        """Draw line in plot"""
        chl_val = self.children[0].children[0].value
        nap_val = self.children[0].children[3].value
        cdom_val = self.children[0].children[4].value
        implement_EAP = self.children[0].children[10].value
        TSM = nap_val + chl_val * float(self.conditions["params"]["Constituents"]["Chl2DW"])

        components = calc_components(
            self.conditions["wavelengths"],
            self.conditions["params"],
            self.conditions["abs_coeff_water"],
            self.conditions["abs_increment"],
            self.conditions["scattering_coefficient"],
            chl_val,
            nap_val,
            cdom_val,
            EAP=implement_EAP)

        self.rrs = components["rrs"]

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

        if self.OLCI_A_bands:
            
            for item in self.OLCI_A_bands:
                item.remove()
            for item in self.OLCI_A_spectra:
                item.remove()

            self.OLCI_A_bars[0].remove()
            for item in self.OLCI_A_bars[1]:
                item.remove()
            for item in self.OLCI_A_bars[2]:
                item.remove()

            self.OLCI_A_bands, self.OLCI_A_spectra, self.OLCI_A_bars = self.plot_sensor_bands('OLCI-A')

        if self.OLCI_B_bands:
            
            for item in self.OLCI_B_bands:
                item.remove()
            for item in self.OLCI_B_spectra:
                item.remove()

            self.OLCI_B_bars[0].remove()
            for item in self.OLCI_B_bars[1]:
                item.remove()
            for item in self.OLCI_B_bars[2]:
                item.remove()

            self.OLCI_B_bands, self.OLCI_B_spectra, self.OLCI_B_bars = self.plot_sensor_bands('OLCI-B')

        if self.MSI_A_bands:
            
            for item in self.MSI_A_bands:
                item.remove()
            for item in self.MSI_A_spectra:
                item.remove()

            self.MSI_A_bars[0].remove()
            for item in self.MSI_A_bars[1]:
                item.remove()
            for item in self.MSI_A_bars[2]:
                item.remove()

            self.MSI_A_bands, self.MSI_A_spectra, self.MSI_A_bars = self.plot_sensor_bands('MSI-A')

        if self.MSI_B_bands:
            
            for item in self.MSI_B_bands:
                item.remove()
            for item in self.MSI_B_spectra:
                item.remove()

            self.MSI_B_bars[0].remove()
            for item in self.MSI_B_bars[1]:
                item.remove()
            for item in self.MSI_B_bars[2]:
                item.remove()

            self.MSI_B_bands, self.MSI_B_spectra, self.MSI_B_bars = self.plot_sensor_bands('MSI-B')

        if self.OLI_bands:
            
            for item in self.OLI_bands:
                item.remove()
            for item in self.OLI_spectra:
                item.remove()

            self.OLI_bars[0].remove()
            for item in self.OLI_bars[1]:
                item.remove()
            for item in self.OLI_bars[2]:
                item.remove()

            self.OLI_bands, self.OLI_spectra, self.OLI_bars = self.plot_sensor_bands('OLI')

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
                item.remove()

    def show_sensor_spectra_OLCI_A(self, change):

        if change.new:
            self.OLCI_A_bands, self.OLCI_A_spectra, self.OLCI_A_bars = self.plot_sensor_bands('OLCI-A')
        else:
            for item in self.OLCI_A_bands:
                item.remove()
            for item in self.OLCI_A_spectra:
                item.remove()

            self.OLCI_A_bars[0].remove()
            for item in self.OLCI_A_bars[1]:
                item.remove()
            for item in self.OLCI_A_bars[2]:
                item.remove()

            self.OLCI_A_bands = None

    def show_sensor_spectra_OLCI_B(self, change):

        if change.new:
            self.OLCI_B_bands, self.OLCI_B_spectra, self.OLCI_B_bars = self.plot_sensor_bands('OLCI-B')
        else:
            for item in self.OLCI_B_bands:
                item.remove()
            for item in self.OLCI_B_spectra:
                item.remove()

            self.OLCI_B_bars[0].remove()
            for item in self.OLCI_B_bars[1]:
                item.remove()
            for item in self.OLCI_B_bars[2]:
                item.remove()

            self.OLCI_B_bands = None

    def show_sensor_spectra_MSI_A(self, change):

        if change.new:
            self.MSI_A_bands, self.MSI_A_spectra, self.MSI_A_bars = self.plot_sensor_bands('MSI-A')
        else:
            for item in self.MSI_A_bands:
                item.remove()
            for item in self.MSI_A_spectra:
                item.remove()

            self.MSI_A_bars[0].remove()
            for item in self.MSI_A_bars[1]:
                item.remove()
            for item in self.MSI_A_bars[2]:
                item.remove()

            self.MSI_A_bands = None

    def show_sensor_spectra_MSI_B(self, change):

        if change.new:
            self.MSI_B_bands, self.MSI_B_spectra, self.MSI_B_bars = self.plot_sensor_bands('MSI-B')
        else:
            for item in self.MSI_B_bands:
                item.remove()
            for item in self.MSI_B_spectra:
                item.remove()

            self.MSI_B_bars[0].remove()
            for item in self.MSI_B_bars[1]:
                item.remove()
            for item in self.MSI_B_bars[2]:
                item.remove()

            self.MSI_B_bands = None

    def show_sensor_spectra_OLI(self, change):

        if change.new:
            self.OLI_bands, self.OLI_spectra, self.OLI_bars = self.plot_sensor_bands('OLI')
        else:
            for item in self.OLI_bands:
                item.remove()
            for item in self.OLI_spectra:
                item.remove()

            self.OLI_bars[0].remove()
            for item in self.OLI_bars[1]:
                item.remove()
            for item in self.OLI_bars[2]:
                item.remove()

            self.OLI_bands = None

    def plot_sensor_bands(self, sensor_name):

        band_centers = np.array(self.sensors[sensor_name]["bands"]["centers"].split(',')).astype(float)
        band_widths = np.array(self.sensors[sensor_name]["bands"]["widths"].split(',')).astype(float)
        sensor_rrs = calculate_srf_integrals(self.conditions["wavelengths"], self.rrs, self.srfs[sensor_name], band_widths, band_centers)

        plot_bands = [None] * np.shape(band_centers)[0]
        plot_spectra = [None] * np.shape(band_centers)[0]
        plot_bars = self.ax2.errorbar(band_centers, sensor_rrs,\
             xerr=band_widths/2, yerr=0,
             color='k', linewidth=0.0, marker='o',markersize=2, elinewidth=0.5)


        for bc, bw, ii in zip(band_centers, band_widths, range(len(band_centers))):
            plot_bands[ii] = self.ax2.fill_betweenx([0, 0.05],\
                [bc - bw/2, bc - bw/2], [bc + bw/2, bc + bw/2],\
                color=wavelength_to_rgb(bc), zorder=0, alpha=0.5)
            plot_spectra[ii] = self.ax2.scatter(bc, sensor_rrs[ii], color="k", zorder=1000, alpha=0.5)

        return plot_bands, plot_spectra, plot_bars