import psycopg2
from psycopg2 import Error

from datetime import datetime

print("\n--Database Interaction with PostgreSQL and Application Programming--\n")

#Connect to the PostgreSQL database
def connect():
    try:
        connection = psycopg2.connect(host="localhost", user="postgres", password="postgres", port=5432, database="students")
        return connection
    except:
        print("Error: Unable to connect to PostgreSQL\n")

#Retrieves and displays all records from the students table.
def getAllStudents():
    try:
        connection = connect()
        cursor = connection.cursor()

        # cursor.execute("""CREATE TABLE IF NOT EXISTS students (
        #     student_id SERIAL PRIMARY KEY,
        #     first_name TEXT NOT NULL,
        #     last_name TEXT NOT NULL,
        #     email TEXT NOT NULL UNIQUE,
        #     enrollment_date DATE);""")

        # cursor.execute("""INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
        # ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
        # ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
        # ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');""")

        #Retrieves all records
        cursor.execute("SELECT * FROM students") 
        #Fetch all rows to return a list of tuples
        students = cursor.fetchall()

        for student in students:
            print(student)


        cursor.close()
    except:
        print("Error: Unable to get all students\n")
    finally:
        if connection:
            connection.close()
        

#Inserts a new student record into the students table.
def addStudent(first_name, last_name, email, enrollment_date):
    try:
        connection = connect()
        cursor = connection.cursor()

        insert_query = "INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (first_name, last_name, email, enrollment_date))

        connection.commit()
        print("Student added successfully\n")
        cursor.close()

    except psycopg2.errors.UniqueViolation as error:
        print("Error: Email already exists\n")
        
    except (Exception, Error) as error:
        print("Error: unable to add student\n", error)
        
    finally:
        if connection:
            connection.close()

#Updates the email address for a student with the specified student_id.
def updateStudentEmail(student_id, new_email):
    try:
        connection = connect()
        cursor = connection.cursor()

        update_query = "UPDATE students SET email = %s WHERE student_id = %s"
        cursor.execute(update_query, (new_email, student_id))

        connection.commit()
        print("Email updated successfully\n")
        cursor.close()

    except (Exception, Error) as error:
        print("Error: unable to update email\n", error)

    finally:
        if connection:
            connection.close()

#Deletes the record of the student with the specified student_id.
def deleteStudent(student_id):
    try:
        connection = connect()
        cursor = connection.cursor()

        delete_query = "DELETE FROM students WHERE student_id = %s"
        cursor.execute(delete_query, (student_id,))

        connection.commit()
        print("Student deleted successfully")
        cursor.close()

    except (Exception, Error) as error:
        print("Error: unable deleting student\n", error)

    finally:
        if connection:
            connection.close()

def quit():
    try:
        connection = connect()
        cursor = connection.cursor()

        #Delete all data and reset the student_id
        cursor.execute("DELETE FROM students;")
        cursor.execute("ALTER SEQUENCE students_student_id_seq RESTART WITH 1")
        
        #Re-insert the original data
        initial_data = [
            ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
            ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
            ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02')
        ]
        cursor.executemany("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)", initial_data)
        
        connection.commit()
    except:
        print("Error: unable to reset table. Database is not resetted.\n")
    finally:
        if connection:
            connection.close()


def main():
    
    print("\nInput 0-4 to run the application:\n")
    print("Quit application: 0")
    print("Get all students from students table: 1")
    print("Add new student record: 2")
    print("Update email address of a student: 3")
    print("Delete a student record: 4\n")
    
    while True:
        try: 
            choice = int(input("\nChoose your number: "))

            if choice == 0:
                print("Quitting application and reseting database.\n")
                quit()
                return
            elif 1<=choice<=4:
                if choice == 1:
                    print("All students from students table:")
                    getAllStudents()
                elif choice == 2:
                    fname = input("Enter new student's first name: ")
                    lname = input("Enter new student's last name: ")
                    email = input("Enter new student's email: ")
                    date = input("Enter enrollment date in the format 'YYYY-MM-DD': ")
                    addStudent(fname, lname, email, date)
                elif choice == 3:
                    id = int(input("Enter student_id to update email: "))
                    newEmail = input("Enter new email: ")
                    updateStudentEmail(id, newEmail)
                elif choice == 4:
                    deleteId = input("Enter student_id to delete that student: ")
                    deleteStudent(deleteId)
            else:
                print("Error: Please enter an integer from 0 to 4.\n")

        except ValueError:
            print("Error: Please enter an integer from 0 to 4.\n")

main()