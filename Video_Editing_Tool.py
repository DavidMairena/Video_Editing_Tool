# ----------------------------------------------------------------------------------------------------------------------
# Name:        Video Editing Tool
# Purpose:     Proyecto Eléctrico - I Semestre 2023
# Python:      3.9
# Author:      David Mairena Castro
# Email:       demc94@gmail.com
# Created:     20/06/2023
# Modified:    -
# Version:     1.0
# ----------------------------------------------------------------------------------------------------------------------

from datetime import datetime, timedelta
import os
import argparse
import moviepy
from moviepy.editor import VideoFileClip
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename

######################################################################################################################################
###################################################### Console App ###################################################################
######################################################################################################################################

def video_postprocessing_console(input, outputpath, name, trimmingtime, tstart, tend, outformat, video_count):
    clip = VideoFileClip(input)
    clipduration = clip.duration

    #Video trimming
    time = add_seconds(trimmingtime, 0, tstart, tend, clipduration)
    processed_clip = clip.subclip(t_start=time[0], t_end=time[1])
    if(name == 'NA'): name = 'Postprocessed Video #{}'.format(video_count)

    #Output
    output_path = outputpath + "/" + name + "." + outformat
    print('\nVideo #{} editing started\n'.format(video_count))
    processed_clip.write_videofile(output_path,codec="libx264")
    print('\nVideo #{} edited successfully\n'.format(video_count))
    clip.close()
    processed_clip.close()

def video_frame_postprocessing_console(input, outputpath, name, frame, tstart, tend, outformat, video_count):
    clip = VideoFileClip(input)
    clipduration = clip.duration

    #Frame Time Calculations
    rate = clip.fps
    frames = int(clip.fps * clipduration)
    time_per_frame = 1/rate
    t_frame = time_per_frame * int(frame)
    print('Video #{}\nFPS: {}\nTotal frames: {}\nTime per frame: {}\nSelected Time (s): {}'.format(video_count,rate,frames,time_per_frame,t_frame))

    #Video trimming at frame time 
    clip = VideoFileClip(input)
    time = add_seconds(0, t_frame, tstart, tend, clipduration)
    processed_clip = clip.subclip(t_start=time[0], t_end=time[1])
    if(name == 'NA'): name = 'Postprocessed Video #{}'.format(video_count)

    #Output
    output_path = outputpath + "/" + name + "." + outformat
    print('\nVideo #{} editing started\n'.format(video_count))
    processed_clip.write_videofile(output_path,codec="libx264")
    print('\nVideo #{} edited successfully\n'.format(video_count))
    clip.close()
    processed_clip.close()

def add_seconds(trimmingtime, frame, ts, te, clipduration):
    #Clip duration time calculation
    hh_clipduration = int(clipduration // 3600)
    mm_clipduration = int((clipduration % 3600) // 60)
    ss_clipduration = clipduration % 60
    clipduration_str = f"{hh_clipduration:02d}:{mm_clipduration:02d}:{ss_clipduration:02f}"
    
    t_f = datetime.strptime(clipduration_str, "%H:%M:%S.%f")
    t_0 = datetime.strptime('00:00:00', "%H:%M:%S")

    #Video trimming by Frame
    if trimmingtime == 0:
        hh = int(frame // 3600)
        mm = int((frame % 3600) // 60)
        ss = frame % 60
        frametime = f"{hh:02d}:{mm:02d}:{ss:02f}"
        frametime = datetime.strptime(frametime, "%H:%M:%S.%f")

        start = frametime - timedelta(seconds=float(ts))
        if start < t_0 : 
            start = t_0
            if input != "NA": print("\nSelected start time out of clip boundaries (00:00:00). \nStart time set to 00:00:00\n")
            else: tk.messagebox.showinfo("Video Editing Tool", "Selected start time out of clip boundaries (00:00:00). \nStart time set to 00:00:00")
        elif start > t_f : 
            if input != "NA": print("\nSelected time out of clip duration ({}). Please insert a valid value\n".format(clipduration_str))
            else: tk.messagebox.showinfo("Video Editing Tool", "Selected time out of clip duration ({}). Please insert a valid value".format(clipduration_str))

        end = frametime + timedelta(seconds=float(te))
        if end > t_f : 
            end = t_f
            if input != "NA": print("\nSelected end time out of clip duration ({}). \nEnd time set to {}\n".format(clipduration_str,clipduration_str))
            else: tk.messagebox.showinfo("Video Editing Tool", "Selected end time out of clip duration ({}). \nEnd time set to {}".format(clipduration_str,clipduration_str))           
        
        new_start = start.strftime("%H:%M:%S.%f")[:-3]
        new_end = end.strftime("%H:%M:%S.%f")[:-3]
    #Video trimming by time
    else:
        time = datetime.strptime(trimmingtime, "%H:%M:%S")

        start = time - timedelta(seconds=float(ts))
        if start < t_0 : 
            start = t_0
            if input != "NA": print("\nSelected start time out of clip boundaries (00:00:00). \nStart time set to 00:00:00\n")
            else: tk.messagebox.showinfo("Video Editing Tool", "Selected start time out of clip boundaries (00:00:00). \nStart time set to 00:00:00")
        elif start > t_f : 
            if input != "NA": print("\nSelected time out of clip duration ({}). Please insert a valid value\n".format(clipduration_str))
            else: tk.messagebox.showinfo("Video Editing Tool", "Selected time out of clip duration ({}). Please insert a valid value".format(clipduration_str))
        
        end = time + timedelta(seconds=float(te))
        if end > t_f : 
            end = t_f
            if input != "NA": print("\nSelected end time out of clip duration ({}). \nEnd time set to {}\n".format(clipduration_str,clipduration_str))
            else: tk.messagebox.showinfo("Video Editing Tool", "Selected end time out of clip duration ({}). \nEnd time set to {}".format(clipduration_str,clipduration_str))           
        
        new_start = start.strftime("%H:%M:%S")
        new_end = end.strftime("%H:%M:%S")
        
    return new_start, new_end

def main(input, outputpath, name, frame, trimmingtime, tstart, tend, outformat):
    #Main from console app
    video_count = 0
    if frame == 'NA' and trimmingtime != "NA":
        for selectedtime in trimmingtime:
            video_count += 1
            video_postprocessing_console(input, outputpath, name, selectedtime, tstart, tend, outformat, video_count)
    elif frame != 'NA' and trimmingtime == "NA":
        for selectedframe in frame:
            video_count += 1
            video_frame_postprocessing_console(input, outputpath, name, selectedframe, tstart, tend, outformat, video_count)
    else:
        print("Insert only one parameter between trimming time or frame number.")


#Main definition
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input', help="Input file path", default="NA")
    parser.add_argument('-o', action='store', dest='outputpath', help="Output path")
    parser.add_argument('-n', action='store', dest='name', help="video output name", default="NA")
    parser.add_argument('-f', nargs='+', dest='frame', help="Trimming Frame", default="NA")
    parser.add_argument('-t', nargs='+', dest='trimmingtime', help="Trimming time", default="NA")
    parser.add_argument('-tb', action='store', dest='tstart', help="Seconds Before", default="30")
    parser.add_argument('-ta', action='store', dest='tend', help="Seconds After", default="30")
    parser.add_argument('-vf', action='store', dest='outformat', help="Output Video Format", default="mp4")
    parser_obj   = parser.parse_args()
    input        = parser_obj.input
    outputpath   = parser_obj.outputpath
    name         = parser_obj.name
    frame        = parser_obj.frame
    trimmingtime = parser_obj.trimmingtime
    tstart       = parser_obj.tstart
    tend         = parser_obj.tend
    outformat    = parser_obj.outformat

    if input != "NA":
        main(input, outputpath, name, frame, trimmingtime, tstart, tend, outformat)


######################################################################################################################################
######################################################## GUI App #####################################################################
######################################################################################################################################

if input == "NA":
    #Functional Functions Definition 

    def video_time_postprocessing_txt(input_path, output_directory):
        with open(input_path, 'r', encoding='utf-8') as input_txt_file:
            videofile = input_txt_file.readlines()
            video_count = 0
        for line in videofile:
            video_count += 1
            if line.strip() == "":
                continue
            else:
                #Parameters
                params = line.split(',')
                video_path = params[0].strip()
                if(video_path == ''): 
                    tk.messagebox.showinfo("Video Editing", "Video #{} path missing.\nCan't postprocess it".format(video_count))
                    continue
                video_name = params[1].strip()
                if(video_name == ''): video_name = 'Postprocessed Video #{}'.format(video_count)
                trimmingtime = params[2].strip()
                if(trimmingtime == ''): 
                    tk.messagebox.showinfo("Video Editing", "Video #{} trimming time missing.\nCan't postprocess it".format(video_count))
                    continue
                t_start = params[3].strip()
                if(t_start == ''): t_start = '30'
                t_end = params[4].strip()
                if(t_end == ''): t_end = '30'
                video_format = params[5].strip()
                if(video_format == ''): video_format = 'mp4'
                
                #Video Trimming
                clip = VideoFileClip(video_path)
                clipduration = clip.duration
                time = add_seconds(trimmingtime, 0, t_start, t_end, clipduration)
                
                processed_clip = clip.subclip(t_start=time[0], t_end=time[1])
                #Output
                output_path = output_directory + "/" + video_name + "." + video_format
                processed_clip.write_videofile(output_path,codec="libx264")
                clip.close()
                processed_clip.close()
            
            tk.messagebox.showinfo("Video Editing", "Video #{} trimmed.".format(video_count))

    def video_frame_postprocessing_txt(input_path, output_directory):
        with open(input_path, 'r',  encoding='utf-8') as input_txt_file:
            videofile = input_txt_file.readlines()
            video_count = 0
        for line in videofile:
            video_count += 1
            if line.strip() == "":
                continue
            else:
                #Parameters
                params = line.split(',')
                
                video_path = params[0].strip()
                if(video_path == ''): 
                    tk.messagebox.showinfo("Video Editing", "Video #{} path missing.\nCan't postprocess it".format(video_count))
                    continue
                video_name = params[1].strip()
                if(video_name == ''): video_name = 'Postprocessed Video #{}'.format(video_count)
                frame = params[2].strip()
                if(frame == ''): 
                    tk.messagebox.showinfo("Video Editing", "Video #{} trimming frame missing.\nCan't postprocess it".format(video_count))
                    continue
                t_start = params[3].strip()
                if(t_start == ''): t_start = '30'
                t_end = params[4].strip()
                if(t_end == ''): t_end = '30'
                video_format = params[5].strip()
                if(video_format == ''): video_format = 'mp4'


                clip = VideoFileClip(video_path)
                clipduration = clip.duration

                #Frame Time Calculations
                rate = clip.fps
                frames = int(clip.fps * clipduration)
                time_per_frame = 1/rate
                trimmingtime = time_per_frame * int(frame)
                tk.messagebox.showinfo("Video Editing", "Parameters Video #{}:\n FPS:{}\n Total Frames: {}\n Time per frame: {}\n Selected Frame Time (s): {}".format(video_count, rate,frames, time_per_frame, trimmingtime))

                #Video trimming at frame time 
                time = add_seconds(0, trimmingtime, t_start, t_end, clipduration)

                processed_clip = clip.subclip(t_start=time[0], t_end=time[1])
                #Output
                output_path = output_directory + "/" + video_name + "." + video_format
                processed_clip.write_videofile(output_path,codec="libx264")
                clip.close()
                processed_clip.close()
            
            tk.messagebox.showinfo("Video Editing", "Video #{} trimmed.".format(video_count))

    def single_video_time_postprocessing(input_path, output_path):
        clip = VideoFileClip(input_path)
        clipduration = clip.duration

        trimmingtime = frame_time_value.get()
        start = start_time_value.get()
        end = end_time_value.get()

        time = add_seconds(trimmingtime, 0, start, end,clipduration)

        #Output
        processed_clip = clip.subclip(t_start=time[0], t_end=time[1])
        processed_clip.write_videofile(output_path,codec="libx264")
        clip.close()
        processed_clip.close()

    def single_video_frame_postprocessing(input_path, output_path):
        clip = VideoFileClip(input_path)
        clipduration = clip.duration

        frame = int(frame_time_value.get())
        rate = clip.fps
        frames = int(clip.fps * clipduration)
        time_per_frame = 1/rate
        trimmingtime = time_per_frame * frame
        tk.messagebox.showinfo("Video Editing Tool", "Parameters:\n FPS:{}\n Total Frames: {}\n Time per frame: {}\n Selected Frame Time (s): {}".format(rate, frames, time_per_frame, trimmingtime))

        start = start_time_value.get()
        end = end_time_value.get()
        time = add_seconds(0, trimmingtime, start, end, clipduration)

        #Output
        processed_clip = clip.subclip(t_start=time[0], t_end=time[1])
        processed_clip.write_videofile(output_path,codec="libx264")
        clip.close()
        processed_clip.close()         

    def add_txtfile():
        #Inputs
        input_path = text_path.get()
        trimmingtime = frame_time_value.get()
        start = start_time_value.get()
        end = end_time_value.get()
        video_format = single_source_combo.get()
        
        line = input_path + ' , ' + ' , ' + str(trimmingtime) + ' , ' + str(start) + ' , ' + str(end) + ' , ' + video_format
        txt_data.append(line)
        tk.messagebox.showinfo("Add to Text File", "Parameters added successfully.")

    #Operative Funtions Definition
    def select_file():
        textpath.set(askopenfilename(filetypes=(('Text files', '*.txt'), ("All files", "*.*"))))

    def select_single_file():
        textpath.set(askopenfilename(filetypes=(('Video files', ['*.mp4','*.wmv', '*.mov', '*.avi', '*.flv', '*.mkv']), ("All files", "*.*"))))

    def select_output_directory():
        textoutpath.set(askdirectory())

    def export_single_video():
        input_path = text_path.get()
        output_directory = text_out_path.get()
        output_format = single_source_combo.get()

        if not input_path or not output_directory:
            tk.messagebox.showinfo("Missing Value", "Select Path.")
            
        value = frame_time_value.get()
        if (value != '0' or value != '00:00:00' or value != ''):
            output_path = output_directory + "/postprocessed_video" + "." + output_format

            if (time_chk.get() == '0' and frame_chk.get() == '1'):
                single_video_frame_postprocessing(input_path, output_path)
            elif (time_chk.get() == '1' and frame_chk.get() == '0'):
                single_video_time_postprocessing(input_path, output_path)
            else:
                tk.messagebox.showinfo("Missing Value", "Select time picker format (by time or byframe).")
                return
        tk.messagebox.showinfo("Export Complete", "Post-processed video exported successfully.")
        frame_time_value.set('00:00:00')

    def export_multiple_videos():
        input_path = text_path.get()
        output_directory = text_out_path.get()

        if not input_path or not output_directory:
            tk.messagebox.showinfo("Missing Value", "Select Path.")
        if (source_combo.get() == "Time"):
            video_time_postprocessing_txt(input_path, output_directory)
        else:
            video_frame_postprocessing_txt(input_path, output_directory)

        tk.messagebox.showinfo("Export Complete", "Post-processed videos exported successfully.")
        textpath.set('')
        textoutpath.set('')

    def export_txtfile():
        output_path = text_out_path.get()
        text_path = output_path + '/video_list.txt' 
        #Writing
        with open(text_path, 'x', encoding='utf-8') as txtfile:
            txtfile.writelines("%s\n" % l for l in txt_data)
            txtfile.close()
        tk.messagebox.showinfo("Add to Text File", "Text file exported successfully.")

    #############################################################################################################################################
    ######################################################## GUI definition #####################################################################
    #############################################################################################################################################
    
    ####################################################### Root definition #####################################################################

    root = Tk()
    root.style = ttk.Style(root)
    root.style.configure('TLabel', font=('Helvetica', 11))
    root.style.configure('TButton', font=('Helvetica', 11))
    root.title('Video Editing Tool')

    mainframe = ttk.Notebook(root, padding='6 6 6 6')
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)



    singleframe = ttk.Frame(mainframe)
    mainframe.add(singleframe, text='Single Video Editing')
    
    multipleframe = ttk.Frame(mainframe)
    mainframe.add(multipleframe, text='Multiple Video Editing')

    #Root Variables
    OS_Username =  StringVar()
    OS_Username.set(os.environ.get('USERNAME'))

    #Single Video Variables
    frame_time_value = StringVar()
    frame_time_value.set('00:00:00')
    time_chk= StringVar()
    time_chk.set('0')
    frame_chk= StringVar()
    frame_chk.set('0')
    videoformat = StringVar()
    videoformat.set('mp4')
    start_time_value = IntVar()
    start_time_value.set(30)
    end_time_value = IntVar()
    end_time_value.set(30)
    txt_data = []

    #Multiple Videos Variables
    textpath = StringVar()
    textoutpath = StringVar()
    measuretype = StringVar()
    measuretype.set('Time')

    ################################################### SINGLE VIDEO TAB ##########################################################


    ttk.Label(singleframe, text='User:').grid(column=1, row=1, sticky=E)
    ttk.Label(singleframe, textvariable=OS_Username, font='Helvetica 12 bold', foreground="green").grid(column=2, row=1, sticky=W)

    ttk.Label(singleframe, text='Output Format:').grid(column=1, row=2, sticky=E)
    single_source_combo = ttk.Combobox(singleframe, textvariable=videoformat, width=15)
    single_source_combo['values'] = ("mp4", "wmv", "mov", "avi", "flv", "mkv")
    single_source_combo.grid(column=2, row=2, sticky=W)

    sep = ttk.Separator(singleframe, orient="vertical")
    sep.grid(column=3, row=1, sticky='ns', rowspan=3)

    ttk.Label(singleframe, text='Timestamp', font='Helvetica 14 bold').grid(column=4, row=0, sticky=W, columnspan=2)

    time_check = ttk.Checkbutton(singleframe, text='by Time (HH:MM:SS)', variable=time_chk, onvalue='1', offvalue='0', state='active')
    time_check.grid(column=4, row=1, sticky=W)
    frame_check = ttk.Checkbutton(singleframe, text='by Frame', variable=frame_chk, onvalue='1', offvalue='0', state='active')
    frame_check.grid(column=4, row=2, sticky=W)
    ttk.Label(singleframe, text='Value:', font='Helvetica 10').grid(column=5, row=1, sticky=W)
    time_frame_value = ttk.Entry(singleframe, width=12, justify='center', textvariable=frame_time_value, state='active')
    time_frame_value.grid(column=5, row=2, sticky=(W, W), columnspan=6)

    sep = ttk.Separator(singleframe, orient="vertical")
    sep.grid(column=6, row=1, sticky='ns', rowspan=3)

    ttk.Label(singleframe, text='Trimming Time', font='Helvetica 14 bold').grid(column=7, row=0, sticky=W, columnspan=2)

    ttk.Label(singleframe, text='Seconds\nBefore:', font='Helvetica 10').grid(column=7, row=1, sticky=W)
    start_time = ttk.Entry(singleframe, width=5, justify='center', textvariable=start_time_value, state='active')
    start_time.grid(column=7, row=2, sticky=(W, W), columnspan=6)
    ttk.Label(singleframe, text='Seconds\nAfter:', font='Helvetica 10').grid(column=8, row=1, sticky=W)
    end_time = ttk.Entry(singleframe, width=5, justify='center', textvariable=end_time_value, state='active')
    end_time.grid(column=8, row=2, sticky=(W, W), columnspan=6)

    sep = ttk.Separator(singleframe, orient="horizontal")
    sep.grid(column=1, row=4, sticky='we', columnspan=8)

    ttk.Label(singleframe, text='Video File:').grid(column=1, row=5, sticky=E)
    text_path = ttk.Entry(singleframe, width=90, textvariable=textpath, state='active')
    text_path.grid(column=2, row=5, sticky=(W, W), columnspan=6)
    text_path_button = ttk.Button(singleframe, text='...', width=3, command=select_single_file, state='active')
    text_path_button.grid(column=8, row=5, sticky=W)

    ttk.Label(singleframe, text='Output Path:').grid(column=1, row=6, sticky=E)
    text_out_path = ttk.Entry(singleframe, width=90, textvariable=textoutpath, state='active')
    text_out_path.grid(column=2, row=6, sticky=(W, W), columnspan=6)
    text_out_path_button = ttk.Button(singleframe, text='...', width=3, command=select_output_directory, state='active')
    text_out_path_button.grid(column=8, row=6, sticky=W)

    sep = ttk.Separator(singleframe, orient="horizontal")
    sep.grid(column=1, row=13, sticky='we', columnspan=8)

    ttk.Label(singleframe, text='Text File Creator', font='Helvetica 12 bold').grid(column=1, row=18, sticky=E)
    add_text_button = ttk.Button(singleframe, text='Add Parameters', width=14, command=add_txtfile, state='active')
    add_text_button.grid(column=1, row=19, sticky=E)
    export_textfile_button = ttk.Button(singleframe, text='Export txt', width=8, command=export_txtfile, state='active')
    export_textfile_button.grid(column=2, row=19, sticky=W, columnspan=2)
    sep = ttk.Separator(singleframe, orient="vertical")
    sep.grid(column=3, row=18, sticky='ns', rowspan=3)

    start_co_button = ttk.Button(singleframe, text='Export\nVideo', width=8, command=export_single_video, state='active')
    start_co_button.grid(column=8, row=19, sticky=W)


    ########################################################## MULTIVIDEO TAB ##############################################################


    ttk.Label(multipleframe, text='User:').grid(column=1, row=1, sticky=E)
    ttk.Label(multipleframe, textvariable=OS_Username, font='Helvetica 12 bold', foreground="green").grid(column=2, row=1, sticky=W)

    ttk.Label(multipleframe, text='Timestamp Format:').grid(column=1, row=2, sticky=E)
    source_combo = ttk.Combobox(multipleframe, textvariable=measuretype, width=15)
    source_combo['values'] = ("Time", "Frame")
    source_combo.grid(column=2, row=2, sticky=W)
    #source_combo.bind('<<ComboboxSelected>>', source_selected)

    sep = ttk.Separator(multipleframe, orient="horizontal")
    sep.grid(column=1, row=3, sticky='we', columnspan=8)

    ttk.Label(multipleframe, text='Input Videos List:').grid(column=1, row=5, sticky=E)
    text_path = ttk.Entry(multipleframe, width=90, textvariable=textpath, state='active')
    text_path.grid(column=2, row=5, sticky=(W, W), columnspan=6)
    text_path_button = ttk.Button(multipleframe, text='...', width=3, command=select_file, state='active')
    text_path_button.grid(column=8, row=5, sticky=W)

    ttk.Label(multipleframe, text='Output Path:').grid(column=1, row=6, sticky=E)
    text_out_path = ttk.Entry(multipleframe, width=90, textvariable=textoutpath, state='active')
    text_out_path.grid(column=2, row=6, sticky=(W, W), columnspan=6)
    text_out_path_button = ttk.Button(multipleframe, text='...', width=3, command=select_output_directory, state='active')
    text_out_path_button.grid(column=8, row=6, sticky=W)

    sep = ttk.Separator(multipleframe, orient="horizontal")
    sep.grid(column=1, row=10, sticky='we', columnspan=8)

    start_co_button = ttk.Button(multipleframe, text='Export\nVideos', width=6, command=export_multiple_videos, state='active')
    start_co_button.grid(column=8, row=19, sticky=W)



    for child in singleframe.winfo_children():
        child.grid_configure(padx=10, pady=10)
        
    for child in multipleframe.winfo_children():
        child.grid_configure(padx=10, pady=10)

    root.mainloop()

