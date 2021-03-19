# FitnessLogManager
A fitness logger, with a main function of writing to .txt files concerned with tracking fitness progress. Uses the command line as its interface.
 
***

To use, simply download FitnessLogManager.exe along with the src folder in the same directory. The source code, FitnessLogManager.py, is also available for you to check out.

***

This application was made with Reddit's bodyweight Routine in mind! Check out their workout program at:

https://www.reddit.com/r/bodyweightfitness/wiki/kb/recommended_routine

This is where I pieced the sample workout program from, I would highly recommend checking their subreddit out for advice.

If you are looking for a workout program for lifting weights, I would heavily recommend this push-pull-legs program which I used for 2 years with great results:

https://www.reddit.com/r/Fitness/comments/37ylk5/a_linear_progression_based_ppl_program_for/

Hope you enjoy this little project! Please do send me suggestions at https://github.com/mostafashalaby for features you would like to see added, or for any issues you may encounter.

***

If you want to get an idea of what a workout program or log looks like, check out the example_log.txt and example_workout_program.txt files in the src folder.

***
Simple breakdown of each option present in FitnessLogManager:

(1) Read the logger

Reads the logger file, from the directory you have set for it to be stored in.

(2) Log a session

Logs a training session. A sample format can be found in "example_log" in the src folder.

(3) Read the current program

Reads the current workout program you are using for your logs. A sample format can be found in "example_workout_program" in the src folder.

(4) Adjust the current program

Adjusts the current workout program being followed.

(5) Remove entries

Removes the last x enteries in the logger file, where x is a number inputted by the user. A backup.txt file is created to store the old version before the removal, just in case.

(6) Read user specifications

Reads the user specifications, aka name and current directory used to store your logs.

(7) Adjust user specifications

Adjusts user specifications, letting user choose a new name and a new directory to store log file as desired. The log file is then copied to new directory.

***
