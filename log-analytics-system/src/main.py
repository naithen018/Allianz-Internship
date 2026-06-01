from generator import generate_logs
from processor import LogProcessor
from config import LOG_DIR


def main():

    print("Generating synthetic logs...")
    generate_logs()

    print("Processing logs...")
    processor = LogProcessor(LOG_DIR)

    processor.process_files()

    summary = processor.generate_summary()

    processor.save_summary(summary)

    print("\nProcessing complete!")
    print("Summary saved successfully.")


if __name__ == "__main__":
    main()