import optuna
import pandas as pd
import numpy as np
import os
import sys
from tabulate import tabulate
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from clip_protocol.utils.utils import save_setup_json, get_real_frequency, display_results
from clip_protocol.utils.errors import compute_error_table

from clip_protocol.count_mean.private_cms_client import run_private_cms_client
from clip_protocol.hadamard_count_mean.private_hcms_client import run_private_hcms_client
class Setup:
    def __init__(self, df):
        self.df = df
        self.events_names, self.privacy_method, self.error_metric, self.error_value, self.tolerance = self.ask_values()
        self.e_ref = 0
        self.found_best_values = False
        self.N = len(self.df)

    def ask_values(self):
        """
        Prompt the user to input configuration parameters.
        Returns:
            tuple: Contains events_names (list), privacy_method (str), 
                   error_metric (str), error (float), tolerance (float)
        """
        print("Please enter the values for the parameters:")

        print(self.df.columns)
        events_inputs = input("🔹 Event columns names (comma-separated): ")
        events_names = [e.strip() for e in events_inputs.split(",") if e.strip()]

        privacy_options = {"1": "PCMeS", "2": "PHCMS"}
        privacy_method = self._ask_option("🔹 Privacy method", privacy_options)
        
        error_metric_options = { "1": "MSE", "2": "RMSE","3": "Lρ Norm"}
        error_metric = self._ask_option("🔹 Error metric", error_metric_options)
        if error_metric == "Lρ Norm":
            self.p = int(input("🔹 ρ value: "))
        
        error_value = float(input("🔹 Error value: "))
        tolerance = float(input("🔹 Tolerance: "))

        return events_names, privacy_method, error_metric, error_value, tolerance
    
    def _ask_option(self, prompt, options):
        """Prompt the user to input configuration parameters."""
        print(f"{prompt}:\n" + "\n".join([f"\t {k}. {v}" for k, v in options.items()]))
        choice = input(f"\t Enter option ({'/'.join(options)}): ").strip()
        while choice not in options:
            choice = input("Invalid option. Try again: ").strip()
        return options[choice]
    
    def filter_dataframe(self):
        """
        Filters the DataFrame to keep only the columns specified,
        if they exist in the DataFrame.
        Returns:
            pd.DataFrame: Filtered DataFrame with selected columns.
        """
        matching_columns = [col for col in self.events_names if col in self.df.columns]
        if not matching_columns:
            print("⚠️ None of the specified event names match the DataFrame columns.")
        
        self.df = self.df[matching_columns]
        self.df.columns = ["user", "value"]

        print(self.df.head())
        before = len(self.df)

        self.df['value'] = self.df['value'].astype(str).apply(lambda x: x.strip())
        self.df = self.df[self.df['value'] != '-']
        self.df = self.df[self.df['value'].str.contains(r'\w', na=False)]

        after = len(self.df)
        print(f"🧹 Removed {before - after} rows with null or zero values.")
        print(f"🧮 Number of rows in the dataset: {self.N}")
        
    
    def run_command(self, e, k, m):
        """
        Runs the selected privacy algorithm with a given privacy budget `e`, `k` y `m`.

        Returns:
            tuple: Containing result, data table, error table, privatized data, and estimated frequencies.
        """
        if self.privacy_method == "PCMeS":
            _, _, df_estimated = run_private_cms_client(k, m, e, self.df)
        elif self.privacy_method == "PHCMS":
            _, _, df_estimated = run_private_hcms_client(k, m, e, self.df)
    
        error_table = compute_error_table(self.real_freq, df_estimated)
        return error_table
    
    def optimize_k_m(self, er=150):
        """
        Optimize the parameters k and m using Optuna.
        Returns:
            tuple: Contains the best k and m values found during optimization.
        """
        self.e_ref = er

        def objective(trial):
            # Choose the event with less frequency
            self.real_freq = get_real_frequency(self.df)
            print(self.real_freq)
            min_freq_value = self.real_freq['Frequency'].min()
            
            # Calculate the value of the range of m
            sobreestimation = float(min_freq_value * self.error_value) / self.N
            m_range = 2.718/sobreestimation

            k = trial.suggest_int("k", 1, 1000)
            m = trial.suggest_int("m", 2, m_range) # m cant be 1 because in the estimation m/m-1 -> 1/0
            print(f"Trying k={k}, m={m}, e={self.e_ref}")

            error_table = self.run_command(self.e_ref, k, m)
            error = float([v for k, v in error_table if k == self.error_metric][0])
            print(f"Error: {error}")

            if error <= (self.error_value * min_freq_value):
                print(f"{error} <= {self.error_value}")
                self.found_best_values = True
                trial.study.stop()
            print(error - (self.error_value * min_freq_value))
            return error - (self.error_value * min_freq_value)
        
        study = optuna.create_study(direction="minimize")
        study.optimize(objective, n_trials=100)

        return study.best_params["k"], study.best_params["m"], er
    
    def no_privacy(self):
        headers=[
            "Element", "Real Frequency", "Real Percentage", 
            "Estimated Frequency", "Estimated Percentage", "Estimation Difference", 
            "Percentage Error"
        ]
        _, _, estimated = run_private_cms_client(self.k, self.m, self.e_ref, self.df)
        real = get_real_frequency(self.df)
        table = display_results(real, estimated)
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

def generate_dataset(n_rows=2000, n_users=1, n_events=1, unique_values_per_event=10):
    np.random.seed(42)
    data = {}

    data["user"] = np.random.choice(
        [f"user_{i+1}" for i in range(n_users)],
        size=n_rows
    )

    for i in range(n_events):
        column_name = f"value"
        data[column_name] = np.random.choice(
            [f"value_{j}" for j in range(1, unique_values_per_event + 1)],
            size=n_rows,
            p=np.random.dirichlet(np.ones(unique_values_per_event))
        )
    
    return pd.DataFrame(data)

def run_setup(df):
    """
    Main function to run the setup process.
    """
    setup_instance = Setup(df)
    setup_instance.filter_dataframe()
    

    while not setup_instance.found_best_values:
        setup_instance.k, setup_instance.m, setup_instance.e = setup_instance.optimize_k_m()
        if not setup_instance.found_best_values:
            setup_instance.e_ref += 50
    
    setup_instance.no_privacy()
    
    print(f"Optimal parameters found: k={setup_instance.k}, m={setup_instance.m}, e={setup_instance.e_ref}")
    print(f"Events: {setup_instance.events_names}")
    print(f"Privacy method: {setup_instance.privacy_method}")
    print(f"Error metric: {setup_instance.error_metric}")
    
    save_setup_json(setup_instance)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run privatization mask with input CSV")
    parser.add_argument("-i", type=str, required=True, help="Path to the input excel file")
    args = parser.parse_args()
    if not os.path.isfile(args.i):
        print(f"❌ File not found: {args.i}")
        sys.exit(1)

    df = pd.read_excel(args.i)
    run_setup(df)