import sched, time
from datetime import datetime
from datetime import timedelta

now = datetime.now()
run_at = now + timedelta(hours=24)
delay = (run_at - now).total_seconds()
threading.Timer(delay, self.update).start()
