# CZ4031-Assignment-2

## Steps to introduce for postgres
 - put csv in the google drive in the csv folder, run the code in utils folder, cleaned csv will be in clean_csv
 - create the tables in postgres sql using sql code in the utils folder
 - import 7 cleaned csvs to respective tables
 - CAN START TO TEST CODE, remember to change postgres credentials in the preprocessing main function part(for testing purpose)

## Steps to run the program
 - Install library from [requirements.txt](requirements.txt) (`pip install -r requirements.txt`)

### Command Line Interface (CLI)
 - Move to this directory
 - Execute `python src/project.py`

### Pycharm IDE
 - Navigate to `src/project.py`
 - Run `src/project.py`

### Sublime Text
 - Open `src/project.py` in Sublime Text
 - Navigate to "Tools" -> "Build"

## Steps to play with the program
 - Enter the PostgreSql server credential on the computer.
   - the default values will be 
     - Host: localhost 
     - Database: postgres
     - Port: 5432
     - Username: postgres
     - Password: 123456
 - Enter query in prompt graphic window **Query** text box (**end query with ;**)
 - Click **Generate** button
 - View annotation in **Annotated Query** text box

### User Interface
![image](https://user-images.githubusercontent.com/49228945/141418919-67901ee8-a7c8-4baa-8458-bff05e67398d.png)
