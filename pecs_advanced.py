import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import glob


def calculate_xy(file, E_red, pH):
    df = pd.read_csv(file, sep=r"\s+", skiprows=19, header=None)
    df.columns = ["No", "time", "potential", "current"]
    x = df["potential"] + E_red + (0.059 * pH)
    y = df["current"] / 0.1979
    return x, y


def process_files(files, E_red, pH, folder, master_dict, plot=False, plot_type=""):
    for file in files:
        x, y = calculate_xy(file, E_red, pH)

        df = pd.DataFrame({'E_vs_RHE': x, 'Current_density': y})
        df.to_csv(file.replace('.txt', '_output.csv'), index=False)

        key_base = os.path.basename(file).replace('.txt', '')
        master_dict[f"{key_base}_x"] = x
        master_dict[f"{key_base}_y"] = y

        if plot:
            plt.plot(x, y, label=key_base)

    if plot and files:
        plt.xlabel('E vs RHE (V)')
        plt.ylabel('Current Density')
        plt.title(f"Plot for {folder}, {plot_type.upper()}")
        plt.legend(loc='upper right', bbox_to_anchor=(1, 1), fontsize=8)
        plt.grid()
        plt.tight_layout()
        plot_path = os.path.join(main_path, folder, f"{plot_type.lower()}_plot")
        plt.savefig(plot_path + ".png", dpi=300)
        plt.savefig(plot_path + ".pdf", dpi=300)
        plt.show()


def main():
    global main_path
    main_path = input("Enter the main path: ").strip()
    folders = [f for f in os.listdir(main_path) if os.path.isdir(os.path.join(main_path, f))]

    plot_yn = input("Do you want to plot the data? (y/n): ").strip().lower()

    E_reds, pHs = [], []
    for f in folders:
        print(f"\nFolder: {f}")
        E_red = float(input("  Enter E_red (0 if not needed): "))
        pH = float(input("  Enter pH (0 if not needed): "))
        E_reds.append(E_red)
        pHs.append(pH)

    lsv_master_dict = {}
    cv_master_dict = {}

    for f, E_red, pH in zip(folders, E_reds, pHs):
        folder_path = os.path.join(main_path, f)
        lsv_files = glob.glob(os.path.join(folder_path, "*lsv*.txt"))
        cv_files = glob.glob(os.path.join(folder_path, "*cv*.txt"))

        if plot_yn == "y":
            process_files(lsv_files, E_red, pH, f, lsv_master_dict, plot=True, plot_type="LSV")
            process_files(cv_files, E_red, pH, f, cv_master_dict, plot=True, plot_type="CV")
        else:
            process_files(lsv_files, E_red, pH, f, lsv_master_dict)
            process_files(cv_files, E_red, pH, f, cv_master_dict)

    # Save master files
    pd.DataFrame(dict([(k, pd.Series(v)) for k, v in lsv_master_dict.items()]))\
        .to_csv(os.path.join(main_path, "master_LSV.csv"), index=False)

    pd.DataFrame(dict([(k, pd.Series(v)) for k, v in cv_master_dict.items()]))\
        .to_csv(os.path.join(main_path, "master_CV.csv"), index=False)

    print("\nKhel Khatam. Natak Band.")
    print("ok friend bye")


if __name__ == "__main__":
    main()