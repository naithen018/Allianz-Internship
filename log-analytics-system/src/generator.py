import os
import random
from collections import defaultdict, Counter, deque
from datetime import datetime, timedelta
from pprint import pprint
from config import (
    LOG_DIR,
    NUM_FILES,
    LOGS_PER_FILE
)

SERVICES = [
    "service_a",
    "service_b",
    "service_c",
    "auth_service",
    "payment_service"
]

LEVELS = ["INFO", "WARN", "ERROR"]

INFO_MESSAGES = [
    "Request completed in 120ms",
    "Connection established",
    "Heartbeat received",
    "User login successful",
    "Cache refreshed"
]

WARN_MESSAGES = [
    "Retry attempt 1",
    "Slow database response",
    "Memory usage high",
    "Rate limit approaching"
]

ERROR_MESSAGES = [
    "Timeout occurred",
    "Database connection failed",
    "Null pointer exception",
    "Service unavailable",
    "Authentication failed"
]


def random_message(level):
    if level == "INFO":
        return random.choice(INFO_MESSAGES)
    elif level == "WARN":
        return random.choice(WARN_MESSAGES)
    return random.choice(ERROR_MESSAGES)


def generate_logs():
    os.makedirs(LOG_DIR, exist_ok=True)

    start_time = datetime(2026, 3, 18, 0, 0, 0)

    for file_num in range(NUM_FILES):
        file_path = os.path.join(LOG_DIR, f"app_log_{file_num + 1}.log")

        with open(file_path, "w") as f:
            current_time = start_time

            for _ in range(LOGS_PER_FILE):
                current_time += timedelta(seconds=random.randint(1, 5))

                level = random.choices(
                    LEVELS,
                    weights=[70, 15, 15],
                    k=1
                )[0]

                service = random.choice(SERVICES)
                message = random_message(level)

                log_line = (
                    f"{current_time.strftime('%Y-%m-%d %H:%M:%S')} | "
                    f"{level} | {service} | {message}\n"
                )

                f.write(log_line)

    print("Synthetic logs generated successfully!")


if __name__ == "__main__":
    generate_logs()