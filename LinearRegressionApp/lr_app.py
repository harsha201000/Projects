import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression

class LinearRegressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Linear Regression ML Model GUI")
        self.root.geometry("600x500")

        self.model = None
        self.X_train, self.y_train = self.generate_dummy_data()

        # --- GUI Elements ---
        self.label = tk.Label(root, text="Enter a value for X to predict Y:")
        self.label.pack(pady=10)

        self.entry_x = tk.Entry(root)
        self.entry_x.pack(pady=5)

        self.predict_button = tk.Button(root, text="Predict Y", command=self.predict_y)
        self.predict_button.pack(pady=10)

        self.result_label = tk.Label(root, text="Prediction: N/A", font=("Helvetica", 12))
        self.result_label.pack(pady=10)

        # Matplotlib plot area
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack(pady=20)

        # Train the model and display initial plot
        self.train_model()
        self.plot_model()

    def generate_dummy_data(self):
        """Generates simple linear dummy data for the model."""
        np.random.seed(0)
        X = 2 * np.random.rand(100, 1)
        y = 4 + 3 * X + np.random.randn(100, 1)
        return X, y

    def train_model(self):
        """Trains the Linear Regression model on the dummy data."""
        self.model = LinearRegression()
        self.model.fit(self.X_train, self.y_train)

    def predict_y(self):
        """Gets user input, predicts Y value, and updates the result label."""
        try:
            x_value = float(self.entry_x.get())
            # Model expects a 2D array: [[value]]
            prediction = self.model.predict([[x_value]])
            self.result_label.config(text=f"Prediction: {prediction[0][0]:.2f}")
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number for X.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def plot_model(self):
        """Plots the data points and the regression line."""
        self.ax.clear()
        self.ax.scatter(self.X_train, self.y_train, color='blue', label='Training Data')
        # Plot the regression line over the range of X data
        X_plot = np.linspace(0, 2, 100).reshape(-1, 1)
        y_plot = self.model.predict(X_plot)
        self.ax.plot(X_plot, y_plot, color='red', linewidth=2, label='Regression Line')
        self.ax.set_title('Linear Regression Fit')
        self.ax.set_xlabel('X Value')
        self.ax.set_ylabel('Y Value')
        self.ax.legend()
        self.canvas.draw()

# --- Run the application ---
if __name__ == "__main__":
    root = tk.Tk()
    app = LinearRegressionApp(root)
    root.mainloop()