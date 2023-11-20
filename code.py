import random
import numpy as np
from sklearn.tree import DecisionTreeRegressor


class BatteryHealthImprovement:
    def __init__(self):
        # Initial battery health score (in percentage)
        self.battery_health = 90
        # Initial battery capacity (in ampere-hours)
        self.battery_capacity = 5.0
        self.battery_life_model = DecisionTreeRegressor()

        self.cycles = 0  # Track the number of cycles
        self.battery_status = "Off"  # Initialize battery status

    def collect_data(self, cycles, health_scores):
        self.cycle_data = np.array(cycles).reshape(-1, 1)
        self.health_data = np.array(health_scores)

    def train_life_prediction_model(self):
        self.battery_life_model.fit(self.cycle_data, self.health_data)

    def predict_battery_health(self, cycles, months_old):
        predicted_health = self.battery_life_model.predict(
            np.array(cycles).reshape(-1, 1))
        # Age effect based on months (you can adjust this based on your data)
        age_effect = months_old / 12.0 * 10  # Assuming 10% health degradation in a year
        predicted_health[0] -= age_effect
        return int(predicted_health[0])

    def check_battery_health(self):
        self.battery_health = max(
            0, min(100, self.battery_health - random.randint(2, 8)))
        self.cycles += 1  # Increase cycle count

        if self.battery_health > 70:
            self.battery_status = "On"
        else:
            self.battery_status = "Off"

        return self.battery_health


class TwoWheelerIgnitionSystem:
    def __init__(self):
        self.battery_health_improvement = BatteryHealthImprovement()
        self.engine_status = False  # Engine status (off by default)

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
        suggestions = []
        battery_health = self.battery_health_improvement.battery_health
        if battery_health > 70:
            suggestions.append(
                "Battery health is good. Keep it well-maintained for a longer lifespan. No need to worry.")
        elif 30 < battery_health <= 70:
            suggestions.append(
                "Battery health is moderate. Follow operational suggestions to improve battery life.")
        else:
            suggestions.append(
                "Battery health is poor. Take immediate action to prevent battery damage. Consider saving money for a new battery")
        return suggestions

    def estimate_battery_replacement(self):
        battery_health = self.battery_health_improvement.battery_health
        cycles = self.battery_health_improvement.cycles
        months_old = cycles / 100  # Assuming 100 cycles per month
        if battery_health < 20:
            replacement_months = int(months_old + (20 - battery_health) * 1.2)
            return f"Based on the current battery health, consider replacing the battery in approximately {replacement_months} months."
        return f"Battery health is within an acceptable range (between 20% and 100%)."

    def battery_status_message(self):
        battery_status = self.battery_health_improvement.battery_status
        return f"Battery is {battery_status} due to the engine{' is still' if self.engine_status else ' has been'} running."


def main():
    ignition_system = TwoWheelerIgnitionSystem()

    # Generate synthetic data for training the model
    cycles = [100, 200, 300, 400, 500]
    health_scores = [90, 85, 75, 70, 65]

    ignition_system.battery_health_improvement.collect_data(
        cycles, health_scores)
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
        print("7. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            print(ignition_system.start_engine())
        elif choice == '2':
            print(ignition_system.stop_engine())
        elif choice == '3':
            suggestions = ignition_system.suggest_operational_changes()
            print("Operational Change Suggestions:")
            for suggestion in suggestions:
                print(suggestion)
        elif choice == '4':
            cycles_input = int(input("Enter the number of cycles: "))
            months_old = int(
                input("Enter how old the battery is (in months): "))
            predicted_health = ignition_system.battery_health_improvement.predict_battery_health(
                cycles_input, months_old)
            print(f"Predicted Battery Health: {predicted_health}%")
        elif choice == '5':
            print(ignition_system.battery_status_message())
        elif choice == '6':
            replacement_message = ignition_system.estimate_battery_replacement()
            print(replacement_message)
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
