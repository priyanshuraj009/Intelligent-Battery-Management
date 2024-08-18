import random
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta


class BatteryHealthImprovement:
    def __init__(self):
        self.battery_health = 90
        self.state_of_charge = 80
        self.battery_capacity = 5.0
        self.battery_life_model = RandomForestRegressor(n_estimators=100)

        self.cycles = 0
        self.battery_status = "Off"
        self.last_charge_time = None

        self.temperature_data = []
        self.kms_data = []
        self.suggestion_box = []

    def collect_data(self, cycles, health_scores, temperatures, soc_values, kms_values):
        if not all(len(arr) == len(cycles) for arr in [health_scores, temperatures, soc_values, kms_values]):
            raise ValueError("Input arrays must have the same length.")

        self.cycle_data = np.array(cycles).reshape(-1, 1)
        self.health_data = np.array(health_scores)
        self.temperature_data = np.array(temperatures)
        self.soc_data = np.array(soc_values)
        self.kms_data = np.array(kms_values)

    def train_life_prediction_model(self):
        self.battery_life_model.fit(
            np.column_stack(
                (self.cycle_data, self.temperature_data,
                 self.soc_data, self.kms_data)
            ),
            self.health_data,
        )

    def predict_battery_health(self, cycles, temperature, soc, kms, months_old):
        predicted_health = self.battery_life_model.predict(
            np.array([[cycles, temperature, soc, kms]])
        )
        age_effect = months_old / 12.0 * 10
        predicted_health[0] -= age_effect
        return int(predicted_health[0])

    def charge_battery(self, ambient_temperature):
        if self.battery_status == "On":
            current_time = datetime.now()
            if self.last_charge_time:
                time_difference = current_time - self.last_charge_time
                charging_increase = (
                    time_difference.total_seconds() / 3600 * 5
                )  # Default charging rate is 5% per hour
                temperature_factor = 1 - (ambient_temperature / 50)
                charging_increase *= temperature_factor
                self.state_of_charge = min(
                    100, self.state_of_charge + charging_increase
                )
            self.last_charge_time = current_time

    def discharge_battery(self, ambient_temperature):
        if self.battery_status == "On":
            # Default discharge rate is 10% per hour
            discharge_amount = (5 / 3600) * 10
            temperature_factor = 1 - (ambient_temperature / 50)
            discharge_amount *= temperature_factor
            self.state_of_charge = max(
                0, self.state_of_charge - discharge_amount)

    def check_battery_health(self, temperature):
        degradation_factor = (
            self.cycle_data[-1] / 500
        ) * (temperature / 30) * (self.soc_data[-1] / 80)
        degradation_factor = max(1, degradation_factor)

        degradation_range = random.uniform(0.95, 1.05)

        self.battery_health = max(
            0,
            min(
                100,
                self.battery_health
                - random.randint(2, 8) * degradation_factor *
                degradation_range,
            ),
        )

        self.cycles += 1

        if self.battery_health > 70:
            self.battery_status = "On"
        else:
            self.battery_status = "Off"

        self.generate_suggestions(temperature)

        return self.battery_health

    def generate_suggestions(self, temperature):
        self.suggestion_box = []

        if self.battery_health > 70:
            self.suggestion_box.append(
                "Battery health is good. Keep it well-maintained for a longer lifespan."
            )
        elif 30 < self.battery_health <= 70:
            self.suggestion_box.append(
                "Battery health is moderate. Follow operational suggestions to improve battery life."
            )
            if temperature > 35:
                self.suggestion_box.append(
                    "Avoid extreme temperatures for better battery health."
                )
            if self.kms_data[-1] > 50:
                self.suggestion_box.append(
                    "Consider reducing average daily kilometers for improved battery life."
                )
        else:
            self.suggestion_box.append(
                "Battery health is poor. Take immediate action to prevent battery damage."
            )
            if temperature > 40:
                self.suggestion_box.append(
                    "Urgent: Extreme temperatures may damage the battery. Take precautions."
                )
            if self.kms_data[-1] > 30:
                self.suggestion_box.append(
                    "Limiting daily kilometers will help preserve battery life."
                )

        return self.suggestion_box


class TwoWheelerIgnitionSystem:
    def __init__(self):
        self.battery_health_improvement = BatteryHealthImprovement()
        self.engine_status = False

    def start_engine(self):
        if self.engine_status:
            return "Engine is already running."
        else:
            self.engine_status = True
            self.battery_health_improvement.battery_status = "On"
            return "Engine started successfully."

    def stop_engine(self):
        if not self.engine_status:
            return "Engine is already off."
        else:
            self.engine_status = False
            self.battery_health_improvement.battery_status = "Off"
            return "Engine stopped successfully."

    def suggest_operational_changes(self):
        suggestions = self.battery_health_improvement.generate_suggestions(
            temperature=self.battery_health_improvement.temperature_data[-1]
        )
        return suggestions

    def improve_battery_life(self):
        while True:
            print("\nImprove Battery Life:")
            print("1. Reduce daily kilometers driven.")
            print("2. Avoid extreme temperatures.")
            print("3. Charge the battery regularly.")
            print("4. Follow suggested operational changes.")
            print("5. Go back")

            choice = input("Enter your choice: ")

            if choice == "1":
                print("Reducing daily kilometers can extend your battery life.")
            elif choice == "2":
                print(
                    "Avoiding extreme temperatures is crucial for preserving battery health.")
            elif choice == "3":
                print("Charging your battery regularly helps maintain optimal health.")
            elif choice == "4":
                operational_changes = self.suggest_operational_changes()
                print("Operational Change Suggestions:")
                for change in operational_changes:
                    print(change)
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please enter a valid option.")

    def estimate_battery_replacement(self):
        battery_health = self.battery_health_improvement.battery_health
        cycles = self.battery_health_improvement.cycles
        months_old = cycles / 100
        if battery_health < 20:
            replacement_months = int(months_old + (20 - battery_health) * 1.2)
            return f"Based on the current battery health, consider replacing the battery in approximately {replacement_months} months."
        return "Battery health is within an acceptable range (between 20% and 100%)."

    def battery_status_message(self):
        battery_status = self.battery_health_improvement.battery_status
        return f"Battery is {battery_status} due to the engine{' is still' if self.engine_status else ' has been'} running."


def main():
    ignition_system = TwoWheelerIgnitionSystem()

    cycles = [100, 200, 300, 400, 500]
    health_scores = [90, 85, 75, 70, 65]
    temperatures = [25, 30, 22, 28, 20]
    soc_values = [80, 75, 85, 78, 80]
    kms_values = [15, 20, 25, 18, 22]

    ignition_system.battery_health_improvement.collect_data(
        cycles, health_scores, temperatures, soc_values, kms_values
    )
    ignition_system.battery_health_improvement.train_life_prediction_model()

    print("2-Wheeler Vehicle Ignition System Model")

    while True:
        print("\nOptions:")
        print("1. Start Engine")
        print("2. Stop Engine")
        print("3. Suggest Operational Changes")
        print("4. Predict Battery Health")
        print("5. Show Battery Status")
        print("6. Estimate Battery Replacement")
        print("7. Improve Battery Life")
        print("8. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print(ignition_system.start_engine())
        elif choice == "2":
            print(ignition_system.stop_engine())
        elif choice == "3":
            suggestions = ignition_system.suggest_operational_changes()
            print("Operational Change Suggestions:")
            for suggestion in suggestions:
                print(suggestion)
        elif choice == "4":
            cycles_input = int(input("Enter the number of cycles: "))
            temperature_input = int(input("Enter the current temperature: "))
            soc_input = int(input("Enter the current state-of-charge: "))
            kms_input = int(
                input("Enter the average kilometers driven per day: "))
            months_old = int(
                input("Enter how old the battery is (in months): "))
            predicted_health = ignition_system.battery_health_improvement.predict_battery_health(
                cycles_input, temperature_input, soc_input, kms_input, months_old
            )
            print(f"Predicted Battery Health: {predicted_health}%")
        elif choice == "5":
            print(ignition_system.battery_status_message())
        elif choice == "6":
            replacement_message = ignition_system.estimate_battery_replacement()
            print(replacement_message)
        elif choice == "7":
            ignition_system.improve_battery_life()
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
