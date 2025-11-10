import json
import os

DATA_FILE = "data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"courses": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_course(data):
    name = input("Course name (e.g. MTH101): ").strip().upper()
    if name in data["courses"]:
        print("Course already exists.")
        return
    credit = input("Course credit (e.g. 3): ").strip()
    if not credit.isdigit():
        print("Invalid credit.")
        return
    data["courses"][name] = {
        "credit": int(credit),
        "scores": []
    }
    save_data(data)
    print(f"Added course: {name}")


def add_score(data):
    name = input("Course name: ").strip().upper()
    if name not in data["courses"]:
        print("Course not found.")
        return
    try:
        score = float(input("Enter score (0-100): "))
    except ValueError:
        print("Invalid score.")
        return

    if score < 0 or score > 100:
        print("Score must be between 0 and 100.")
        return

    data["courses"][name]["scores"].append(score)
    save_data(data)
    print(f"Added score {score} to {name}")


def calculate_course_average(scores):
    if not scores:
        return None
    return sum(scores) / len(scores)


def show_report(data):
    if not data["courses"]:
        print("No courses yet.")
        return

    total_weighted = 0
    total_credits = 0

    print("\n=== COURSE REPORT ===")
    for name, info in data["courses"].items():
        avg = calculate_course_average(info["scores"])
        credit = info["credit"]
        if avg is None:
            print(f"{name}: no scores yet (credit {credit})")
            continue
        print(f"{name}: avg = {avg:.2f} (credit {credit})")
        total_weighted += avg * credit
        total_credits += credit

    if total_credits > 0:
        overall = total_weighted / total_credits
        print(f"\nOverall weighted average: {overall:.2f}")
        if overall < 50:
            print("⚠ Warning: Your overall average is low. Time to lock in.")
        elif overall < 70:
            print("Keep pushing, you can do better.")
        else:
            print("🔥 Solid work. Keep it up.")
    print()


def menu():
    data = load_data()

    while True:
        print("=== UNI PROGRESS TRACKER ===")
        print("1. Add course")
        print("2. Add score to course")
        print("3. Show report")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_course(data)
        elif choice == "2":
            add_score(data)
        elif choice == "3":
            show_report(data)
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid option.\n")


if __name__ == "__main__":
    menu()

