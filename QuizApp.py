import re
import json

# Class for user management
class User:
    """
    Represents a user in the quiz app.
    Attributes:
        name (str): Name of the user.
        email (str): Email of the user.
        enrollment (str): Enrollment number of the user.
        password (str): Password of the user.
        results (list): Stores the user's quiz attempts and results.
    """
    def __init__(self, name, email, enrollment, password):
        self.name = name
        self.email = email
        self.enrollment = enrollment
        self.password = password
        self.results = []  # To save quiz attempts and results

# Quiz App Class
class QuizApp:
    """
    Quiz application class handling user registration, login, quizzes, and results.
    Attributes:
        users (dict): Stores registered users with email as the key.
        current_user (User): The currently logged-in user.
        questions (dict): Quiz questions categorized by subjects.
    """
    def __init__(self):
        self.users = {}
        self.current_user = None
        self.questions = {
            "1. Python Basics": [
                {
                    "question": "What is the output of 3 + 2 * 2?",
                    "options": ["10", "7", "9", "5"],
                    "answer": "7",
                    "description": "The order of operations in Python follows PEMDAS (Parentheses, Exponents, Multiplication/Division, Addition/Subtraction)."
                },
                {
                    "question": "Which keyword is used to define a function in Python?",
                    "options": ["func", "def", "function", "define"],
                    "answer": "def",
                    "description": "The 'def' keyword is used to define functions in Python."
                },
            ],
            "2. DBMS": [
                {
                    "question": "What does SQL stand for?",
                    "options": ["Structured Query Language", "Simple Query Language", "Sequential Query Language", "Standard Query Language"],
                    "answer": "Structured Query Language",
                    "description": "SQL stands for Structured Query Language, used to communicate with relational databases."
                },
                {
                    "question": "Which of the following is a primary key constraint?",
                    "options": ["Unique", "Null", "Duplicate", "Primary"],
                    "answer": "Unique",
                    "description": "The primary key constraint ensures unique identification of each row in a table."
                },
            ]
        }

    def register(self):
        """Registers a new user by collecting their details."""
        print("\n=== Register ===")
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("Invalid email format!")
            return
        enrollment = input("Enter your enrollment number: ")
        password = input("Create a password: ")
        confirm_password = input("Confirm your password: ")

        if password != confirm_password:
            print("Passwords do not match! Try again.")
            return

        if email in self.users:
            print("User already exists! Please login.")
            return

        self.users[email] = User(name, email, enrollment, password)
        print("Registration successful! Please login to continue.")

    def login(self):
        """Logs in an existing user by validating their email and password."""
        print("\n=== Login ===")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        if email in self.users and self.users[email].password == password:
            self.current_user = self.users[email]
            print(f"Welcome {self.current_user.name}!")
        else:
            print("Invalid email or password!")

    def take_quiz(self):
        """Allows the user to take a quiz, saves the result, and displays a summary."""
        if not self.current_user:
            print("Please login first!")
            return

        print("\n=== Quiz Section ===")
        print("Select a subject:")
        for key in self.questions.keys():
            print(key)

        try:
            subject_choice = input("Enter the subject number: ").strip()
            subject_key = next((key for key in self.questions if key.startswith(subject_choice)), None)
            if not subject_key:
                print("Invalid subject selection!")
                return

            score = {"correct": 0, "wrong": 0, "attempts": 0}
            for q in self.questions[subject_key]:
                print("\n" + q["question"])
                for i, option in enumerate(q["options"], 1):
                    print(f"{i}. {option}")

                while True:
                    try:
                        answer = int(input("Enter your choice (1-4): "))
                        if 1 <= answer <= 4:
                            chosen_option = q["options"][answer - 1]
                            score["attempts"] += 1
                            if chosen_option == q["answer"]:
                                print("Correct!")
                                print("Explanation:", q["description"])
                                score["correct"] += 1
                                break
                            else:
                                print("Wrong answer. Try again.")
                                score["wrong"] += 1
                        else:
                            print("Invalid choice. Please select a number between 1 and 4.")
                    except ValueError:
                        print("Invalid input. Please enter a number between 1 and 4.")

            self.current_user.results.append({
                "subject": subject_key.split(". ")[1],
                "correct": score["correct"],
                "wrong": score["wrong"],
                "attempts": score["attempts"]
            })

            print("\n=== Quiz Result ===")
            print(f"Subject: {subject_key.split('. ')[1]}")
            print(f"Correct Answers: {score['correct']}")
            print(f"Wrong Attempts: {score['wrong']}")
            print(f"Total Attempts: {score['attempts']}")

        except Exception as e:
            print("An unexpected error occurred:", str(e))

    def view_results(self):
        """Displays the results of all previous quizzes taken by the logged-in user."""
        if not self.current_user:
            print("Please login first!")
            return

        print("\n=== Previous Quiz Results ===")
        if not self.current_user.results:
            print("No quiz results found!")
            return

        for idx, result in enumerate(self.current_user.results, 1):
            print(f"\nAttempt {idx}:")
            print(f"Subject: {result['subject']}")
            print(f"Correct Answers: {result['correct']}")
            print(f"Wrong Attempts: {result['wrong']}")
            print(f"Total Attempts: {result['attempts']}")

    def start(self):
        """Starts the quiz app and provides options for registration, login, quiz, and results."""
        while True:
            print("\n=== Welcome to Quiz App ===")
            print("1. Register")
            print("2. Login")
            print("3. Take Quiz")
            print("4. View Results")
            print("5. Exit")

            choice = input("Enter your choice: ")
            if choice == "1":
                self.register()
            elif choice == "2":
                self.login()
            elif choice == "3":
                self.take_quiz()
            elif choice == "4":
                self.view_results()
            elif choice == "5":
                print("Thank you for using the Quiz App!")
                break
            else:
                print("Invalid choice! Please try again.")

# Run the app
if __name__ == "__main__":
    app = QuizApp()
    app.start()
