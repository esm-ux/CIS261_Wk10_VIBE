# Esther Jean-Michel
# CIS261
# Vibe Coding

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional


class Student:
    """Student class with name, ID, test scores, and calculated average and grade."""
    
    def __init__(self, name: str, id: str) -> None:
        """Initialize a student with name and ID."""
        if not name.strip():
            raise ValueError("Student name cannot be empty.")
        if not id.strip():
            raise ValueError("Student ID cannot be empty.")
        
        self.name = name.strip()
        self.id = id.strip()
        self.test_scores: List[float] = []

    def set_score(self, test_number: int, score: float) -> None:
        """Set or update a test score."""
        if test_number < 1 or test_number > 3:
            raise ValueError("Test number must be 1, 2, or 3.")
        if score < 0 or score > 100:
            raise ValueError("Score must be between 0 and 100.")
        
        # Ensure list has at least test_number elements
        while len(self.test_scores) < test_number:
            self.test_scores.append(None)
        
        self.test_scores[test_number - 1] = score

    def get_score(self, test_number: int) -> Optional[float]:
        """Get a test score by test number."""
        if test_number < 1 or test_number > 3:
            raise ValueError("Test number must be 1, 2, or 3.")
        if test_number - 1 < len(self.test_scores):
            return self.test_scores[test_number - 1]
        return None

    @property
    def average(self) -> Optional[float]:
        """Calculate and return the average of all test scores."""
        scores = [s for s in self.test_scores if s is not None]
        if not scores:
            return None
        return sum(scores) / len(scores)

    @property
    def grade(self) -> str:
        """Calculate and return the letter grade based on average."""
        avg = self.average
        if avg is None:
            return "N/A"
        if avg >= 90:
            return "A"
        if avg >= 80:
            return "B"
        if avg >= 70:
            return "C"
        if avg >= 60:
            return "D"
        return "F"

    def report(self) -> str:
        """Generate a formatted report of the student's information."""
        scores_list = []
        for i, score in enumerate(self.test_scores, start=1):
            if score is not None:
                scores_list.append(f"Test {i}: {score}")
        
        average = self.average
        average_text = f"{average:.2f}" if average is not None else "N/A"
        scores_text = ", ".join(scores_list) if scores_list else "No scores entered"
        
        return (
            f"Student Name: {self.name}\n"
            f"Student ID: {self.id}\n"
            f"Scores: {scores_text}\n"
            f"Average: {average_text}\n"
            f"Letter Grade: {self.grade}"
        )


class StudentManager:
    """Manager class for handling multiple Student records."""
    
    def __init__(self, filename: str = "student_grades.txt") -> None:
        """Initialize the manager and load existing student records."""
        self.students: dict[str, Student] = {}
        self.filename = Path(filename)
        self.load_from_file()

    def add_student(self, name: str, student_id: str) -> Student:
        """Add a new student to the manager."""
        normalized_name = name.strip()
        if normalized_name in self.students:
            raise ValueError(f"A student named '{normalized_name}' already exists.")
        student = Student(name, student_id)
        self.students[normalized_name] = student
        return student

    def remove_student(self, name: str) -> None:
        """Remove a student by name."""
        normalized = name.strip()
        if normalized not in self.students:
            raise KeyError(f"No student named '{normalized}' was found.")
        del self.students[normalized]

    def get_student(self, name: str) -> Student:
        """Get a student by name."""
        normalized = name.strip()
        if normalized not in self.students:
            raise KeyError(f"No student named '{normalized}' was found.")
        return self.students[normalized]

    def search_student(self, name: str) -> List[Student]:
        """Search for students by partial name match (case-insensitive)."""
        normalized = name.strip().lower()
        results = [
            student for student in self.students.values()
            if normalized in student.name.lower()
        ]
        return sorted(results, key=lambda s: s.name)

    def list_students(self) -> List[Student]:
        """Get all students sorted by name."""
        return sorted(self.students.values(), key=lambda student: student.name)

    def get_class_statistics(self) -> dict:
        """Calculate class statistics (highest, lowest, and class average)."""
        students_with_scores = [
            s for s in self.students.values() if s.average is not None
        ]
        if not students_with_scores:
            return {
                "count": 0,
                "highest_average": None,
                "lowest_average": None,
                "class_average": None,
                "highest_student": None,
                "lowest_student": None,
            }
        
        averages = [s.average for s in students_with_scores]
        highest_student = max(students_with_scores, key=lambda s: s.average)
        lowest_student = min(students_with_scores, key=lambda s: s.average)
        
        return {
            "count": len(students_with_scores),
            "highest_average": max(averages),
            "lowest_average": min(averages),
            "class_average": sum(averages) / len(averages),
            "highest_student": highest_student,
            "lowest_student": lowest_student,
        }

    def save_to_file(self) -> None:
        """Save all student records to a JSON file with error handling."""
        try:
            data = []
            for student in self.students.values():
                data.append({
                    "name": student.name,
                    "id": student.id,
                    "test_scores": student.test_scores,
                })
            with open(self.filename, "w") as f:
                json.dump(data, f, indent=2)
            print(f"✓ Student records saved to {self.filename}")
        except IOError as e:
            print(f"✗ Error saving to file: {e}")
        except Exception as e:
            print(f"✗ Unexpected error during save: {e}")

    def load_from_file(self) -> None:
        """Load student records from a JSON file with error handling."""
        if not self.filename.exists():
            return
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
            for record in data:
                student = Student(record["name"], record["id"])
                student.test_scores = record.get("test_scores", [])
                self.students[student.name] = student
            if data:
                print(f"✓ Loaded {len(data)} student record(s) from file.\n")
        except json.JSONDecodeError as e:
            print(f"✗ Error: Invalid data format in file: {e}")
        except KeyError as e:
            print(f"✗ Error: Missing required field in file: {e}")
        except IOError as e:
            print(f"✗ Error reading file: {e}")
        except Exception as e:
            print(f"✗ Unexpected error during load: {e}")


def prompt_float(prompt_text: str) -> float:
    while True:
        value = input(prompt_text).strip()
        try:
            score = float(value)
            if score < 0 or score > 100:
                raise ValueError
            return score
        except ValueError:
            print("Please enter a valid score between 0 and 100.")


def show_menu() -> None:
    print("\n" + "=" * 50)
    print("         STUDENT RECORD MANAGER")
    print("=" * 50)
    print("1. Add new student (with three test scores)")
    print("2. Search for a student by name")
    print("3. Display all students in table format")
    print("4. Show class statistics")
    print("5. Show individual student report")
    print("6. Update a test score")
    print("7. Remove a student")
    print("8. Save and exit (or press ESC)")
    print("=" * 50)


def choose_student(manager: StudentManager) -> Optional[Student]:
    """Prompt user to select a student by name."""
    name = input("Enter student name: ").strip()
    if not name:
        print("Student name cannot be empty.")
        return None
    try:
        return manager.get_student(name)
    except KeyError as error:
        print(error)
        return None


def main() -> None:
    """Main program loop for Student Record Manager."""
    manager = StudentManager()
    
    print("\n" + "=" * 50)
    print("    WELCOME TO STUDENT RECORD MANAGER")
    print("=" * 50)

    while True:
        show_menu()
        choice = input("Select an option (or ESC to exit): ").strip()

        if choice.lower() == "esc" or choice == "\x1b" or choice == "8":
            if manager.students:
                manager.save_to_file()
            print("Thank you for using Student Record Manager. Goodbye!")
            break

        elif choice == "1":
            # Add new student with scores
            print("\n" + "-" * 50)
            print("ADD NEW STUDENT")
            print("-" * 50)
            name = input("Enter student name: ").strip()
            if not name:
                print("✗ Student name cannot be empty.\n")
                continue
            
            student_id = input("Enter student ID: ").strip()
            if not student_id:
                print("✗ Student ID cannot be empty.\n")
                continue
            
            try:
                student = manager.add_student(name, student_id)
                print(f"✓ Added student '{name}' (ID: {student_id}).")
                
                # Prompt for three test scores
                print("\nEnter the three test scores:")
                test1 = prompt_float("  Test 1 score (0-100): ")
                test2 = prompt_float("  Test 2 score (0-100): ")
                test3 = prompt_float("  Test 3 score (0-100): ")
                
                student.set_score(1, test1)
                student.set_score(2, test2)
                student.set_score(3, test3)
                print(f"✓ Scores recorded.")
                print(f"  Average: {student.average:.2f} | Grade: {student.grade}\n")
                manager.save_to_file()
            except ValueError as error:
                print(f"✗ Error: {error}\n")

        elif choice == "2":
            # Search for student
            print("\n" + "-" * 50)
            print("SEARCH FOR STUDENT")
            print("-" * 50)
            search_term = input("Enter student name to search: ").strip()
            if not search_term:
                print("✗ Search term cannot be empty.\n")
                continue
            results = manager.search_student(search_term)
            if not results:
                print(f"✗ No students found matching '{search_term}'.\n")
            else:
                print(f"✓ Found {len(results)} student(s):")
                print("-" * 70)
                print(f"{'Name':<20} {'ID':<10} {'Test 1':<8} {'Test 2':<8} {'Test 3':<8} {'Avg':<8} {'Grade':<6}")
                print("-" * 70)
                for student in results:
                    t1 = f"{student.get_score(1):.2f}" if student.get_score(1) is not None else "N/A"
                    t2 = f"{student.get_score(2):.2f}" if student.get_score(2) is not None else "N/A"
                    t3 = f"{student.get_score(3):.2f}" if student.get_score(3) is not None else "N/A"
                    avg = f"{student.average:.2f}" if student.average is not None else "N/A"
                    print(f"{student.name:<20} {student.id:<10} {t1:<8} {t2:<8} {t3:<8} {avg:<8} {student.grade:<6}")
                print("-" * 70 + "\n")

        elif choice == "3":
            # Display all students
            students = manager.list_students()
            if not students:
                print("\n✗ No students registered yet.\n")
                continue
            print("\n" + "=" * 70)
            print("ALL STUDENTS - FORMATTED TABLE")
            print("=" * 70)
            print(f"{'Name':<20} {'ID':<10} {'Test 1':<8} {'Test 2':<8} {'Test 3':<8} {'Avg':<8} {'Grade':<6}")
            print("-" * 70)
            for student in students:
                t1 = f"{student.get_score(1):.2f}" if student.get_score(1) is not None else "N/A"
                t2 = f"{student.get_score(2):.2f}" if student.get_score(2) is not None else "N/A"
                t3 = f"{student.get_score(3):.2f}" if student.get_score(3) is not None else "N/A"
                avg = f"{student.average:.2f}" if student.average is not None else "N/A"
                print(f"{student.name:<20} {student.id:<10} {t1:<8} {t2:<8} {t3:<8} {avg:<8} {student.grade:<6}")
            print("=" * 70 + "\n")

        elif choice == "4":
            # Display class statistics
            stats = manager.get_class_statistics()
            if stats["count"] == 0:
                print("\n✗ No students with scores yet.\n")
            else:
                print("\n" + "=" * 50)
                print("CLASS STATISTICS")
                print("=" * 50)
                print(f"Total Students with Scores: {stats['count']}")
                print(f"Highest Average: {stats['highest_average']:.2f} ({stats['highest_student'].name})")
                print(f"Lowest Average: {stats['lowest_average']:.2f} ({stats['lowest_student'].name})")
                print(f"Class Average: {stats['class_average']:.2f}")
                print("=" * 50 + "\n")

        elif choice == "5":
            # Show individual student report
            print("\n" + "-" * 50)
            student = choose_student(manager)
            if student is not None:
                print()
                print(student.report())
                print()

        elif choice == "6":
            # Update test score
            print("\n" + "-" * 50)
            print("UPDATE TEST SCORE")
            print("-" * 50)
            student = choose_student(manager)
            if student is None:
                continue
            print("\nCurrent scores:")
            t1 = f"{student.get_score(1):.2f}" if student.get_score(1) is not None else "Not set"
            t2 = f"{student.get_score(2):.2f}" if student.get_score(2) is not None else "Not set"
            t3 = f"{student.get_score(3):.2f}" if student.get_score(3) is not None else "Not set"
            print(f"  Test 1: {t1}")
            print(f"  Test 2: {t2}")
            print(f"  Test 3: {t3}")
            
            test_choice = input("Which test to update (1, 2, or 3)? ").strip()
            if test_choice in ["1", "2", "3"]:
                score = prompt_float(f"  Enter new Test {test_choice} score (0-100): ")
                student.set_score(int(test_choice), score)
                print(f"✓ Test {test_choice} updated.")
                print(f"  New average: {student.average:.2f} | Grade: {student.grade}\n")
                manager.save_to_file()
            else:
                print("✗ Invalid test number.\n")

        elif choice == "7":
            # Remove student
            print("\n" + "-" * 50)
            print("REMOVE STUDENT")
            print("-" * 50)
            name = input("Enter student name to remove: ").strip()
            if not name:
                print("✗ Student name cannot be empty.\n")
                continue
            try:
                manager.remove_student(name)
                print(f"✓ Removed student '{name}'.\n")
                manager.save_to_file()
            except KeyError as error:
                print(f"✗ Error: {error}\n")

        else:
            print("✗ Please choose a valid menu option (1-8) or press ESC to exit.\n")


if __name__ == "__main__":
    main()
