import os
import sys
sys.path.append("api/calculation/src/")
from calculation.src.airplane import Airplane
import json

def process_data():
    try:
        # Read the contents of the matrix.json file
        print("matrix.json")
        with open("matrix.json", "r") as f:
            matrix_content = json.load(f)

        # Return the file in the response
        return {
            "success": True,
            "data": matrix_content,
            "headers": {
                "Content-Disposition": f"attachment; filename={os.path.basename('matrix.json')}",
                "Content-Type": "application/json"
            }
        }
    except Exception as e:
        print("Error:", e)
        return {"success": False, "error": "An error occurred."}





# create function that put aircraft matrix and control matrix in a txt file

def write_matrix(aircraft_matrix, control_matrix):
    # Write both matrices to a JSON file
    with open("matrix.json", "w") as f:
        matrix = {
            "aircraft_matrix": aircraft_matrix.tolist(),
            "control_matrix": control_matrix.tolist()
        }

        json.dump(matrix, f)


print("ici")
input_data = sys.argv[1]
# Parse the JSON string to get the list of files
files = json.loads(input_data)['input']

# Access the individual files in the list
file1 = files[0]
file2 = files[1]

data = [file1, file2]
print(data)

# Example to use the class
# (the values are from a Business JET aircraft)
S = 21.55 # Wing area
A = 5.09 # Aspect ratio
lambda_ = 0.5 # Taper ratio
b = 10.48 # Wingspan
c_mean = 2.13 # Mean chord
e = 0.94 # Oswald factor

airplane = Airplane("Business JET", S, A, lambda_, b, c_mean, e, data)
print("--------------------------------")
print("Exemple to get the aircraft matrix:\n")
airplane.get_longitudinal_aicraft_matrix()
print(airplane.aircraft_matrix)
print("--------------------------------")

# print("Eigen values:\n")
# airplane.set_characteristic_equation()
# airplane.set_eigenvalues()
# print(airplane.get_eigenvalues())
# print("--------------------------------")

print("Exemple to get a cruise condition")
print("U0 = ", airplane.get_cruise_condition("V"))
print("--------------------------------")


# print("Parameters")
# params = ["Xu", "Xw", "Zu", "Zw", "Zw_dot", "Zq", "Mu", "Mw", "Mw_dot", "Mq"]
# for param in params:
#     print(param, " = ", getattr(airplane, param))
# print("--------------------------------")

airplane.get_longitudinal_control_matrix()
print("Control matrix (elevator/throttle) for longitudinal stability")
print(airplane.get_long_stability_control_matrix())

write_matrix(airplane.aircraft_matrix, airplane.control_matrix)

process_data()






