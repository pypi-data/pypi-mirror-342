from datetime import datetime


class LOG():
    def __init__(self, log: dict) -> None:
        self.log = log
        self.log['log_created_at'] = datetime.now()

    def __repr__(self) -> str:
        return self.log
