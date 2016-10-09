#! /usr/bin/env python3

import time
import os
import argparse


class Gloves:
    def __init__(self):
        try:
            self.load_config()
        except Exception as e:
            print(e.with_traceback)
            exit(1)
        
    def load_config(self, root="~", relpath=".config/gloves/config.py"):
        self.CONFIG_PATH = os.path.join(os.path.expanduser(root), relpath)
        if os.path.exists(self.CONFIG_PATH):
            import imp
            self.config = imp.load_source("config", self.CONFIG_PATH)
        else:
            # In the case of portable use.
            print("Configuration file \'{}\' does not exists!".format(self.CONFIG_PATH))
            print("Trying of loading the \'example./config.py\' file")
            if os.path.exists("./example.config.py"):
                self.config = imp.load_source("config", "./config.py")
            else:
                raise FileExistsError(
                    "Configuration file does not exists!"
                )
                
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
        action="store_true"
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
    parser.parse_args()
