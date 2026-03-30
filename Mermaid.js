const diagram = `
classDiagram

    class AddPet {
        +String name
        +String breed
        +int age
        +float weight
        +addPet()
    }

    class CreateTask {
        +String taskName
        +String taskDescription
        +String taskTime
        +createTask()
    }

    class SwitchProfile {
        +List petProfiles
        +String currentProfile
        +switchProfile()
        +addProfile()
    }

    class CreateSchedule {
        +List tasks
        +List generatedSchedule
        +createSchedule()
    }

    class CheckTasks {
        +List todaySchedule
        +String lastUpdated
        +updateSchedule()
        +getTodaySchedule()
    }

    AddPet --> SwitchProfile : pet added to profile
    SwitchProfile --> CreateTask : select pet profile
    CreateTask --> CreateSchedule : tasks used to build schedule
    CreateSchedule --> CheckTasks : schedule passed for daily check
`;

export default diagram;
