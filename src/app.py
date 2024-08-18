from flask import Flask, render_template, request
from battery_simulation import TwoWheelerIgnitionSystem

app = Flask(__name__)
ignition_system = TwoWheelerIgnitionSystem()

# Load the model on startup
cycles = [100, 200, 300, 400, 500]
health_scores = [90, 85, 75, 70, 65]
temperatures = [25, 30, 22, 28, 20]
soc_values = [80, 75, 85, 78, 80]
kms_values = [15, 20, 25, 18, 22]

ignition_system.battery_health_improvement.collect_data(
    cycles, health_scores, temperatures, soc_values, kms_values
)
ignition_system.battery_health_improvement.train_life_prediction_model()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_input', methods=['POST'])
def process_input():
    try:
        cycles = int(request.form['cycles'])
        temperature = int(request.form['temperature'])
        soc = int(request.form['soc'])
        kms = int(request.form['kms'])
        months_old = int(request.form['months_old'])

        # Train the model with new data before making predictions
        ignition_system.battery_health_improvement.train_life_prediction_model()

        predicted_health = ignition_system.battery_health_improvement.predict_battery_health(
            cycles, temperature, soc, kms, months_old
        )

        battery_status = ignition_system.battery_status_message()

        return render_template('result.html', predicted_health=predicted_health, battery_status=battery_status)

    except Exception as e:
        return render_template('error.html', error=str(e))


if __name__ == "__main__":
    app.run(debug=True)
