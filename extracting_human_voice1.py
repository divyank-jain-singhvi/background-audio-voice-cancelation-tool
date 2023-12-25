from pydub import AudioSegment
import os
import wave
import numpy as np
import librosa
import soundfile as sf
from firebase_admin import storage,credentials
import firebase_admin
from pydub.playback import play
import subprocess 



count=0

def audio_convert(filename,types):

    if 'wav' in filename:
        print(filename,types)
        replaced_filename=filename.replace('.wav','.'+types)
        subprocess.call(['ffmpeg', '-i','./user audio data/'+filename, 
    				'./user audio data/'+replaced_filename])
        
    else:
        replaced_filename=filename.replace('.'+types,'.wav')
        subprocess.call(['ffmpeg', '-i','./user audio data/'+filename, 
    				'./user audio data/'+replaced_filename])


def play_audio(play_file):
    print("playing")
    audio = AudioSegment.from_file(play_file)
    play(audio)

def firebase_upload(file_path):
    dir_path = './user audio data'
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    bucket = storage.bucket()
    try:
        blob = storage.bucket().blob(file_path.filename)
        blob.upload_from_string(file_path.read())
    except (AttributeError):
        blob = storage.bucket().blob('extracted.wav')
        blob.upload_from_filename('./user audio data/'+file_path)
        


def firebase_extraction(file_path):
    dir_path = './user audio data'
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    bucket = storage.bucket()
    blob = bucket.blob(file_path)
    local_file_path = os.path.join(dir_path, os.path.basename(file_path))
    blob.download_to_filename(local_file_path)
    
    # a = plot_audio_waveform(local_file_path)


def split_audio(input_file, output_prefix, segment_length_ms):
    global count
    count=0
    audio = AudioSegment.from_file(input_file)


    num_segments = len(audio) // segment_length_ms
    # print(num_segments)

    for i in range(num_segments):
        
        start_time = i * segment_length_ms
        end_time = (i + 1) * segment_length_ms
        segment = audio[start_time:end_time]

        output_file = f"{output_prefix}_{i + 1}.wav"
        segment.export("./audio_segment/"+output_file, format="wav")
        count+=1
    return count



def find_time_of_max_amplitude(audio_path):
    # Step 2: Load the Audio File
    audio = AudioSegment.from_wav(audio_path)

    # Step 3: Convert to NumPy Array
    audio_data = np.array(audio.get_array_of_samples())
    

    # Step 4: Find the Time of Maximum Amplitude
    max_amplitude_index = np.argmax(np.abs(audio_data))

    time_of_max_amplitude = max_amplitude_index / audio.frame_rate
    return time_of_max_amplitude

def count_variable_x(main_max_amplitude_list):
    global count
    main_max_amplitude_list.sort()
    midpoint=len(main_max_amplitude_list)//2

    first_part = main_max_amplitude_list[:midpoint]
    second_part = main_max_amplitude_list[midpoint:]
    print(first_part,second_part)
        
    
    mid = len(first_part) // 2
    if (mid*2)%2==0:
        Q1 = (first_part[mid-1] + first_part[mid]) / 2
    else:
        Q1 = (first_part[mid+1]) / 2
    mid1 = len(second_part) // 2
    if (mid1*2)%2==0:
        Q3 = (second_part[mid1-1] + second_part[mid1]) / 2
    else:
        Q3 = (second_part[mid1]) / 2
    print(Q3,second_part[mid1],second_part[mid1])
    
    IQR=Q3-Q1
    print(IQR)
    IQR=IQR*1.5  #99.7 accuracy
    print(IQR)
    Q1=Q1-IQR
    Q3=Q3+IQR
    print(Q1,Q3)
    if  (Q1<0 and Q3>20000):
        return Q3+Q1,second_part
    else:
        return IQR,second_part

def plot_audio_waveform(audio_file_path):

    with wave.open(audio_file_path, 'rb') as wf:

        framerate = wf.getframerate()
        nframes = wf.getnframes()


        audio_data = wf.readframes(nframes)


    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    # for i in audio_array:
    #     print(i)

   # time_values = np.arange(0, nframes) / framerate

    # plt.figure(figsize=(10, 4))
    # plt.plot(time_values, audio_array, color='b')
    # plt.title('Audio Waveform')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Amplitude')
    # plt.grid(True)
    # plt.show()
    print(audio_array)
    return max(audio_array)



def change_amplitude(audio_file_path, start_time, end_time, scaling_factor, output_file_path):
    # Step 1: Load the Audio File
    signal, sample_rate = librosa.load(audio_file_path, sr=None)

    # Step 2: Select the Time Frame
    start_sample = int(start_time * sample_rate)
    end_sample = int(end_time * sample_rate)

    # Step 3: Modify Amplitude
    signal[start_sample:end_sample] *= scaling_factor

    # Step 4: Save Modified Audio using soundfile
    sf.write(output_file_path, signal, sample_rate)