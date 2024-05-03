from moviepy.editor import VideoFileClip
from lag_prediction import predict_cv
from extract_csv_functions import rt_extract_timestamp, vid_extract_timestamp, convert_RT_speed20Hz, combine_pred_rt_speeds
import datetime
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def convert_video(input_file, output_file, target_resolution=(640, 480), target_fps=20):
    clip = VideoFileClip(input_file)
    clip_resized = clip.resize(target_resolution)
    clip_fps = clip_resized.set_fps(target_fps)
    clip_fps.write_videofile(output_file, codec='libx264')

def find_lag(input_file, rt_file, vid_pattern, rt_pattern):
    rt_starttime = rt_extract_timestamp(rt_file,rt_pattern)
    vid_starttime = vid_extract_timestamp(input_file, vid_pattern)

    start_difference = (rt_starttime - vid_starttime).total_seconds()

    print('Video Start Time: ', vid_starttime)
    print('RT Start Time: ', rt_starttime)
    print('Start Time Difference 1: ', start_difference)

    convert_rt_20hz = convert_RT_speed20Hz(rt_file)

    pred_file = "predicted_speed_20hz.txt"
    # pred_file= 'detect_result_class_test.txt'
    combine_df = combine_pred_rt_speeds(convert_rt_20hz, pred_file, start_difference)
    lag_detection(combine_df)
    return True

def lag_detection(dff):
    rt_speed = dff['Speed [kph]']
    pred_speed = dff['predicted_speed']
    plt.figure(figsize=(12,8))
    plt.plot(rt_speed, color='r')
    plt.plot(pred_speed, color='g', alpha=0.5)
    plt.title('Before')
    plt.savefig('Before.png')

    def calculate_variance(series1, series2):
        return np.var(series1 - series2)

    def minimize_variance(pred_speed, rt_speed):
        min_variance = float('inf')
        best_shift = 0
        print('Initial variance: ', calculate_variance(pred_speed, rt_speed))
        for shift in range(0, 60):
            shifted_series1 = np.roll(pred_speed, shift)
            variance = calculate_variance(shifted_series1[shift:], rt_speed[shift:])
            
            if variance < min_variance:
                min_variance = variance
                best_shift = shift
                shifted_series = shifted_series1
        
        return best_shift, min_variance, shifted_series

    best_shift, min_variance, shifted_series = minimize_variance(pred_speed, rt_speed)
    print("Best shift:", best_shift, "Min var: ", min_variance)
    plt.figure(figsize=(12,8))
    plt.plot(rt_speed.values, color='r')
    plt.plot(shifted_series, color='g', alpha=0.5)
    plt.title(f'After lag {best_shift}')
    plt.savefig(f'After_lag={best_shift}.png')


if __name__=='__main__':
    input_file = '2022-01-21_13-42-23_1604-Cam1.avi'
    rt_file = '2010_012122_Fixed_RT.csv'

    rt_pattern = "r'(\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}:\d{2} [APMapm]{2})'"
    vid_pattern = "r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})'" #e.g 2023-08-29_10-26-06_135-Cam1.avi

    
    # output_file = 'converted_video.mp4'  # Do not change

    # convert_video(input_file, output_file)
    # predict_cv()
    done = find_lag(input_file, rt_file, vid_pattern, rt_pattern)
    if done:
        print('Completed.')