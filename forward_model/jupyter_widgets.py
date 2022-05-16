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
            description='chl'
        )

        nap_slider = widgets.FloatLogSlider(
            value=self.conditions["nap_default"], 
            min=-3, 
            max=3, 
            step=0.001,
            description='nap'
        )

        cdom_slider = widgets.FloatLogSlider(
            value=self.conditions["cdom_default"], 
            min=-3, 
            max=3, 
            step=0.001,
            description='cdom'
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

        # define sample widgets
        options_two_species = widgets.Checkbox(
            value=False,
            description='Use two species model',
            disabled=False,
            indent=False
        )

        return chl_slider, nap_slider, cdom_slider, rrs_samples,\
               user_samples, saved_samples, options_fQ, options_two_species