# main.py
"""
Main entry point for running the simulation.
Use command-line arguments to choose between the console runner and the GUI.
"""
import sys
import tkinter as tk

def run_console_analysis():
    """Runs the multi-simulation analysis in the console."""
    print("--- Running Console Analysis ---")
    try:
        from console_runner import run_and_analyze
        run_and_analyze()
    except ImportError:
        print("Error: Could not import 'console_runner'. Make sure the file exists.")
    except Exception as e:
        print(f"An error occurred during console analysis: {e}")

def launch_gui_application():
    """Launches the interactive GUI application."""
    print("--- Launching GUI Application ---")
    try:
        from gui import Application
        root = tk.Tk()
        app = Application(master=root)
        app.mainloop()
    except ImportError as e:
        print(f"Error: Could not import GUI components. {e}")
        print("Please ensure 'gui_app.py', 'gui_plotting.py', and 'sv_ttk' are available.")
    except Exception as e:
        print(f"An error occurred while launching the GUI: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'console':
        # To run the console version: python main.py console
        run_console_analysis()
    else:
        # To run the GUI version (default): python main.py
        # You will need to install sv-ttk: pip install sv-ttk
        launch_gui_application()