class TokenSystem:
    STATUS_NOT_START = 0
    STATUS_ALREADY_START = 1

    id: int
    topic: str
    bucket: int
    token_per_second: int
    status: int
    create_time: int
    update_time: int
