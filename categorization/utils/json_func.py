import json


def read(input_filepath: str) -> dict:
    with open(input_filepath, "r", encoding='utf-8') as read_file:
        return json.load(read_file)


def write(output_filepath: str, data_to_write: dict) -> None:
    with open(output_filepath, "w", encoding='utf-8') as write_file:
        json.dump(data_to_write, write_file, sort_keys=False, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    write("verified_receipt_test.json", read("verified_receipt.json"))