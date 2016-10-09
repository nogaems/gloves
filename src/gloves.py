#! /usr/bin/env python3

import time
import os
import argparse
import logging as log

class Gloves:
    def __init__(self, v=False):
        self.v = v
        try:
            self.load_config()
        except Exception as e:
            print(e)
            exit(1)
        
    def load_config(self, root="~", relpath=".config/gloves/config.py"):
        self.CONFIG_PATH = os.path.join(os.path.expanduser(root), relpath)
        import imp
        if os.path.exists(self.CONFIG_PATH):
            if self.v:
                print()
            self.config = imp.load_source("config", self.CONFIG_PATH)
        else:
            # In the case of portable use.
            print("Configuration file \'{}\' does not exists!".format(self.CONFIG_PATH))
            print("Trying of loading the \'example.config.py\' file")
            portable_config_path = "./example.config.py"
            if os.path.exists(portable_config_path):
                self.config = imp.load_source("config", portable_config_path)                
            else:
                raise FileExistsError(
                    "Configuration file does not exists!"
                )
        sections = [
            "squeezing_duration",
            "short_break_duration",
            "long_break_duration",
            "order",
            "alert_command",            
            "relax_command"
        ]
        for section in sections:
            missed = []
            if section not in dir(self.config):
                missed.append(section)
        if len(missed) is not 0:
            raise ImportError(
                "Some sections in the configuration file was missed out: {}".format(missed)
            )         
           
    def squeeze(self):
        if "order" in dir(self.config):
            print('start')
            
    def _timer(delay, func, *args, **kwargs):
        time.sleep(delay)
        return func(*args, **kwargs)
    

if __name__ == "__main__":
    gloves = Gloves()    

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--loop",
        help="Repeat all",
        action="store_true",
        default=False        
    )
    parser.add_argument(
        "--no-log",
        help="Disable logging",
        action="store_true"
    )
    parser.add_argument(
        "-f",
        "--config-file",
        help="Load a custom configuration file"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Increase output verbosity"
    )

    args = parser.parse_args()

    if args.loop:
        while True:
            gloves.squeeze()
    else:
        gloves.squeeze()
            
