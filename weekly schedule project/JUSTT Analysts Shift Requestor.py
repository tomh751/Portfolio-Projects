import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import calendar
import os
import openpyxl
import gspread
from pygsheets import *
from gspread_dataframe import set_with_dataframe, get_as_dataframe
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials


# A function to return the full path of the files.
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Creating a service account in order to have access to the Google Sheets file.
sa = gspread.service_account(resource_path('cbk_ops_credentials_for_weekly_schedule.json'))
key = '1HUQEUv-1SjHNL-xW7aN3EFGBuhLnt8fPBMkZKIDVihI' # SheetId
sheet = sa.open_by_key(key) # Entering into the sheet file.
wks = sheet.get_worksheet(-1) # First worksheet.

# Using the google sheet file in order to fetch the name, email and tier of the analyst
# in order to use them for later usage when arranging the shifts.
info_sa = gspread.service_account(resource_path('cbk_ops_credentials_for_weekly_schedule.json'))
info_key = '1BeDEhxAYmopiDIKMu9grJFe7DxWzlPsmlfrKr9MVdJs' #analysts info sheetId
info_sheet = info_sa.open_by_key(info_key)
info_wks = info_sheet.get_worksheet(0)
emails_df = get_as_dataframe(info_wks, evaluate_formulas=True, usecols=[0,1,2]).dropna()
emails_df

# Creating a service account in order to have access to the Google Sheets policy file.
policy_sa = gspread.service_account(resource_path('cbk_ops_credentials_for_weekly_schedule.json'))
policy_key = '1LsHGTKCLi4ZV6cpEflUXqLPUNpi8HBxusW7-vLunrl4' # SheetId
policy_sheet = policy_sa.open_by_key(policy_key) # Entering into the sheet file.
policy_wks = policy_sheet.get_worksheet(-1) # First worksheet.
policy_val = policy_wks.acell('A2').value.lower()
# print(policy_val)

# Analysts names.
analysts = [name.title() for name in emails_df['Name']]
time_range = pd.date_range('08:00','20:00',freq='15min')
time_lst = time_range.strftime('%H:%M:%S')
time_lst # List that have time range between 8AM to 8PM.

# Time range to use for entering the hour you start your shift.
start_shift = time_lst.copy().tolist()

# Time range to use for entering the hour you end your shift.
end_shift = time_lst.copy().tolist()

days = list(calendar.day_name)
sunday = days[-1]
rest_of_the_week = days[:-3]

# An organized week list from Sunday-Thursday.
week = [sunday] + rest_of_the_week

# Option where you choose to work.
workplace = ['Home - Full Shift','Office - Full Shift']

# List of the subcolumn name.
headers = ['In', 'Out', 'Hours', 'Workplace']

# Creating the MultiIndex dataframe.
mux = pd.MultiIndex.from_product([week, headers])
full_week = pd.DataFrame(columns=mux)
full_week.insert(0, 'Analyst', emails_df['Name'].str.title())
full_week.insert(21, column='Total Hours',value=0)
full_week.insert(22, column='Notes',value='')
full_week = full_week.fillna('')

# A function to combine all the events in the main menu window.
def creating_main_menu():
    global cbn
    global cbn_value
    
    # Creating the GUI main window.
    roo = Tk()
    roo.title('JUSTT Shift Request')
    
    # Making the window pop in the middle of the screen.
    main_window_width = 600
    main_window_height = 450

    screen_width = roo.winfo_screenwidth()
    screen_height = roo.winfo_screenheight()

    x_cord = (screen_width/2) - (main_window_width/2)
    y_cord = (screen_height/2) - (main_window_height/2)
    roo.geometry(f'{main_window_width}x{main_window_height}+{int(x_cord)}+{int(y_cord)}')
   
    picture = PhotoImage(file=resource_path('JUSTT BG For Main Window.png'), master=roo)
    
    # Creating a canvas for the main window menu to choose your shifts.
    main_menu_canvas = Canvas(roo, width=500, height=450, highlightbackground='#30D5C8', highlightcolor='#30D5C8')
    main_menu_canvas.pack(fill='both', expand=True)
    main_menu_canvas.create_image(0, 0, image=picture, anchor='nw')
    
    # These lines will display the analyst name at the top.
    analyst_name = next(iter(name_and_status_dict.values())).split()[0]
    main_menu_canvas.create_text(280,35,fill='turquoise',font='calibri 20 bold',
                        text=f'Hello {analyst_name}!')

    # Changing the combobox menu style.
    style = ttk.Style(main_menu_canvas)
    style.theme_use('clam')
    roo.option_add('*TCombobox*Listbox.selectBackground', '#30D5C8') # change highlight color
    roo.option_add('*TCombobox*Listbox.selectForeground', 'white') # change text color
    
    # Creating a customize style for the comboboxes and applying it.
    style = ttk.Style()
    combostyle = ttk.Style()
    combostyle.theme_create('combostyle', parent='clam',
                            settings = {'TCombobox': 
                                        {'configure': {'selectbackground': 'white',
                                                        'fieldbackground': 'white',
                                                        'background': '#30D5C8',
                                                        'bordercolor':'#30D5C8',
                                                       'selectforeground': 'black',
                                                      'cursor':'hand2'}}})
    style.theme_use('combostyle')

    # Configurating the buttons styles.
    style.configure('TButton', anchor='center', font=('calibri', 13), focuscolor='#550a8a')
    style.map('TButton', foreground=[('!disabled', 'white'), ('active', 'white')],
              background=[('!disabled', '#550a8a'), ('active', '#550a8a')],
              bordercolor=[('!disabled', '#550a8a'), ('active', '#550a8a')],
              borderwidth=[('!disabled', 0), ('active', 0)])
    

    style.map('TCheckbutton', background=[('!disabled', '#F4F4F4'), ('active', '#F4F4F4')])
    
    
    # First drop-down menu.
    chosen2 = tk.StringVar(value='Shift Starting Hour')
    vyber2 = ttk.Combobox(main_menu_canvas, textvariable=chosen2, state='readonly', justify='center')
    vyber2['values'] = start_shift
    vyber2.place(relx=0.27, rely=0.16, relwidth=0.45, relheight=0.09)
    vyber2.config(font=('calibri', '13'))
    
    # Second drop-down menu.
    chosen3 = tk.StringVar(value='Shift Ending Hour')
    vyber3 = ttk.Combobox(main_menu_canvas, textvariable=chosen3, state='readonly', justify='center')
    vyber3.config(font=('calibri', '13'))
    vyber3['values'] = end_shift
    vyber3.place(relx=0.27, rely=0.27, relwidth=0.45, relheight=0.09)
    vyber3.config(font=('calibri', '13'))

    # Third drop-down menu.
    chosen4 = tk.StringVar(value='Weekday')
    vyber4 = ttk.Combobox(main_menu_canvas, textvariable=chosen4, state='readonly', justify='center')
    vyber4['value'] = week
    vyber4.place(relx=0.27, rely=0.38, relwidth=0.45, relheight=0.09)
    vyber4.config(font=('calibri', '13'))

    # Forth drop-down menu.
    chosen5 = tk.StringVar(value='Workplace Preference')
    vyber5 = ttk.Combobox(main_menu_canvas, textvariable=chosen5, state='readonly', justify='center')
    vyber5['value'] = workplace
    vyber5.place(relx=0.27, rely=0.49, relwidth=0.45, relheight=0.09)
    vyber5.config(font=('calibri', '13'))

    # Creating the text box to write notes.
    text_box_default_val = tk.StringVar(value='Notes...')
    default_val = text_box_default_val.get()
    text_box = Text(main_menu_canvas, width=45, height=6, font=('calibri','13'))
    text_box.insert(INSERT, default_val)
    text_box.config(highlightthickness=0.5, highlightbackground='#30D5C8', highlightcolor='#30D5C8')
    main_menu_canvas.create_window(300, 336, window=text_box)
    
    # Creating a right-click menu for the main window.
    right_click_on_text_box_menu = Menu(roo, tearoff = False) 
    right_click_on_text_box_menu.add_command(label="Cut", accelerator="Ctrl+X",
                  command=lambda: roo.focus_get().event_generate('<<Cut>>')) 
    right_click_on_text_box_menu.add_command(label ="Copy", accelerator="Ctrl+C",
                  command=lambda: roo.focus_get().event_generate('<<Copy>>'))
    right_click_on_text_box_menu.add_command(label ="Paste", accelerator="Ctrl+V",
                  command=lambda: roo.focus_get().event_generate('<<Paste>>')) 
    right_click_on_text_box_menu.add_command(label ="Select All", accelerator="Ctrl+A",
                  command=lambda: roo.focus_get().event_generate('<<SelectAll>>')) 
    right_click_on_text_box_menu['bg'] = 'white'
    
    # This part is for finding thr correct place of Shay's picture :).
    shay = PhotoImage(file=resource_path('shay head.png'), master=roo)
    
    def where_is_shay(event):
        global x
        global y
        x = event.x
        y = event.y

        if 40 < x < 45 and 40 < y < 50:
            surprise = main_menu_canvas.create_image(4, -35, image=shay, anchor='nw')

    # This row will bind the click where Shay's face is!
    roo.bind('<1>', where_is_shay)
    
    # A function to check the day and time in order to let the user enter hours or not at specific times.
    def check_the_time_and_day():
        now = time.strftime('%H:%M:%S')
        time_to_start_or_end_hours_entry = '13:00:00'
        time_to_start_or_end_hours_entry = time.strftime(time_to_start_or_end_hours_entry)

        curr_date = datetime.today().weekday()
        day = calendar.day_name[curr_date]

        entering_days = ['Tuesday', 'Wednesday', 'Thursday']
        
        if cbn.instate(['selected']):
            cbn_value.set(0)
        if cbn_note.instate(['selected']):
            cbn_note_value.set(0)
        else:
            pass

        if day == 'Tuesday' and now < time_to_start_or_end_hours_entry:
            messagebox.showerror('Error', "Error: You Can't Change/Enter Hours At This Time!")
            roo.after_cancel(mainloop())
        elif day == 'Thursday' and now >= time_to_start_or_end_hours_entry:
            messagebox.showerror('Error', "Error: You Can't Change/Enter Hours At This Time!")
            roo.after_cancel(mainloop())
        elif time_to_start_or_end_hours_entry <= now and day in entering_days:
            pass
        elif now <= time_to_start_or_end_hours_entry and day in entering_days:
            pass
        else:
            messagebox.showerror('Error', "Error: You Can't Change/Enter Hours At This Time!")
            roo.after_cancel(mainloop())

    # A function to operate the right-click menu.
    def do_popup_for_textbox(event): 
        try: 
            right_click_on_text_box_menu.tk_popup(event.x_root, event.y_root) 
        finally: 
            right_click_on_text_box_menu.grab_release() 

    # Binding the function to the right-click menu.
    text_box.bind("<Button-3>", do_popup_for_textbox)


    # Creating the notes textbox and the function to retrieve the input.
    def retrieve_input(text_box_val):
        input_val = text_box_val.get('1.0','end-1c')
        return input_val
    
    # Function to calculate the total hours of the shift.
    def total_shift_hours(start, end):
        format = "%H:%M:%S"
        start = datetime.strptime(start, format)
        end = datetime.strptime(end, format)
        
        duration = timedelta(hours=end.hour-start.hour, minutes=end.minute-start.minute)
        total_shift = duration.seconds/3600
        return total_shift
    
    # This function creates a window for the user
    # to choose there the hours he wants to split.
    def split_a_shift():
#         check_the_time_and_day()
        cbn_value.set(1)
        w = Toplevel(roo)
        w.title('JUSTT Shift Request')

        # Making the window pop in the middle of the screen.
        w_width = 300
        w_height = 200

        screen_width = w.winfo_screenwidth()
        screen_height = w.winfo_screenheight()

        x_cord = (screen_width/2) - (w_width/2)
        y_cord = (screen_height/2) - (w_height/2)
        w.geometry(f'{w_width}x{w_height}+{int(x_cord)}+{int(y_cord)}')

        picture = PhotoImage(file=resource_path('login window bg.png'), master=w)
        w.option_add('*TCombobox*Listbox.selectBackground', '#30D5C8') # change highlight color
        w.option_add('*TCombobox*Listbox.selectForeground', 'white') # change text color


        # Creating a canvas to add on it the comboboxes, background and text.
        w_canvas = Canvas(w, width=300, height=200,
                                    highlightbackground='#30D5C8', highlightcolor='#30D5C8')
        w_canvas.pack(fill='both', expand=True)
        w_canvas.create_image(0, 0, image=picture, anchor='nw')

        w_canvas.create_text(150,55,fill='#550a8a',font='calibri 14 bold',
                            text='First Half')

        start_time_to_split1 = tk.StringVar(value='In')
        start_time_to_split_combobox1 = ttk.Combobox(w, textvariable=start_time_to_split1, state='readonly',
                                                     justify='center')
        start_time_to_split_combobox1['values'] = start_shift
        start_time_to_split_combobox1.config(font=('calibri', '13'), width=8)
        start_time_to_split_combobox1.place(x=60, y=70)


        end_time_to_split1 = tk.StringVar(value='Out')
        end_time_to_split_combobox1 = ttk.Combobox(w, textvariable=end_time_to_split1, state='readonly',
                                                   justify='center')
        end_time_to_split_combobox1['values'] = end_shift
        end_time_to_split_combobox1.config(font=('calibri', '13'), width=8)
        end_time_to_split_combobox1.place(x=160, y=70)

        w_canvas.create_text(150,110,fill='#550a8a',font='calibri 14 bold',
                            text='Second Half')

        start_time_to_split2 = tk.StringVar(value='In')
        start_time_to_split_combobox2 = ttk.Combobox(w, textvariable=start_time_to_split2, state='readonly',
                                                     justify='center')
        start_time_to_split_combobox2['values'] = start_shift
        start_time_to_split_combobox2.config(font=('calibri', '13'), width=8)
        start_time_to_split_combobox2.place(x=60, y=130)


        end_time_to_split2 = tk.StringVar(value='Out')
        end_time_to_split_combobox2 = ttk.Combobox(w, textvariable=end_time_to_split2, state='readonly',
                                                   justify='center')
        end_time_to_split_combobox2['values'] = end_shift
        end_time_to_split_combobox2.config(font=('calibri', '13'), width=8)
        end_time_to_split_combobox2.place(x=160, y=130)


        style = ttk.Style()
        style.configure('TButton', anchor='center', font=('calibri', 13), focuscolor='#550a8a', width=15)
        style.map('TButton', foreground=[('!disabled', 'white'), ('active', 'white')],
                  background=[('!disabled', '#550a8a'), ('active', '#550a8a')],
                  bordercolor=[('!disabled', '#550a8a'), ('active', '#550a8a')],
                  borderwidth=[('!disabled', 0), ('active', 0)])


        # This function will calcualte the total hours of the splitted shift.
        def total_shift_hours_when_splitting(start_time, end_time):
            global total_splitted_shift_hours
            format = "%H:%M:%S"
            s = datetime.strptime(start_time, format)
            e = datetime.strptime(end_time, format)
            duration = timedelta(hours=e.hour-s.hour, minutes=e.minute-s.minute)
            total_splitted_shift = duration.seconds/3600
            return total_splitted_shift

        # This function will orginize all the time splits of the shift
        # and will be able to access them later when the user will want
        # to save the shift hours into the google sheet file.
        def get_splits_hours():
            global start_shift_part1
            global end_shift_part2
            global total_splitted_shift_hours

            first_part_hour_start = start_time_to_split1.get()
            first_part_hour_end = end_time_to_split1.get()
            second_part_hour_start = start_time_to_split2.get()
            second_part_hour_end = end_time_to_split2.get()

            start_shift_part1 = f'{start_time_to_split1.get()} - {end_time_to_split1.get()}'
            chosen2.set(start_shift_part1)
            total_hours_for_first_part = total_shift_hours_when_splitting(first_part_hour_start, first_part_hour_end)
            end_shift_part2 = f'{start_time_to_split2.get()} - {end_time_to_split2.get()}'
            chosen3.set(end_shift_part2)
            total_hours_for_second_part = total_shift_hours_when_splitting(second_part_hour_start, second_part_hour_end)
            total_splitted_shift_hours = total_hours_for_first_part + total_hours_for_second_part
  
        # This function will operate the two functions above and will close the window.
        def if_clicked():
            get_splits_hours()
            w.destroy()
           
        # This function will work if the user closed the split shift
        # window with the top right side "X" button and will untick 
        # the split shift button.
        def if_closed_split_win():
            if cbn.instate(['selected']):
                cbn_value.set(0)
                w.destroy()
            else:
                w.destroy()
            
        w.protocol('WM_DELETE_WINDOW', if_closed_split_win)

        day_to_split_btn = ttk.Button(w, text='Split This Shift', cursor='hand2', command=if_clicked)
        day_to_split_btn.place(relx=0.313, rely=0.81, relwidth=0.38, relheight=0.15)    

        w.iconbitmap(resource_path('JUSTT Logo.ico'))
        w.resizable(False, False)
        w.mainloop()
        
    # This function combine all the assets for the clear notes window to work
    # when the user press on the 'Delete A Note' button.
    def clear_notes():
#         check_the_time_and_day()
        clean_notes_win = Toplevel(roo)
        clean_notes_win.title('JUSTT Shift Request')

        # Making the window pop in the middle of the screen.
        clean_notes_win_width = 300
        clean_notes_win_height = 200

        screen_width = clean_notes_win.winfo_screenwidth()
        screen_height = clean_notes_win.winfo_screenheight()

        x_cord = (screen_width/2) - (clean_notes_win_width/2)
        y_cord = (screen_height/2) - (clean_notes_win_height/2)
        clean_notes_win.geometry(f'{clean_notes_win_width}x{clean_notes_win_height}+{int(x_cord)}+{int(y_cord)}')

        picture = PhotoImage(file=resource_path('login window bg.png'), master=clean_notes_win)

        # A function to find the analysts total notes and return
        # them inside a dictionary.
        def get_notes_number():
            global notes_d
            global notes_spot
            
            name_lst = next(iter(name_and_status_dict.values())).split()
            full_name = ' '.join(name_lst) #this gives the full name of the analyst.

            # Will iterate in the dataframe in order to later use the row
            # number near the right analyst name for later usage to enter
            # the input into the right spots.
            for index, col in full_week.iterrows():
                    if col[0] == full_name:
                        row = index
            try:
                notes_spot = f'W{str(row+3)}'
                notes = wks.acell(notes_spot).value 
                notes = notes.split('\n\n')

                notes_d = {}
                notes_count = 0
                for note in notes:
                    notes_count+=1
                    notes_d[f'Note No. {notes_count}'] = note

                total_notes_num_lst = list(notes_d.keys())
                return total_notes_num_lst
            except:
                pass

        # A function to make sure the user can close the notes deletion
        # and still continue working inside the app.
        def if_closed_del_notes_win():
            if cbn_note.instate(['selected']):
                cbn_note_value.set(0)
                clean_notes_win.destroy()
            else:
                clean_notes_win.destroy()

        clean_notes_win.protocol('WM_DELETE_WINDOW', if_closed_del_notes_win)

        # Creating a canvas to add all the combobox, background and text.
        clean_notes_canvas = Canvas(clean_notes_win, width=300, height=200,
                                    highlightbackground='#30D5C8', highlightcolor='#30D5C8')
        clean_notes_canvas.pack(fill='both', expand=True)
        clean_notes_canvas.create_image(0, 0, image=picture, anchor='nw')
        clean_notes_canvas.create_text(150,80,fill='turquoise',font='calibri 13 bold',
                            text='Which Note You\n Want To Delete?')

        note_chose_to_delete = tk.StringVar(value='Notes')
        note_chose_to_delete_list = ttk.Combobox(clean_notes_canvas, textvariable=note_chose_to_delete,
                                                state='readonly', cursor='hand2', justify='center')

        # Creating a dynamic combobox that is depending on the amount of notes.
        note_chose_to_delete_list['value'] = get_notes_number()
        note_chose_to_delete_list.config(font=('calibri', '13'), width=15) 
        note_chose_to_delete_list.place(x=70, y=110, anchor='nw')

        # A function to arrange all the notes in a list and delete the unwanted notes
        # and send everything back to the google sheet file.
        def get_value():
            chosen_note = note_chose_to_delete.get()
            notes_d_vals = list(notes_d.values())
            if len(notes_d_vals) <= 2:
                for note in notes_d_vals:
                    for key in notes_d:
                        if key in chosen_note:
                            del notes_d[key]
                            break
                new_edited_note = ''.join(notes_d.values())
                if new_edited_note.startswith('Another note: '):
                    new_edited_note = new_edited_note.replace('Another note: ', 'Note: ', 1)
                wks.update(notes_spot, new_edited_note)
                cbn_note_value.set(0)
                clean_notes_win.destroy()
            else:
                for note in notes_d_vals:
                    for key in notes_d:
                        if key in chosen_note:
                            del notes_d[key]
                            break
                new_edited_note = '\n\n'.join(notes_d.values())
                if new_edited_note.startswith('Another note: '):
                    new_edited_note = new_edited_note.replace('Another note: ', 'Note: ', 1)
                wks.update(notes_spot, new_edited_note)
                cbn_note_value.set(0)
                clean_notes_win.destroy()

        # A function to throw a warning to ask if the user sure he wants
        # to delete the note.
        def delete_note():
            MsgBox = tk.messagebox.askquestion('Note Delete','Are You Sure You Want To Delete This Note?',
                                                icon = 'warning')

            if MsgBox == 'yes':
                get_value()
                clean_notes_win.destroy()
            else:
                pass

        # A button to delete the note.
        note_to_delete_btn = ttk.Button(clean_notes_canvas, text='Delete This Note?',
                                        cursor='hand2', command=delete_note)
        note_to_delete_btn.place(relx=0.26, rely=0.8, relwidth=0.43, relheight=0.15)

        clean_notes_win.resizable(False, False)
        clean_notes_win.iconbitmap(resource_path('JUSTT Logo.ico'))
        clean_notes_win.mainloop()
        
    # Creating a checkbox to tick if you need to split a shift.
    cbn_value = IntVar()
    cbn = ttk.Checkbutton(main_menu_canvas, variable=cbn_value, takefocus=0, onvalue=1,
                          offvalue=0, command=split_a_shift)
    cbn.place(relx=0.75, rely=0.153)
    
    main_menu_canvas.create_text(505,76,fill='#30D5C8',font='calibri 10 bold',
                    text='Split My Shift')
    
    # Creating a checkbox to tick if you need to delete a note.
    cbn_note_value = IntVar()
    cbn_note = ttk.Checkbutton(main_menu_canvas, variable=cbn_note_value, takefocus=0, onvalue=1,
                          offvalue=0, command=clear_notes)
    cbn_note.place(relx=0.75, rely=0.213)
    
    main_menu_canvas.create_text(510,103,fill='#30D5C8',font='calibri 10 bold',
                    text='Delete A Note?')
    
    # Creating a checkbox to tick if you only need to add a note.
    notes_only_btn_value = IntVar()
    notes_only_btn = ttk.Checkbutton(main_menu_canvas, variable=notes_only_btn_value, takefocus=0, onvalue=1,
                          offvalue=0)
    notes_only_btn.place(relx=0.75, rely=0.273)
    
    main_menu_canvas.create_text(517,130,fill='#30D5C8',font='calibri 10 bold',
                    text='Only Add A Note?')
    

    # Function to organize all the input inside of a list.
    # If there's a splitted shift, the function will adjust
    # accordingly.
    def show_chosen_info():
        global day
        analyst_name_and_tier_dict = name_and_status_dict
        analyst = analyst_name_and_tier_dict['Name']
        if cbn.instate(['selected']):
            start = start_shift_part1
            end = end_shift_part2
            total_hours = total_splitted_shift_hours
            day = chosen4.get()
            place = chosen5.get()
            notes = retrieve_input(text_box)
            info = [analyst, start, end, total_hours, day, place, notes]
            return info
        elif notes_only_btn.instate(['selected']):
            start = ''
            end = ''
            total_hours = ''
            day = ''
            place = ''
            notes = retrieve_input(text_box)
            info = [analyst, start, end, total_hours, day, place, notes]
            return info
        else:
            start = chosen2.get()
            end = chosen3.get()
            total_hours = total_shift_hours(start, end)
            day = chosen4.get()
            place = chosen5.get()
            notes = retrieve_input(text_box)
            info = [analyst, start, end, total_hours, day, place, notes]
            return info
    
    # A function to retrieve the row number of the specific analyst.
    def get_row_num():
        choices = show_chosen_info()
        analyst = choices[0]
        
        for index, col in full_week.iterrows():
            if col[0] == analyst:
                row = index
        return row
    
    # A function to check if there's a note or other notes and will act accordinly to the conditions.
    def check_for_existing_notes():
        cell = retrieve_input(text_box)
        
        row = get_row_num()
        notes_place = f'W{str(row+3)}'
        if cell == '':
            print('change me')
            wks.update(notes_place, wks.acell(notes_place).value, raw=False)
        elif wks.acell(notes_place).value is None and cell == 'Notes...':
            print('no text was here before')
            wks.update(notes_place, '', raw=False)
        elif wks.acell(notes_place).value is None and cell != 'Notes...':
            print('adding a note to the blank cell')
            wks.update(notes_place, 'Note: ' + cell, raw=False)
        elif 'Note: ' in wks.acell(notes_place).value or 'Another note: ' in wks.acell(notes_place).value:
            if wks.acell(notes_place).value[6:] == cell or wks.acell(notes_place).value[13:] == cell:
                print('this is the same note')
                wks.update(notes_place, wks.acell(notes_place).value + '', raw=False)
            elif wks.acell(notes_place).value != None and cell == 'Notes...':
                print('add nothing')
                wks.update(notes_place, wks.acell(notes_place).value + '', raw=False)
            elif wks.acell(notes_place).value.startswith('Another note: ') and cell != 'Notes...':
                wks.update(notes_place, 'Note: ' + wks.acell(notes_place).value[14:] + '\n\n' + 'Another note: ' + cell,
                           raw=False)
            else:
                print('adding another note')
                wks.update(notes_place, wks.acell(notes_place).value + '\n\n' + 'Another note: ' + cell)

     # Loading bar function to indicate that something is happening. 
    def loading_bar():
        progress_bar['value'] += 0
        progress_bar['value'] += 25
        ro.update_idletasks()
#         time.sleep(0.5)
        
    
    # A function to enter the user input into the right cells
    # in the google sheet.
    def enter_data_to_gsheets():
        global row
        global notes_place
        global notes
        global shift_hours
        
        # Checking if the analyst pressed the button to only add a note.
        # Else, the app will check for entering a shift. Also, adding a 
        # progress bar to indicate that something is happening.
        if notes_only_btn.instate(['selected']):
            for i in range(4):
                loading_bar()
                time.sleep(0.5)
            check_for_existing_notes()
            notes_only_btn_value.set(0)
        else:
            choices = show_chosen_info()
            cols = ['Analyst','In', 'Out', 'Hours', 'Weekday', 'Workplace', 'Notes']
            d = dict(zip(cols, choices))
            day = d['Weekday']
            notes = d['Notes']

            row = get_row_num()

            # This Value will be used in the function to check if the 15 hours limit was passed.
            shift_hours = choices[3]

            # Creating a temp dict in order to enter only the 'In', 'Out',
            # 'Hours' and 'Workplace'.
            def del_d_vals():
                new_dict = d
                del new_dict['Analyst']
                del new_dict['Weekday']
                del new_dict['Notes']

                lst = []
                for val in new_dict.values():
                    lst.append(val)
                return lst

            # The formula to sum all the weeks hours and enter the notes and 
            # total hours in the correct cell for each analyst.
            formula = '='+'SUM'+'('+f'D{str(row+3)}''+'+f'H{str(row+3)}'+'+'+f'L{str(row+3)}'+'+'+f'P{str(row+3)}'+'+'+f'T{str(row+3)}'+')'
            total_hours_place = f'V{str(row+3)}'
            notes_place = f'W{str(row+3)}'

            # These conditions will check for each day the user entered
            # and will insert it in the right row and right cells of the
            # analyst name.
            if d['Weekday'] == 'Sunday':
                input_lst = del_d_vals()
                sunday_range = wks.range(f'B{str(row+3)}:E{str(row+3)}')
                for i, val in enumerate(input_lst):
                    loading_bar()
                    sunday_range[i].value = val
                    wks.update_cells(sunday_range, value_input_option='USER_ENTERED')
                    wks.update(total_hours_place, formula, raw=False)
                check_for_existing_notes()
            elif d['Weekday'] == 'Monday':
                input_lst = del_d_vals()
                monday_range = wks.range(f'F{str(row+3)}:I{str(row+3)}')
                for i, val in enumerate(input_lst):
                    loading_bar()
                    monday_range[i].value = val
                    wks.update_cells(monday_range)
                    wks.update(total_hours_place, formula, raw=False)
                check_for_existing_notes()
            elif d['Weekday'] == 'Tuesday':
                input_lst = del_d_vals()
                tuesday_range = wks.range(f'J{str(row+3)}:M{str(row+3)}')
                for i, val in enumerate(input_lst):
                    loading_bar()
                    tuesday_range[i].value = val
                    wks.update_cells(tuesday_range)
                    wks.update(total_hours_place, formula, raw=False)
                check_for_existing_notes()
            elif d['Weekday'] == 'Wednesday':
                input_lst = del_d_vals()
                wednesday_range = wks.range(f'N{str(row+3)}:Q{str(row+3)}')
                for i, val in enumerate(input_lst):
                    loading_bar()
                    wednesday_range[i].value = val
                    wks.update_cells(wednesday_range)
                    wks.update(total_hours_place, formula, raw=False)
                check_for_existing_notes()
            elif d['Weekday'] == 'Thursday':
                input_lst = del_d_vals()
                thursday_range = wks.range(f'R{str(row+3)}:U{str(row+3)}')
                for i, val in enumerate(input_lst):
                    loading_bar()
                    thursday_range[i].value = val
                    wks.update_cells(thursday_range)
                    wks.update(total_hours_place, formula, raw=False)
                check_for_existing_notes()
            else:
                pass
        
    # A function to make sure the analyst won't be able to enter less than 3 hours shift.
    # If the checkbutton was clicked, the function will act accordingly.
    def check_total_shift_hours_amount():
        choices = show_chosen_info()

        if cbn.instate(['selected']) and choices[3] < 3:
            messagebox.showerror('Error', 'Error: Shifts Can Not Be Less Than 3 Hours!')
            chosen2.set('Shift Starting Hour')
            chosen3.set('Shift Ending Hour')
            cbn_value.set(0)
            roo.after_cancel(mainloop())
        elif cbn.instate(['selected']) and choices[3] > 8.25:
            messagebox.showerror('Error', 'Error: Shifts Can Not Be More Than 8.24 Hours!')
            chosen2.set('Shift Starting Hour')
            chosen3.set('Shift Ending Hour')
            cbn_value.set(0)
            roo.after_cancel(mainloop())
        elif choices[3] < 3:
            messagebox.showerror('Error', 'Error: Shifts can not be less than 3 hours!')
            roo.after_cancel(mainloop())
        elif choices[3] > 8.25:
            messagebox.showerror('Error', 'Error: Shifts Can Not Be More Than 8.24 Hours!')
            roo.after_cancel(mainloop())
    
    # A function to use the analyst name and delete the shift cells for each day he chose
    # when he wants to get rid of a specific shift.
    def clear_cells(chosen_day):
        for index, col in full_week.iterrows():
            analyst_name = next(iter(name_and_status_dict.values()))
            if col[0] == analyst_name and chosen_day in full_week.columns:
                row = index

        if chosen_day == 'Sunday':
            sunday_clear_range = wks.range(f'B{str(row+3)}:E{str(row+3)}')
            notes_day_to_delete = chosen_day
            note_changes = wks.acell(f'W{str(row+3)}')
            for cell in sunday_clear_range:
                    cell.value = ''
            wks.update_cells(sunday_clear_range)
        elif chosen_day == 'Monday':
            monday_clear_range = wks.range(f'F{str(row+3)}:I{str(row+3)}')
            for cell in monday_clear_range:
                    cell.value = ''
            wks.update_cells(monday_clear_range)
        elif chosen_day == 'Tuesday':
            tuesday_clear_range = wks.range(f'J{str(row+3)}:M{str(row+3)}')
            for cell in tuesday_clear_range:
                    cell.value = ''
            wks.update_cells(tuesday_clear_range)
        elif chosen_day == 'Wednesday':
            wednesday_clear_range = wks.range(f'N{str(row+3)}:Q{str(row+3)}')
            for cell in wednesday_clear_range:
                    cell.value = ''
            wks.update_cells(wednesday_clear_range)
        elif chosen_day == 'Thursday':
            thursday_clear_range = wks.range(f'R{str(row+3)}:U{str(row+3)}')
            for cell in thursday_clear_range:
                    cell.value = ''
            wks.update_cells(thursday_clear_range)

    # A function to combine all the assests for the clean shift window to work.
    def clear_shifts():
#         check_the_time_and_day()
        clean_shift_win = Toplevel(roo)
        clean_shift_win.title('JUSTT Shift Request')
        
        # Making the window pop in the middle of the screen.
        clean_shift_win_width = 300
        clean_shift_win_height = 200

        screen_width = clean_shift_win.winfo_screenwidth()
        screen_height = clean_shift_win.winfo_screenheight()

        x_cord = (screen_width/2) - (clean_shift_win_width/2)
        y_cord = (screen_height/2) - (clean_shift_win_height/2)
        clean_shift_win.geometry(f'{clean_shift_win_width}x{clean_shift_win_height}+{int(x_cord)}+{int(y_cord)}')
        
        picture = PhotoImage(file=resource_path('login window bg.png'), master=clean_shift_win)
        clean_shift_win.option_add('*TCombobox*Listbox.selectBackground', '#30D5C8') # change highlight color
        clean_shift_win.option_add('*TCombobox*Listbox.selectForeground', 'white') # change text color

        clean_shift_canvas = Canvas(clean_shift_win, width=300, height=200,
                                    highlightbackground='#30D5C8', highlightcolor='#30D5C8')
        clean_shift_canvas.pack(fill='both', expand=True)
        clean_shift_canvas.create_image(0, 0, image=picture, anchor='nw')
        clean_shift_canvas.create_text(150,80,fill='turquoise',font='calibri 13 bold',
                            text='Which Day You Want\n To Delete Your Shift?')

        day_chose_to_delete = tk.StringVar(value='Weekday')
        day_chose_to_delete_list = ttk.Combobox(clean_shift_canvas, textvariable=day_chose_to_delete,
                                                state='readonly', cursor='hand2', justify='center')


        day_chose_to_delete_list['value'] = week
        day_chose_to_delete_list.config(font=('calibri', '13'), width=15) 
        day_chose_to_delete_list.place(x=70, y=110, anchor='nw')

        # A function to make sure that the analyst wants to delete the shift.
        def delete_shift():
            MsgBox = tk.messagebox.askquestion('Shift Cancellation','Are You Sure You Want To Delete This Shift?',
                                                icon = 'warning')
            if MsgBox == 'yes':
                clear_cells(day_chose_to_delete.get())
                clean_shift_win.destroy()
            else:
                pass

        day_to_delete_btn = ttk.Button(clean_shift_canvas, text='Delete This Shift', cursor='hand2', command=delete_shift)
        day_to_delete_btn.place(relx=0.28, rely=0.8, relwidth=0.4, relheight=0.15)


        style = ttk.Style()
        style.configure('TButton', anchor='center', font=('calibri', 13),focuscolor='#550a8a')


        clean_shift_win.resizable(False, False)
        clean_shift_win.iconbitmap(resource_path('JUSTT Logo.ico'))
        clean_shift_win.mainloop()
        
    # A function to make sure that if an analyst wants to take more than 15 hours in a week,
    # he needs to add a note mentioning how many hours he's taking and from whom.
    def passing_the_limit_tier1(cell_num, current_hours, current_note):
        tot_hours = float(wks.acell(f'V{str(cell_num+3)}').value)
        notes = wks.acell(f'W{str(cell_num+3)}').value

        if tot_hours + float(current_hours) > 15:
            if notes == None:
                if bool(re.search('\d+', current_note)) == None or bool(re.search('\d+', current_note)) == False:
                    print('first error')
                    messagebox.showerror('Error', "Error: You Passed The Hours Limit! If You're Taking Hours Please Add A Note!")
                    roo.after_cancel(mainloop())
                elif bool(re.search('\d+', current_note)) == True:
                    sub_total = float(re.search('\d+', current_note).group(0))
                    if tot_hours - sub_total <= 15:
                        print('itssss working')
                        pass
                    else:
                        print('second error')
                        messagebox.showerror('Error', "Error: You Passed The Hours Limit! If You're Taking Hours Please Add A Note!")
                        roo.after_cancel(mainloop())
            elif notes != None:
                print('has text')
                if re.search('\d+', notes) == None:
                    print('no match')
                    if current_note == 'Notes...':
                        messagebox.showerror('Error', "Error: This Shift Will Pass The Hours Limit! If You're Taking Hours Please Add A Note!")
                        roo.after_cancel(mainloop())
                elif notes != None and bool(re.search('\d+', notes)) == True:
                    all_words = re.findall(r'\btaking\b\s\d+\shours?|\btook\b\s\d+\sH?h?ours?',notes)
                    if bool(all_words) == True:
                        find_nums = re.findall('\d+',notes)
                    current_addition_hours = sum(int(x) for x in find_nums)
                    print(current_addition_hours)
                    try:
                        taking_hours = current_addition_hours + float(re.search('\d+',current_note).group(0))
                        if tot_hours - taking_hours <= 15:
                            print('its working')
                            pass
                    except:
                        messagebox.showerror('Error', "Error: You Didn't Mention You're Taking More Hours Then You Should")
                        roo.after_cancel(mainloop())
            elif bool(re.search('\d+', notes)) == True:
                pass
            
    def passing_the_limit_tier2(cell_num, current_hours, current_note):
        tot_hours = float(wks.acell(f'V{str(cell_num+3)}').value)
        notes = wks.acell(f'W{str(cell_num+3)}').value

        if tot_hours + float(current_hours) > 20:
            if notes == None:
                if bool(re.search('\d+', current_note)) == None or bool(re.search('\d+', current_note)) == False:
                    print('first error')
                    messagebox.showerror('Error', "Error: You Passed The Hours Limit! If You're Taking Hours Please Add A Note!")
                    roo.after_cancel(mainloop())
                elif bool(re.search('\d+', current_note)) == True:
                    sub_total = float(re.search('\d+', current_note).group(0))
                    if tot_hours - sub_total <= 20:
                        print('itssss working')
                        pass
                    else:
                        print('second error')
                        messagebox.showerror('Error', "Error: You Passed The Hours Limit! If You're Taking Hours Please Add A Note!")
                        roo.after_cancel(mainloop())
            elif notes != None:
                print('has text')
                if re.search('\d+', notes) == None:
                    print('no match')
                    if current_note == 'Notes...':
                        messagebox.showerror('Error', "Error: This Shift Will Pass The Hours Limit! If You're Taking Hours Please Add A Note!")
                        roo.after_cancel(mainloop())
                elif notes != None and bool(re.search('\d+', notes)) == True:
                    all_words = re.findall(r'\bT?t?aking\b\s\d+\shours?|\bT?t?ook\b\s\d+\sH?h?ours?',notes)
                    if bool(all_words) == True:
                        find_nums = re.findall('\d+',notes)
                    current_addition_hours = sum(int(x) for x in find_nums)
                    print(current_addition_hours)
                    try:
                        taking_hours = current_addition_hours + float(re.search('\d+',current_note).group(0))
                        if tot_hours - taking_hours <= 20:
                            print('its working')
                            pass
                    except:
                        messagebox.showerror('Error', "Error: You Didn't Mention You're Taking More Hours Then You Should")
                        roo.after_cancel(mainloop())
            elif bool(re.search('\d+', notes)) == True:
                pass


    # Function to open the top level window to ask the user if they want another shift.
    def open_mini_window():
        global ro
#         check_the_time_and_day()
        
        # Those 3 variables are being recreated in order to use the data to check if the analyst
        # wrote he's taking from anyone hours and will be entered into the function 'passing_the_limit_tier1' or
        # 'passing_the_limit_tier2'.
        choices = show_chosen_info()
        analyst = choices[0]
        shift_hours = choices[3]
        specific_note = choices[-1]

        for index, name in enumerate(emails_df['Name']):
            if name == analyst:
                row = index
                tier = emails_df['Status'].iloc[row]
        if notes_only_btn.instate(['selected']):
            pass
        else:
            check_total_shift_hours_amount()
            if policy_val == 'min':
                print
            elif policy_val == 'max':
                if tier == 'Tier 1':
                    passing_the_limit_tier1(row, shift_hours, specific_note)
                else:
                    passing_the_limit_tier2(row, shift_hours, specific_note)
            
        # Creating the window.
        ro = Toplevel(roo)
        ro.title('JUSTT Shift Request')
        
        # Making the window pop in the middle of the screen.
        mini_window_width = 400
        mini_window_height = 250

        screen_width = ro.winfo_screenwidth()
        screen_height = ro.winfo_screenheight()

        x_cord = (screen_width/2) - (mini_window_width/2)
        y_cord = (screen_height/2) - (mini_window_height/2)
        ro.geometry(f'{mini_window_width}x{mini_window_height}+{int(x_cord)}+{int(y_cord)}')
        
        top_level_picture = PhotoImage(file=resource_path('JUSTT BG For Top Level Window.png'), master=ro)
        top_level_bg = Label(ro, image=top_level_picture)
        top_level_bg.place(x=0, y=0, relwidth=1, relheight=1)
        ro.iconbitmap(resource_path('JUSTT Logo.ico'))


        def save_yes_button_press(): # Saving the user choices and allowing him to go back to enter another shift.
            global progress_bar
            style = ttk.Style()
            style.configure("TProgressbar", background='#30D5C8', troughcolor='#DBDBDB',
                            bordercolor='#DBDBDB', lightcolor='#30D5C8', darkcolor='#30D5C8')

            # Creating a progress bar to indicate that the hours are loading into the google sheets.
            progress_bar = ttk.Progressbar(ro, orient = HORIZONTAL,
                        length =300, mode = 'determinate')
            progress_bar.place(relx=0.18, rely=0.6,  width=250, height=15)
            retrieve_input(text_box)
            enter_data_to_gsheets()
            if cbn.instate(['selected']):
                cbn_value.set(0)
            else:
                pass
            chosen2.set('Shift Starting Hour')
            chosen3.set('Shift Ending Hour')
            chosen4.set('Weekday')
            chosen5.set('Workplace Preference')
            text_box.delete("1.0", "end-1c")
            text_box.insert(INSERT, default_val)
            ro.destroy()

        def save_no_button_press(): # Saving the user choices and closing the whole program.
            global progress_bar
            style = ttk.Style()
            style.configure("TProgressbar", background='#30D5C8', troughcolor='#DBDBDB',
                            bordercolor='#DBDBDB', lightcolor='#30D5C8', darkcolor='#30D5C8')

            # Creating a progress bar to indicate that the hours are loading into the google sheets.
            progress_bar = ttk.Progressbar(ro, orient = HORIZONTAL,
                        length =300, mode = 'determinate')
            progress_bar.place(relx=0.18, rely=0.6,  width=250, height=15)
            retrieve_input(text_box)
            enter_data_to_gsheets()
            if cbn.instate(['selected']):
                cbn_value.set(0)
            else:
                pass
            roo.destroy()

        yes_button = ttk.Button(ro, text='Yes', cursor='hand2', command=save_yes_button_press)
        yes_button.place(relx=0.05, rely=0.80,  width=150, height=35)

        no_button = ttk.Button(ro, text='No', cursor='hand2', command=save_no_button_press)
        no_button.place(relx=0.55, rely=0.80,  width=150, height=35)

        ro.resizable(False, False)
        ro.mainloop()

    def open_window(): # The function that opens the main window to insert input.
        open_windows_commands = {}
        key = f'{chosen1.get()}{chosen2.get()}{chosen3.get()}{chosen4.get()}{chosen5.get()}{retrieve_input()}'  # Create key from choices.
        open_window_command = open_windows_commands.get(key, show_chosen_info)
        open_window_command()
        open_mini_window()

    save_btn = ttk.Button(roo, text='Save My Request', cursor='hand2',
                     command=open_mini_window) # A clickable button to save the request.
    save_btn.place(x=162, y=410, width=130, height=30)
    
    cancel_btn = ttk.Button(roo, text='Cancel A Shift?', cursor='hand2',
                     command=clear_shifts) # A clickable button to open the shift cancellation window.
    cancel_btn.place(x=302, y=410, width=130, height=30)

    roo.iconbitmap(resource_path('JUSTT Logo.ico'))
    roo.resizable(False, False)
    roo.mainloop()

# Opens a login page to use your justt email in order to later
# use it for doing shifts schedules.
def open_login_window():
    login_window = Tk()
    login_window.title('JUSTT Shift Request')
    
    # Making the window pop in the middle of the screen.
    login_window_width = 300
    login_window_height = 200

    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()

    x_cord = (screen_width/2) - (login_window_width/2)
    y_cord = (screen_height/2) - (login_window_height/2)
    login_window.geometry(f'{login_window_width}x{login_window_height}+{int(x_cord)}+{int(y_cord)}')
    
    picture = PhotoImage(file=resource_path('login window bg.png'), master=login_window)
    
    # Styling the login button.
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TButton', anchor='center', font=('calibri', 13), focuscolor='#550a8a')
    style.map('TButton', foreground=[('!disabled', 'white'), ('active', 'white')],
              background=[('!disabled', '#550a8a'), ('active', '#550a8a')],
              bordercolor=[('!disabled', '#550a8a'), ('active', '#550a8a')],
              borderwidth=[('!disabled', 0), ('active', 0)])

    canvas = Canvas(login_window, width=300, height=200)
    canvas.pack(fill='both', expand=True)
    canvas.create_image(0, 0, image=picture, anchor='nw')

    canvas.create_text(55,110,fill='turquoise',font='calibri 13 bold',
                        text='Email:')

    canvas.create_text(150,70,fill='turquoise',font='calibri 17 bold',
                        text='Welcome!')

    # Where the analyst will write his work email.
    email_entry = Entry(login_window)
    email_entry.config(highlightthickness=2, highlightbackground='#30D5C8', highlightcolor='#30D5C8')
    email_entry.place(x=85, y=100)
    
    # Creating a right-click menu.
    login_right_click_menu = Menu(login_window, tearoff = False) 
    login_right_click_menu.add_command(label="Cut", accelerator="Ctrl+X",
                  command=lambda: login_window.focus_get().event_generate('<<Cut>>')) 
    login_right_click_menu.add_command(label ="Copy", accelerator="Ctrl+C",
                  command=lambda: login_window.focus_get().event_generate('<<Copy>>'))
    login_right_click_menu.add_command(label ="Paste", accelerator="Ctrl+V",
                  command=lambda: login_window.focus_get().event_generate('<<Paste>>')) 
    login_right_click_menu.add_command(label ="Select All", accelerator="Ctrl+A",
                  command=lambda: login_window.focus_get().event_generate('<<SelectAll>>')) 

    login_right_click_menu['bg'] = 'white'

    # A function to operate the right-click menu of the login window.
    def do_popup_for_login(event): 
        try: 
            login_right_click_menu.tk_popup(event.x_root, event.y_root) 
        finally: 
            login_right_click_menu.grab_release() 

    # Binding the function to the right-click menu.
    email_entry.bind("<Button-3>", do_popup_for_login) 

    # The text that the user entered.
    def get_email():
        global analyst_email
        analyst_email = email_entry.get().lower()
        return analyst_email

    # Making sure the email domain is only Justt's email.
    def if_its_work_email():
        analyst_email = get_email()
        if analyst_email.endswith('@justt.ai') and analyst_email not in emails_df['Email'].values:
            messagebox.showerror('Error', 'Error: Invalid Email!')
            login_window.after_cancel(get_name_and_tier())
        elif analyst_email.endswith('@justt.ai') and analyst_email in emails_df['Email'].values:
            return analyst_email
        else:
            messagebox.showerror('Error', 'Error: This is not your work email! Try again!')
            login_window.after_cancel(get_name_and_tier())

    # Creating a dictionary with the name and satus of the analyst:
    # Tier 1 or Tier 2.
    def get_name_and_tier():
        global analyst_info
        analyst_email = get_email()
        analyst_info = {}
        for index, col in emails_df.iterrows():
                if col[-1] == analyst_email:
                    name = emails_df['Name'].loc[emails_df['Email']== analyst_email].values.item()
                    tier = emails_df['Status'].loc[emails_df['Email']== analyst_email].values.item()
                    analyst_info['Name'] = name
        return analyst_info

    # A function to operate the login button.
    def destory_login():
        global name_and_status_dict
        if_its_work_email()
        name_and_status_dict = get_name_and_tier()
        login_window.destroy()
        creating_main_menu()

    # Creating the login button.
    login_button = ttk.Button(login_window, text='Login', cursor='hand2',
                              command=destory_login, width=7)
    login_button.place(relx=0.37, rely=0.8)

    login_window.iconbitmap(resource_path('JUSTT Logo.ico'))
    login_window.resizable(False,False)
    login_window.mainloop()
    
if __name__ == '__main__':
    open_login_window()