class IdGenerator:

    def __init__(self):
        self.count = 10

    def __call__(self) -> int:
        self.count += 1
        return self.count


class EventLogger:

    def __call__(self, event_code: str):
        print(event_code)


id_generator = IdGenerator()
event_logger = EventLogger()
