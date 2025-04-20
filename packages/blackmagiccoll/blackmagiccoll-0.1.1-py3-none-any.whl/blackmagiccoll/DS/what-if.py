import numpy as np
from scipy.optimize import fsolve

grades = [58, 70, 72, 60]

def find_required_final(x):
    all_grades = grades + [x]
    return np.mean(all_grades) - 72

required_final_score = fsolve(find_required_final, 60)[0]

print(f"The student needs to score {required_final_score:.2f} in the final exam to pass.")
