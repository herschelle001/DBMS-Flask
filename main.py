from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="eu-cdbr-west-03.cleardb.net",
    user="bd4d277efac44c",
    password="329d45ef",
    database="heroku_5766ac2c8f1063b"
)
cursor = mydb.cursor()


# ----------------------------------------------- routes ---------------------------------------------------------

@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/college")
def college():
    return render_template("college.html", college_names=college_names)


@app.route("/coaching")
def coaching():
    return render_template("coaching.html", coaching_names=coaching_names)


@app.route("/student", methods=["GET", "POST"])
def student():
    return render_template("student.html")


@app.route("/parent")
def parent():
    return render_template("parent.html")


# --------------------------------------------------- index.html ------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def receive_index_data():
    selected = request.form["selected"]
    if selected == "Student":
        selected = "student"
    elif selected == "Parent":
        selected = "parent"
    elif selected == "College Admin":
        selected = "college"
    elif selected == "Coaching Institute":
        selected = "coaching"
    return redirect("/" + selected)


# ------------------------------------------------- index.html end-------------------------------------------------

@app.route("/student/success", methods=["GET", "POST"])
def receive_student_data():
    if request.form['submit'] == 'college':  # for top section
        rank = request.form["rank"]
        cbse = request.form["cbse-percent"]
        interest = request.form["interest"]
        exam = request.form["exam-top"]
        state = request.form["state-top"]
        res = student_college(rank, interest, state, cbse, exam)
        return f'{res}'

    elif request.form['submit'] == 'exam':  # for middle section
        month_of_exam = request.form["choose_month"]
        mode_of_exam = request.form["mode-of-exam"]
        name_of_exam = request.form["exam_name"]

        arr = []

        if not (month_of_exam == "") and not (mode_of_exam == ""):
            month_res = execute1('entrance_exams', month_of_exam)
            exam_res = execute2('entrance_exams', mode_of_exam)
            for i in month_res:
                for j in exam_res:
                    if i == j:
                        arr.append(i)

        elif not (month_of_exam == "") and (mode_of_exam == ""):
            month_res = execute1('entrance_exams', month_of_exam)
            for i in month_res:
                arr.append(i)

        elif (mode_of_exam == "") and not (mode_of_exam == ""):
            exam_res = execute2('entrance_exams', mode_of_exam)
            for i in exam_res:
                arr.append(i)

        if not (name_of_exam == ""):
            res = execute3('entrance_exams', name_of_exam)
            return f'{res}'

        return f'{arr}'

    else:  # for bottom section
        exam_to_prepare = request.form["exam_name"]
        state = request.form["state"]

        # if only exam name is selected
        if not (exam_to_prepare == "") and (state == ""):
            res = execute4('coaching_institute', exam_to_prepare)
            return f'{res}'

        # if only state is selected
        elif not (state == "") and (exam_to_prepare == ""):
            res = execute5('coaching_institute', state)
            return f'{res}'

        # if both are selected
        elif not (state == "") and not (exam_to_prepare == ""):
            res = execute6('coaching_institute', state, exam_to_prepare)
            return f'{res}'


# ------------------------------------------------- student end-------------------------------------------------


# --------------------------------------------------- parent -------------------------------------------------

@app.route("/parent/success", methods=["GET", "POST"])
def receive_parent_data():
    if request.form['submit'] == 'college':  # for top section
        fee = request.form.get("fee")
        hostel_avail = request.form.get("hostel")
        state = request.form["state"]
        package = request.form.get("pkg")

        if fee == '1':
            fee = '1000000000'
        elif fee == '2':
            fee = "50000"
        elif fee == '3':
            fee = '100000'
        else:
            fee = '200000'

        if package == '1':
            package = '1'
        elif package == '2':
            package = '6'
        elif package == '3':
            package = '10'
        else:
            package = '15'

        if state == 'Any':
            res = get_parent_data2(fee, hostel_avail, package)
        else:
            res = get_parent_data1(fee, hostel_avail, state, package)

        return f'{res}'

    else:  # bottom section
        fee = request.form["fee-bottom"]
        hostel_avail = request.form["hostel-bottom"]
        state = request.form["state-bottom"]
        package = request.form["selections"]
        # query here
        return fee + hostel_avail + state + package


# --------------------------------------------------parent end--------------------------------------------------


# --------------------------------------------------- coaching -----------------------------------------------

query = "SELECT * from coaching_institute"
cursor.execute(query)
result = cursor.fetchall()
coaching_names = []
for j in result:
    coaching_names.append(j[1])


@app.route("/coaching/success", methods=["GET", "POST"])
def receive_coaching_data():
    selected = request.form["selected"]
    college_id = -1
    for i in range(len(coaching_names)):
        if selected == coaching_names[i]:
            college_id = i + 1
            break

    name_update = request.form["name-update"]
    taught_update = request.form["taught-update"]
    fee_update = request.form["fee-update"]
    hostel_avail_update = request.form["hostel-update"]

    if not (name_update == ""):
        update_coaching_data(college_id, 'coaching_institute', 'institute_name', name_update)

    if not (fee_update == ""):
        update_coaching_data(college_id, 'coaching_institute', 'fees', fee_update)

    if not (hostel_avail_update == ""):
        update_coaching_data(college_id, 'coaching_institute', 'hostel_availability', hostel_avail_update)

    if not (taught_update == ""):
        update_coaching_data(college_id, 'coaching_institute', 'exams_taught', taught_update)

    return "Success"


# ---------------------------------------------coaching end----------------------------------------------------------

# --------------------------------------------- college ---------------------------------------------------------------


query = "SELECT * from college_general"
cursor.execute(query)
result = cursor.fetchall()
college_names = []
for j in result:
    college_names.append(j[2])


@app.route("/college/success", methods=["GET", "POST"])
def receive_college_data():
    selected = request.form["selected"]
    college_id = -1
    for i in range(len(college_names)):
        if selected == college_names[i]:
            college_id = i + 1
            break

    name = request.form["name"]
    website = request.form["website"]
    placed_students = request.form["placed"]
    avg_pkg = request.form["avg"]
    highest_pkg = request.form["highest"]
    area = request.form["area"]
    fee = request.form["fee"]
    mode_of_admission = request.form["admission"]

    if not (website == ""):
        update_college_data(college_id, 'college_general', 'college_website', website)

    if not (placed_students == ""):
        update_college_data(college_id, 'college_placement_stats', 'students_placed_percent', placed_students)

    if not (avg_pkg == ""):
        update_college_data(college_id, 'college_placement_stats', 'avg_package', avg_pkg)

    if not (highest_pkg == ""):
        update_college_data(college_id, 'college_placement_stats', 'highest_package', highest_pkg)

    if not (fee == ""):
        update_college_data(college_id, 'college_general', 'fees', fee)

    if not (mode_of_admission == ""):
        update_college_data(college_id, 'college_general', 'mode_of_admission', mode_of_admission)

    if not (name == ""):
        update_college_data(college_id, 'college_general', 'full_name', name)

    if not (area == ""):
        update_college_data(college_id, 'college_location', 'area_in_acres', area)

    return "Success"


# ------------------------------------------------ college end---------------------------------------------------------

# ------------------------------------------------ Queries ------------------------------------------------------------

# ----- Student ------

def student_college(rank, interest, state, cbse, exam):
    cursor.execute(
        "SELECT `full_name` FROM `college_general` LEFT OUTER JOIN `college_admission_criteria` ON (college_general.college_id = college_admission_criteria.college_id) LEFT OUTER JOIN college_course ON (college_general.college_id = college_course.college_id) LEFT OUTER JOIN college_location ON (college_location.college_id = college_general.college_id) LEFT OUTER JOIN location ON (location.location_id = college_location.location_id) WHERE (end_rank >= '" + rank + "') and (course_name = '" + interest + "') and (state = '" + state + "') and (cutoff_in_boards < '" + cbse + "') and (mode_of_admission = '" + exam + "')")
    res = cursor.fetchall()
    return res


def execute1(table, value):
    cursor.execute("SELECT * FROM `" + table + "` WHERE (`exam_month` = '" + str(value) + "')")
    res = cursor.fetchall()
    return res


def execute2(table, value):
    cursor.execute("SELECT * FROM `" + table + "` WHERE (`mode_of_exam` = '" + str(value) + "')")
    res = cursor.fetchall()
    return res


def execute3(table, value):
    cursor.execute("SELECT * FROM `" + table + "` WHERE (`exam_name` = '" + str(value) + "')")
    res = cursor.fetchall()
    return res


def execute4(table, value):
    cursor.execute("SELECT * FROM `" + table + " LEFT OUTER JOIN coaching_institute_exam ON (coaching_institute_exam.institute_id= coaching_institute.institute_id) LEFT OUTER JOIN entrance_exams ON (entrance_exams.exam_id = coaching_institute_exam.exam_id) LEFT OUTER JOIN location ON (location.location_id = coaching_institute.location_id) WHERE (`entrance_exams`.`exam_name` = '" + str(value) + "')")
    res = cursor.fetchall()
    return res


def execute5(table, value):
    cursor.execute("SELECT * FROM `" + table + "` LEFT OUTER JOIN coaching_institute_exam ON (coaching_institute_exam.institute_id= coaching_institute.institute_id) LEFT OUTER JOIN entrance_exams ON (entrance_exams.exam_id = coaching_institute_exam.exam_id) LEFT OUTER JOIN location ON (location.location_id = coaching_institute.location_id) WHERE (`location`.`state` = '" + str(value) + "') ")
    res = cursor.fetchall()
    return res


def execute6(table, values, valuee):
    cursor.execute("SELECT * FROM `" + table + "` LEFT OUTER JOIN coaching_institute_exam ON (coaching_institute_exam.institute_id= coaching_institute.institute_id) LEFT OUTER JOIN entrance_exams ON (entrance_exams.exam_id = coaching_institute_exam.exam_id) LEFT OUTER JOIN location ON (location.location_id = coaching_institute.location_id) WHERE (`entrance_exams`.`exam_name` = '" + str(valuee) + "') AND (`location`.`state` = '" + str(values) + "')")
    res = cursor.fetchall()
    return res

    # ----- Student ------

    # ----- Parent ------


def get_parent_data1(fee, hostel, state, package):
    cursor.execute("Select `full_name` from `college_general` LEFT OUTER JOIN `college_placement_stats` ON (`college_placement_stats`.`college_id` = `college_general`.`college_id`) LEFT OUTER JOIN college_location ON (`college_location`.`college_id` = `college_general`.`college_id`) LEFT OUTER JOIN location ON (`location`.`location_id` = `college_location`.`location_id`) WHERE (`fees` < '" + fee + "') and (`avg_package` > '" + package + "') and (`state` = '" + state + "')")
    res = cursor.fetchall()
    return res


def get_parent_data2(fee, hostel, package):
    cursor.execute("Select `full_name` from `college_general` LEFT OUTER JOIN `college_placement_stats` ON (`college_placement_stats`.`college_id` = `college_general`.`college_id`) LEFT OUTER JOIN college_location ON (`college_location`.`college_id` = `college_general`.`college_id`) LEFT OUTER JOIN location ON (`location`.`location_id` = `college_location`.`location_id`) WHERE (`fees` < '" + fee + "') and (`avg_package` > '" + package + "')")
    res = cursor.fetchall()
    return res

    # ----- Parent ------

    # ----- Coaching ------


def update_coaching_data(college_id, table, column, value):
    cursor.execute("UPDATE `" + table + "` SET `" + column + "` = '" + value + "' WHERE (`institute_id` = '" + str(college_id) + "')")
    mydb.commit()

    # ----- Coaching ------

    # ----- College ------


def update_college_data(college_id, table, column, value):
    cursor.execute("UPDATE `" + table + "` SET `" + column + "` = '" + value + "' WHERE (`college_id` = '" + str(college_id) + "')")
    mydb.commit()

    # ----- College ------


# ----------------------------------------------- Queries End ---------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)

# query = "SELECT * from coaching_institute"
# cursor.execute(query)
# res = cursor.fetchall()
# institute_id = 1
# for i in res:
#     institute_id += 1


# def insert(columns):
#     print("INSERT INTO`coaching_institute` "
#           "(`institute_id`, `institute_name`, `location_id`, `exams_taught`, `fees`, `hostel_availability`, `results`) "
#           "VALUES ('" + str(institute_id) + "', '" + columns[0] + "', '" + columns[1] + "', '" + columns[2] + "', '" + columns[3] + "', '" +
#           columns[4] + "', '" + columns[5] + "')")
#     cursor.execute("INSERT INTO`coaching_institute` "
#                    "(`institute_id`, `institute_name`, `location_id`, `exams_taught`, `fees`, `hostel_availability`, `results`) "
#                    "VALUES ('" + str(institute_id) + "', '" + columns[0] + "', '" + columns[1] + "', '" + columns[2] + "', '" + columns[
#                        3] + "', '" + columns[4] + "', '" + columns[5] + "')")
#     mydb.commit()

# name = request.form["name"]
# exam = request.form["exam"]
# selection = request.form["selection"]
# location = request.form["location"]
# fee = request.form["fee"]
# hostel_availability = request.form["hostel"]
# columns = [name, location, exam, fee, hostel_availability, selection]
# insert(columns)
