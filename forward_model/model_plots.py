"""Module responsible for building the plots."""
import numpy as np
import matplotlib.pyplot as plt

def set_input_plot(self):

    self.x = [1, 3, 5, 7]
    self.y = [np.log10(self.conditions["chl_default"]), 
              np.log10(self.conditions["nap_default"]), 
              np.log10(self.conditions["cdom_default"]),
              np.log10(self.conditions["nap_default"] + self.conditions["chl_default"] * float(self.conditions["params"]["Constituents"]["Chl2DW"]))]

    with self.output_vals:
        self.fig1, self.ax1 = plt.subplots(constrained_layout=True, figsize=(3,2))
        self.fig1.canvas.header_visible = False
        self.fig1.canvas.footer_visible = False
        self.line1a, = self.ax1.plot(self.x[0:3], self.y[0:3], "o", linewidth=0, color="r")
        self.line1b, = self.ax1.plot(self.x[3], self.y[3], "o", linewidth=0, color="0.5")
        self.ax1.set_ylabel('$Concentration$')
        self.ax1.set_xlim([0, 8])
        self.ax1.set_ylim([-3, 4])
        self.ax1.set_yticks(range(-3, 4))
        self.ax1.set_yticklabels([10**exp for exp in range(-3, 4)])
        self.ax1.set_xticks(self.x)
        self.ax1.set_xticklabels(["[Chl-a]\n$[mg.m^{-3}]$", "NAP\n$[g.m^{-3}]$", "CDOM$_{443}$\n$[m^{-1}]$", "TSM\n$[g.m^{-3}]$"], fontsize=8)
        plt.show()

    self.fig1.canvas.toolbar_visible = False
    self.ax1.grid(True)

def set_spectral_rrs_plot(self, wavs, components):

        with self.output_spectral_rrs:
            self.fig2, self.ax2 = plt.subplots(constrained_layout=True, figsize=(6,4))
            self.fig2.canvas.header_visible = False
            self.fig2.canvas.footer_visible = False

            self.line2a, = self.ax2.plot(wavs, components["rrs"], 'k')
            self.ax2.set_xlabel('$Wavelength \: [nm]$')
            self.ax2.set_ylabel('$R_{rs} \: [sr^{-1}]$')
            self.ax2.yaxis.labelpad = 20

            self.ax2.set_xlim([min(wavs), max(wavs)])
            self.ax2.set_ylim([0, 0.05])
            leg = plt.legend([self.line2a],['$R_{rs}$'], fontsize=6)
            leg.get_frame().set_linewidth(0.0)
            plt.show()

        self.fig2.canvas.toolbar_position = 'bottom'
        self.ax2.grid(True)
        self.rrs = components["rrs"]

def set_spectral_absorption_plot(self, wavs, components):

        self.wavs = range(0,700)

        with self.output_spectral_absorption:
            self.fig3, self.ax3 = plt.subplots(constrained_layout=True, figsize=(6,2))
            self.fig3.canvas.header_visible = False
            self.fig3.canvas.footer_visible = False

            self.line3a, = self.ax3.plot(wavs, components["total_absorption"], 'k')
            self.line3b, = self.ax3.plot(wavs, components["aw"], 'r')
            self.line3c, = self.ax3.plot(wavs, components["aph"], 'b')
            self.line3d, = self.ax3.plot(wavs, components["aCDOM"], 'g')
            self.line3e, = self.ax3.plot(wavs, components["aNAP"], '0.25')

            self.ax3.set_xlabel('$Wavelength \: [nm]$')
            self.ax3.set_ylabel('$Absorption \: [m]^{-1}$')
            self.ax3.yaxis.labelpad = 32.5

            self.ax3.set_xlim([min(wavs), max(wavs)])
            self.ax3.set_ylim([0, 5])
            leg = plt.legend([self.line3a, self.line3b, self.line3c, self.line3d, self.line3e],['total absorption', 'aw', 'aph', 'aCDOM', 'aNAP'], fontsize=6)
            leg.get_frame().set_linewidth(0.0)
            plt.show()

        self.fig3.canvas.toolbar_position = 'bottom'
        self.ax3.grid(True)

def set_spectral_backscatter_plot(self, wavs, components):

        with self.output_spectral_backscatter:
            self.fig4, self.ax4 = plt.subplots(constrained_layout=True, figsize=(6,2))
            self.fig4.canvas.header_visible = False
            self.fig4.canvas.footer_visible = False

            self.line4a, = self.ax4.plot(wavs, np.log10(components["total_backscatter"]), 'k')
            self.line4b, = self.ax4.plot(wavs, np.log10(components["bbw"]), 'r')
            self.line4c, = self.ax4.plot(wavs, np.log10(components["bbph"]), 'g')
            self.line4d, = self.ax4.plot(wavs, np.log10(components["bbpNAP"]), 'b')

            self.ax4.set_xlabel('$Wavelength \: [nm]$')
            self.ax4.set_ylabel('$Backscatter \: [m^{-1}]$')
            self.ax4.set_xlim([min(wavs), max(wavs)])
            self.ax4.set_ylim([-4, 2])
            self.ax4.set_yticks(range(-4, 2))
            self.ax4.set_yticklabels([10**exp for exp in range(-4, 2)])
            leg = plt.legend([self.line4a, self.line4a, self.line4b, self.line4c, self.line4d],['total backscatter', 'bbw', 'bbph', 'bbpNAP'], fontsize=6)
            leg.get_frame().set_linewidth(0.0)
            plt.show()
            
        self.fig4.canvas.toolbar_position = 'bottom'
        self.ax4.grid(True)
