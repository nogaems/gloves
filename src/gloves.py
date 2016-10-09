#! /usr/bin/env python3

import time, os


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
            self.config = imp.load_source('config', self.CONFIG_PATH)
        else:
            raise FileExistsError(
                "Configuration file \'{}\' does not exists!".format(self.CONFIG_PATH)
            )
        
    def _timer(delay, func, *args, **kwargs):
        time.sleep(delay)
        return func(*args, **kwargs)
    

if __name__ == "__main__":
    gloves = Gloves()


