#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Waifu2x Converter CPP Driver
Author: K4YT3X
Date Created: February 8, 2019
Last Modified: August 3, 2019

Description: This class is a high-level wrapper
for waifu2x-converter-cpp.
"""

# local imports
import common

# built-in imports
import pathlib
import subprocess
import threading

# third-party imports
from avalon_framework import Avalon


class Waifu2xConverter:
    """This class communicates with waifu2x cui engine

    An object will be created for this class, containing information
    about the binary address and the processing method. When being called
    by the main program, other detailed information will be passed to
    the upscale function.
    """

    def __init__(self, settings, model_dir):
        self.settings = settings
        self.settings['model_dir'] = model_dir
        self.print_lock = threading.Lock()

    def upscale(self, input_directory, output_directory, scale_ratio, jobs, image_format, upscaler_exceptions):
        """ Waifu2x Converter Driver Upscaler
        This method executes the upscaling of extracted frames.

        Arguments:
            input_directory {string} -- source directory path
            output_directory {string} -- output directory path
            scale_ratio {int} -- frames' scale ratio
            threads {int} -- number of threads
        """

        try:
            # overwrite config file settings
            self.settings['input'] = input_directory
            self.settings['output'] = output_directory
            self.settings['scale-ratio'] = scale_ratio
            self.settings['jobs'] = jobs
            self.settings['output-format'] = image_format

            # models_rgb must be specified manually for waifu2x-converter-cpp
            # if it's not specified in the arguments, create automatically
            if self.settings['model-dir'] is None:
                self.settings['model-dir'] = pathlib.Path(self.settings['path']) / 'models_rgb'

            # print thread start message
            self.print_lock.acquire()
            Avalon.debug_info(f'[upscaler] Thread {threading.current_thread().name} started')
            self.print_lock.release()

            # list to be executed
            # initialize the list with waifu2x binary path as the first element
            execute = [common.find_path(self.settings['path'])]

            for key in self.settings.keys():

                value = self.settings[key]

                # the key doesn't need to be passed in this case
                if key == 'waifu2x_converter_path':
                    continue

                # null or None means that leave this option out (keep default)
                elif value is None or value is False:
                    continue
                else:
                    if len(key) == 1:
                        execute.append(f'-{key}')
                    else:
                        execute.append(f'--{key}')

                    # true means key is an option
                    if value is True:
                        continue

                    execute.append(str(value))

            Avalon.debug_info(f'Executing: {execute}')
            return subprocess.run(execute, check=True).returncode

        except Exception as e:
            upscaler_exceptions.append(e)
