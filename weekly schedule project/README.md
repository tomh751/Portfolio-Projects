Hello! In this subfolder you can see all the files that i used for the making of this project, **exept for credential files, in order to keep all data secured.**

This project was created in order to help all my previous co-workers, including myslef, entring hours in a fast, simple and intuitive program. Since the departmant
had many students (aproximitily 65), each person would have needed to enter the hours they can give each week into a large table inside of a Google Sheets file.
After speaking with multiple people, a lot of them said that the proccess was tedious and sometimes they wolud enter their hours to the wrong spots, because of how big
was the hours table. In order to sweeten the proccess, I created a program for each analyst to log in with their work email and through that, the hours will be added
to the hole week, next to their name. the code for the whole build up of this is under the file named **JUSTT Analysts Shift Requestor.py.**

The images below show the login menu and the menu where thry could choose to add or edit their shifts until Thursday 13:00pm.

**Login Menu:**

<img width="225" alt="image" src="https://user-images.githubusercontent.com/86208159/186675813-17706c63-32b3-4594-aa5d-dfb7f7656119.png">

**Add/Edit Shift Menu:**

<img width="451" alt="image" src="https://user-images.githubusercontent.com/86208159/186674579-3709c262-feab-43f0-b824-4a502f526812.png">

Then, We wanted to use a could service where multiple people could enter their hours simultaneously. We decided to use Google sheets.
We created a script that will create a new worksheet and style it according to table that was created manually each week. The code for this file is under the
file name **Automated Google Worksheets Creator.py.**


The next step in the project was to create a script that will organize the weekly schedule after the analysts have entered their hours into the worksheet.
According to the rules my team lead at the time gave me, and how they would manually organize the schedule, I created the script to pull the data from the
Google Worksheet of each week, organize it and return it as a new table below the table it took the data from. This was in order to show the changes between what 
the analysts asked for and what they actually got. You can see the code for this script under the file name **Shift Analysts Scheduler.py.**

After finishing to work on the analysts program and creating and organizing the weekly schedule, It was needed to create a program for the team leads as well. Their
program is needed in order to create each week a new worksheet and organizing the weeklky schedule when they will decide. they will have a button for creating the
worksheet and a button for organizing it. The script for this part will be under the file name **Team Lead Program.py.**

The image below will show the program of the team leads.

**Team Leads Admin Pannel:**

<img width="226" alt="image" src="https://user-images.githubusercontent.com/86208159/186682122-90759c1f-6257-438e-911d-fa4ff9401b46.png">


With the combination of all the different scripts, I created a system that could replace the manually entered hours and orgainizng it in a **fast and easy proccess**
to help both side benefit from it - both the analysts with entering their hours properly and the team leads to make the orgainzing and creating new worksheet proccess
much faster.
