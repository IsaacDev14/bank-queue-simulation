from simulation import run_simulation

run_simulation()

def launch_gui():
    window = tk.Tk()
    window.title("Bank Queue Simulation")
    window.geometry("400x250")
    window.config(bg="#f0f0f0")

    title = tk.Lable(window, text="Bank Queue Simulation", font=("Arial", 16, "bold"), bg="#f0f0f0")
    title.pack(pady=20)

    run_button = tk.Button(window, text="Run Simulation", command=run_from_gui, font=("Arial", 12), bg="#4CAF50", fg="white", padx=20, pady=10)
    run_button.pack(pady=10)

    window.mainloop()