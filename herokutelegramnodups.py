# -*- coding: utf-8 -*-
# @Author Michael Pavlov

import datetime
import time
import threading

class HerokuTgNoDups:

    def __init__(self, lifetime_seconds=1):
        self.sessions = {}
        self.lifetime_s = lifetime_seconds

    def in_cache(self, user_, command_):
        ts_ = datetime.datetime.now()
        key = str(user_) + str(command_)
        if self.sessions.get(key) is not None:
            # session exists, it means duplicate message received. Need to update timestamp
            self.sessions[key] = ts_
            print("update", self.sessions)
            return True
        else:
            # if nothing found need to create new item
            self.sessions[key] = ts_
            print("add", self.sessions)
            return False

    def gc(self, ts_):
        try:
            for key, value in self.sessions.copy().items():
                if value + datetime.timedelta(seconds=self.lifetime_s) < ts_:
                    print("remove", key)
                    self.sessions.pop(key)
        except Exception as e:
            print("error:", e)
            pass

    def run_gc(self):
        while True:
            current_ts = datetime.datetime.now()
            self.gc(current_ts)
            time.sleep(.500)

    def run(self):
        self.t_gc = threading.Thread(target=self.run_gc,daemon=True)
        self.t_gc.start()


if __name__ == '__main__':
    HD = HerokuTgNoDups()
    HD.run()
    print(HD.in_cache("user1","/start"))

