import re
import sqlite3
conn = sqlite3.connect("library.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys=ON")

#user table---
cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user(
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT CHECK(role IN ('admin','librarian','staff'))
                    );
               
                    """)

#Member Table----
cursor.execute("""
                    CREATE TABLE IF NOT EXISTS member(
                    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_name TEXT NOT NULL,
                    phone_number TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    address TEXT NOT NULL,
                    join_date TEXT NOT NULL,
                    member_role TEXT CHECK(member_role IN('teacher','student','staff'))
                    );
                """)


#Book Category---
cursor.execute("""
                    CREATE TABLE IF NOT EXISTS category(
                    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_name UNIQUE NOT NULL
                    );
                """)
#Book table---
#### cursor.execute("DROP TABLE IF EXISTS book")

cursor.execute("""
                    CREATE TABLE IF NOT EXISTS book(
                    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXt NOT NULL,
                    publisher TEXT NOT NULL,
                    category_id INTEGER,
                    quantity INTEGER NOT NULL,
                    available_copies INTEGER NOT NULL,
                    FOREIGN KEY (category_id) REFERENCES category(category_id) ON DELETE CASCADE
                    );
                """)   #clarify  title,author

#Issue return table--
cursor.execute("""
                    CREATE TABLE IF NOT EXISTS issue_return(
                    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER,
                    member_id INTEGER,
                    issue_date TEXT NOT NULL,
                    return_date TEXT,
                    due_date TEXT NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY (book_id) REFERENCES book(book_id) ON DELETE CASCADE,
                    FOREIGN KEY (member_id) REFERENCES member(member_id) ON DELETE CASCADE
                    );
                """)

#Staff Information----
cursor.execute("""
                    CREATE TABLE IF NOT EXISTS staff_information(
                    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    staff_name TEXT NOT  NULL,
                    staff_email TEXT NOT NULL,
                    staff_phone TEXT NOT NULL,
                    shift TEXT NOT NULL,
                    joining_date TEXT NOT NULL,
                    staff_role TEXT CHECK(staff_role IN('admin','librarian','assistant'))
                    );
                """)

conn.commit()


#------------------------Fetch books with category join------------------------------------
def view_book_category():
    cursor.execute("""
                        SELECT
                        book.book_id,
                        book.title,
                        category.category_name
                        FROM book
                        JOIN category ON book.category_id=category.category_id
                     """)
    print("="*15,"BOOK CATEGORY","="*15)
    book_list=cursor.fetchall()
    for books in book_list:
        print(books[0],"-",books[2],"--",books[1])

#-------------------------Add Category-------------------------------------------------------
def add_category():
    print("---Add Category---")
    while True:
        category_name=input("Enter category name(or 0 to stop): ")
        if category_name == 0:
            print("Category entry stopped by user")
            break
        cursor.execute(" INSERT INTO category(category_name) VALUES (?)",(category_name,))
        conn.commit()
        print("Category added successfully...")
#----------------------------View Category---------------------------------------------------
def view_category():
    print("="*15,"BOOK CATEGORY","="*15)
    cursor.execute("SELECT * FROM  category")
    show_category=cursor.fetchall()
    for category in show_category:
        print(category[0],"-",category[1])
#---------------------------Delete Category---------------------------------------------------
def delete_category():
    print("---Delete Category---")
    while True:
        view_category()
        try:
             book_category_id=input("Enter category ID to delete (o to stop): ")
        except ValueError:
            print("Invalid category ID! Enter numbers only")
            continue
        cursor.execute("SELECT * FROM category WHERE category_id=?",
                       (book_category_id,))  # search any data ,then delete found data
        found = cursor.fetchone()
        if book_category_id == 0:
            print("Category delete stopped by user")
            break
        elif found:
            cursor.execute("DELETE FROM category WHERE category_id=?",(book_category_id,))
            print("Category Deleted...")
        else:
            print("Category not found....")
        conn.commit()
#---------------------------Update Category----------------------------------------------------
def update_category():
    print("---Update Category---")
    while True:
        try:
             category_id=int(input("Enter category ID (or 0 to stop): "))
        except ValueError:
            print("Invalid category ID! Enter numbers only")
            continue
        cursor.execute("SELECT * FROM category WHERE category_id=?",(category_id,))
        old_category=cursor.fetchone()
        if category_id == 0:
            print("Category entry stopped by user")
            break
        elif old_category:
            update_category_name=input(f"Enter category name '{old_category[1]}' to update: ': ") or old_category[1]
            cursor.execute("""
                                UPDATE category SET category_name=? WHERE category_id=?
                                """,(update_category_name,category_id))
            print("Category updated....")
            conn.commit()
        else:
            print("Category not found....")



#----------------------------Add Book ----------------------------------------------------------
def add_book():
    while True:
        view_category()
        print("---Add Book---")
        print("-"*15)
        try:
            input_category_id = int(input("Choose category ID (or o to stop): "))
        except ValueError:
            print("Invalid category ID! Enter numbers only")
            continue
        cursor.execute("SELECT * FROM category WHERE category_id=?",(input_category_id,))
        found=cursor.fetchone()

        if input_category_id == 0:
            print("Book entry stopped by user")
            break
        elif found:

            while True:
                title = input("Enter book title: ")
                if re.fullmatch(r"[A-Za-z0-9 .,-]+", title):
                    break
                else:
                    print("Invalid title! Use letters and numbers only")


            while True:
                author = input("Enter book author: ")
                if re.fullmatch(r"[A-Za-z .]+", author):
                    break
                else:
                    print("Invalid author name! Letters only")

            while True:
                publisher = input("Enter book publisher: ")
                if re.fullmatch(r"[A-Za-z0-9 .,-]+", publisher):
                    break
                else:
                    print("Invalid publisher! Use letters and numbers only")

            while True:
                quantity = input("Enter book quantity: ")
                if re.fullmatch(r"[0-9]+",quantity ):
                    quantity = int(quantity)
                    break
                else:
                    print("Invalid quantity! Enter numbers only")
            while True:
                available_copies=input("Enter book available copies: ")
                if re.fullmatch(r"[0-9]+", available_copies):
                    available_copies = int(available_copies)
                    break
                else:
                    print("Invalid quantity! Enter numbers only")

            cursor.execute("""INSERT INTO book(category_id,title,author,publisher,quantity,available_copies)
                            VALUES(?,?,?,?,?,?);""",(input_category_id,title,author,publisher,quantity,available_copies))
            conn.commit()
            print("Book added successfully....")
        else:
            print("Book not found!")

# --------------------------Delete Book--------------------------------------------------------
def delete_book():
    print("Choose Book ID for delete book")
    while True:
        view_book_category()
        print("---Delete Book---")
        try:
            book_id=int(input("Which book do you want in delete. Enter book ID (o to stop):"))
        except ValueError:
            print("Invalid book ID! Enter numbers only")
            continue
        if book_id == 0:
            print("Book entry stopped by user")
            break
        cursor.execute("SELECT * FROM book WHERE book_id=?",(book_id,))
        found=cursor.fetchone()
        if found:
            cursor.execute("DELETE FROM book WHERE book_id=?",(book_id,))
            conn.commit()
            print("Book Deleted...")
        else:
            print("Book not found....")
#---------------------------Update Book----------------------------------------------------------
def update_book():
    while True:
        print("Choose Book ID to update: ")
        view_book_category()
        print("Update Book")
        print("-" * 15)
        try:
            book_id=int(input("Enter book id to update (o to stop): "))
        except ValueError:
            print("Invalid book ID! Enter numbers only")
            continue
        cursor.execute("SELECT * FROM book WHERE book_id=?",(book_id,))
        old_data=cursor.fetchone()
        # print(old_data)
        if book_id == 0:
            print("Book update stopped by user")
            break
        elif old_data:
            while True:
                update_title = input(f"New book title '{old_data[1]}': ") or old_data[0]
                if re.fullmatch(r"[A-Za-z0-9 .,-]+", update_title):
                    break
                else:
                    print("Invalid title! Letters and numbers only")

            while True:
                update_author = input(f"New book author '{old_data[2]}': ") or old_data[2]
                if re.fullmatch(r"[A-Za-z .]+", update_author):
                    break
                else:
                    print("Invalid author! Letters only")

            while True:
                update_publisher = input(f"New book publisher '{old_data[3]}': ") or old_data[3]
                if re.fullmatch(r"[A-Za-z0-9 .,-]+", update_publisher):
                    break
                else:
                    print("Invalid publisher input")
            while True:
                update_category_id = input(f"New category id '{old_data[4]}': ") or old_data[4]
                if re.fullmatch(r"[0-9]+", str(update_category_id)):
                    update_category_id = int(update_category_id)
                    break
                else:
                    print("Invalid category ID! Numbers only")
            while True:
                update_quantity = input(f"New book quantity '{old_data[5]}': ") or old_data[5]
                if re.fullmatch(r"[0-9]+", str(update_quantity)):
                    update_quantity = int(update_quantity)
                    break
                else:
                    print("Invalid quantity! Numbers only")
            while True:
                update_available_copies = input(f"Enter book available copies '{old_data[6]}': ") or old_data[6]
                if re.fullmatch(r"[0-9]+", str(update_available_copies)):
                    update_available_copies = int(update_available_copies)
                    break
                else:
                    print("Invalid input! Enter numbers only")
            cursor.execute("""
                                UPDATE book
                                SET title=?, author=?, publisher=?, category_id=?,
                                quantity=?, available_copies=?
                                WHERE book_id=?
                            """,(update_title,update_author,update_publisher,
                                 update_category_id,update_quantity,update_available_copies,book_id))
            conn.commit()
            print("Book Updated successfully...")

        else:
            print("Book not found")

#------------------------------View Book-------------------------------------------------------------

def view_book_data():
    print("=" * 20, "BOOK DATA", "=" * 20)
    cursor.execute("SELECT * FROM  book")
    show_book = cursor.fetchall()
    for b in show_book:
       print(f"{b[0]} - {b[1]} - {b[2]} - {b[3]} - {b[4]} - {b[5]} - {b[6]}")

#-----------------------------Search Books----------------------------------------------------------
def search_books():
    cursor.execute("SELECT book_id,title FROM book" )
    show_book=cursor.fetchall()
    print(" AVAILABLE BOOKS:")
    print("-"*15)
    for s in show_book:
        print(s[0],"-",s[1])

#---------------------------Check Book Availability------------------------------------------------
def check_available_copies():
    print("-"*15,"CHECK BOOK AVAILABILITY","-"*15)
    while True:
        try:
            book_id = int(input("Enter book id to check (or 0 to stop): "))
        except ValueError:
            print("Invalid book ID! Enter numbers only")
            continue
        if book_id == 0:
            print("Check book availability stopped by user.")
            break
        cursor.execute(
            "SELECT available_copies FROM book WHERE book_id=?",
            (book_id,))

        check_copies = cursor.fetchone()

        if check_copies:
            if check_copies[0] <= 0:
                print("Book not available!!!")
            else:
                print("Available copies:", check_copies[0])
        else:
            print("Book not found!!!")

#---------------------------Show Book Availability---------------------------------------------
def show_book_availability():
    cursor.execute("SELECT book_id,title,available_copies FROM book")
    show_copies = cursor.fetchall()
    print()
    print("-" * 20, "SHOW BOOK AVAILABILITY", "-" * 20)
    print()
    for book in show_copies:
        print(f"Book ID: {book[0]}   Book Name:{book[1]}    Copies:{book[2]}")

#----------------------- ----Add Member-------------------------------------------------------
def add_member():
    while True:
        print("Add Member")
        print("-" * 15)
        member_name=input("Enter member name(or 0 to stop):")
        if member_name == "0":
            print("Member add stopped by user")
            break
        else:
            input_phone=input("Enter phone number:")
            input_email=input("Enter email:")
            input_address=input("Enter address:")
            input_join_date=input("Enter join date:")
            input_role=input("Enter  Member role (teacher/student/staff'):")

            cursor.execute("""
                                INSERT INTO member(member_name,phone_number,email,address,join_date,member_role)
                                VALUES(?,?,?,?,?,?);""",
                        (member_name,input_phone,input_email,input_address,input_join_date,input_role))

            conn.commit()
            print("Member added successfully...")

#-------------------------- Delete Member------------------------------------------------------------
def delete_member():
    while True:
        print("Delete Member")
        print("-" * 15)
        try:
             member_id=int(input("Enter member id (or 0 to stop):"))
        except ValueError:
            print("Invalid member id!! Enter number only")
            continue
        cursor.execute("SELECT * FROM member WHERE member_id=?",(member_id,))
        member_data=cursor.fetchone()
        # print(member_data)
        if member_id==0:
            print("member delete stopped by user")
            break
        elif member_data:
            cursor.execute("DELETE FROM member WHERE member_id=?", (member_id,))
            conn.commit()
            print("Member Deleted...")
        else:
            print("Member not found!")

#-----------------------------Update member------------------------------------------------------------
def update_member():
    while True:
        print("Update Member")
        print("-" * 15)
        try:
             member_id=int(input("Enter member id (or 0 to stop):"))
        except ValueError:
            print("Invalid member id!! Enter number only")
            continue
        cursor.execute("SELECT * FROM member WHERE member_id=?",(member_id,))
        old_member=cursor.fetchone()
        if member_id==0:
            print("Member update stopped by user")
            break
        elif old_member:
                    update_member_name=input(f"New member name '{old_member[1]}':") or old_member[1]
                    update_phone=input(f"New phone number '{old_member[2]}':") or old_member[2]
                    update_email=input(f"New email '{old_member[3]}':") or old_member[3]
                    update_address=input(f"New address '{old_member[4]}':") or old_member[4]
                    update_join_date=input(f"New join date '{old_member[5]}':") or old_member[5]
                    update_role=input(f"New Member role (teacher/student/staff')'{old_member[6]}':") or old_member[6]

                    cursor.execute("""
                                         UPDATE member
                                         SET member_name=?,phone_number=?,email=?,address=?,join_date=?,member_role=?
                                         WHERE member_id=?
                                       """, (update_member_name,update_phone,update_email,
                                             update_address,update_join_date,update_role,member_id))
                    conn.commit()
                    print("Member Updated successfully...")
                    print("-"*20)
        else:
            print("Member not found!!!")
#--------------------------------View Member-------------------------------------------------------
def view_all_members():
    print("-"*25,"ALL MEMBERS DATA","-"*25)
    cursor.execute("SELECT * FROM  member")
    show_member=cursor.fetchall()
    for member in show_member:
        print(f"{member[0]} - {member[1]} - {member[2]} - {member[3]} - {member[4]} - {member[5]}")

#--------------------------------Search Members------------------------------------------------------
def search_member_list():
    cursor.execute("SELECT member_id, member_name FROM member" )
    search_members=cursor.fetchall()
    print("ALL MEMBERS LIST:")
    print("-"*20)
    for member in search_members:
        print(member[0],"-",member[1])
#---------------------------------------Search one member data----------------------------------------
def search_one_member():
    while True:
        try:
            member_id=int(input("Enter member id (or 0 to stop):"))
        except ValueError:
            print("Invalid member id!! Enter number only")
            continue
        if member_id==0:
            print("member search stopped by user")
            break
        cursor.execute("SELECT * FROM member WHERE member_id=?",(member_id,)  )
        search_member=cursor.fetchone()
        print(f"{search_member[1]} - {search_member[2]} - {search_member[3]} - {search_member[4]} - {search_member[5]}")


#-----------------------------Add staff Information---------------------------------------------------
def add_staff_information():
    while True:
        print("---Add Staff---")
        staff_name=input("Enter staff name (or 0 to stop): ")
        if staff_name=="0":
            print("Staff add stopped  by user ")
            break
        else:
            staff_email=input("Enter staff email: ")
            staff_phone=input("Enter staff phone: ")
            shift=input("Enter shift: ")
            joining_date=input("Enter joining date: ")
            staff_role=input("Enter staff role (Admin/Librarian/Assistant): ")
            cursor.execute("""
                                INSERT INTO staff_information
                                (staff_name,staff_email,staff_phone,shift,joining_date,staff_role)
                                VALUES (?,?,?,?,?,?);""",
                           (staff_name,staff_email,staff_phone,shift,joining_date,staff_role))
            conn.commit()
            print("Staff information added successfully...")
            print("-"*20)
#--------------------------Update Staff Information----------------------------------------------
def update_staff_information():
    while True:
        print("--- Update Staff---")
        try:
            staff_id=int(input("Enter staff ID (or 0 to stop): "))
        except ValueError:
            print("Invalid staff ID!! Enter number only")
            continue
        cursor.execute("SELECT * FROM staff_information WHERE staff_id=?",(staff_id,))
        old_staff=cursor.fetchone()

        if staff_id==0:
            print("Update staff stopped by user")
            break
        elif old_staff:
            update_staff_name=input(f"Update staff name '{old_staff[1]}': ") or old_staff[1]
            update_email=input(f"Update staff email '{old_staff[2]}': ") or old_staff[2]
            update_phone=input(f"Update staff phone '{old_staff[3]}': ") or old_staff[3]
            update_shift=input(f"Update staff shift '{old_staff[4]}': ") or old_staff[4]
            update_join_date=input(f"Update staff join date '{old_staff[5]}': ") or old_staff[5]
            update_role=input(f"Update staff role (Admin/Librarian/Assistant)'{old_staff[6]}': ") or old_staff[6]

            cursor.execute("""
                                UPDATE staff_information
                                SET staff_name=?,staff_email=?,staff_phone=?,shift=?,joining_date=?,staff_role=?
                                WHERE staff_id=?""",
                                (update_staff_name,update_email,update_phone,
                                 update_shift,update_join_date,update_role,staff_id))
            conn.commit()
            print("Update staff information done")
            print("-"*20)
        else:
            print("Staff not found!!!")
#---------------------------Delete Staff Information--------------------------------------------------

def delete_staff_information():
    print("---Delete Staff---")
    while True:
        try:
            staff_id=int(input("Enter staff ID (or 0 to stop): "))
        except ValueError:
            print("Invalid staff ID!! Enter number only")
            continue
        cursor.execute("SELECT * FROM staff_information WHERE staff_id=?",(staff_id,))
        staff_data=cursor.fetchone()
        if staff_id==0:
            print("Staff delete stopped by user")
            break
        elif staff_data:
            cursor.execute("DELETE FROM staff_information WHERE staff_id=?", (staff_id,))
            conn.commit()
            print("Staff data Deleted...")
        else:
            print("Staff not found!")

#----------------------------View Staff Information------------------------------------------------
def view_staff_information():
    print("="*20,"STAFF DATA","="*20)
    cursor.execute("SELECT * FROM  staff_information")
    show_staff=cursor.fetchall()
    for staff in show_staff:
        print(f"{staff[0]} - {staff[1]} - {staff[2]} - {staff[3]} - {staff[4]} - {staff[5]} - {staff[6]}")

#----------------------------Add Issue Return---------------------------------------------------------
def issue_return():
    while True:
        search_books()         #show Book list- To see easy
        search_member_list()   #show member list
        print("---Add Issue/Return---")
        try:
            book_id=int(input("Enter book ID (o to stop):"))
        except ValueError:
            print("Invalid ID!! Enter number only")
            continue
        if book_id == 0:
            print("Add issue stopped by user")
            break
        member_id = int(input("Enter member ID :"))
        cursor.execute("SELECT * FROM book WHERE book_id=?", (book_id,))
        book = cursor.fetchone()
        if not book:
            print("Book not found!")
            continue

        cursor.execute("SELECT * FROM member WHERE member_id=?",(member_id,))
        member=cursor.fetchone()
        if member:
            issue_date=input("Enter issue date: ")
            return_date=input("Enter return date: ")
            due_date=input("Enter due date: ")
            status=input("Enter status (issued/returned): ")
        #check available copies
            cursor.execute("SELECT available_copies FROM book WHERE book_id=?", (book_id,))
            copies = cursor.fetchone()
            if status == "issued" and copies[0] <= 0:
                print("Book not available!")
                continue
            cursor.execute(""" INSERT INTO issue_return(book_id,member_id,issue_date,return_date,due_date,status)
                            VALUES (?,?,?,?,?,?)""",
                           (book_id,member_id,issue_date,return_date,due_date,status))
         # update available copies based on status
            if status == "issued":
                cursor.execute("""
                            UPDATE book SET available_copies = available_copies - 1
                            WHERE book_id = ?
                        """, (book_id,))
                conn.commit()

            elif status == "returned":
                cursor.execute("""
                            UPDATE book SET available_copies = available_copies + 1
                            WHERE book_id = ?
                        """, (book_id,))

                conn.commit()
            print("Transaction completed successfully...")
            print("-"*40)
        else:
            print("Member not found!!!")
#---------------------------Update Issue------------------------------------------------------------------

def update_issue_return():
    print("---Update Issue/Return---")
    while True:
        #show Issue detail
        try:
            issue_id=int(input("Enter issue ID (or 0 to stop):"))
        except ValueError:
            print("Invalid issue ID!! Enter number only")
            continue
        cursor.execute("SELECT * FROM issue_return WHERE issue_id=?",(issue_id,))
        old_issue=cursor.fetchone()
        if issue_id==0:
            print("Update issue stopped by user")
            break
        elif old_issue:
            update_issue=input(f"Update issue date'{old_issue[3]}':") or old_issue[3]
            update_return=input(f"Update return date '{old_issue[4]}':") or old_issue[4]
            update_due=input(f"Update due date '{old_issue[5]}':") or old_issue[5]
            update_status=input(f"Update status (issued/returned) '{old_issue[6]}':") or old_issue[6]

            cursor.execute("""
                                UPDATE issue_return
                                SET issue_date=?,return_date=?,due_date=?,status=? WHERE issue_id=?""",
                           (update_issue,update_return,update_due,update_status,issue_id))
            conn.commit()
            print("Issue and Return updated successfully...")
            print("_"*40)
        else:
            print("Issue ID not found!")
#----------------------------Delete Issue---------------------------------------------------------------
def delete_issue_return():
    print("---Delete Issue/Return---")
    while True:
        try:
            issue_id=int(input("Enter issue ID (or 0 to stop) : "))
        except ValueError:
            print("Invalid issue ID!! Enter number only")
            continue
        cursor.execute("SELECT * FROM issue_return WHERE issue_id=?",(issue_id,))
        issue_data=cursor.fetchone()
        if issue_id==0:
            print("Delete issue stopped by user")
            break
        if issue_data:
            cursor.execute("DELETE FROM issue_return WHERE issue_id=?",(issue_id,))
            conn.commit()
            print("Issue Deleted Successfully...")
        else:
            print("Issue ID not found!")

#--------------------------View Issue ------------------------------------------------------------------
def view_issue_return():
    print("-"*15,"View all Issue/Return Records","-"*15)
    cursor.execute("SELECT * FROM issue_return")
    show_issue=cursor.fetchall()
    for i in show_issue:
        print(f"{i[0]} - {i[1]} - {i[2]} - {i[3]} - {i[4]} - {i[5]} - {i[6]}")

#---------------------------LIBRARY ISSUE RETURN REPORT-------------------------------------------
def issue_return_report():
    cursor.execute("""
                            SELECT
                            issue_return.issue_id,
                            book.title,
                            member.member_name,
                            issue_return.issue_date,
                            issue_return.due_date,
                            issue_return.status
                            FROM issue_return
                            JOIN book ON issue_return.book_id = book.book_id
                            JOIN member ON issue_return.member_id = member.member_id
                        """)

    print("="*20,"ISSUE/RETURN REPORT","="*20)
    show_report=cursor.fetchall()
    for report in show_report:
        print(f"{report[0]} - {report[1]} - {report[2]} - {report[3]} - {report[4]} - {report[5]}")

#---------------------------Search Issue By Member---------------------------------------------------------
def search_issue_by_member():
    try:
         member_id=int(input("Enter member ID: "))
    except ValueError:
        print("Invalid member ID!! Enter number only")
        member_id = int(input("Enter member ID: "))

    cursor.execute("""
                                SELECT
                                issue_return.issue_id,
                                book.title,
                                issue_return.issue_date,
                                issue_return.due_date,
                                issue_return.status
                                FROM issue_return
                                JOIN book ON issue_return.book_id = book.book_id
                                JOIN member ON issue_return.member_id = member.member_id
                            """)
    search_member=cursor.fetchone()
    print(f"{search_member[0]} - {search_member[1]} - {search_member[2]} - {search_member[3]} - {search_member[4]}")

#------------------------ISSUE/RETURN MANAGEMENT---------------------------------------------------------
def issue_return_menu():
    while True:
        print("="*10,"ISSUE/RETURN BOOK","="*10)
        print("1. Add Issue / Return")
        print("2. Update Issue Record")
        print("3. Delete Issue Record")
        print("4. View All Issue Records")
        print("5. Library Report")
        print("0. Go Back")
        print("="*40)

        try:
            choose=int(input("Enter your choice 0-5:"))
        except ValueError:
            print("Enter number only. Try again")
            continue

        if choose== 1:
            issue_return()
        elif choose == 2:
            update_issue_return()
        elif choose == 3:
            delete_issue_return()
        elif choose == 4:
            view_issue_return()
        elif choose == 5:
            issue_return_report()
        elif choose == 0:
            break
        else:
            print("Invalid choice! Try again")

#---------------------STAFF MANAGEMENT MENU-----------------------------------------------------------------
def staff_menu():
    while True:
        print("="*15,"STAFF MANAGEMENT","="*15)
        print("1. Add Staff")
        print("2. Update Staff")
        print("3. Delete Staff")
        print("4. View Staff")
        print("0. Go Back")

        try:
            options=int(input("Enter your choice 0-4:"))
        except ValueError:
            print("Enter number only. Try again")
            continue
        if options==1:
            add_staff_information()
        elif options==2:
            update_staff_information()
        elif options==3:
            delete_staff_information()
        elif options==4:
            view_staff_information()
        elif options==0:
            break
        else:
            print("Invalid option!")

#---------------------MEMBER MANAGEMENT  MENU----------------------------------------------------------------
def member_menu():
    while True:
        print("="*20,"MEMBER MANAGEMENT","="*20)
        print("1. Add Member")
        print("2. Update Member")
        print("3. Delete Member")
        print("4. View Member")
        print("5. Search Members")
        print("6. Single member data")
        print("0. Go Back")

        try:
            select=int(input("Enter your choice 0-6:"))
        except ValueError:
            print("Enter number only.Try again")
            continue
        if select==1:
            add_member()
        elif select==2:
            update_member()
        elif select==3:
            delete_member()
        elif select==4:
            view_all_members()
        elif select==5:
            search_member_list()
        elif select==6:
            search_one_member()
        elif select==0:
            break
        else:
            print("Invalid choice")

#---------------------CATEGORY MANAGEMENT MENU-------------------------------------------------------------
def category_menu():
    while True:
        print("="*20,"CATEGORY MANAGEMENT","="*20)
        print("1. Add Category")
        print("2. Update Category")
        print("3. Delete Category")
        print("4. View Category")
        print("0. Go back")
        print("="*40)
        try:
            selection=int(input("Enter your Choice 0-4 : "))
        except ValueError:
            print("Try again. Enter number only")
            continue
        if selection==1:
            add_category()
        elif selection==2:
            update_category()
        elif selection==3:
            delete_category()
        elif selection==4:
            view_category()
        elif selection==0:
            break
        else:
            print("Invalid Choice")

#---------------------BOOK MANAGEMENT MENU---------------------------------------------
def book_menu():
    while True:
        print("="*15,"BOOK MANAGEMENT","="*15)
        print("1. Add Book")
        print("2. Update Book")
        print("3. Delete Book")
        print("4. View Book Data")
        print("5. View Books")
        print("6. Check Book Availability")
        print("0. Go Back")
        print("="*45)

        try:
             select=int(input("Enter your choice 0-6:"))
        except ValueError:
            print("Enter number only.Try again")
            continue

        if select==1:
            add_book()
        elif select==2:
            update_book()
        elif select==3:
            delete_book()
        elif select==4:
            view_book_data()
        elif select==5:
            search_books()
        elif select==6:
            check_available_copies()
        elif select==0:
            break
        else:
            print("Invalid choice")

#---------------------ADMIN MENU------------------------------------------------
def admin_fn():
    while True:
        print("="*18,"WELCOME ADMIN PAGE","="*18)
        print("1. Category management")
        print("2. Book management")
        print("3. Member Management")
        print("4. Staff Management")
        print("5. Issue/Return management")
        print("0. Log out")
        print("="*50)

        try:
            option=int(input("Enter your choice 0-5:"))
        except ValueError:
            print("Enter number only.")
            continue
        if option==1:
         category_menu()
        elif option==2:
            book_menu()
        elif option==3:
            member_menu()
        elif option==4:
            staff_menu()
        elif option==5:
            issue_return_menu()
        elif option==0:
            print("Logging out...")
            break
        else:
            print("Invalid choice!")


#----------------------------LIBRARIAN MENU----------------------------------------
def librarian_fn():
    while True:
        print("="*15,"WELCOME TO LIBRARIAN PAGE","="*15)
        print("1. Book management")
        print("2. Member Management")
        print("3. Issue/Return Management")
        print("4. Library Report")
        print("5. Check Book Availability")
        print("0. Log out")
        print("="*50)

        try:
            ch=int(input("Enter your choice 0-5:"))
        except ValueError:
            print("Enter number only.")
            continue

        if ch==1:
            book_menu()
        elif ch==2:
            member_menu()
        elif ch==3:
            issue_return_menu()
        elif ch==4:
            issue_return_report()
        elif ch==5:
            check_available_copies()
        elif ch==0:
            print("Logging out...")
            break
        else:
            print("Invalid choice!")

#---------------------------STAFF PAGE---------------------------------------------
def staff_fn():
    while True:
        print("="*15,"WELCOME TO STAFF PAGE","="*15)
        print("1. Issue / Return Book")
        print("2. Update Issue/Return Book")
        print("3. View All Issue Records")
        print("4. Search Issue by Member")
        print("5. Check Book Availability")
        print("6. Show Book Availability")
        print("0. Log out")

        try:
            option=int(input("Enter your choice 0-6:"))
        except ValueError:
            print("Please enter number only")
            continue

        if option==1:
            issue_return()
        elif option==2:
            update_issue_return()
        elif option==3:
            view_issue_return()
        elif option==4:
            search_issue_by_member()
        elif option==5:
            check_available_copies()
        elif option==6:
            show_book_availability()
        elif option==0:
            print("Logging out...")
            break
        else:
            print("Invalid choice!")

#-----------------------------user login---------------------------------------------
def user_login():
    print("="*18,"WELCOME TO USER LOGIN","="*18)
    while True:
        input_name = input("Enter User name (or 0 to quit): ")
        if input_name == "0":
            print("Login stopped by user")
            break
        if re.fullmatch(r"[A-Za-z0-9 ]{3,20}", input_name):
            break
        else:
            print("Invalid username! Only letters and spaces allowed")
    while True:
        input_pass = input("Enter your password: ")
        if re.fullmatch(r"[A-Za-z0-9@#$%]{6,15}", input_pass):
            break
        else:
            print("Invalid password!")

    cursor.execute(""" SELECT * FROM user WHERE user_name=? AND password=?""",
                   (input_name,input_pass))

    user= cursor.fetchone()            #(id-0, uname-1,pwd-2,role-3)return tuple or none
    if user:
        print("Login Successful....")
        if user[3]=='admin':
            admin_fn()
        elif user[3]=='librarian':
            librarian_fn()
        elif user[3]=='staff':
            staff_fn()
        else:
            print("Unknown role!")
    else:
        print("Invalid credentials!!!")

#--------------------------User Registration-----------------------------------------------

# cursor.execute(""" INSERT INTO user(user_name,Password,role)
#                VALUES ('Aswathy','aswathy123','admin');
#                """)
# conn.commit()
def user_reg():
    while True:
        print("="*18,"WELCOME TO REGISTRATION","="*18)
        print("1.Register Admin")
        print("2.Register Librarian")
        print("3.Register Staff")
        print("0.Log Out")

        try:
            choice = int(input("Enter your choice 0-3:"))
        except ValueError:
            print("Please enter number only")
            continue

        if choice==1:
            print("-"*20,"ADMIN REGISTRATION","-"*20)
            while True:
                reg_name = input("Enter name (0 to stop): ")
                if reg_name == "0":
                    print("Register stopped by user")
                    break
                if re.fullmatch(r"[A-Za-z ]{3,20}", reg_name):
                    break
                else:
                    print("Invalid name! Only letters")

            reg_pass = input("Enter password:")
            confirm_password = input("Confirm password:")
            if reg_pass!=confirm_password:
                print("Password does not match")
            else:
                cursor.execute("""INSERT INTO  user(user_name,password,role)
                VALUES(?,?,?);              
                        """,(reg_name,reg_pass,'admin'))
                print("Successfully registered...")
                conn.commit()

        elif choice==2:
            print("-"*20,"LIBRARIAN REGISTRATION","-"*20)
            while True:
                reg_name = input("Enter name (0 to stop): ")
                if reg_name == "0":
                    print("Register stopped by user")
                    break
                if re.fullmatch(r"[A-Za-z ]{3,20}", reg_name):
                    break
                else:
                    print("Invalid name! Only letters allowed")
            if reg_name != "0":
                reg_pass = input("Enter password:")
                confirm_password = input("Confirm password:")
                if reg_pass != confirm_password:
                    print("Password does not match")
                else:
                    cursor.execute("""INSERT INTO user(user_name,password,role)
                           VALUES(?,?,?);              
                            """,(reg_name,reg_pass,'librarian'))
                    print("Successfully registered...")

                    conn.commit()

        elif choice==3:
            print("-"*20,"STAFF REGISTRATION","-"*20)
            reg_name = input("Enter name:")
            if reg_name=="0" :
                print("Register stopped by user ")
                break
            reg_pass = input("Enter password:")
            confirm_password = input("Confirm password:")
            if reg_pass != confirm_password:
                print("Password does not match")
            else:
                cursor.execute("""INSERT INTO  user(user_name,password,role)
                        VALUES(?,?,?);""",(reg_name,reg_pass,'staff'))
                print("Successfully registered...")
                conn.commit()

        elif choice==0:
            print("Logging out...")
            break

        else:
            print("Invalid choice.Try again")

conn.commit()

while True:
    print("="*60)
    print(" "*15,"LIBRARY MANAGEMENT SYSTEM")
    print("="*60)
    print("1.Registration")
    print("2.User Login")
    print("0.Exit")
    try:
        choices = int(input("Enter your choice:"))
    except ValueError:
        print("Please enter number only")
        continue

    if choices==1:
        user_reg()
    elif choices==2:
        user_login()
    elif choices==0:
        print("Exited")
        break
    else:
        print("Invalid choice!")




