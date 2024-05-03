import pickle
from model_skeleton import speed_detection
def predict_cv():
    with open('./speedmodel/2007rv_params_large.pkl','rb') as file:
        mse, MEAN_CONST, STD_CONST = pickle.load(file)

    speed_detection('./speedmodel/Model_large2.h5', 'converted_video.mp4', 'predicted_speed_20hz2.txt', 0.5, 8, 6, MEAN_CONST, STD_CONST)
# detect_result_class_test
# def convert_avi_to_mp4(input_file, output_file):
#     command = ['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-crf', '23', '-c:a', 'aac', '-b:a', '128k', output_file]
#     subprocess.run(command)

if __name__ == "__main__":
    predict_cv()
#     input_file = "2023-12-14_14-56-29_1200-Cam1.avi"
#     output_file = "output.mp4"

#     convert_avi_to_mp4(input_file, output_file)
