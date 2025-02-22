import json
import os
from typing import List, Dict, Any
from datetime import datetime
from tabulate import tabulate
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Constants for colors
MAIN_MENU_COLOR = Fore.CYAN
SUB_MENU_COLOR = Fore.BLUE
TABLE_HEADER_COLOR = Fore.YELLOW
TABLE_CONTENT_COLOR = Fore.GREEN

# Global counters for generating unique IDs
crn_counter = 1000
mem_id_counter = 1000

def generate_crn() -> int:
    """Generate a unique CRN for courses."""
    global crn_counter
    crn_counter += 1
    return crn_counter

def generate_mem_id() -> str:
    """Generate a unique member ID for employees and students."""
    global mem_id_counter
    mem_id_counter += 1
    return f"MEM{mem_id_counter}"

class FileHandler:
    """Handles reading and writing records to/from JSON files."""

    def __init__(self, file_name: str) -> None:
        self.__file_name = file_name

    def read_records_file(self) -> List[Dict[str, Any]]:
        """Read records from the JSON file."""
        if not os.path.isfile(self.__file_name):
            return []
        try:
            with open(self.__file_name, "r", encoding="UTF-8") as file:
                return [json.loads(line) for line in file]
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"{Fore.RED}Error reading file: {e}{Style.RESET_ALL}")
            return []

    def write_record(self, records: List[Dict[str, Any]]) -> None:
        """Write records to the JSON file."""
        try:
            with open(self.__file_name, "w", encoding="UTF-8") as file:
                for record in records:
                    file.write(json.dumps(record) + "\n")
        except IOError as e:
            print(f"{Fore.RED}Error writing to file: {e}{Style.RESET_ALL}")

class Course:
    """Represents a course with its details."""

    def __init__(self, subject: str, crn: int, start_date: datetime, end_date: datetime, start_time: str,
                 end_time: str, cost: float) -> None:
        self.__subject = subject
        self.__crn = crn
        self.__start_date = start_date
        self.__end_date = end_date
        self.__start_time = start_time
        self.__end_time = end_time
        self.__cost = cost

    def to_dict(self) -> Dict[str, Any]:
        """Convert the course object to a dictionary."""
        return {
            "Subject": self.__subject,
            "CRN": self.__crn,
            "Start Date": self.__start_date.isoformat(),
            "End Date": self.__end_date.isoformat(),
            "Start Time": self.__start_time,
            "End Time": self.__end_time,
            "Cost": self.__cost
        }

    @property
    def subject(self) -> str:
        return self.__subject

    @property
    def crn(self) -> int:
        return self.__crn

    @property
    def start_date(self) -> datetime:
        return self.__start_date

    @property
    def end_date(self) -> datetime:
        return self.__end_date

    @property
    def start_time(self) -> str:
        return self.__start_time

    @property
    def end_time(self) -> str:
        return self.__end_time

    @property
    def cost(self) -> float:
        return self.__cost

class Person(FileHandler):
    """Represents a person with basic details."""

    def __init__(self, name: str, mem_id: str, dob: datetime, address: Dict[str, str]) -> None:
        super().__init__("persons.json")
        self.__name = name
        self.__mem_id = mem_id
        self.__dob = dob
        self.__address = address

    def to_dict(self) -> Dict[str, Any]:
        """Convert the person object to a dictionary."""
        return {
            "Name": self.__name,
            "ID": self.__mem_id,
            "DOB": self.__dob.isoformat(),
            "Address": self.__address
        }

    @property
    def name(self) -> str:
        return self.__name

    @property
    def mem_id(self) -> str:
        return self.__mem_id

    @property
    def dob(self) -> datetime:
        return self.__dob

    @property
    def address(self) -> Dict[str, str]:
        return self.__address

class Employee(Person):
    """Represents an employee with additional details like department and salary."""

    BASE_SALARY = 30000  # Base salary for all employees
    PER_COURSE_BONUS = 5000  # Bonus per course assigned

    def __init__(self, name: str, mem_id: str, dob: datetime, address: Dict[str, str], department: str) -> None:
        super().__init__(name, mem_id, dob, address)
        self.__department = department
        self.__courses: List[Course] = []
        self.__salary = self.BASE_SALARY

    def assign_course(self, course: Course) -> None:
        """Assign a course to the employee and update their salary."""
        self.__courses.append(course)
        self.__salary = self.BASE_SALARY + (len(self.__courses) * self.PER_COURSE_BONUS)

    def remove_course(self, course: Course) -> None:
        """Remove a course from the employee and update their salary."""
        if course in self.__courses:
            self.__courses.remove(course)
            self.__salary = self.BASE_SALARY + (len(self.__courses) * self.PER_COURSE_BONUS)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the employee object to a dictionary."""
        person_dict = super().to_dict()
        person_dict.update({
            "Department": self.__department,
            "Courses": [course.to_dict() for course in self.__courses],
            "Salary": self.__salary
        })
        return person_dict

    @property
    def department(self) -> str:
        return self.__department

    @property
    def courses(self) -> List[Course]:
        return self.__courses

    @property
    def salary(self) -> float:
        return self.__salary

class Student(Person):
    """Represents a student with additional details like courses and balance."""

    def __init__(self, name: str, mem_id: str, dob: datetime, address: Dict[str, str], courses: List[str],
                 balance: float) -> None:
        super().__init__(name, mem_id, dob, address)
        self.__courses = courses
        self.__balance = balance

    def to_dict(self) -> Dict[str, Any]:
        """Convert the student object to a dictionary."""
        person_dict = super().to_dict()
        person_dict.update({
            "Courses": self.__courses,
            "Balance": self.__balance
        })
        return person_dict

    @property
    def courses(self) -> List[str]:
        return self.__courses

    @property
    def balance(self) -> float:
        return self.__balance

def main_menu() -> str:
    """Display the main menu and return the user's choice."""
    print(f"\n{MAIN_MENU_COLOR}--- Main Menu ---{Style.RESET_ALL}")
    print(f"{MAIN_MENU_COLOR}1. Admin{Style.RESET_ALL}")
    print(f"{MAIN_MENU_COLOR}2. Professor{Style.RESET_ALL}")
    print(f"{MAIN_MENU_COLOR}3. Student{Style.RESET_ALL}")
    print(f"{MAIN_MENU_COLOR}4. Exit{Style.RESET_ALL}")
    return input(f"{MAIN_MENU_COLOR}Enter your choice: {Style.RESET_ALL}")

def admin_menu() -> str:
    """Display the admin menu and return the user's choice."""
    print(f"\n{SUB_MENU_COLOR}--- Admin Menu ---{Style.RESET_ALL}")
    print(f"{SUB_MENU_COLOR}1. Add Employee{Style.RESET_ALL}")
    print(f"{SUB_MENU_COLOR}2. Add Student{Style.RESET_ALL}")
    print(f"{SUB_MENU_COLOR}3. Add Course{Style.RESET_ALL}")
    print(f"{SUB_MENU_COLOR}4. View Employees{Style.RESET_ALL}")
    print(f"{SUB_MENU_COLOR}5. View Students{Style.RESET_ALL}")
    print(f"{SUB_MENU_COLOR}6. View Courses{Style.RESET_ALL}")
    print(f"{SUB_MENU_COLOR}7. Assign Course to Employee{Style.RESET_ALL}")
    print(f"{SUB_MENU_COLOR}8. Back to Main Menu{Style.RESET_ALL}")
    return input(f"{SUB_MENU_COLOR}Enter your choice: {Style.RESET_ALL}")

def professor_menu() -> str:
    """Display the professor menu and return the user's choice."""
    print(f"\n{SUB_MENU_COLOR}--- Professor Menu ---{Style.RESET_ALL}")
    print(f"{SUB_MENU_COLOR}1. View Schedule (Assigned Courses){Style.RESET_ALL}")
    print(f"{SUB_MENU_COLOR}2. Unassign Course{Style.RESET_ALL}")
    print(f"{SUB_MENU_COLOR}3. View Monthly Salary{Style.RESET_ALL}")
    print(f"{SUB_MENU_COLOR}4. Back to Main Menu{Style.RESET_ALL}")
    return input(f"{SUB_MENU_COLOR}Enter your choice: {Style.RESET_ALL}")

def student_menu() -> str:
    """Display the student menu and return the user's choice."""
    print(f"\n{SUB_MENU_COLOR}--- Student Menu ---{Style.RESET_ALL}")
    print(f"{SUB_MENU_COLOR}1. View Courses{Style.RESET_ALL}")
    print(f"{SUB_MENU_COLOR}2. Check Balance{Style.RESET_ALL}")
    print(f"{SUB_MENU_COLOR}3. Register for Course{Style.RESET_ALL}")
    print(f"{SUB_MENU_COLOR}4. Unregister from Course{Style.RESET_ALL}")
    print(f"{SUB_MENU_COLOR}5. Back to Main Menu{Style.RESET_ALL}")
    return input(f"{SUB_MENU_COLOR}Enter your choice: {Style.RESET_ALL}")

def add_employee() -> None:
    """Add a new employee to the system."""
    print(f"\n{SUB_MENU_COLOR}--- Add Employee ---{Style.RESET_ALL}")
    name = input(f"{SUB_MENU_COLOR}Enter name: {Style.RESET_ALL}")
    mem_id = generate_mem_id()
    dob = datetime.strptime(input(f"{SUB_MENU_COLOR}Enter DOB (YYYY-MM-DD): {Style.RESET_ALL}"), "%Y-%m-%d")
    address = {
        "city": input(f"{SUB_MENU_COLOR}Enter city: {Style.RESET_ALL}"),
        "country": input(f"{SUB_MENU_COLOR}Enter country: {Style.RESET_ALL}"),
        "zip_code": input(f"{SUB_MENU_COLOR}Enter zip code: {Style.RESET_ALL}")
    }
    department = input(f"{SUB_MENU_COLOR}Enter department: {Style.RESET_ALL}")
    employee = Employee(name, mem_id, dob, address, department)
    file_handler = FileHandler("employees.json")
    records = file_handler.read_records_file()
    records.append(employee.to_dict())
    file_handler.write_record(records)
    print(f"{Fore.GREEN}Employee added successfully!{Style.RESET_ALL}")

def add_student() -> None:
    """Add a new student to the system."""
    print(f"\n{SUB_MENU_COLOR}--- Add Student ---{Style.RESET_ALL}")
    name = input(f"{SUB_MENU_COLOR}Enter name: {Style.RESET_ALL}")
    mem_id = generate_mem_id()
    dob = datetime.strptime(input(f"{SUB_MENU_COLOR}Enter DOB (YYYY-MM-DD): {Style.RESET_ALL}"), "%Y-%m-%d")
    address = {
        "city": input(f"{SUB_MENU_COLOR}Enter city: {Style.RESET_ALL}"),
        "country": input(f"{SUB_MENU_COLOR}Enter country: {Style.RESET_ALL}"),
        "zip_code": input(f"{SUB_MENU_COLOR}Enter zip code: {Style.RESET_ALL}")
    }
    courses = []
    balance = 0.0
    student = Student(name, mem_id, dob, address, courses, balance)
    file_handler = FileHandler("students.json")
    records = file_handler.read_records_file()
    records.append(student.to_dict())
    file_handler.write_record(records)
    print(f"{Fore.GREEN}Student added successfully!{Style.RESET_ALL}")

def add_course() -> None:
    """Add a new course to the system."""
    print(f"\n{SUB_MENU_COLOR}--- Add Course ---{Style.RESET_ALL}")
    subject = input(f"{SUB_MENU_COLOR}Enter subject: {Style.RESET_ALL}")
    crn = generate_crn()
    start_date = datetime.strptime(input(f"{SUB_MENU_COLOR}Enter start date (YYYY-MM-DD): {Style.RESET_ALL}"), "%Y-%m-%d")
    end_date = datetime.strptime(input(f"{SUB_MENU_COLOR}Enter end date (YYYY-MM-DD): {Style.RESET_ALL}"), "%Y-%m-%d")
    start_time = input(f"{SUB_MENU_COLOR}Enter start time (HH:MM): {Style.RESET_ALL}")
    end_time = input(f"{SUB_MENU_COLOR}Enter end time (HH:MM): {Style.RESET_ALL}")
    cost = float(input(f"{SUB_MENU_COLOR}Enter cost: {Style.RESET_ALL}"))
    course = Course(subject, crn, start_date, end_date, start_time, end_time, cost)
    file_handler = FileHandler("courses.json")
    records = file_handler.read_records_file()
    records.append(course.to_dict())
    file_handler.write_record(records)
    print(f"{Fore.GREEN}Course added successfully!{Style.RESET_ALL}")

def view_employees() -> None:
    """Display all employees in a table."""
    print(f"\n{SUB_MENU_COLOR}--- View Employees ---{Style.RESET_ALL}")
    file_handler = FileHandler("employees.json")
    records = file_handler.read_records_file()
    if not records:
        print(f"{TABLE_CONTENT_COLOR}No employees found.{Style.RESET_ALL}")
        return
    table_data = [
        [
            f"{TABLE_CONTENT_COLOR}{record.get('Name', 'N/A')}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{record.get('ID', 'N/A')}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{record.get('DOB', 'N/A')}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{record.get('Address', {}).get('city', 'N/A')}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{record.get('Address', {}).get('country', 'N/A')}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{record.get('Address', {}).get('zip_code', 'N/A')}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{record.get('Department', 'N/A')}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{len(record.get('Courses', []))}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{record.get('Salary', 'N/A')}{Style.RESET_ALL}"
        ]
        for record in records
    ]
    headers = [
        f"{TABLE_HEADER_COLOR}Name{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}ID{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}DOB{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}City{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}Country{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}Zip Code{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}Department{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}Courses Assigned{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}Salary{Style.RESET_ALL}"
    ]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def view_students() -> None:
    """Display all students in a table."""
    print(f"\n{SUB_MENU_COLOR}--- View Students ---{Style.RESET_ALL}")
    file_handler = FileHandler("students.json")
    records = file_handler.read_records_file()
    if not records:
        print(f"{TABLE_CONTENT_COLOR}No students found.{Style.RESET_ALL}")
        return
    table_data = [
        [
            f"{TABLE_CONTENT_COLOR}{record.get('Name', 'N/A')}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{record.get('ID', 'N/A')}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{record.get('DOB', 'N/A')}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{record.get('Address', {}).get('city', 'N/A')}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{record.get('Address', {}).get('country', 'N/A')}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{record.get('Address', {}).get('zip_code', 'N/A')}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{len(record.get('Courses', []))}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{record.get('Balance', 'N/A')}{Style.RESET_ALL}"
        ]
        for record in records
    ]
    headers = [
        f"{TABLE_HEADER_COLOR}Name{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}ID{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}DOB{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}City{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}Country{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}Zip Code{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}Courses Enrolled{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}Balance{Style.RESET_ALL}"
    ]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def view_courses() -> None:
    """Display all courses in a table."""
    print(f"\n{SUB_MENU_COLOR}--- View Courses ---{Style.RESET_ALL}")
    file_handler = FileHandler("courses.json")
    records = file_handler.read_records_file()
    if not records:
        print(f"{TABLE_CONTENT_COLOR}No courses found.{Style.RESET_ALL}")
        return
    table_data = [
        [
            f"{TABLE_CONTENT_COLOR}{record.get('Subject', 'N/A')}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{record.get('CRN', 'N/A')}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{record.get('Start Date', 'N/A')}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{record.get('End Date', 'N/A')}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{record.get('Start Time', 'N/A')}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{record.get('End Time', 'N/A')}{Style.RESET_ALL}",
            f"{TABLE_CONTENT_COLOR}{record.get('Cost', 'N/A')}{Style.RESET_ALL}"
        ]
        for record in records
    ]
    headers = [
        f"{TABLE_HEADER_COLOR}Subject{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}CRN{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}Start Date{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}End Date{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}Start Time{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}End Time{Style.RESET_ALL}",
        f"{TABLE_HEADER_COLOR}Cost{Style.RESET_ALL}"
    ]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def assign_course_to_employee() -> None:
    """Assign a course to an employee."""
    print(f"\n{SUB_MENU_COLOR}--- Assign Course to Employee ---{Style.RESET_ALL}")
    mem_id = input(f"{SUB_MENU_COLOR}Enter employee's member ID: {Style.RESET_ALL}")
    crn = int(input(f"{SUB_MENU_COLOR}Enter the CRN of the course to assign: {Style.RESET_ALL}"))

    # Load employees
    employee_handler = FileHandler("employees.json")
    employees = employee_handler.read_records_file()

    # Load courses
    course_handler = FileHandler("courses.json")
    courses = course_handler.read_records_file()

    # Find the employee
    employee_found = False
    for employee in employees:
        if employee["ID"] == mem_id:
            employee_found = True
            # Find the course
            course_found = False
            for course in courses:
                if course["CRN"] == crn:
                    course_found = True
                    # Assign the course
                    if "Courses" not in employee:
                        employee["Courses"] = []
                    employee["Courses"].append(course)
                    # Update salary
                    employee["Salary"] = Employee.BASE_SALARY + (len(employee["Courses"]) * Employee.PER_COURSE_BONUS)
                    employee_handler.write_record(employees)
                    print(f"{Fore.GREEN}Course {course['Subject']} assigned to {employee['Name']}.{Style.RESET_ALL}")
                    break
            if not course_found:
                print(f"{Fore.RED}Course not found.{Style.RESET_ALL}")
            break
    if not employee_found:
        print(f"{Fore.RED}Employee not found.{Style.RESET_ALL}")

def view_professor_schedule(mem_id: str) -> None:
    """Display the schedule of a professor."""
    print(f"\n{SUB_MENU_COLOR}--- Professor Schedule ---{Style.RESET_ALL}")
    file_handler = FileHandler("employees.json")
    records = file_handler.read_records_file()
    for record in records:
        if record["ID"] == mem_id:
            if "Courses" in record and record["Courses"]:
                table_data = [
                    [
                        f"{TABLE_CONTENT_COLOR}{course.get('Subject', 'N/A')}{Style.RESET_ALL}",
                        f"{TABLE_CONTENT_COLOR}{course.get('CRN', 'N/A')}{Style.RESET_ALL}",
                        f"{TABLE_CONTENT_COLOR}{course.get('Start Date', 'N/A')}{Style.RESET_ALL}",
                        f"{TABLE_CONTENT_COLOR}{course.get('End Date', 'N/A')}{Style.RESET_ALL}",
                        f"{TABLE_CONTENT_COLOR}{course.get('Start Time', 'N/A')}{Style.RESET_ALL}",
                        f"{TABLE_CONTENT_COLOR}{course.get('End Time', 'N/A')}{Style.RESET_ALL}"
                    ]
                    for course in record["Courses"]
                ]
                headers = [
                    f"{TABLE_HEADER_COLOR}Subject{Style.RESET_ALL}",
                    f"{TABLE_HEADER_COLOR}CRN{Style.RESET_ALL}",
                    f"{TABLE_HEADER_COLOR}Start Date{Style.RESET_ALL}",
                    f"{TABLE_HEADER_COLOR}End Date{Style.RESET_ALL}",
                    f"{TABLE_HEADER_COLOR}Start Time{Style.RESET_ALL}",
                    f"{TABLE_HEADER_COLOR}End Time{Style.RESET_ALL}"
                ]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
            else:
                print(f"{TABLE_CONTENT_COLOR}You have no assigned courses.{Style.RESET_ALL}")
            return
    print(f"{Fore.RED}Professor not found.{Style.RESET_ALL}")

def unassign_course(mem_id: str) -> None:
    """Unassign a course from a professor."""
    print(f"\n{SUB_MENU_COLOR}--- Unassign Course ---{Style.RESET_ALL}")
    file_handler = FileHandler("employees.json")
    records = file_handler.read_records_file()
    for record in records:
        if record["ID"] == mem_id:
            if "Courses" in record and record["Courses"]:
                print(f"{TABLE_HEADER_COLOR}Your Assigned Courses:{Style.RESET_ALL}")
                table_data = [
                    [
                        f"{TABLE_CONTENT_COLOR}{i + 1}{Style.RESET_ALL}",
                        f"{TABLE_CONTENT_COLOR}{course.get('Subject', 'N/A')}{Style.RESET_ALL}",
                        f"{TABLE_CONTENT_COLOR}{course.get('CRN', 'N/A')}{Style.RESET_ALL}",
                        f"{TABLE_CONTENT_COLOR}{course.get('Start Date', 'N/A')}{Style.RESET_ALL}",
                        f"{TABLE_CONTENT_COLOR}{course.get('End Date', 'N/A')}{Style.RESET_ALL}",
                        f"{TABLE_CONTENT_COLOR}{course.get('Start Time', 'N/A')}{Style.RESET_ALL}",
                        f"{TABLE_CONTENT_COLOR}{course.get('End Time', 'N/A')}{Style.RESET_ALL}"
                    ]
                    for i, course in enumerate(record["Courses"])
                ]
                headers = [
                    f"{TABLE_HEADER_COLOR}#{Style.RESET_ALL}",
                    f"{TABLE_HEADER_COLOR}Subject{Style.RESET_ALL}",
                    f"{TABLE_HEADER_COLOR}CRN{Style.RESET_ALL}",
                    f"{TABLE_HEADER_COLOR}Start Date{Style.RESET_ALL}",
                    f"{TABLE_HEADER_COLOR}End Date{Style.RESET_ALL}",
                    f"{TABLE_HEADER_COLOR}Start Time{Style.RESET_ALL}",
                    f"{TABLE_HEADER_COLOR}End Time{Style.RESET_ALL}"
                ]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
                try:
                    course_index = int(input(f"{SUB_MENU_COLOR}Enter the number of the course to unassign: {Style.RESET_ALL}")) - 1
                    if 0 <= course_index < len(record["Courses"]):
                        removed_course = record["Courses"].pop(course_index)
                        # Update salary after unassigning the course
                        record["Salary"] = Employee.BASE_SALARY + (len(record["Courses"]) * Employee.PER_COURSE_BONUS)
                        file_handler.write_record(records)
                        print(f"{Fore.GREEN}Course {removed_course['Subject']} unassigned successfully.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Invalid course number.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
            else:
                print(f"{TABLE_CONTENT_COLOR}You have no assigned courses to unassign.{Style.RESET_ALL}")
            return
    print(f"{Fore.RED}Professor not found.{Style.RESET_ALL}")

def view_monthly_salary(mem_id: str) -> None:
    """Display the monthly salary of a professor."""
    print(f"\n{SUB_MENU_COLOR}--- Monthly Salary ---{Style.RESET_ALL}")
    file_handler = FileHandler("employees.json")
    records = file_handler.read_records_file()
    for record in records:
        if record["ID"] == mem_id:
            print(f"{TABLE_CONTENT_COLOR}Your Monthly Salary: ${record['Salary']}{Style.RESET_ALL}")
            return
    print(f"{Fore.RED}Professor not found.{Style.RESET_ALL}")

def view_student_courses(mem_id: str) -> None:
    """Display the courses of a student."""
    print(f"\n{SUB_MENU_COLOR}--- Student Courses ---{Style.RESET_ALL}")
    file_handler = FileHandler("students.json")
    records = file_handler.read_records_file()
    for record in records:
        if record["ID"] == mem_id:
            if "Courses" in record and record["Courses"]:
                table_data = [
                    [f"{TABLE_CONTENT_COLOR}{i + 1}{Style.RESET_ALL}", f"{TABLE_CONTENT_COLOR}{course}{Style.RESET_ALL}"]
                    for i, course in enumerate(record["Courses"])
                ]
                headers = [f"{TABLE_HEADER_COLOR}#{Style.RESET_ALL}", f"{TABLE_HEADER_COLOR}Course{Style.RESET_ALL}"]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
            else:
                print(f"{TABLE_CONTENT_COLOR}You have no courses.{Style.RESET_ALL}")
            return
    print(f"{Fore.RED}Student not found.{Style.RESET_ALL}")

def check_student_balance(mem_id: str) -> None:
    """Display the balance of a student."""
    print(f"\n{SUB_MENU_COLOR}--- Student Balance ---{Style.RESET_ALL}")
    file_handler = FileHandler("students.json")
    records = file_handler.read_records_file()
    for record in records:
        if record["ID"] == mem_id:
            print(f"{TABLE_CONTENT_COLOR}Your Balance: ${record['Balance']}{Style.RESET_ALL}")
            return
    print(f"{Fore.RED}Student not found.{Style.RESET_ALL}")

def register_for_course(mem_id: str) -> None:
    """Register a student for a course."""
    print(f"\n{SUB_MENU_COLOR}--- Register for Course ---{Style.RESET_ALL}")
    file_handler = FileHandler("students.json")
    records = file_handler.read_records_file()
    for record in records:
        if record["ID"] == mem_id:
            # Check if the student already has 5 courses
            if len(record["Courses"]) >= 5:
                print(f"{Fore.RED}You cannot register for more than 5 courses.{Style.RESET_ALL}")
                return
            if record["Balance"] >= 10000:
                print(f"{Fore.RED}Your balance is too high to register for more courses.{Style.RESET_ALL}")
                return
            view_courses()
            try:
                crn = int(input(f"{SUB_MENU_COLOR}Enter the CRN of the course you want to register for: {Style.RESET_ALL}"))
                course_handler = FileHandler("courses.json")
                courses = course_handler.read_records_file()
                for course in courses:
                    if course["CRN"] == crn:
                        record["Courses"].append(course["Subject"])
                        record["Balance"] += course["Cost"]
                        file_handler.write_record(records)
                        print(f"{Fore.GREEN}Course registered successfully!{Style.RESET_ALL}")
                        return
                print(f"{Fore.RED}Course not found.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid input. Please enter a valid CRN.{Style.RESET_ALL}")
            return
    print(f"{Fore.RED}Student not found.{Style.RESET_ALL}")

def unregister_from_course(mem_id: str) -> None:
    """Unregister a student from a course."""
    print(f"\n{SUB_MENU_COLOR}--- Unregister from Course ---{Style.RESET_ALL}")
    file_handler = FileHandler("students.json")
    records = file_handler.read_records_file()
    for record in records:
        if record["ID"] == mem_id:
            if "Courses" in record and record["Courses"]:
                print(f"{TABLE_HEADER_COLOR}Your Enrolled Courses:{Style.RESET_ALL}")
                table_data = [
                    [f"{TABLE_CONTENT_COLOR}{i + 1}{Style.RESET_ALL}", f"{TABLE_CONTENT_COLOR}{course}{Style.RESET_ALL}"]
                    for i, course in enumerate(record["Courses"])
                ]
                headers = [f"{TABLE_HEADER_COLOR}#{Style.RESET_ALL}", f"{TABLE_HEADER_COLOR}Course{Style.RESET_ALL}"]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
                try:
                    course_index = int(input(f"{SUB_MENU_COLOR}Enter the number of the course to unregister: {Style.RESET_ALL}")) - 1
                    if 0 <= course_index < len(record["Courses"]):
                        removed_course = record["Courses"].pop(course_index)
                        # Deduct the course cost from the balance
                        course_handler = FileHandler("courses.json")
                        courses = course_handler.read_records_file()
                        for course in courses:
                            if course["Subject"] == removed_course:
                                record["Balance"] -= course["Cost"]
                                break
                        file_handler.write_record(records)
                        print(f"{Fore.GREEN}Course {removed_course} unregistered successfully.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Invalid course number.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
            else:
                print(f"{TABLE_CONTENT_COLOR}You have no courses to unregister.{Style.RESET_ALL}")
            return
    print(f"{Fore.RED}Student not found.{Style.RESET_ALL}")

def main() -> None:
    """Main function to run the program."""
    while True:
        choice = main_menu()
        if choice == "1":  # Admin
            while True:
                sub_choice = admin_menu()
                if sub_choice == "1":
                    add_employee()
                elif sub_choice == "2":
                    add_student()
                elif sub_choice == "3":
                    add_course()
                elif sub_choice == "4":
                    view_employees()
                elif sub_choice == "5":
                    view_students()
                elif sub_choice == "6":
                    view_courses()
                elif sub_choice == "7":
                    assign_course_to_employee()
                elif sub_choice == "8":
                    break
                else:
                    print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
        elif choice == "2":  # Professor
            mem_id = input(f"{SUB_MENU_COLOR}Enter your member ID: {Style.RESET_ALL}")
            while True:
                sub_choice = professor_menu()
                if sub_choice == "1":
                    view_professor_schedule(mem_id)
                elif sub_choice == "2":
                    unassign_course(mem_id)
                elif sub_choice == "3":
                    view_monthly_salary(mem_id)
                elif sub_choice == "4":
                    break
                else:
                    print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
        elif choice == "3":  # Student
            mem_id = input(f"{SUB_MENU_COLOR}Enter your member ID: {Style.RESET_ALL}")
            while True:
                sub_choice = student_menu()
                if sub_choice == "1":
                    view_student_courses(mem_id)
                elif sub_choice == "2":
                    check_student_balance(mem_id)
                elif sub_choice == "3":
                    register_for_course(mem_id)
                elif sub_choice == "4":
                    unregister_from_course(mem_id)
                elif sub_choice == "5":
                    break
                else:
                    print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
        elif choice == "4":  # Exit
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
    print(f"{Fore.CYAN}Thank you for using this program!{Style.RESET_ALL}")