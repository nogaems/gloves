#! /usr/bin/env python3

import time, os

def timer(delay, func, *args, **kwargs):
    time.sleep(delay)
    return func(*args, **kwargs)

#timer(2, os.system, "xmessage -center mess")


class Config:
    def __init__(self):
        self.CONFIG_PATH = os.path.join(os.path.expanduser("~"),".config/gloves/config.py")
        if os.path.exists(self.CONFIG_PATH):
            print(123)
        else:
            raise FileExistsError(
                "Configuration file \'{}\' does not exists!".format(self.CONFIG_PATH)
            )

c = Config()



