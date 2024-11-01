#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FM Double Station
# Author: Ben Cometto
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
import numpy as np
import sip



class fmDoubleStation(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FM Double Station", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FM Double Station")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "fmDoubleStation")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.dec = dec = 65
        self.audio_rate = audio_rate = 44100
        self.samp_rate = samp_rate = audio_rate*dec
        self.vol_station2 = vol_station2 = 0.25
        self.vol_station1 = vol_station1 = 0.25
        self.vol_max = vol_max = 0.5
        self.taps_fm = taps_fm = firdes.low_pass(1.0, samp_rate, 100000,25000, window.WIN_HAMMING, 6.76)
        self.station2_range = station2_range = 1400000
        self.freq_station2_offset = freq_station2_offset = 800000
        self.freq_station1 = freq_station1 = 98100000
        self.fm_bw = fm_bw = 200000
        self.fd = fd = 75000

        ##################################################
        # Blocks
        ##################################################

        self._vol_station2_range = qtgui.Range(0, 1, 0.01, 0.25, 200)
        self._vol_station2_win = qtgui.RangeWidget(self._vol_station2_range, self.set_vol_station2, "'vol_station2'", "dial", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._vol_station2_win)
        self._vol_station1_range = qtgui.Range(0, 1, 0.01, 0.25, 200)
        self._vol_station1_win = qtgui.RangeWidget(self._vol_station1_range, self.set_vol_station1, "'vol_station1'", "dial", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._vol_station1_win)
        self._freq_station2_offset_range = qtgui.Range(-station2_range, station2_range, fm_bw, 800000, 200)
        self._freq_station2_offset_win = qtgui.RangeWidget(self._freq_station2_offset_range, self.set_freq_station2_offset, "'freq_station2_offset'", "eng_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._freq_station2_offset_win)
        self._freq_station1_range = qtgui.Range(88100000, 108100000, fm_bw, 98100000, 200)
        self._freq_station1_win = qtgui.RangeWidget(self._freq_station1_range, self.set_freq_station1, "'freq_station1'", "eng_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._freq_station1_win)
        self.soapy_rtlsdr_source_0_0 = None
        dev = 'driver=rtlsdr'
        stream_args = 'bufflen=16384'
        tune_args = ['']
        settings = ['']

        def _set_soapy_rtlsdr_source_0_0_gain_mode(channel, agc):
            self.soapy_rtlsdr_source_0_0.set_gain_mode(channel, agc)
            if not agc:
                  self.soapy_rtlsdr_source_0_0.set_gain(channel, self._soapy_rtlsdr_source_0_0_gain_value)
        self.set_soapy_rtlsdr_source_0_0_gain_mode = _set_soapy_rtlsdr_source_0_0_gain_mode

        def _set_soapy_rtlsdr_source_0_0_gain(channel, name, gain):
            self._soapy_rtlsdr_source_0_0_gain_value = gain
            if not self.soapy_rtlsdr_source_0_0.get_gain_mode(channel):
                self.soapy_rtlsdr_source_0_0.set_gain(channel, gain)
        self.set_soapy_rtlsdr_source_0_0_gain = _set_soapy_rtlsdr_source_0_0_gain

        def _set_soapy_rtlsdr_source_0_0_bias(bias):
            if 'biastee' in self._soapy_rtlsdr_source_0_0_setting_keys:
                self.soapy_rtlsdr_source_0_0.write_setting('biastee', bias)
        self.set_soapy_rtlsdr_source_0_0_bias = _set_soapy_rtlsdr_source_0_0_bias

        self.soapy_rtlsdr_source_0_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)

        self._soapy_rtlsdr_source_0_0_setting_keys = [a.key for a in self.soapy_rtlsdr_source_0_0.get_setting_info()]

        self.soapy_rtlsdr_source_0_0.set_sample_rate(0, samp_rate)
        self.soapy_rtlsdr_source_0_0.set_frequency(0, freq_station1)
        self.soapy_rtlsdr_source_0_0.set_frequency_correction(0, 0)
        self.set_soapy_rtlsdr_source_0_0_bias(bool(False))
        self._soapy_rtlsdr_source_0_0_gain_value = 60
        self.set_soapy_rtlsdr_source_0_0_gain_mode(0, bool(False))
        self.set_soapy_rtlsdr_source_0_0_gain(0, 'TUNER', 60)
        self.rational_resampler_xxx_1_0 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=dec,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_1 = filter.rational_resampler_fff(
                interpolation=1,
                decimation=dec,
                taps=[],
                fractional_bw=0)
        self.qtgui_freq_sink_x_0_1_0_0_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Station 2 Predemod", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_1_0_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_1_0_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_1_0_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_1_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1_0_0_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0_1_0_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_1_0_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_1_0_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_1_0_0_0.enable_control_panel(True)
        self.qtgui_freq_sink_x_0_1_0_0_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1_0_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1_0_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1_0_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_1_0_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_1_0_0_0_win)
        self.qtgui_freq_sink_x_0_1_0_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Station 1 Predemod", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_1_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_1_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_1_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1_0_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0_1_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_1_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_1_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_1_0_0.enable_control_panel(True)
        self.qtgui_freq_sink_x_0_1_0_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_1_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_1_0_0_win)
        self.qtgui_freq_sink_x_0_1_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Input", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_1_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_1_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_1_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0_1_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_1_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_1_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_1_0.enable_control_panel(True)
        self.qtgui_freq_sink_x_0_1_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_1_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_1_0_win)
        self.qtgui_freq_sink_x_0_0_0 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Station 2 Demod", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_0.enable_control_panel(True)
        self.qtgui_freq_sink_x_0_0_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_0_win)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Station 1 Demod", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(True)
        self.qtgui_freq_sink_x_0_0.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.freq_xlating_fir_filter_xxx_1 = filter.freq_xlating_fir_filter_ccf(1, taps_fm, freq_station2_offset, samp_rate)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccf(1, taps_fm, 0, samp_rate)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff((vol_station2*vol_max))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff((vol_station1*vol_max))
        self.audio_sink_1 = audio.sink(audio_rate, '', False)
        self.analog_fm_demod_cf_0_0 = analog.fm_demod_cf(
        	channel_rate=samp_rate,
        	audio_decim=1,
        	deviation=fd,
        	audio_pass=14000,
        	audio_stop=20000,
        	gain=1.0,
        	tau=(75e-6),
        )
        self.analog_fm_demod_cf_0 = analog.fm_demod_cf(
        	channel_rate=samp_rate,
        	audio_decim=1,
        	deviation=fd,
        	audio_pass=14000,
        	audio_stop=20000,
        	gain=1.0,
        	tau=(75e-6),
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_demod_cf_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_fm_demod_cf_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.analog_fm_demod_cf_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.analog_fm_demod_cf_0_0, 0), (self.qtgui_freq_sink_x_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.rational_resampler_xxx_1_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_fm_demod_cf_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_freq_sink_x_0_1_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.analog_fm_demod_cf_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.qtgui_freq_sink_x_0_1_0_0_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.audio_sink_1, 1))
        self.connect((self.rational_resampler_xxx_1_0, 0), (self.audio_sink_1, 0))
        self.connect((self.soapy_rtlsdr_source_0_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.soapy_rtlsdr_source_0_0, 0), (self.freq_xlating_fir_filter_xxx_1, 0))
        self.connect((self.soapy_rtlsdr_source_0_0, 0), (self.qtgui_freq_sink_x_0_1_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fmDoubleStation")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_dec(self):
        return self.dec

    def set_dec(self, dec):
        self.dec = dec
        self.set_samp_rate(self.audio_rate*self.dec)

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.set_samp_rate(self.audio_rate*self.dec)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_taps_fm(firdes.low_pass(1.0, self.samp_rate, 100000, 25000, window.WIN_HAMMING, 6.76))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0_1_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0_1_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0_1_0_0_0.set_frequency_range(0, self.samp_rate)
        self.soapy_rtlsdr_source_0_0.set_sample_rate(0, self.samp_rate)

    def get_vol_station2(self):
        return self.vol_station2

    def set_vol_station2(self, vol_station2):
        self.vol_station2 = vol_station2
        self.blocks_multiply_const_vxx_0_0.set_k((self.vol_station2*self.vol_max))

    def get_vol_station1(self):
        return self.vol_station1

    def set_vol_station1(self, vol_station1):
        self.vol_station1 = vol_station1
        self.blocks_multiply_const_vxx_0.set_k((self.vol_station1*self.vol_max))

    def get_vol_max(self):
        return self.vol_max

    def set_vol_max(self, vol_max):
        self.vol_max = vol_max
        self.blocks_multiply_const_vxx_0.set_k((self.vol_station1*self.vol_max))
        self.blocks_multiply_const_vxx_0_0.set_k((self.vol_station2*self.vol_max))

    def get_taps_fm(self):
        return self.taps_fm

    def set_taps_fm(self, taps_fm):
        self.taps_fm = taps_fm
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.taps_fm)
        self.freq_xlating_fir_filter_xxx_1.set_taps(self.taps_fm)

    def get_station2_range(self):
        return self.station2_range

    def set_station2_range(self, station2_range):
        self.station2_range = station2_range

    def get_freq_station2_offset(self):
        return self.freq_station2_offset

    def set_freq_station2_offset(self, freq_station2_offset):
        self.freq_station2_offset = freq_station2_offset
        self.freq_xlating_fir_filter_xxx_1.set_center_freq(self.freq_station2_offset)

    def get_freq_station1(self):
        return self.freq_station1

    def set_freq_station1(self, freq_station1):
        self.freq_station1 = freq_station1
        self.soapy_rtlsdr_source_0_0.set_frequency(0, self.freq_station1)

    def get_fm_bw(self):
        return self.fm_bw

    def set_fm_bw(self, fm_bw):
        self.fm_bw = fm_bw

    def get_fd(self):
        return self.fd

    def set_fd(self, fd):
        self.fd = fd




def main(top_block_cls=fmDoubleStation, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
