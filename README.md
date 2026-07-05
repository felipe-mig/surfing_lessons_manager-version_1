# 🏄 Surfing Lessons Manager

A command-line application for managing surfing lesson sessions, student enrolments, and payment tracking.

---

## Features

- **Create lessons** — Set up sessions with instructor, day, time, beach location, board type, conditions, skills focus, and price per student.
- **View lessons** — Browse a summary table of all lessons or drill into full details for any session.
- **Enrol students** — Add students to a lesson (max 7 per session), with duplicate detection.
- **Track payments** — Mark individual students as paid and view collected vs outstanding revenue per lesson.
- **Persist data** — All lessons and student records are saved to and loaded from a plain-text file (`surfing_lessons.txt`).

---

## Getting Started

### Prerequisites

- Python 3.x (no external libraries required)

### Running the Program

```bash
python felipe_iglesias_garcia_COMP5002_A3.py
```

The program will load any existing lessons from `surfing_lessons.txt` in the same directory, or start fresh if the file doesn't exist.

---

## Usage

On launch, you'll see the main menu:

```
===========================================
      SURFING LESSONS MANAGER🏄
===========================================

  MAIN MENU
  1. 📋 View all lessons
  2. 🔍 View lesson details
  3. ➕ Create new lesson
  4. 🏄‍♂️ Enrol a student
  5. 💰 Indicate that a student has paid
  6. 💾 Save and exit
```

Select an option by entering its number. Changes are only written to disk when you choose **Save and exit (6)**.

---

## Data File Format

Lessons are stored in `surfing_lessons.txt` using a plain-text format:

```
TEACHER: John Smith
DAY: Saturday
TIME: 09:00
BEACH: Snapper Rocks
CONDITIONS: Sunny, 1-2m swell
BOARD: Blue Longboard
SKILLS: Paddling, pop-up technique
PRICE: 75.0
STUDENT: Jane Doe | False
STUDENT: Mark Lee | True
-------------------------------------------------------
```

---

## Project Structure

```
.
├── main.py   # Main application
└── surfing_lessons.txt                      # Auto-generated data file (created on first save)
```

---

## Configuration

The following constants at the top of the file can be adjusted:

| Constant | Default | Description |
|---|---|---|
| `DATA_FILE` | `surfing_lessons.txt` | Data file path |
| `LESSON_DURATION` | `2` | Duration of each lesson in hours |
| `MAX_STUDENTS` | `7` | Maximum students per lesson |
| `BEACHES` | *(list)* | Available beach locations |
| `BOARD_TYPES` | *(list)* | Available board types |

---

## Author

**Felipe Martin Iglesias Garcia**  

