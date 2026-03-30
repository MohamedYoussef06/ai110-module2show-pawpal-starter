from pawpal_system import Owner, AddPet, CreateTask, CheckTasks, Scheduler

# --- Setup ---
add_pet = AddPet()
create_task = CreateTask()

# --- Create Owner ---
owner = Owner(owner_name="Jordan")

# --- Add Pets to Owner ---
mochi = add_pet.add_pet(owner, name="Mochi", breed="Shiba Inu", age=3, weight=22.5)
luna  = add_pet.add_pet(owner, name="Luna",  breed="Tabby Cat",  age=5, weight=9.0)

# --- Add Tasks to Mochi ---
create_task.create_task(mochi, "Morning Walk",   "Walk around the block",      "7:00 AM",  "high",   30)
create_task.create_task(mochi, "Feed Breakfast", "One cup of dry food",        "8:00 AM",  "high",   10)
create_task.create_task(mochi, "Playtime",       "Fetch in the backyard",      "11:00 AM", "medium", 20)
create_task.create_task(mochi, "Grooming",       "Brush coat and clean ears",  "3:00 PM",  "low",    15)

# --- Add Tasks to Luna ---
create_task.create_task(luna, "Feed Breakfast", "Half can of wet food",        "8:30 AM",  "high",   10)
create_task.create_task(luna, "Litter Box",     "Clean and refill litter box", "9:00 AM",  "medium", 10)
create_task.create_task(luna, "Play Session",   "Wand toy for enrichment",     "1:00 PM",  "low",    15)


# --- Scheduler ---
scheduler = Scheduler(owner)
checker   = CheckTasks(scheduler)

# --- Mochi's Schedule ---
scheduler.set_active_pet("Mochi")
scheduler.organize_schedule()
checker.update_schedule()

print(f"\nOwner: {owner.owner_name}")
print(f"Pets: {[p.name for p in owner.pets]}")
print(f"Total tasks across all pets: {len(owner.get_all_tasks())}")
print()
print(scheduler.get_schedule_summary())
print()
print("Today's schedule via CheckTasks:")
for task in checker.get_today_schedule():
    print(f"  [{task.priority.upper()}] {task.task_name} — {task.task_time} ({task.duration_minutes} min)")

# --- Switch to Luna ---
scheduler.set_active_pet("Luna")
scheduler.organize_schedule()
checker.update_schedule()

print()
print()
print("Today's schedule via CheckTasks:")
for task in checker.get_today_schedule():
    print(f"  [{task.priority.upper()}] {task.task_name} — {task.task_time} ({task.duration_minutes} min)")
