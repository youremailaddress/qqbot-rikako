class TimeUnit():
    def __init__(self,start,interval) -> None:
        self.start = start
        self.interval = interval
        assert self._correct_check()

    def _correct_check(self):
        try:
            self.start = int(self.start)
            self.interval = int(self.interval)
            return True
        except:
            return False

    def _in_same_minute(self,time1:int,time2:int):
        if int(time1)//60 == int(time2)//60:
            return True
        else:
            return False
    
    def __contains__(self,time:int):
        if isinstance(time,int) == False:
            return False
        if self.interval == 0:
            return self._in_same_minute(self.start,time)
        else:
            reslis = [self._in_same_minute(self.start+k*self.interval,time) for k in range((time-60-self.start)//self.interval,(time+60-self.start)//self.interval+1)]
            if True in reslis:
                return True
            else:
                return False