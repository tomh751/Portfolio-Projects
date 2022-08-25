import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
import shutil
import threading
import subprocess
import openpyxl

# A function to return the full path of the files.
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# The Function that will run the whole program.
def run_program():
    # Creating the window.
    team_lead_window = tk.Tk()
    team_lead_window.title('JUSTT Team Lead Administor')
    
    # Making the window pop in the middle of the screen.
    team_lead_window_width = 300
    team_lead_window_height = 200

    screen_width = team_lead_window.winfo_screenwidth()
    screen_height = team_lead_window.winfo_screenheight()

    x_cord = (screen_width/2) - (team_lead_window_width/2)
    y_cord = (screen_height/2) - (team_lead_window_height/2)
    team_lead_window.geometry(f'{team_lead_window_width}x{team_lead_window_height}+{int(x_cord)}+{int(y_cord)}')
    
    # An image to use for the background.
    picture = tk.PhotoImage(file=resource_path('login window bg.png'), master=team_lead_window)
    
    # Loading bar function to indicate that the worksheet is in building proccess. 
    def loading_bar_for_wks_update():
        progress_bar['value'] += 0
        progress_bar['value'] += 0.23
        team_lead_window.update_idletasks()

    # Loading bar function to indicate that the weekly schedule is being organaized.
    def loading_bar_for_organizing_schedule_update():
        progress_bar['value'] += 0
        progress_bar['value'] += 0.25
        team_lead_window.update_idletasks()
        
    # This function will run the python script to create new and styled worksheet.
    def run_new_worksheet_code():
        return subprocess.run(['python', resource_path('Automated Google Worksheets Creator.py')], shell=True)
#         return os.system('python script_to_create_automated_sheets_each_week.py')

    # This function will let the code run without freezing the GUI and creating the loading bar
    # once you pressed the "Create Worksheet" button.
    def new_thread_for_wks_code():
        global submit_thread
        global progress_bar
        submit_thread = threading.Thread(target=run_new_worksheet_code)
        submit_thread.daemon = True
        submit_thread.start()
        team_lead_window.after(20, check_when_wks_is_ready)
        
        style = ttk.Style()
        style.configure("TProgressbar", background='#30D5C8', troughcolor='#DBDBDB',
                            bordercolor='#DBDBDB', lightcolor='#30D5C8', darkcolor='#30D5C8')

        # Creating a progress bar to indicate that the hours are loading into the google sheets.
        progress_bar = ttk.Progressbar(team_lead_window, orient = 'horizontal',
                    length =300, mode = 'determinate')
        progress_bar.place(relx=0.08, rely=0.6,  width=250, height=15)

    # This function will check every 20 ms if the worksheet is still being prepared
    # and when it will finish - a pop-up message will say it's done!
    def check_when_wks_is_ready():
        if submit_thread.is_alive():
            team_lead_window.after(20, check_when_wks_is_ready)
            loading_bar_for_wks_update() 
        else:
            progress_bar.destroy()
            tk.messagebox.showinfo('New Worksheet', 'New Worksheet Has Created Succsefully!')

    # This function will run the python script to organaize the weekly schedule.
    def run_weekly_schedule_organizer():
        return subprocess.run(['python', resource_path('Shift Analysts Scheduler.py')], shell=True)

    # This function will let the code run without freezing the GUI and creating the loading bar
    # once you pressed the "Organize Schedule" button.
    def new_thread_for_organaize_schedule_code():
        global submit_thread
        global progress_bar
        submit_thread = threading.Thread(target=run_weekly_schedule_organizer)
        submit_thread.daemon = True
        submit_thread.start()
        team_lead_window.after(20, check_when_schedule_is_ready)
        
        style = ttk.Style()
        style.configure("TProgressbar", background='#30D5C8', troughcolor='#DBDBDB',
                            bordercolor='#DBDBDB', lightcolor='#30D5C8', darkcolor='#30D5C8')

        # Creating a progress bar to indicate that the hours are loading into the google sheets.
        progress_bar = ttk.Progressbar(team_lead_window, orient = 'horizontal',
                    length =300, mode = 'determinate')
        progress_bar.place(relx=0.08, rely=0.6,  width=250, height=15)
        
    # This function will check every 20 ms if the weekly schedule organizer is still working and
    # when it will finish - a pop-up message will say it's done and that the schedule is ready!   
    def check_when_schedule_is_ready():
        if submit_thread.is_alive():
            team_lead_window.after(20, check_when_schedule_is_ready)
            loading_bar_for_organizing_schedule_update() 
        else:
            progress_bar.destroy()
            tk.messagebox.showinfo('Schedule Ready', 'The Weekly Schedule Is Ready!')
    
    # Styling the GUI buttons.
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TButton', anchor='center', font=('calibri', 13), focuscolor='#550a8a')
    style.map('TButton', foreground=[('!disabled', 'white'), ('active', 'white')],
              background=[('!disabled', '#550a8a'), ('active', '#550a8a')],
              bordercolor=[('!disabled', '#550a8a'), ('active', '#550a8a')],
              borderwidth=[('!disabled', 0), ('active', 0)])
    
    # Creating a canvas in order to add the picture for the background and the
    # 'Welcome!' text.
    canvas = tk.Canvas(team_lead_window, width=300, height=200)
    canvas.pack(fill='both', expand=True)
    canvas.create_image(0, 0, image=picture, anchor='nw')

    canvas.create_text(150,100,fill='turquoise',font='calibri 20 bold',
                        text='Welcome!')
    
    # Creating the weekly schedule button to organize the weekly schedule.
    weekly_schedule_button = ttk.Button(team_lead_window, text='Organize\nSchedule', cursor='hand2',
                              command=new_thread_for_organaize_schedule_code, width=7)
    weekly_schedule_button.place(relx=0.15, rely=0.7, relwidth=0.3, relheight=0.25)
    
    # Creating the worksheet button to create new worksheet in the Google spreadsheet.
    create_wks_button = ttk.Button(team_lead_window, text='  Create\nWorksheet', cursor='hand2',
                              command=new_thread_for_wks_code, width=7)
    create_wks_button.place(relx=0.55, rely=0.7, relwidth=0.3, relheight=0.25)

    team_lead_window.iconbitmap(resource_path('JUSTT.ico')) #creating the JUSTT logo as an icon for the GUI.
    team_lead_window.resizable(False,False)# Disabling the availability to adjust the GUI's size.
    team_lead_window.mainloop()
    
if __name__ == '__main__':
    run_program()