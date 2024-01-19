from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ners:Ners!23@122.175.43.71:5003/experiment'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    experience_level = db.Column(db.String(20), nullable=False)
    team = db.Column(db.String(20), nullable=False)

# 1. Post API for registering an employee
@app.route('/register', methods=['POST'])
def register_employee():
    data = request.get_json()

    new_employee = Employees(
        name=data['name'],
        position=data['position'],
        experience_level=data['experience_level'],
        team=data['team']
    )

    db.session.add(new_employee)
    db.session.commit()

    return jsonify({'message': 'Employee registered successfully'}), 201

# 2. Filter employees based on experience level
@app.route('/employees/sorted', methods=['GET'])
def get_sorted_employees():
    sorted_employees = Employees.query.order_by(Employees.experience_level.desc()).all()
    employee_list = [{'name': employee.name, 'position': employee.position, 'experience_level': employee.experience_level, } for employee in sorted_employees]

    return jsonify({'employees': employee_list})

# 3. Count and details of developers in different teams
@app.route('/developers/count', methods=['GET'])
def get_developer_count():
    ui_developers_count = Employees.query.filter_by(team='UI').count()
    be_developers_count = Employees.query.filter_by(team='BE').count()
    testing_developers_count = Employees.query.filter_by(team='Testing').count()

    ui_developers = [{'name': employee.name, 'position': employee.position, 'experience_level': employee.experience_level} for employee in Employees.query.filter_by(team='UI').all()]
    be_developers = [{'name': employee.name, 'position': employee.position, 'experience_level': employee.experience_level} for employee in Employees.query.filter_by(team='BE').all()]
    testing_developers = [{'name': employee.name, 'position': employee.position, 'experience_level': employee.experience_level} for employee in Employees.query.filter_by(team='Testing').all()]

    result = {
        'UI_Developers_Count': ui_developers_count,
        'UI_Developers_Details': ui_developers,
        'BE_Developers_Count': be_developers_count,
        'BE_Developers_Details': be_developers,
        'Testing_Developers_Count': testing_developers_count,
        'Testing_Developers_Details': testing_developers
    }

    return jsonify(result)

if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)
