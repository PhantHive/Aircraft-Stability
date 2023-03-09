import os
import re
import sys
sys.path.append("api/calculation/src/")
from calculation.src.airplane import Airplane
import json

def process_data():

    try:
        # Read the contents of the latMatrix.json file
        with open("latMatrix.json", "r") as f:
            matrix_content = json.load(f)

        # Return the file in the response
        return {
            "success": True,
            "data": matrix_content,
            "headers": {
                "Content-Disposition": f"attachment; filename={os.path.basename('latMatrix.json')}",
                "Content-Type": "application/json"
            }
        }
    except Exception as e:
        print("Error:", e)
        return {"success": False, "error": "Vérifier que les fichiers sont bien au bon format et dans le bon ordre. Voir README.md"}


# create function that put aircraft matrix and control matrix in a txt file

def write_matrix(aircraft_matrix, control_matrix):
    # Write both matrices to a JSON file
    with open("latMatrix.json", "w") as f:
        matrix = {
            "aircraft_matrix": aircraft_matrix.tolist(),
            "control_matrix": control_matrix.tolist()
        }

        json.dump(matrix, f)

def replacer(data_file):
    data_file = re.sub(r'\s+', '', data_file)
    return data_file


# collect sys arg as a string
data_str1 = sys.argv[1] # latgitudinalSD.json
data_str2 = sys.argv[2] # steadyConditions.json


data_str1 = data_str1.replace('\\r', '').replace('\\n', ''). replace(' ', '').replace('\\', '')
data_str2 = data_str2.replace('\\r', '').replace('\\n', ''). replace(' ', '').replace('\\', '')

# remove any extra spaces
data_str1 = replacer(data_str1)
data_str2 = replacer(data_str2)

# match exactly if there is a ',n'
data_str1 = re.sub(r',n', ',', data_str1)
data_str2 = re.sub(r',n', ',', data_str2)

# match exactly if there is a 'r,'
data_str1 = re.sub(r',r', ',', data_str1)
data_str2 = re.sub(r',r', ',', data_str2)


# do something with file1 and file2
# print(f"Contents of file1: {data_str1}")
# print(f"Contents of file2: {data_str2}")


data = [data_str2, data_str1]

# Example to use the class
# (the values are from a Business JET aircraft)
S = 21.55  # Wing area
A = 5.09  # Aspect ratio
lambda_ = 0.5  # Taper ratio
b = 10.48  # Wingspan
c_mean = 2.13  # Mean chord
e = 0.94  # Oswald factor

# CAUTION
# IF YOU WANT TO USE THE DEFAULT FILES, JUST PUT "None" FOR THE LAST ARGUMENT
airplane = Airplane("Business JET", S, A, lambda_, b, c_mean, e, "lateral", data)

print("--------------------------------")

print("Exemple to get the aircraft matrix:\n")
airplane.get_lateral_aircraft_matrix()
print(airplane.aircraft_matrix)

print("--------------------------------")

print("Eigen values:")
airplane.set_eigenvalues()
airplane.set_characteristic_equation()
print(airplane.get_eigenvalues())
poly = airplane.get_characteristic_equation()
print("\nCharacteristic equation:")
for i in range(len(poly) - 1):
    print(abs(poly[-1 - i]), "* s^", len(poly) - i - 1, " + ", end="")
print(abs(poly[0]))

print("--------------------------------")
#
# airplane.set_natural_frequency()
# airplane.set_damping_ratio()
#
# print("Natural frequencies:")
# print(airplane.get_natural_frequency())
#
# print("Damping ratios:")
# print(airplane.get_damping_ratio())
#
# print("--------------------------------")
#
# print("Exemple to get a cruise condition")
# print("U0 = ", airplane.get_cruise_condition("V"))
#
# print("--------------------------------")


# print("Parameters")
# params = ["Xu", "Xw", "Zu", "Zw", "Zw_dot", "Zq", "Mu", "Mw", "Mw_dot", "Mq"]
# for param in params:
#     print(param, " = ", getattr(airplane, param))
# print("--------------------------------")


print("Control matrix (Rudder/Throttle) for lateral stability")
airplane.get_lateral_control_matrix()
print(airplane.control_matrix)
#
# print("--------------------------------")
# print("Plotting the latgitudinal stability")
# # # short_period or phugoid
#
# data = airplane.lat_plot_stability("phugoid")
# print(f"ImageDataPhugoid<{data}>Phugoid")
# data2 = airplane.lat_plot_stability("short_period")
# print(f"ImageDataShort<{data2}>Short")



# write_matrix(airplane.aircraft_matrix, airplane.control_matrix)

# process_data()






