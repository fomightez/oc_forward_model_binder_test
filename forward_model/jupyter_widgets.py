"""Module responsible for building the Jupyter notebook widgets for model interaction."""
from ipywidgets import widgets
import os

def build_widgets(self):
 
        # define slider widgets
        chl_slider = widgets.FloatLogSlider(
            value=self.conditions["chl_default"], 
            min=-3, 
            max=3, 
            step=0.001,
            description='Chlorophyll'
        )

        eff_slider = widgets.FloatSlider(
            value=self.conditions["eff_default"], 
            min=1, 
            max=20, 
            step=1,
            description='Eff. diam [μm]'
        )

        ddf_slider = widgets.FloatSlider(
            value=self.conditions["ddf_default"], 
            min=0, 
            max=1, 
            step=0.01,
            description='DD fraction'
        )

        nap_slider = widgets.FloatLogSlider(
            value=self.conditions["nap_default"], 
            min=-3, 
            max=3, 
            step=0.001,
            description='Non-algal'
        )

        cdom_slider = widgets.FloatLogSlider(
            value=self.conditions["cdom_default"], 
            min=-3, 
            max=3, 
            step=0.001,
            description='CDOM'
        )

        # define sample widgets
        rrs_samples = widgets.Checkbox(
            value=False,
            description='Show sample $R_{rs}$ spectra',
            disabled=False,
            indent=False
        )

        user_samples = widgets.Checkbox(
            value=False,
            description='Show user $R_{rs}$ spectra',
            disabled=False,
            indent=False
        )

        saved_samples = widgets.Checkbox(
            value=False,
            description='Show saved $R_{rs}$ spectra << WIP',
            disabled=False,
            indent=False
        )
 
        # define options widgets
        options_fQ = widgets.Checkbox(
            value=False,
            description='Use variable f/Q',
            disabled=False,
            indent=False
        )

        options_EAP = widgets.Checkbox(
            value=False,
            description='Use EAP model',
            disabled=False,
            indent=False
        )

        # define sensor widgets
        options_show_OLCI_A = widgets.Checkbox(
            value=False,
            description='Show S3 OLCI-A L2 sampling',
            disabled=False,
            indent=False
        )

        options_show_OLCI_B = widgets.Checkbox(
            value=False,
            description='Show S3 OLCI-B L2 sampling',
            disabled=False,
            indent=False
        )

        options_show_MSI_A = widgets.Checkbox(
            value=False,
            description='Show S2 MSI-A L2 sampling',
            disabled=False,
            indent=False
        )

        options_show_MSI_B = widgets.Checkbox(
            value=False,
            description='Show S2 MSI-B L2 sampling',
            disabled=False,
            indent=False
        )

        options_show_OLI = widgets.Checkbox(
            value=False,
            description='Show L8 OLI L2 sampling',
            disabled=False,
            indent=False
        )
        return chl_slider, eff_slider, ddf_slider, nap_slider, cdom_slider, rrs_samples,\
               user_samples, saved_samples, options_fQ, options_EAP, options_show_OLCI_A,\
               options_show_OLCI_B, options_show_MSI_A, options_show_MSI_B, options_show_OLI