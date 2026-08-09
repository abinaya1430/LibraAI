import gradio as gr
from datetime import date, timedelta

# =========================================================
# STUDENTS
# =========================================================

students = {
    "LIB001": {"name": "Abinaya", "password": "1234"},
    "LIB002": {"name": "Anushiya", "password": "2345"},
    "LIB003": {"name": "Kavitha", "password": "3456"}
}

# =========================================================
# ADMIN
# =========================================================

ADMIN_USERNAME = "ADMIN"
ADMIN_PASSWORD = "admin123"

# =========================================================
# BOOK DATABASE
# =========================================================
books = [
    ["Python Programming", "John Smith", "Programming", "Available"],
    ["Data Science Fundamentals", "Anna Wilson", "Data Science", "Available"],
    ["Artificial Intelligence", "David Brown", "AI", "Available"],
    ["Machine Learning Basics", "Sarah Lee", "AI/ML", "Available"],
    ["Web Development", "Mike Johnson", "Web", "Available"],
    ["Deep Learning", "Tom Davis", "AI/ML", "Available"],
    ["Python for Beginners", "James Lee", "Programming", "Available"],
    ["Introduction to Robotics", "Robert King", "Robotics", "Available"]
]

# =========================================================
# DATA
# =========================================================

borrowed_books = {}
reservations = {}
return_requests = {}

timer_seconds = 0
current_reservation = None


# =========================================================
# STATUS BADGE
# =========================================================

def status_badge(status):

    if status == "Available":
        return """
        <span style="
        background:#16a34a;
        color:white;
        padding:6px 14px;
        border-radius:20px;
        font-weight:bold;">
        🟢 Available
        </span>
        """

    elif status == "Reserved":
        return """
        <span style="
        background:#f59e0b;
        color:white;
        padding:6px 14px;
        border-radius:20px;
        font-weight:bold;">
        🟠 Reserved
        </span>
        """

    elif status == "Issued":
        return """
        <span style="
        background:#dc2626;
        color:white;
        padding:6px 14px;
        border-radius:20px;
        font-weight:bold;">
        🔴 Issued
        </span>
        """

    return status


# =========================================================
# BOOK DISPLAY
# ========================================================
def create_book_list(book_list):

    if not book_list:

        return "## ❌ No books found."

    html = """

    <div style="width:100%;">

    """

    for book in book_list:

        html += f"""

        <div style="

            padding:20px;

            margin:14px 0;

            border-radius:18px;

            background:#90D5FF;

            border:1px solid #30394f;

            text-align:left;

            color:#000000;

        ">

            <div style="

                font-size:22px;

                font-weight:bold;

                margin-bottom:12px;

            ">

                📚 {book[0]}

            </div>

            <div style="margin:8px 0;">

                👤 <b>Author:</b> {book[1]}

            </div>

            <div style="margin:8px 0;">

                🏷️ <b>Category:</b> {book[2]}

            </div>

            <div style="margin:8px 0;">

                📌 <b>Status:</b> {status_badge(book[3])}

            </div>

        </div>

        """

    html += "</div>"

    return html

        

# =========================================================
# STUDENT LOGIN
# =========================================================

def student_login(register_number, password):

    if register_number in students:

        if students[register_number]["password"] == password:

            name = students[register_number]["name"]

            return (
                gr.update(visible=False),
                gr.update(visible=True),
                gr.update(visible=False),
                f"### 🎉 Welcome, {name}!"
            )

        return (
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(visible=False),
            "❌ **Wrong Password!**"
        )

    return (
        gr.update(visible=True),
        gr.update(visible=False),
        gr.update(visible=False),
        "❌ **Register Number not found!**"
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

def admin_login(username, password):

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

        return (
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True),
            "### 🎉 Welcome Admin!"
        )

    return (
        gr.update(visible=True),
        gr.update(visible=False),
        gr.update(visible=False),
        "❌ **Invalid Admin Login!**"
    )


# =========================================================
# LOGOUT
# =========================================================

def logout():

    return (
        gr.update(visible=True),
        gr.update(visible=False),
        gr.update(visible=False),
        "👋 **Logged out successfully!**"
    )


# =========================================================
# SEARCH BOOKS
# =========================================================

def search_books(search_text):

    if not search_text:
        return create_book_list(books)

    text = search_text.lower()

    results = []

    for book in books:

        if (
            text in book[0].lower()
            or text in book[1].lower()
            or text in book[2].lower()
        ):
            results.append(book)

    return create_book_list(results)


# =========================================================
# BOOK NOW
# =========================================================

def book_book(book_name, register_number):

    global timer_seconds
    global current_reservation

    if not register_number:

        return (
            "❌ Please login first.",
            "⏱️ Timer not started.",
            gr.update(active=False),
            create_book_list(books)
        )

    if not book_name:

        return (
            "❌ Please select a book.",
            "⏱️ Timer not started.",
            gr.update(active=False),
            create_book_list(books)
        )

    if register_number in reservations:

        return (
            "⚠️ You already have an active reservation.",
            "⏱️ Finish your current reservation first.",
            gr.update(active=True),
            create_book_list(books)
        )

    for book in books:

        if book[0] == book_name:

            if book[3] == "Available":

                book[3] = "Reserved"

                timer_seconds = 900

                current_reservation = {
                    "register": register_number,
                    "book": book_name
                }

                reservations[register_number] = {
                    "book": book_name,
                    "status": "Waiting for Collection"
                }

                return (
                    f"""
## 📚 Book Reserved Successfully!

📖 **Book:** {book_name}

👤 **Student:** {students[register_number]["name"]}

🟠 **Status:** Reserved

⏱️ **Collect the book within 15 minutes.**
""",
                    "⏱️ **15:00 Timer Started!**",
                    gr.update(active=True),
                    create_book_list(books)
                )

            elif book[3] == "Reserved":

                return (
                    "🟠 **This book is already reserved.**",
                    "⏱️ Timer not started.",
                    gr.update(active=False),
                    create_book_list(books)
                )

            else:

                return (
                    "🔴 **This book is already issued.**",
                    "⏱️ Timer not started.",
                    gr.update(active=False),
                    create_book_list(books)
                )

    return (
        "❌ Book not found.",
        "⏱️ Timer not started.",
        gr.update(active=False),
        create_book_list(books)
    )


# =========================================================
# TIMER
# =========================================================

def countdown():

    global timer_seconds
    global current_reservation

    if timer_seconds > 0:

        timer_seconds -= 1

        minutes = timer_seconds // 60
        seconds = timer_seconds % 60

        return (
            f"# ⏱️ {minutes:02d}:{seconds:02d}",
            create_book_list(books)
        )

    if current_reservation is not None:

        register_number = current_reservation["register"]
        book_name = current_reservation["book"]

        for book in books:

            if book[0] == book_name:

                if book[3] == "Reserved":
                    book[3] = "Available"

                break

        if register_number in reservations:
            del reservations[register_number]

        current_reservation = None

        return (
            """
# ⏱️ 00:00

## ❌ Reservation Expired!

The book was not collected within 15 minutes.

🟢 **Book is Available again.**
""",
            create_book_list(books)
        )

    return (
        "# ⏱️ 00:00",
        create_book_list(books)
    )


# =========================================================
# MY BOOKS
# =========================================================

def show_my_books(register_number):

    if not register_number:
        return "❌ Please login first."

    my_books = borrowed_books.get(register_number, [])

    if not my_books:

        return """
## 📕 My Books

You currently have no issued books.
"""

    result = "## 📕 My Books\n\n"

    today = date.today()

    for item in my_books:

        due_date = date.fromisoformat(item["due_date"])
        days_left = (due_date - today).days

        result += f"""
### 📚 {item["title"]}

🔴 **Status:** Issued

📅 **Due Date:** {item["due_date"]}

⏳ **Days Remaining:** {days_left}

---
"""

    return result


# =========================================================
# NOTIFICATIONS
# =========================================================

def show_notifications(register_number):

    if not register_number:
        return "❌ Please login first."

    result = "## 🔔 Notifications\n\n"
    found = False

    if register_number in reservations:

        found = True

        result += f"""
⏱️ **COLLECTION REMINDER**

📚 {reservations[register_number]["book"]}

🟠 Collect your book within 15 minutes.

---
"""

    if register_number in return_requests:

        for book_name in return_requests[register_number]:

            found = True

            result += f"""
⏳ **RETURN REQUEST**

📚 {book_name}

👨‍💼 Waiting for Admin approval.

---
"""

    my_books = borrowed_books.get(register_number, [])

    today = date.today()

    for item in my_books:

        due_date = date.fromisoformat(item["due_date"])
        days_left = (due_date - today).days

        if days_left <= 3:

            found = True

            result += f"""
⚠️ **DUE DATE REMINDER**

📚 {item["title"]}

📅 Due Date: {item["due_date"]}

⏳ {days_left} days remaining.

---
"""

    if not found:
        result += "✅ No new notifications."

    return result


# =========================================================
# RETURN REQUEST
# =========================================================

def request_return(book_name, register_number):

    if not register_number:
        return "❌ Please login first."

    student_books = borrowed_books.get(register_number, [])

    found = False

    for item in student_books:

        if item["title"] == book_name:
            found = True
            break

    if not found:
        return "❌ This book is not in your My Books."

    if register_number not in return_requests:
        return_requests[register_number] = []

    if book_name in return_requests[register_number]:
        return "⚠️ Return request already sent."

    return_requests[register_number].append(book_name)

    return f"""
## 📤 Return Request Sent!

📚 **Book:** {book_name}

👤 **Student:** {students[register_number]["name"]}

⏳ Waiting for Admin approval.
"""


# =========================================================
# AI RECOMMENDATION
# =========================================================

def recommend_books():

    return """
## 🤖 AI Recommended Books

📘 **Python Programming**

⭐ Great for beginners.

---

🧠 **Machine Learning Basics**

⭐ Perfect for AI/ML students.

---

🤖 **Artificial Intelligence**

⭐ Learn intelligent systems.

---

📊 **Data Science Fundamentals**

⭐ Learn data and machine learning.
"""


# =========================================================
# ADMIN COLLECTION REQUESTS
# =========================================================

def show_collection_requests():

    if not reservations:

        return """
## 📦 Collection Requests

✅ No pending collection requests.
"""

    result = "## 📦 Pending Collection Requests\n\n"

    for register_number, data in reservations.items():

        result += f"""
👤 **Student:** {students[register_number]["name"]}

🪪 **Register:** {register_number}

📚 **Book:** {data["book"]}

🟠 **Status:** Waiting for Collection

---
"""

    return result


# =========================================================
# ADMIN COLLECTED
# =========================================================

def admin_collected(register_number, book_name):

    global timer_seconds
    global current_reservation

    if register_number not in reservations:

        return (
            "❌ No active reservation found.",
            create_book_list(books)
        )

    if reservations[register_number]["book"] != book_name:

        return (
            "❌ Book name does not match.",
            create_book_list(books)
        )

    for book in books:

        if book[0] == book_name:

            book[3] = "Issued"

            break

    due_date = date.today() + timedelta(days=14)

    if register_number not in borrowed_books:
        borrowed_books[register_number] = []

    borrowed_books[register_number].append({
        "title": book_name,
        "due_date": str(due_date)
    })

    del reservations[register_number]

    timer_seconds = 0
    current_reservation = None

    return (
        f"""
## ✅ BOOK COLLECTED!

📚 **Book:** {book_name}

👤 **Student:** {students[register_number]["name"]}

🔴 **Status:** Issued

📅 **Due Date:** {due_date}

🎉 Book is now available in **My Books**.
""",
        create_book_list(books)
    )


# =========================================================
# ADMIN RETURN REQUESTS
# =========================================================

def show_return_requests():

    if not return_requests:

        return """
## 📋 Return Requests

✅ No pending return requests.
"""

    result = "## 📋 Pending Return Requests\n\n"

    for register_number, book_list in return_requests.items():

        result += f"""
👤 **Student:** {students[register_number]["name"]}

🪪 **Register:** {register_number}

"""

        for book_name in book_list:
            result += f"📚 **{book_name}**\n\n"

        result += "---\n"

    return result


# =========================================================
# APPROVE RETURN
# =========================================================

def approve_return(register_number, book_name):

    if register_number not in return_requests:

        return (
            "❌ No return request found.",
            create_book_list(books)
        )

    if book_name not in return_requests[register_number]:

        return (
            "❌ This book is not in the request.",
            create_book_list(books)
        )

    return_requests[register_number].remove(book_name)

    if not return_requests[register_number]:
        del return_requests[register_number]

    if register_number in borrowed_books:

        borrowed_books[register_number] = [
            item
            for item in borrowed_books[register_number]
            if item["title"] != book_name
        ]

    for book in books:

        if book[0] == book_name:

            book[3] = "Available"

            break

    return (
        f"""
## ✅ RETURN APPROVED!

📚 **Book:** {book_name}

👤 **Student:** {students[register_number]["name"]}

🟢 **Status:** Available
""",
        create_book_list(books)
    )


# =========================================================
# CSS
# =========================================================

css = """

body {
    background:#080d1c;
}

.hero {
    background:linear-gradient(135deg,#5546ed,#1769ff);
    border-radius:30px;
    padding:40px;
    text-align:center;
    color:white;
    margin-bottom:30px;
    box-shadow:0 15px 40px rgba(70,70,255,0.35);
}

.hero h1 {
    font-size:55px;
}

.hero h2 {
    font-size:25px;
}

.section-title {
    font-size:28px;
    font-weight:bold;
    margin-top:25px;
}

"""


# =========================================================
# APP
# =========================================================

with gr.Blocks(
    css=css,
    theme=gr.themes.Soft(),
    title="LibraAI"
) as app:

    # =====================================================
    # LOGIN PAGE
    # =====================================================

    with gr.Column(visible=True) as login_page:

        gr.Markdown("""
# 📚 LibraAI

## 🤖 Smart Library Assistant

### 👋 **Hey, Smart Learners!**

### 📚 **Book Your Books**

✨ *Discover • Book • Learn • Grow*
""")

        with gr.Tabs():

            # STUDENT LOGIN

            with gr.Tab("👨‍🎓 Student Login"):

                student_register = gr.Textbox(
                    label="🪪 Register Number",
                    placeholder="Example: LIB001"
                )

                student_password = gr.Textbox(
                    label="🔑 Password",
                    type="password"
                )

                student_login_button = gr.Button(
                    "🚀 STUDENT LOGIN",
                    variant="primary"
                )

                student_login_result = gr.Markdown()


            # ADMIN LOGIN

            with gr.Tab("👨‍💼 Admin Login"):

                admin_username = gr.Textbox(
                    label="👤 Admin Username"
                )

                admin_password = gr.Textbox(
                    label="🔑 Admin Password",
                    type="password"
                )

                admin_login_button = gr.Button(
                    "🔐 ADMIN LOGIN",
                    variant="primary"
                )

                admin_login_result = gr.Markdown()


    # =====================================================
    # STUDENT DASHBOARD
    # =====================================================

    with gr.Column(visible=False) as student_dashboard:

        gr.HTML("""
        <div class="hero">

            <div style="font-size:60px;">📚</div>

            <h1>LibraAI</h1>

            <h2>🤖 Smart Library Dashboard</h2>

            <p>📖 Your Smart Library Assistant</p>

        </div>
        """)

        # STUDENT NAME APPEARS HERE

        student_welcome = gr.Markdown(
            "🎉 **Welcome!**"
        )


        # =================================================
        # SEARCH BOOKS
        # =================================================

        gr.Markdown(
            "## 🔎 Search Books",
            elem_classes="section-title"
        )

        search_box = gr.Textbox(
            label="📚 Search",
            placeholder="Search by book name, author or category..."
        )

        with gr.Row():

            search_button = gr.Button(
                "🔍 SEARCH",
                variant="primary"
            )

            Refresh_button = gr.Button(
                "🔄Refresh"
            )

        search_results = gr.Markdown(
            value=create_book_list(books)
        )


        # =================================================
        # RESERVE BOOK
        # =================================================

        gr.Markdown(
            "## 📚 Reserve a Book",
            elem_classes="section-title"
        )

        book_selection = gr.Dropdown(
            choices=[book[0] for book in books],
            label="📚 Select Book"
        )

        book_button = gr.Button(
            "📚 BOOK NOW",
            variant="primary"
        )

        book_result = gr.Markdown()

        timer_status = gr.Markdown(
            "⏱️ Timer not started."
        )

        timer_display = gr.Markdown(
            "# ⏱️ 15:00"
        )

        countdown_timer = gr.Timer(
            value=1,
            active=False
        )


        # =================================================
        # MY BOOKS
        # =================================================

        gr.Markdown(
            "## 📕 My Books",
            elem_classes="section-title"
        )

        my_books_button = gr.Button(
            "📕 VIEW MY BOOKS"
        )

        my_books_output = gr.Markdown()


        # =================================================
        # NOTIFICATIONS
        # =================================================

        gr.Markdown(
            "## 🔔 Notifications",
            elem_classes="section-title"
        )

        notification_button = gr.Button(
            "🔔 VIEW NOTIFICATIONS",
            variant="primary"
        )

        notification_output = gr.Markdown()


        # =================================================
        # AI RECOMMENDATION
        # =================================================

        gr.Markdown(
            "## 🤖 AI Recommendation",
            elem_classes="section-title"
        )

        ai_button = gr.Button(
            "✨ GET AI RECOMMENDATION",
            variant="primary"
        )

        ai_output = gr.Markdown()


        # =================================================
        # RETURN BOOK
        # =================================================

        gr.Markdown(
            "## ↩️ Return Book",
            elem_classes="section-title"
        )

        return_book_selection = gr.Dropdown(
            choices=[book[0] for book in books],
            label="📕 Select Book"
        )

        return_button = gr.Button(
            "📤 REQUEST RETURN",
            variant="primary"
        )

        return_output = gr.Markdown()


        # =================================================
        # LOG OUT - BOTTOM
        # =================================================

        gr.Markdown("---")

        logout_student_button = gr.Button(
            "🚪 LOG OUT",
            variant="stop"
        )


    # =====================================================
    # ADMIN DASHBOARD
    # =====================================================

    with gr.Column(visible=False) as admin_dashboard:

        gr.HTML("""
        <div class="hero">

            <div style="font-size:60px;">👨‍💼</div>

            <h1>LibraAI Admin</h1>

            <h2>📚 Library Management Dashboard</h2>

            <p>Manage • Collect • Return • Monitor</p>

        </div>
        """)

        gr.Markdown(
            "## 👨‍💼 Welcome, Librarian!"
        )


        # COLLECTION REQUESTS

        gr.Markdown(
            "## 📦 Pending Collection Requests",
            elem_classes="section-title"
        )

        view_collection_button = gr.Button(
            "📋 VIEW COLLECTION REQUESTS",
            variant="primary"
        )

        collection_output = gr.Markdown()


        # COLLECTED

        gr.Markdown(
            "## ✅ Confirm Book Collection",
            elem_classes="section-title"
        )

        admin_register = gr.Textbox(
            label="🪪 Student Register Number"
        )

        admin_book = gr.Textbox(
            label="📚 Book Name"
        )

        collected_button = gr.Button(
            "✅ COLLECTED",
            variant="primary"
        )

        collected_output = gr.Markdown()


        # RETURN REQUESTS

        gr.Markdown(
            "## ↩️ Return Requests",
            elem_classes="section-title"
        )

        view_return_button = gr.Button(
            "📋 VIEW RETURN REQUESTS"
        )

        return_requests_output = gr.Markdown()


        # APPROVE RETURN

        gr.Markdown(
            "### ✅ Approve Return"
        )

        return_register = gr.Textbox(
            label="🪪 Student Register Number"
        )

        return_book = gr.Textbox(
            label="📚 Book Name"
        )

        approve_return_button = gr.Button(
            "✅ APPROVE RETURN",
            variant="primary"
        )

        approve_output = gr.Markdown()


        # BOOK STATUS

        gr.Markdown(
            "## 📊 Book Status",
            elem_classes="section-title"
        )

        status_button = gr.Button(
            "📚 VIEW ALL BOOK STATUS"
        )

        status_output = gr.Markdown(
            value=create_book_list(books)
        )


    # =====================================================
    # EVENTS
    # =====================================================

    # STUDENT LOGIN

    student_login_button.click(
        student_login,
        inputs=[
            student_register,
            student_password
        ],
        outputs=[
            login_page,
            student_dashboard,
            admin_dashboard,
            student_login_result
        ]
    )


    # ADMIN LOGIN

    admin_login_button.click(
        admin_login,
        inputs=[
            admin_username,
            admin_password
        ],
        outputs=[
            login_page,
            student_dashboard,
            admin_dashboard,
            admin_login_result
        ]
    )


    # LOGOUT

    logout_student_button.click(
        logout,
        outputs=[
            login_page,
            student_dashboard,
            admin_dashboard,
            student_login_result
        ]
    )


    # SEARCH

    search_button.click(
        search_books,
        inputs=search_box,
        outputs=search_results
    )


    # CLEAR

    Refresh_button.click(
        lambda: ("", create_book_list(books)),
        outputs=[
            search_box,
            search_results
        ]
    )


    # BOOK NOW

    book_button.click(
        book_book,
        inputs=[
            book_selection,
            student_register
        ],
        outputs=[
            book_result,
            timer_status,
            countdown_timer,
            search_results
        ]
    )


    # TIMER

    countdown_timer.tick(
        countdown,
        outputs=[
            timer_display,
            search_results
        ]
    )


    # MY BOOKS

    my_books_button.click(
        show_my_books,
        inputs=student_register,
        outputs=my_books_output
    )


    # NOTIFICATIONS

    notification_button.click(
        show_notifications,
        inputs=student_register,
        outputs=notification_output
    )


    # AI

    ai_button.click(
        recommend_books,
        outputs=ai_output
    )


    # RETURN

    return_button.click(
        request_return,
        inputs=[
            return_book_selection,
            student_register
        ],
        outputs=return_output
    )


    # ADMIN COLLECTION

    view_collection_button.click(
        show_collection_requests,
        outputs=collection_output
    )


    # ADMIN COLLECTED

    collected_button.click(
        admin_collected,
        inputs=[
            admin_register,
            admin_book
        ],
        outputs=[
            collected_output,
            search_results
        ]
    )


    # ADMIN RETURN REQUESTS

    view_return_button.click(
        show_return_requests,
        outputs=return_requests_output
    )


    # APPROVE RETURN

    approve_return_button.click(
        approve_return,
        inputs=[
            return_register,
            return_book
        ],
        outputs=[
            approve_output,
            search_results
        ]
    )


    # BOOK STATUS

    status_button.click(
        lambda: create_book_list(books),
        outputs=status_output
    ) 
import os

app.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860)),
    share=False
)
