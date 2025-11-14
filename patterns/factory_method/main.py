import json

from factory_method import ParserCreator
from master_exams_schedule_parser import MasterExamParserCreator
from master_lessons_schedule_parser import MasterLessonsParserCreator


# ---------------------------
# Client Code
# ---------------------------
def client_code(creator: ParserCreator, file_path: str, output_json: str):
    df = creator.process_schedule(file_path)
    data = df.to_dict(orient='records')

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Processed schedule:", data)

if __name__ == "__main__":
    print("📘 Running MASTER parser:")
    client_code(MasterLessonsParserCreator(), "../../master-lessons.pdf", "master-lessons.json")

    print("\n📗 Running EXAM parser:")
    client_code(MasterExamParserCreator(), "../../master-exams.pdf", "master-exams.json")
