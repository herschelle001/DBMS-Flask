from flask import Flask, render_template, request
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


@app.route("/student")
def student():
    return render_template("student.html")


@app.route("/parent")
def parent():
    return render_template("parent.html")

# --------------------------------------------------- student ------------------------------------------------


# ------------------------------------------------- student end-------------------------------------------------


# --------------------------------------------------- parent -------------------------------------------------


# --------------------------------------------------parent end--------------------------------------------------


# --------------------------------------------------- coaching -----------------------------------------------



query = "SELECT * from coaching_institute"
cursor.execute(query)
result = cursor.fetchall()
coaching_names = []
for i in result:
    coaching_names.append(i[1])

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
        update_coaching(college_id, 'coaching_institute', 'institute_name', name_update)

    if not (fee_update == ""):
        update_coaching(college_id, 'coaching_institute', 'fees', fee_update)

    if not (hostel_avail_update == ""):
        update_coaching(college_id, 'coaching_institute', 'hostel_availability', hostel_avail_update)

    if not (taught_update == ""):
        update_coaching(college_id, 'coaching_institute', 'exams_taught', taught_update)

    return "Success"



def update_coaching(college_id, table, column, value):
    print("UPDATE `" + table + "` SET `" + column + "` = '" + value + "' WHERE (`college_id` = '" + str(college_id) + "')")
    cursor.execute("UPDATE `" + table + "` SET `" + column + "` = '" + value + "' WHERE (`institute_id` = '" + str(college_id) + "')")
    mydb.commit()
    pass


# ---------------------------------------------coaching end----------------------------------------------------------

# --------------------------------------------- college ---------------------------------------------------------------


query = "SELECT * from college_general"
cursor.execute(query)
result = cursor.fetchall()
college_names = []
for i in result:
    college_names.append(i[2])


@app.route("/college/success", methods=["GET", "POST"])
def receive_college_data():
    selected = request.form["selected"]
    college_id = -1
    for i in range(len(college_names)):
        if selected == college_names[i]:
            college_id = i + 1
            break

    name = request.form["name"]
    hostelAvailability = request.form["hostel"]
    website = request.form["website"]
    placed_students = request.form["placed"]
    avg_pkg = request.form["avg"]
    highest_pkg = request.form["highest"]
    area = request.form["area"]
    fee = request.form["fee"]
    mode_of_admission = request.form["admission"]

    if not (website == ""):
        update(college_id, 'college_general', 'college_website', website)

    if not (placed_students == ""):
        update(college_id, 'college_placement_stats', 'students_placed_percent', placed_students)

    if not (avg_pkg == ""):
        update(college_id, 'college_placement_stats', 'avg_package', avg_pkg)

    if not (highest_pkg == ""):
        update(college_id, 'college_placement_stats', 'highest_package', highest_pkg)

    if not (fee == ""):
        update(college_id, 'college_general', 'fees', fee)

    if not (mode_of_admission == ""):
        update(college_id, 'college_general', 'mode_of_admission', mode_of_admission)

    if not (name == ""):
        update(college_id, 'college_general', 'full_name', name)

    if not (area == ""):
        update(college_id, 'college_location', 'area_in_acres', area)

    return "Success"


def update(college_id, table, column, value):
    print("UPDATE `" + table + "` SET `" + column + "` = '" + value + "' WHERE (`college_id` = '" + str(college_id) + "')")
    cursor.execute("UPDATE `" + table + "` SET `" + column + "` = '" + value + "' WHERE (`college_id` = '" + str(college_id) + "')")
    mydb.commit()

# ------------------------------------------------college end---------------------------------------------------------


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