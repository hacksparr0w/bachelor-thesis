import json
import sys

import numpy as np


def main():
    data = json.load(sys.stdin)
    ev_curves = data["ev_curves"]

    v_0_data = []
    b_0_data = []

    for ev_curve in ev_curves:
        fit = ev_curve["eos_fit"]

        if fit["eos"] != "birch_murnaghan":
            continue

        params = fit["params"]

        v_0_data.append(params["V0"])
        b_0_data.append(params["B0"])

    v_0_data = np.array(v_0_data)
    b_0_data = np.array(b_0_data)

    print("V_0: {:.2f} +/- {:.2f}".format(v_0_data.mean(), v_0_data.std()))
    print("B_0: {:.2f} +/- {:.2f}".format(b_0_data.mean(), b_0_data.std()))


if __name__ == "__main__":
    main()
