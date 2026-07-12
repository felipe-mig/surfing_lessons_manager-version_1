# Student Name: [Felipe Martin Iglesias Garcia]
# Student ID: [25258376]
# COMP5002 Assessment 3: [Surfing Lessons Manager]

# ── Constants ─────────────────────────────────────────────────────────────────

DATA_FILE = "surfing_lessons.txt"
LESSON_DURATION = 2
MAX_STUDENTS = 7
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
BEACHES = ["Snapper Rocks", "Kirra Beach", "Coolangatta Beach", "Burleigh Heads", "Testing1!", "Byron Bay"]
BOARD_TYPES = ["Longboard", "Shortboard", "Training Board"]

# \033[91m String \033[0m <-- this chunk of code is setting the colour of the string based on the ANSI colours table.
# 91m <-- e.g. is the code for red, this is the part we change for each colour.
'''
    \033[ --> starts the ANSI escape sequence
    33 --> e.g. colour code for yellow (foreground)
    m --> applies the style
    \033[0m --> resets formatting back to normal
'''
BOARD_COLOURS = ["\033[97mWhite\033[0m",
                 "\033[93mYellow\033[0m", 
                 "\033[94mBlue\033[0m", 
                 "\033[91mRed\033[0m",
                 "\033[92mGreen\033[0m",
                 ]

# ── SurfLesson class ──────────────────────────────────────────────────────────

class SurfLesson:
    """Represent a single surf lesson session."""

    def __init__(self, teacher, day, time, beach, conditions, board, skills, price):
        """Initialise a surf lesson.

        Parameters:
            teacher (str): Instructor name
            day (str): Day of the week
            time (str): Start time (HH:MM)
            beach (str): Beach location
            conditions (str): Weather conditions
            board (str): Colour and type of board
            skills (str): Skills to train
            price (float): Price per student
        """
        self.teacher = teacher
        self.day = day
        self.time = time
        self.beach = beach
        self.conditions = conditions
        self.board = board
        self.skills = skills
        self.price = price
        self.students = []   # empty list to entry student with the arguments: [name, paid (bool)]

    def add_student(self, name):
        """Enrol a student in this lesson.

        Parameters:
            name (str): Student full name

        Returns:
            bool: True if enrolled, False if class full or duplicate name
        """
        if len(self.students) >= MAX_STUDENTS:
            return False
        for entry in self.students:
            if entry[0].lower() == name.lower():
                return False
        self.students.append([name, False])
        return True

    def indicate_payment(self, name):
        """Mark a student's payment as received.

        Parameters:
            name (str): Student name

        Returns:
            bool: True if found and updated, False otherwise
        """
        for entry in self.students:
            if entry[0].lower() == name.lower():
                entry[1] = True # key variable that will be used to control payment logic. 
                return True
        return False

    def get_revenue(self):
        """Calculate total revenue collected from paid students.

        Returns:
            float: Number of paid students multiplied by price
        """
        paid = 0
        for entry in self.students:
            if entry[1]: # [1] = true <-- from line 85
                paid += 1
        return paid * self.price

    def get_outstanding(self):
        """Calculate total amount still owed by unpaid students.

        Returns:
            float: Number of unpaid students multiplied by price
        """
        unpaid = 0
        for entry in self.students:
            if not entry[1]: # [1] = true <-- from line 85
                unpaid += 1
        return unpaid * self.price
    
    # (I asked Claude to help me create a table with a nice display) 
    def display(self):
        """Print a formatted summary of this lesson."""
        time_parts = self.time.split(":") if ":" in self.time else [self.time, "00"]
        end_hour = int(time_parts[0]) + LESSON_DURATION
        end_time = f"{end_hour:02d}:{time_parts[1]}"
        print(f"\n  {'─' * 50}")
        print(f"  Teacher    : {self.teacher}")
        print(f"  When       : {self.day}  {self.time} – {end_time}  ({LESSON_DURATION} hrs)")
        print(f"  Beach      : {self.beach}")
        print(f"  Board      : {self.board}")
        print(f"  Conditions : {self.conditions}")
        print(f"  Skills     : {self.skills}")
        print(f"  Price      : ${self.price:.2f} per student")
        print(f"\n  Students ({len(self.students)}/{MAX_STUDENTS}):")
        if not self.students:
            print("    (none enrolled)")
        else:
            print(f"  {'Name':<24} {'Paid':>5}  {'Owes':>8}")
            print(f"  {'─' * 40}")
            for entry in self.students:
                paid_label = "\033[32mYES\033[0m" if entry[1] else "\033[31mNO\033[0m"
                owes = "$0.00" if entry[1] else f"${self.price:.2f}"
                print(f"  {entry[0]:<24} {paid_label:>5}  {owes:>8}")
            print(f"  {'─' * 50}")  
            print(f"  Collected: ${self.get_revenue():.2f}   "
                  f"Outstanding: ${self.get_outstanding():.2f}")

# END class SurfLesson
# ── File functions ────────────────────────────────────────────────────────────

def load_lessons(filename):
    """Load lessons from a plain-text file.

    Parameters:
        filename (str): Path to the .txt data file

    Returns:
        list: List of SurfLesson objects, empty list if file not found
    """
    lessons = []
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
        current = None # This is reseting the variable so it doesn’t point to any previous data
        for line in lines:
            line = line.strip()
            if line == "":
                continue
            # (I asked Claude to help me find a way to read info from the .txt file in a way that makes sense for this program)
            # startwith method is checking if the line starts with a specific string, in this case TEACHER
            if line.startswith("TEACHER:"):
                current = {"teacher": line.split(":", 1)[1].strip(),
                           "day": "", "time": "", "beach": "",
                           "conditions": "", "board": "",
                           "skills": "", "price": 0.0, "students": []}
            elif current is not None: # This checks if there is any lesson on the .txt file
                if line.startswith("DAY:"):
                    current["day"] = line.split(":", 1)[1].strip()
                elif line.startswith("TIME:"):
                    current["time"] = line.split(":", 1)[1].strip()
                elif line.startswith("BEACH:"):
                    current["beach"] = line.split(":", 1)[1].strip()
                elif line.startswith("CONDITIONS:"):
                    current["conditions"] = line.split(":", 1)[1].strip()
                elif line.startswith("BOARD:"):
                    current["board"] = line.split(":", 1)[1].strip()
                elif line.startswith("SKILLS:"):
                    current["skills"] = line.split(":", 1)[1].strip()
                elif line.startswith("PRICE:"):
                    # Errors handling 
                    try:
                        current["price"] = float(line.split(":", 1)[1].strip())
                    except ValueError:
                        print(f"  Skipping invalid PRICE: '{line}'")
                        
                elif line.startswith("STUDENT:"):
                    
                    try:
                        parts = line.split(":", 1)[1].strip().split("|")
                        current["students"].append(
                            [parts[0].strip(), parts[1].strip() == "True"])
                    except (ValueError, IndexError):
                        print(f"Skipping invalid STUDENT: '{line}'")
                        
                elif line == "-------------------------------------------------------":
                    lesson = SurfLesson(
                        current["teacher"], current["day"], current["time"],
                        current["beach"], current["conditions"],
                        current["board"], current["skills"], current["price"]
                    )
                    for entry in current["students"]:
                        lesson.add_student(entry[0])
                        if entry[1]: # [1] = true <-- from line 85
                            lesson.indicate_payment(entry[0])
                    lessons.append(lesson)
                    current = None # This is reseting the variable so it doesn’t point to any previous data
    except FileNotFoundError:
        print("  No existing file found — starting fresh.")
    return lessons


def save_lessons(lessons, filename):
    """Save all lessons to a plain-text file.

    Parameters:
        lessons  (list): List of SurfLesson objects
        filename (str):  Path to the .txt data file
    """
    try:
        with open(filename, "w") as file:
            for lesson in lessons:
                file.write(f"TEACHER: {lesson.teacher}\n")
                file.write(f"DAY: {lesson.day}\n")
                file.write(f"TIME: {lesson.time}\n")
                file.write(f"BEACH: {lesson.beach}\n")
                file.write(f"CONDITIONS: {lesson.conditions}\n")
                file.write(f"BOARD: {lesson.board}\n")
                file.write(f"SKILLS: {lesson.skills}\n")
                file.write(f"PRICE: {lesson.price}\n")
                for entry in lesson.students:
                    file.write(f"STUDENT: {entry[0]} | {entry[1]}\n") # [1] = true <-- from line 85
                file.write("-------------------------------------------------------\n\n")
        print("  \nRecords saved")
    except OSError:
        print("ERROR: Could not save. Check disk space or permissions.")

# ── Control functions ──────────────────────────────────────────────────────────

# limit the user inputs to the numbers displayed on screen and avoids repetition 
def get_int_input(prompt, low, high):
    """ e.g. 
        1 to 3 for | 1.shortboard | 2.longboard | 3.trainingboard |
        The user cannot enter a number lower than 1 or higher than 3
    
    Prompt for a validated integer within [low, high].

    Parameters:
        prompt (str): Message to show to the user
        low    (int): Minimum acceptable value
        high   (int): Maximum acceptable value

    Returns:
        int: Valid integer entered by the user
    """
    while True:
        try:
            value = int(input(prompt).strip())
            if low <= value <= high:
                return value
            print(f"  Enter a number between {low} and {high}.")
        except ValueError:
            print("  Please only enter numbers!")


def list_lessons(lessons):
    """Print a one-line summary of every lesson with an index number.

    Parameters:
        lessons (list): List of SurfLesson objects
    """
    if not lessons:
        print("  No lessons on record.")
        return
    print(f"\n  {'#':<4} {'Teacher':<20} {'Day':<11} "
          f"{'Time':<7} {'Beach':<22} {'Students':>8}")
    print("  " + "-" * 75)
    for index_number, lesson in enumerate(lessons): # enumerate loops over the list and gets both the index position and the lesson (Claude suggest me to do it using this method)
        print(f"  {index_number + 1:<4} {lesson.teacher:<20} {lesson.day:<11} " f"{lesson.time:<7} {lesson.beach:<22} "f"{len(lesson.students):>4}/{MAX_STUDENTS}")

# ── Main program ──────────────────────────────────────────────────────────────

def main():
    """Run the Surfing Lessons Manager."""
    print("\n")
    print("=" * 43)
    print("     🌊 SURFING LESSONS MANAGER 🏄")
    print("=" * 43)

    lessons = load_lessons(DATA_FILE)
    print(f"  {len(lessons)} lesson(s) loaded.")

    while True:
        print("\n  MAIN MENU")
        print("  1.📋 View all lessons")
        print("  2.🔍 View lesson details")
        print("  3.➕ Create new lesson")
        print("  4.🏄‍♂️ Enrol a student")
        print("  5.💰 Indicate that a student has paid")
        print("  6.💾 Save and exit")

        choice = input("\n  Enter choice (1-6): ").strip()

        # ── 1. View all lessons ───────────────────────────────────────────────
        if choice == "1":
            list_lessons(lessons)

        # ── 2. View lesson details ────────────────────────────────────────────
        elif choice == "2":
            list_lessons(lessons)
            if not lessons:
                continue
            index = get_int_input("\nSelect Lesson number: ", 1, len(lessons))
            '''
                Accessing the correct lesson:
                Why [index - 1]?
                User enters 1 --> Python index 0
                User enters 2 --> Python index 1
                
                This is because Python lists use 0-based indexing and users think in 1-based numbering
            '''
            lessons[index - 1].display()

        # ── 3. Create new lesson ──────────────────────────────────────────────
        elif choice == "3":
            teacher = input("Instructor name: ").strip()
            if not teacher:
                print("Name cannot be empty.")
                continue
            # Create a formatted string. Loops through the list DAYS 
            # join method joins all those strings into one single line separated by commas
            # enumerate loops over the list and gets both the index position and the day name (Claude suggested me to do it using this method)
            print("\n Days:", ", ".join(f"{index_number + 1}.{day_name}" for index_number, day_name in enumerate(DAYS)))
            day = DAYS[get_int_input("Select day: ", 1, len(DAYS)) - 1]

            time_input = input("Start time (e.g. 08:00): ").strip()
            if not time_input:
                print("Time cannot be empty.")
                continue

            print("\nBeaches:", ", ".join(f"{index_number + 1}.{beach_name}" for index_number, beach_name in enumerate(BEACHES)))
            beach = BEACHES[get_int_input("Select beach: ", 1, len(BEACHES)) - 1]

            conditions = input("Conditions (e.g. Sunny, 1-2m swell): ").strip()
            if not conditions:
                print("Conditions cannot be empty.")
                continue

            print("\nBoard types:", ", ".join(f"{index_number + 1}.{board_type_name}" for index_number, board_type_name in enumerate(BOARD_TYPES)))
            board_type = BOARD_TYPES[get_int_input("Select board type: ", 1, len(BOARD_TYPES)) - 1]

            print("\nColours:", ", ".join(f"{index_number + 1}.{colour_name}" for index_number, colour_name in enumerate(BOARD_COLOURS)))
            board_colour = BOARD_COLOURS[get_int_input("Select board colour: ", 1, len(BOARD_COLOURS)) - 1]

            skills = input("Skills to train: ").strip()
            if not skills:
                print("Skills cannot be empty.")
                continue
            
            # Validate the user input    
            while True:
                try:
                    price = float(input("Price per student ($): ").strip())
                    if price > 0:
                        break
                    print("Price must be greater than 0.")
                except ValueError:
                    print("Enter a valid number (e.g. 75.00).")

            lessons.append(SurfLesson(teacher, day, time_input, beach, conditions, f"{board_colour} {board_type}", skills, price))
            print(f"\nLesson created: {teacher} | {day} {time_input} | {beach}")

        # ── 4. Enrol a student ────────────────────────────────────────────────
        elif choice == "4":
            list_lessons(lessons)
            if not lessons:
                continue
            index = get_int_input("Lesson number: ", 1, len(lessons))
            lesson = lessons[index - 1]
            if len(lesson.students) >= MAX_STUDENTS:
                print(f"Lesson is full ({MAX_STUDENTS} students max).")
                continue
            name = input("Student name: ").strip()
            if not name:
                print("Name cannot be empty.")
                continue
            if lesson.add_student(name):
                print(f"'{name}'enrolled." f"({len(lesson.students)}/{MAX_STUDENTS} students)")
            else:
                print(f"Could not enrol '{name}' student already enrolled.")

        # ── 5. Indiucate student has paid ───────────────────────────────────────────
        elif choice == "5":
            list_lessons(lessons)
            if not lessons:
                continue
            index = get_int_input("Lesson number: ", 1, len(lessons))
            lesson = lessons[index - 1]
            lesson.display()
            name = input("\nStudent name to mark as paid: ").strip()
            
            if lesson.indicate_payment(name):
                print(f"Payment recorded for '{name}'.")
            else:
                print(f"'{name}' not found in this lesson.")

        # ── 6. Save and exit ──────────────────────────────────────────────────
        elif choice == "6":
            save_lessons(lessons, DATA_FILE)
            print("\nGoodbye! 🤙🌊\n")
            break

        else:
            print("Please enter a number from 1 to 6.")

# this is checking if there is a program named main.  
if __name__ == "__main__":
    main()
