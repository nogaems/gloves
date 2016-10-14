#! /usr/bin/env python3

import time
import os
import sys
import argparse
import logging as log

class Gloves:
    def __init__(self, no_log=False):
        try:
            self.load_config()
        except Exception as e:
            log.error(e.args[0])
            exit(1)

        if no_log:
            def to_track(atom):
                pass
        else:
            abspath = os.path.expanduser(self.config.log_path)
            if not os.path.exists(abspath):
                try:
                    os.makedirs(abspath)
                except Exception as e:
                    log.error(e.args[0])
                    exit(1)
            def to_track(atom):
                with open(os.path.join(abspath, './gloves.hist'), 'a') as output:
                    output.write('{}\t{}\t{}\t{}\n'.format(
                        atom['type'],
                        atom['start'],
                        atom['stop'],
                        atom['default_time']
                    ))                    
                    exit(0)
                
            
        self.to_track = to_track
        
    def load_config(self, root="~", relpath=".config/gloves/config.py"):
        self.CONFIG_PATH = os.path.join(os.path.expanduser(root), relpath)
        import imp
        if os.path.exists(self.CONFIG_PATH):
            log.info("Trying to load the \'{}\' file...".format(self.CONFIG_PATH))
            self.config = imp.load_source("config", self.CONFIG_PATH)
        else:
            # In the case of portable use.
            log.info("Configuration file \'{}\' does not exists!".format(self.CONFIG_PATH))
            self.CONFIG_PATH = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),                
                "example.config.py"
            )
            log.info("Trying to load the \'{}\' file...".format(self.CONFIG_PATH))
            if os.path.exists(self.CONFIG_PATH):
                self.config = imp.load_source("config", self.CONFIG_PATH)            
            else:
                raise FileExistsError(
                    "Configuration file does not exists!"
                )

        sections = [
            "squeezing_duration",
            "short_break_duration",
            "long_break_duration",
            "sequence",
            "alert_command",            
            "relax_command"
        ]
        log.info("Check the configuration is correct...")
        for section in sections:
            missed = []
            if section not in dir(self.config):
                missed.append(section)
        if len(missed) is not 0:
            raise ImportError(
                "Some sections in the configuration file was missed out: {}".format(missed)
            )
        try:
            iter_test = iter(self.config.sequence)
        except TypeError as te:
            raise ImportError(te)
        if isinstance(self.config.sequence, str):
            self.config.sequence = self.config.sequence.split(' ')
        for action in self.config.sequence:
            if action not in ['g', 's', 'l']:
                log.error("Incorrect action \'{}\'".format(action))
                exit(1)
        
        log.info("Configuration file was loaded successfully!")
           
    def squeeze(self):
        log.info("Start squeezing!")
        for action in self.config.sequence:
            atom = {
                'start': time.strftime("%d.%m.%Y %H:%M:%S"),
                'type': action
            }
            if action is 'g':
                code = self._timer(
                    self.config.squeezing_duration,
                    os.system,
                    self.config.alert_command + "Stop working!"
                )
                atom['default_time'] = self.config.squeezing_duration
            if action is 's':
                code = self._timer(
                    self.config.short_break_duration,
                    os.system,
                    self.config.alert_command + "Start working!"   
                )
                atom['default_time'] = self.config.short_break_duration
            if action is 'l':
                code = self._time(
                    self.config.long_break_duration,
                    os.system,
                    self.config.alert_command + "Start working!"
                )
                atom['default_time'] = self.config.long_break_duration
            atom['stop'] = time.strftime("%d.%m.%Y %H:%M:%S")
            if code is 0:
                self.to_track(atom)
            else:
                # handling
                pass
            
    def _timer(self, delay, func, *args, **kwargs):
        import signal
        def stop(signum, frame):
            raise KeyboardInterrupt()
        signal.signal(signal.SIGTSTP, stop)
        start = time.time()
        while(time.time() - start < delay):
            code = 0
            try:
                left = delay - time.time() + start
                m, s = divmod(round(left), 60)
                print(" " * 80, end="\r")
                print("      Time Remaining: {0} m {1} s ({2:.3f})".format(m, s, left), end="\r")
                sys.stdout.flush()
                time.sleep(0.1)
            except (KeyboardInterrupt, EOFError) as err:
                def get_answer():
                    try:
                        return input("\n    Are you sure? (y/N): ")
                    except (KeyboardInterrupt, EOFError) as err:
                        return get_answer()                            
                waiting_start = time.time()                
                answer = get_answer()                    
                if answer is not "" and answer.upper() in ['Y', 'YES']:
                    code = 1
                    break
                else:
                    delay = delay + time.time() - waiting_start
        if code is 0:
            sys.stdout.write('      Time Remaining 0 m 0 s (0.000)\n')
            return func(*args, **kwargs)
        else:
            log.info("Aborting.")
            exit(1)
    

if __name__ == "__main__":
    
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
        help="Increase output verbosity",
        action="store_true"
    )
    args = parser.parse_args()
    
    if args.verbose:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        log.info("Verbose output.")
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")

    gloves = Gloves(no_log=args.no_log)

    if args.loop:
        while True:
            gloves.squeeze()
    else:
        gloves.squeeze()

