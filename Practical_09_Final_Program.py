"""Practical 09: Statistical analysis of chemical engineering measurements."""

import pandas as pd


def print_ascii_boxplot(data: pd.DataFrame) -> None:
    """Display a text-based box plot for each experiment without extra packages."""
    print("\nTemperature distribution by experiment (text box plots)")
    width = 40

    for experiment_id, group in data.groupby("Experiment_ID"):
        values = group["Temperature_C"].dropna().sort_values()
        minimum = float(values.min())
        maximum = float(values.max())
        first_quartile = float(values.quantile(0.25))
        median = float(values.median())
        third_quartile = float(values.quantile(0.75))

        def position(value: float) -> int:
            if minimum == maximum:
                return width // 2
            return round((value - minimum) / (maximum - minimum) * width)

        plot = [" "] * (width + 1)
        for index in range(position(minimum), position(maximum) + 1):
            plot[index] = "-"
        plot[position(minimum)] = "|"
        plot[position(maximum)] = "|"
        plot[position(first_quartile)] = "["
        plot[position(third_quartile)] = "]"
        plot[position(median)] = "|"

        print(f"{experiment_id:>5}: {''.join(plot)}")
        print(
            f"       min={minimum:.2f}, Q1={first_quartile:.2f}, "
            f"median={median:.2f}, Q3={third_quartile:.2f}, max={maximum:.2f}"
        )

    print("       | = minimum/median/maximum; [ ] = middle 50% of measurements")


def main() -> None:
    print("PRACTICAL 09: EXPERIMENTAL MEASUREMENT STATISTICS")

    # Activities 1-3: create repeated temperature data and compare manual and Pandas means.
    temperature_data = pd.DataFrame(
        {
            "Measurement_No": [1, 2, 3, 4, 5],
            "Temperature_C": [78.2, 79.1, 78.7, 79.0, 78.5],
        }
    )
    readings = temperature_data["Temperature_C"].tolist()
    manual_mean = sum(readings) / len(readings)
    pandas_mean = temperature_data["Temperature_C"].mean()

    print("\nActivities 1-3: repeated temperature measurements")
    print(temperature_data.to_string(index=False))
    print(f"Manual mean: {manual_mean:.2f} C")
    print(f"Pandas mean: {pandas_mean:.2f} C")

    # Activities 4-5 and 8: compare two experimental conditions.
    condition_data = pd.DataFrame(
        {
            "Condition_A": [78.2, 79.1, 78.7, 79.0, 78.5],
            "Condition_B": [76.0, 81.5, 78.7, 82.0, 74.8],
        }
    )
    condition_summary = condition_data.agg(["mean", "std"]).T
    print("\nActivities 4, 5, and 8: condition comparison")
    print(condition_summary.to_string(float_format=lambda value: f"{value:.2f}"))
    print("Condition B has more variation because its sample standard deviation is larger.")

    # Activities 6-7: summarize all the chemical-process measurements.
    experiment_data = pd.DataFrame(
        {
            "Temperature_C": [78.2, 79.1, 78.7, 79.0, 78.5, 78.8, 79.2, 78.6],
            "Pressure_bar": [2.10, 2.12, 2.08, 2.11, 2.09, 2.13, 2.10, 2.07],
            "Concentration_mol_L": [0.82, 0.80, 0.81, 0.83, 0.79, 0.82, 0.81, 0.80],
            "pH": [6.9, 7.0, 6.8, 7.1, 6.9, 7.0, 6.9, 6.8],
        }
    )
    numeric_columns = experiment_data.select_dtypes(include="number").columns
    print("\nActivities 6-7: multiple experimental measurements")
    print(experiment_data.to_string(index=False))
    print("\nPandas descriptive statistics:")
    print(experiment_data.describe().to_string(float_format=lambda value: f"{value:.3f}"))
    print("\nMean and sample standard deviation:")
    print(
        experiment_data[numeric_columns]
        .agg(["mean", "std", "min", "max"])
        .T.to_string(float_format=lambda value: f"{value:.3f}")
    )

    # Activity 9: calculate a grouped summary for three experiments.
    grouped_data = pd.DataFrame(
        {
            "Experiment_ID": ["Exp1"] * 3 + ["Exp2"] * 3 + ["Exp3"] * 3,
            "Measurement_No": [1, 2, 3] * 3,
            "Temperature_C": [78.2, 79.1, 78.7, 79.0, 78.5, 78.8, 79.2, 78.6, 78.9],
        }
    )
    before_summary = grouped_data.groupby("Experiment_ID")["Temperature_C"].agg(
        ["count", "mean", "std", "min", "max"]
    )
    print("\nActivity 9: grouped mean and standard deviation")
    print(before_summary.to_string(float_format=lambda value: f"{value:.3f}"))

    # Activity 10: add, but do not automatically remove, an unusual reading.
    data_with_unusual_reading = pd.concat(
        [
            grouped_data,
            pd.DataFrame(
                [{"Experiment_ID": "Exp1", "Measurement_No": 4, "Temperature_C": 100.0}]
            ),
        ],
        ignore_index=True,
    )
    after_summary = data_with_unusual_reading.groupby("Experiment_ID")[
        "Temperature_C"
    ].agg(["count", "mean", "std", "min", "max"])
    print("\nActivity 10: Exp1 before and after adding the unusual 100.0 C reading")
    print(
        pd.concat(
            {
                "Before": before_summary.loc["Exp1"],
                "After": after_summary.loc["Exp1"],
            },
            axis=1,
        ).to_string(float_format=lambda value: f"{value:.3f}")
    )
    print("An unusual measurement should be investigated, not automatically deleted.")

    # Activity 11: a text box plot shows the distribution without requiring Matplotlib.
    print_ascii_boxplot(grouped_data)

    # Compare relative variation only for ratio-scale measurements, not logarithmic pH.
    ratio_scale_columns = ["Temperature_C", "Pressure_bar", "Concentration_mol_L"]
    coefficients_of_variation = (
        experiment_data[ratio_scale_columns].std()
        / experiment_data[ratio_scale_columns].mean().abs()
        * 100
    )
    most_variable = coefficients_of_variation.idxmax()
    least_variable = coefficients_of_variation.idxmin()

    print("\nEngineering interpretation")
    print(
        f"Among temperature, pressure, and concentration, {most_variable} has the "
        f"largest relative variation (CV {coefficients_of_variation[most_variable]:.2f}%)."
    )
    print(
        f"{least_variable} is the most consistent by relative variation "
        f"(CV {coefficients_of_variation[least_variable]:.2f}%)."
    )
    print(
        "Standard deviation describes the spread of repeated measurements around "
        "their mean; it does not by itself establish accuracy."
    )
    print(
        "The 100.0 C reading changes Exp1's mean and spread substantially, so it "
        "should be checked against the lab record and instrument before any decision."
    )
    print("pH is logarithmic, so its coefficient of variation is not compared here.")


if __name__ == "__main__":
    main()
