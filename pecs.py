import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import glob


def calculate_xy(file, E_red, pH):
    df = pd.read_csv(file, sep = "\\s+", skiprows = 19, header = None)
    df.columns = ["No", "time", "potential", "current"]
    x = df["potential"] + E_red + (0.059 * pH) #Col("Potential")+Ered.+(0.059*pH)
    y = df["current"]/0.1979 #Col("Current")*1000
    return x, y


main_path = str(input("Enter the main path: "))
folders = os.listdir(main_path)

print("Select the following options:")
print("'y' if you wish to save the plots")
print("'n' if you do not wish to save the plots (Only the output csv will be created)")
plot_yn = str(input("Do you want to plot the data? (y/n)"))

E_reds, pHs = [], []
for f in folders:
    # f = f.replace(" ", "_")
    E_red, pH = float(input(f"Enter the E_red value for {f} (Enter 0 if it is not needed for your calculation): ")), float(input(f"Enter the pH value for {f} (Enter 0 if it is not needed for your calculation): "))
    E_reds.append(E_red)
    pHs.append(pH)


lsv_master_dict = {}
cv_master_dict = {}

if plot_yn == "y":
    master_df_list = []
    for f, E_red, pH in zip(folders, E_reds, pHs):
        lsv_files = glob.glob(os.path.join(main_path, f, "*lsv*.txt"))
        cv_files = glob.glob(os.path.join(main_path, f, "*cv*.txt"))

        for lsv_file in lsv_files:
            x,y = calculate_xy(lsv_file, E_red, pH)
            plt.plot(x, y, label=lsv_file.split('\\')[-1].split('.')[0])
            plt.xlabel('E vs RHE (V)')
            plt.ylabel('Current Density')
            plt.legend(loc='upper right', bbox_to_anchor=(1, 1), fontsize=8)
            
            df = pd.DataFrame({'E_vs_RHE': x, 'Current_density': y})
            df.to_csv(lsv_file.replace('.txt', '_output.csv'), index=False)

            key_base = os.path.basename(lsv_file).replace('.txt', '')
            lsv_master_dict[f"{key_base}_x"] = x
            lsv_master_dict[f"{key_base}_y"] = y

        plt.grid()
        plt.title(f"Plot for {f}, LSV")
        plt.savefig(os.path.join(main_path, f, "lsv_plot.png"), dpi=300)
        plt.savefig(os.path.join(main_path, f, "lsv_plot.pdf"), dpi=300)
        plt.show()


        for cv_file in cv_files:
            x,y = calculate_xy(cv_file, E_red, pH)

            plt.plot(x, y, label=cv_file.split('\\')[-1].split('.')[0])
            plt.xlabel('E vs RHE (V)')
            plt.ylabel('Current Density')
            plt.legend(loc='upper right', bbox_to_anchor=(1, 1), fontsize=8)
            
            df = pd.DataFrame({'E_vs_RHE': x, 'Current_density': y})
            df.to_csv(cv_file.replace('.txt', '_output.csv'), index=False)

            key_base = os.path.basename(cv_file).replace('.txt', '')
            cv_master_dict[f"{key_base}_x"] = x
            cv_master_dict[f"{key_base}_y"] = y

        plt.grid()
        plt.title(f"Plot for {f}, CV")
        plt.savefig(os.path.join(main_path, f, "cv_plot.png"), dpi=300)
        plt.savefig(os.path.join(main_path, f, "cv_plot.pdf"), dpi=300)
        plt.show()

else:
    for f, E_red, pH in zip(folders, E_reds, pHs):
        lsv_files = glob.glob(os.path.join(main_path, f, "*lsv*txt"))
        cv_files = glob.glob(os.path.join(main_path, f, "*cv*txt"))

        for lsv_file in lsv_files:
            x, y = calculate_xy(lsv_file, E_red, pH)

            # Save individual output
            df = pd.DataFrame({'E_vs_RHE': x, 'Current_density': y})
            df.to_csv(lsv_file.replace('.txt', '_output.csv'), index=False)

            # Add to master dict
            key_base = os.path.basename(lsv_file).replace('.txt', '')
            lsv_master_dict[f"{key_base}_x"] = x
            lsv_master_dict[f"{key_base}_y"] = y

        for cv_file in cv_files:
            x, y = calculate_xy(cv_file, E_red, pH)

            # Save individual output
            df = pd.DataFrame({'E_vs_RHE': x, 'Current_density': y})
            df.to_csv(cv_file.replace('.txt', '_output.csv'), index=False)

            # Add to master dict
            key_base = os.path.basename(cv_file).replace('.txt', '')
            cv_master_dict[f"{key_base}_x"] = x
            cv_master_dict[f"{key_base}_y"] = y


# Convert to DataFrames and save
lsv_master_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in lsv_master_dict.items()]))
cv_master_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in cv_master_dict.items()]))

lsv_master_df.to_csv(os.path.join(main_path, "master_LSV.csv"), index=False)
cv_master_df.to_csv(os.path.join(main_path, "master_CV.csv"), index=False)

print("Khel Khatam natak band")
print("ok friend bye")
