

import datetime

# --- Global Database (Dictionary) to store project data ---
# In a real system, this would be a database. Here, it's a dictionary in memory.
projects_db = {}

# --- 1. Input Validation Functions ---
def get_valid_float(prompt):
    """Ensures the user inputs a valid positive number."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print(">> Error: Value cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print(">> Error: Invalid input. Please enter a numerical value.")

def get_valid_string(prompt):
    """Ensures the user doesn't leave text fields blank."""
    while True:
        value = input(prompt).strip()
        if value == "":
            print(">> Error: This field cannot be empty.")
            continue
        return value

# --- 2. Core System Functions ---
def setup_project():
    """Sets up a new project and adds activities."""
    print("\n--- Setup New Project ---")
    project_id = get_valid_string("Enter Project ID (e.g., P-01): ").upper()
    project_name = get_valid_string("Enter Project Name: ")

    # Initialize the project structure in the dictionary
    projects_db[project_id] = {
        "name": project_name,
        "date_started": datetime.date.today().strftime("%Y-%m-%d"),
        "activities": {}
    }

    print(f"\nAdding activities to {project_name}. Type 'DONE' when finished.")
    while True:
        act_id = get_valid_string("Enter Activity ID (or 'DONE' to finish): ").upper()
        if act_id == 'DONE':
            break

        act_name = get_valid_string("Enter Activity Name: ")
        planned_qty = get_valid_float("Enter Planned Quantity: ")
        budget = get_valid_float("Enter Allocated Budget (Rs.): ")

        # Store activity data in a nested dictionary
        projects_db[project_id]["activities"][act_id] = {
            "name": act_name,
            "planned_qty": planned_qty,
            "budget": budget,
            "actual_qty": 0.0,
            "actual_cost": 0.0
        }
        print(f"Activity '{act_id}' added successfully!\n")

    print(f">> Project '{project_name}' setup complete.")

def update_progress():
    """Updates daily progress and calculates automated variances."""
    print("\n--- Update Daily Progress ---")
    if not projects_db:
        print(">> No projects found. Please setup a project first.")
        return

    project_id = get_valid_string("Enter Project ID: ").upper()
    if project_id not in projects_db:
        print(">> Error: Project ID not found.")
        return

    act_id = get_valid_string("Enter Activity ID to update: ").upper()
    if act_id not in projects_db[project_id]["activities"]:
        print(">> Error: Activity ID not found in this project.")
        return

    activity = projects_db[project_id]["activities"][act_id]

    print(f"\nUpdating: {activity['name']} (Planned Qty: {activity['planned_qty']})")

    # Get new updates
    qty_done_today = get_valid_float("Enter Quantity Completed Today: ")
    cost_incurred_today = get_valid_float("Enter Cost Incurred Today (Rs.): ")

    # Update cumulative totals
    activity["actual_qty"] += qty_done_today
    activity["actual_cost"] += cost_incurred_today

    print(f">> Progress updated successfully for {act_id}.")

def generate_report():
    """Generates the automated progress report and flags delays/overruns."""
    print("\n--- Generate Progress Report ---")
    if not projects_db:
        print(">> No projects found. Please setup a project first.")
        return

    project_id = get_valid_string("Enter Project ID to generate report: ").upper()
    if project_id not in projects_db:
        print(">> Error: Project ID not found.")
        return

    project = projects_db[project_id]

    print("\n" + "="*50)
    print(f"          PROJECT PROGRESS REPORT")
    print("="*50)
    print(f"Project ID   : {project_id}")
    print(f"Project Name : {project['name']}")
    print(f"Report Date  : {datetime.date.today().strftime('%Y-%m-%d')}")
    print("-" * 50)

    total_budget = 0
    total_cost = 0

    for act_id, details in project["activities"].items():
        planned_qty = details["planned_qty"]
        actual_qty = details["actual_qty"]
        budget = details["budget"]
        actual_cost = details["actual_cost"]

        total_budget += budget
        total_cost += actual_cost

        # 1. Automated Percentage Calculation
        if planned_qty > 0:
            percent_complete = (actual_qty / planned_qty) * 100
        else:
            percent_complete = 0

        # 2. Automated Variance Calculation
        cost_variance = budget - actual_cost

        # 3. Automated Alert Generation
        alerts = []
        if percent_complete < 100 and percent_complete > 0:
            # Simplistic schedule check for demonstration
            alerts.append("[IN PROGRESS]")
        elif percent_complete >= 100:
             alerts.append("[COMPLETED]")

        if cost_variance < 0:
            alerts.append("[BUDGET OVERRUN]")

        print(f"Activity ID : {act_id} ({details['name']})")
        print(f"Completion  : {percent_complete:.2f}% ({actual_qty}/{planned_qty})")
        print(f"Cost Status : Rs. {actual_cost:.2f} / Rs. {budget:.2f} (Variance: Rs. {cost_variance:.2f})")
        print(f"ALERTS      : {' '.join(alerts) if alerts else '[ON TRACK]'}")
        print("-" * 50)

    print(f"TOTAL PROJECT BUDGET : Rs. {total_budget:.2f}")
    print(f"TOTAL ACTUAL COST    : Rs. {total_cost:.2f}")
    print("="*50)

# --- 3. Main Menu (User Interface Loop) ---
def main():
    """Main program loop serving as the user interface."""
    while True:
        print("\n" + "="*40)
        print(" CONSTRUCTION PROGRESS MONITORING SYSTEM")
        print("="*40)
        print("1. Setup New Project")
        print("2. Update Daily Progress")
        print("3. Generate Progress Report")
        print("4. Exit System")
        print("="*40)

        choice = input("Select an option (1-4): ").strip()

        if choice == '1':
            setup_project()
        elif choice == '2':
            update_progress()
        elif choice == '3':
            generate_report()
        elif choice == '4':
            print("Exiting System. Goodbye!")
            break
        else:
            print(">> Error: Invalid selection. Please enter a number between 1 and 4.")

# Entry point of the script
if __name__ == "__main__":
    main()
