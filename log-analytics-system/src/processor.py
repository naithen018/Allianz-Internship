import os
import json
from collections import defaultdict, Counter, deque
from datetime import datetime, timedelta
from pprint import pprint
from config import (
    ERROR_THRESHOLD,
    WINDOW_SIZE_MINUTES,
    TOP_K,
    LOG_DIR,
    OUTPUT_DIR
)
class LogProcessor:
    def __init__(self, log_dir):
        self.log_dir = log_dir

        self.total_logs = 0
        self.level_counts = defaultdict(int)
        self.service_counts = defaultdict(int)
        self.service_errors = defaultdict(int)

        self.error_messages = Counter()
        self.anomalies = []

        self.error_window = deque()

    def parse_line(self, line):

        try:
            timestamp, level, service, message = [
                part.strip() for part in line.split("|", 3)
            ]

            return {
                "timestamp": datetime.strptime(
                    timestamp,
                    "%Y-%m-%d %H:%M:%S"
                ),
                "level": level,
                "service": service,
                "message": message
            }

        except Exception:
            return None

    def process_log(self, log):
        self.total_logs += 1

        level = log["level"]
        service = log["service"]

        self.level_counts[level] += 1
        self.service_counts[service] += 1

        if level == "ERROR":
            self.service_errors[service] += 1
            self.error_messages[log["message"]] += 1

            self.detect_anomaly(log["timestamp"])

    def detect_anomaly(self, timestamp):

        self.error_window.append(timestamp)

        window_start = timestamp - timedelta(minutes=WINDOW_SIZE_MINUTES)

        while self.error_window and self.error_window[0] < window_start:
            self.error_window.popleft()

        if len(self.error_window) > ERROR_THRESHOLD:
            self.anomalies.append({
                "window_start": self.error_window[0].strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "window_end": timestamp.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "error_count": len(self.error_window)
            })

    def process_files(self):

        for filename in os.listdir(self.log_dir):
            file_path = os.path.join(self.log_dir, filename)

            if not os.path.isfile(file_path):
                continue

            with open(file_path, "r") as file:
                for line in file:
                    parsed = self.parse_line(line)

                    if parsed:
                        self.process_log(parsed)

    def generate_summary(self):
        error_rate_per_service = {}

        for service in self.service_counts:
            total = self.service_counts[service]
            errors = self.service_errors[service]

            error_rate_per_service[service] = round(
                errors / total,
                4
            )

        return {
            "summary": {
                "total_logs": self.total_logs,
                "levels": dict(self.level_counts),
                "services": dict(self.service_counts),
                "error_rate_per_service": error_rate_per_service
            },
            "top_errors": [
                {
                    "message": msg,
                    "count": count
                }
                for msg, count in self.error_messages.most_common(TOP_K)
            ],
            "anomalies": self.anomalies
        }
    
    def save_summary(self, summary):

        os.makedirs(OUTPUT_DIR, exist_ok=True)

        output_file = os.path.join(
            OUTPUT_DIR,
            "summary.json"
        )

        with open(output_file, "w") as f:
            json.dump(
                summary,
                f,
                indent=4
            )

        print(f"Summary saved to {output_file}")
    
if __name__ == "__main__":

    processor = LogProcessor(LOG_DIR)

    processor.process_files()

    summary = processor.generate_summary()

    processor.save_summary(summary)

    print(summary)