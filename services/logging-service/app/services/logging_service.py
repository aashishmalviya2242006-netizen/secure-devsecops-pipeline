from app.schemas import LogCreate


class LoggingService:

    def __init__(self):
        self.logs = []
        self.next_id = 1

    def create_log(self, log: LogCreate):

        new_log = {
            "id": self.next_id,
            "service": log.service,
            "level": log.level,
            "message": log.message,
        }

        self.logs.append(new_log)
        self.next_id += 1

        return new_log

    def get_all_logs(self):
        return self.logs

    def get_log_by_id(self, log_id):

        for log in self.logs:
            if log["id"] == log_id:
                return log

        return None

    def delete_log(self, log_id):

        log = self.get_log_by_id(log_id)

        if log is None:
            return False

        self.logs.remove(log)

        return True


logging_service = LoggingService()
