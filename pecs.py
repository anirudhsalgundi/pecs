import pandas as pd
import os
import matplotlib.pyplot as plt
import glob


def calculate_xy(file, E_red, pH):
    """
    This function reads the txt file containing the LSV or CV data,
    extracts the relevant columns, and calculates the x and y values for plotting.
    The function takes the file path, E_red, and pH as inputs.
    It reads the file, skips the first 19 rows, and assigns column names.
    The function then extracts the 'potential' and 'current' columns. 
    The x in the fuction is E vs RHE (V) and y is the current density.
    """

    # Read the data file and skip the first 19 rows
    df = pd.read_csv(file, sep = "\\s+", skiprows = 19, header = None)

    # Assign column names
    df.columns = ["No", "time", "potential", "current"]

    # Calculate x and y values
    x = df["potential"] + E_red + (0.059 * pH)
    y = df["current"]/0.1979 

    # return x, y values
    return x, y


main_path = str(input("Enter the main path: ")) # instead of input, you can directly define the path here "D\nam\data\20250411"
folders = os.listdir(main_path) # Lists all the folders in the main path

E_reds, pHs = [], [] # Define empty lists to store E_red and pH values

# Loop through each folder and get the E_red and pH values
for f in folders:
    # Go inside each folder and Ask the user for E_red and pH values for each folder
    E_red, pH = float(input(f"Enter the E_red value for {f} (Enter 0 if it is not needed for your calculation): ")), float(input(f"Enter the pH value for {f} (Enter 0 if it is not needed for your calculation): "))

    # Once you enter the values, append them to the lists
    E_reds.append(E_red)
    pHs.append(pH)


# Now lets ask the user if they want to save the plots
# Print the options for saving the plots
print("""
Select the following options:
press 'y' if you wish to save the plots
press 'n' if you do not wish to save the plots (Only the output csv will be created)
      """)

# Ask the user if they want to save the plots
plot_yn = str(input("Do you want to plot the data? (y/n)"))


# define empty dictionaries to store the data for LSV and CV
lsv_master_dict = {}
cv_master_dict = {}

# If the user wants to plot and save the data
if plot_yn == "y":
    # loop through each folder and read the LSV and CV files, while taking the E_red and pH values into account for the respective folder
    for f, E_red, pH in zip(folders, E_reds, pHs):
        # Get the LSV and CV files in the folder
        # The glob module is used to find all the pathnames matching a specified pattern
        lsv_files = glob.glob(os.path.join(main_path, f, "*lsv*.txt"))
        cv_files = glob.glob(os.path.join(main_path, f, "*cv*.txt"))

        # Let us loop through the LSV files to read them one by one
        for lsv_file in lsv_files:
            # read the lsv file, and use our function to calculate x and y values (E vs RHE and current density)
            # The function calculate_xy is defined above
            x,y = calculate_xy(lsv_file, E_red, pH)

            # plot the x and y data. We have split the file name to get the name of the file without the path and extension and using it as the plot legend
            plt.plot(x, y, label=lsv_file.split('\\')[-1].split('.')[0])

            # Define x and y labels and legend
            plt.xlabel('E vs RHE (V)')
            plt.ylabel('Current Density')
            plt.legend(loc='upper right', bbox_to_anchor=(1, 1), fontsize=8)

            # Save individual output as a data frame and convert it into a CSV file
            df = pd.DataFrame({'E_vs_RHE': x, 'Current_density': y})
            df.to_csv(lsv_file.replace('.txt', '_output.csv'), index=False)

            # Read the file name, remove the .txt in the file name and replace it with filename_x and filename_y for the columns of the master data
            key_base = os.path.basename(lsv_file).replace('.txt', '')
            lsv_master_dict[f"{key_base}_x"] = x
            lsv_master_dict[f"{key_base}_y"] = y

        # Once all the lsv files are read and plotted, show them as a single plot with all the data.
        # If you put these codes inside the loop, you will get individual plots for each file
        # But since we want to see all the lsv plots in a single plot, we will do it here
        # Save the plot as a png and pdf file
        # We will add grids and title to the plot
        plt.grid()
        plt.title(f"Plot for {f}, LSV")
        plt.tight_layout()
        plt.savefig(os.path.join(main_path, f, "lsv_plot.png"), dpi=300)
        plt.savefig(os.path.join(main_path, f, "lsv_plot.pdf"), dpi=300)
        # Show the plot
        plt.show()


        # Same procedure for the CV files, everything is same as above for LSV files. Only file name is changed.
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
        plt.tight_layout()
        plt.savefig(os.path.join(main_path, f, "cv_plot.png"), dpi=300)
        plt.savefig(os.path.join(main_path, f, "cv_plot.pdf"), dpi=300)
        plt.show()

else:
    # loop through each folder and read the LSV and CV files, while taking the E_red and pH values into account for the respective folder
    for f, E_red, pH in zip(folders, E_reds, pHs):
        # Get the LSV and CV files in the folder
        # The glob module is used to find all the pathnames matching a specified pattern
        lsv_files = glob.glob(os.path.join(main_path, f, "*lsv*txt"))
        cv_files = glob.glob(os.path.join(main_path, f, "*cv*txt"))

        # Let us loop through the LSV files to read them one by one
        for lsv_file in lsv_files:

            # read the lsv file, and use our function to calculate x and y values (E vs RHE and current density)
            # The function calculate_xy is defined above
            x, y = calculate_xy(lsv_file, E_red, pH)

            # Save individual output as a data frame and convert it into a CSV file
            df = pd.DataFrame({'E_vs_RHE': x, 'Current_density': y})
            df.to_csv(lsv_file.replace('.txt', '_output.csv'), index=False)

            # Read the file name, remove the .txt in the file name and replace it with filename_x and filename_y for the columns of the master data
            key_base = os.path.basename(lsv_file).replace('.txt', '')
            lsv_master_dict[f"{key_base}_x"] = x
            lsv_master_dict[f"{key_base}_y"] = y

        # Same procedure for the CV files
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

# Convert LSV master dictionary to DataFrame and save
lsv_master_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in lsv_master_dict.items()]))
lsv_master_df.to_csv(os.path.join(main_path, "master_LSV.csv"), index=False)

# Convert CV master dictionary to DataFrame and save
cv_master_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in cv_master_dict.items()]))
cv_master_df.to_csv(os.path.join(main_path, "master_CV.csv"), index=False)

print("Khel Khatam natak band")
print("ok friend bye")
