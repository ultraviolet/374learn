#!/usr/bin/env python3
"""
Standalone external grader for fooling-set coding questions.
Reads /grade/student/user_code.py and /grade/tests/language_definition.py.
Does NOT depend on the python_autograder framework or data.json params.
"""

import json
import sys
import traceback

sys.path.insert(0, "/grade/tests")
sys.path.insert(0, "/grade/student")

RESULTS_PATH = "/grade/results/results.json"


def write_result(score, message):
    with open(RESULTS_PATH, "w") as f:
        json.dump({"gradable": True, "score": score, "message": message}, f)


try:
    from language_definition import NUM_ELEMENTS_TO_CHECK, isInLanguage
except Exception as e:
    write_result(0, f"Internal error loading language definition: {e}")
    sys.exit(0)

try:
    import user_code
except Exception as e:
    write_result(0, f"Error in your code:\n{traceback.format_exc()}")
    sys.exit(0)

# Collect fooling set elements
try:
    elements = {}
    for n in range(1, NUM_ELEMENTS_TO_CHECK + 1):
        elements[n] = user_code.getFoolingSetElement(n)
except Exception as e:
    write_result(0, f"Error calling getFoolingSetElement:\n{traceback.format_exc()}")
    sys.exit(0)

# Check all pairs
for i, x in elements.items():
    for j, y in elements.items():
        if i == j:
            continue

        try:
            z = user_code.getDistinguishingSuffix(i, j)
        except Exception as e:
            write_result(0, f"Error calling getDistinguishingSuffix({i}, {j}):\n{traceback.format_exc()}")
            sys.exit(0)

        xz = x + z
        yz = y + z
        x_in = isInLanguage(xz)
        y_in = isInLanguage(yz)

        if x_in == y_in:
            if x_in:
                detail = f"Both xz = '{xz}' and yz = '{yz}' are in the language."
            else:
                detail = f"Both xz = '{xz}' and yz = '{yz}' are NOT in the language."
            write_result(
                0,
                f"When i = {i} and j = {j}, suffix z = '{z}' fails to distinguish:\n"
                f"  x = '{x}'\n  y = '{y}'\n{detail}",
            )
            sys.exit(0)

write_result(1, "All pairs of distinct elements are correctly distinguished!")
