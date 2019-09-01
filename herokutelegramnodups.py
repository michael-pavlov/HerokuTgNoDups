# -*- coding: utf-8 -*-
# @Author Michael Pavlov

import datetime
import time
import threading

class HerokuTgNoDups:

    def __init__(self, lifetime_seconds=1):
        self.sessions = []
        self.lifetime_s = lifetime_seconds

    def in_cache(self, user_, command_):
        ts_ = datetime.datetime.now()
        for session in self.sessions:
            if session["user"] == user_ and session["command"] == command_:
                # session exists, it means duplicate message received. Need to update timestamp
                session["ts"] = ts_
                print("update", session)
                return True

        # if nothing found need to create new item
        session = {}
        session["user"] = user_
        session["command"] = command_
        session["ts"] = ts_
        self.sessions.append(session)
        print("add", session)
        return False

    def gc(self, ts_):
        i = 0
        while i < len(self.sessions) and len(self.sessions) > 0:
            try:
                session = self.sessions[i]
                if session["ts"] + datetime.timedelta(seconds=self.lifetime_s) < ts_:
                    print("remove", session["ts"], ts_)
                    self.sessions.remove(session)
                else:
                    i += 1
            except Exception as e:
                pass

    def run_gc(self):
        while True:
            current_ts = datetime.datetime.now()
            self.gc(current_ts)
            time.sleep(1)

    def run(self):
        self.t_gc = threading.Thread(target=self.run_gc,daemon=True)
        self.t_gc.start()


if __name__ == '__main__':
    HD = HerokuTgNoDups()
    HD.run()
    print(HD.in_cache("user1","/start"))

