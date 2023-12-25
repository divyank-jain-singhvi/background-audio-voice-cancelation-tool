from flask import Flask, render_template,request, redirect, url_for,send_file
import wave
import struct
import os
from extracting_human_voice1 import *
import shutil



types_of_audio=('8svx','aac','ac3','aiff','amb','amr','ape','au','avr','caf','cdda','cvs','cvsd','cvu','dss','dts','dvms',
                'fap','flac','fssd','gsm','gsrt','hcdm','htk','ima','ircam','m4a','m4r','maud','mp2','mp3','nist','oga',
                'ogg','opus','paf','prc','pvf','ra','sd2','shn','sln','smp','snd','sndr','sndt','sou','sph','spx','tak','tta',
                'txw','vms','voc','vox','vqf','w64','wma','wv','wve','xa')
app = Flask(__name__)
app = Flask(__name__, static_url_path='/static', static_folder='static')
duration = 15
answer=''
sample_rate = 44100
time_frame_counter=0
file_path=''
filename=''
convert_flag=0
types=''

cred = credentials.Certificate("voice-extraction-firebase-adminsdk-mxc5w-ec1c227e24.json")
firebase_admin.initialize_app(cred, {"storageBucket": "voice-extraction.appspot.com"})


def record(filename,filename_extracted):
    global time_frame_counter,types
    if not os.path.exists('./audio extracted data'):
        print('dir 1')
        os.mkdir('./audio extracted data')
    if not os.path.exists('./audio_segment'):
        print('dir 1')
        os.mkdir('./audio_segment')
# Open the file
    WAVE_OUTPUT_FILENAME = filename
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
    
    # Get the properties of the audio file
    CHANNELS = waveFile.getnchannels()
    RATE = waveFile.getframerate()
    SAMPLE_WIDTH = waveFile.getsampwidth()
    
    # Read the frames
    frames = waveFile.readframes(-1)
    
    # Close the file
    waveFile.close()
    
    
    count=0
    main_max_amplitude_list=[]
    max_amplitude_time_list=[]
    main_list=[]
    input_file = WAVE_OUTPUT_FILENAME
    output_prefix = 'output_segment'
    segment_length_ms = 1000
    main_amplitude_split=[]
    count=split_audio(input_file, output_prefix, segment_length_ms)
    # a=plot_audio_waveform(input_file)
    for i in range(0,count):
        audio_file_segment_path = f'./audio_segment/output_segment_{i+1}.wav'
        max_audio_amplitude=plot_audio_waveform(audio_file_segment_path)
        main_max_amplitude_list.append(max_audio_amplitude)
        main_amplitude_split.append(max_audio_amplitude)
        print(max_audio_amplitude)
        max_amplitude_time = find_time_of_max_amplitude(audio_file_segment_path)
        print(f"Time of maximum amplitude: {max_amplitude_time} seconds")
        max_amplitude_time_list.append(max_amplitude_time)
    print(main_max_amplitude_list)
    variable_x,second_list=count_variable_x(main_max_amplitude_list)
    print(variable_x)
    duration=int(request.values.get('filesize'))
    while True:    
        for i in range(0,count):
            if main_amplitude_split[i]<=variable_x:
                time_frame_counter=(time_frame_counter+1)%duration
            else:
                main_list.append(time_frame_counter)
                time_frame_counter=(time_frame_counter+1)%duration
        if main_amplitude_split[i] >variable_x:
            main_list.append(time_frame_counter)
            
        if main_list!=[]:
            break
        else:
            variable_x=second_list[0]
    print(main_max_amplitude_list)
    print(max_amplitude_time_list)
    print(main_list)
    
        
    try:
        start_time = 0.0  # start time in seconds
        end_time = main_list[0]  # end time in seconds
        scaling_factor = 0.001   # adjust this value to change amplitude
        output_file_path = WAVE_OUTPUT_FILENAME
        
        change_amplitude(input_file, start_time, end_time, scaling_factor, output_file_path)
        
        for i in range(0,len(main_list)):
    
            start_time = main_list[i]+1  # start time in seconds
            if i==len(main_list)-1:
                end_time=duration
            else:
                end_time = main_list[i+1]
            print(start_time,end_time)
            change_amplitude(output_file_path, start_time, end_time, scaling_factor, output_file_path)
        print(start_time,end_time)
        change_amplitude(output_file_path, start_time, end_time, scaling_factor, output_file_path)
    except IndexError:
        pass
    firebase_upload(filename_extracted)
    print('upload',filename_extracted)
    print(types)
    audio_convert('extracted.wav',types)
    
    if os.path.exists('./audio extracted data/'):
        shutil.rmtree('./audio extracted data/')
    if os.path.exists('./audio_segment/'):
        shutil.rmtree('./audio_segment/')
    firebase_extraction('extracted.wav')
    
    
    # play_audio(WAVE_OUTPUT_FILENAME)
    # a=plot_audio_waveform(input_file)
    
    
    
    # a=plot_audio_waveform(WAVE_OUTPUT_FILENAME)
    


@app.route('/', methods=['GET', 'POST'])
def index():
    if os.path.exists('./user audio data/'):
        shutil.rmtree('./user audio data/')
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def index1():
    global file_path,filename,types,types_of_audio
    file_path = request.files['file']
    filename=file_path.filename
    firebase_upload(file_path)
    print('upload',file_path)
    firebase_extraction(filename)
    print('extract',filename)
    
    # if 'mp3' in filename:
    #     audio_convert(filename)
    #     filename=filename.replace('mp3','wav')
    #     print('mp3-->wav')
    # elif 'm4a' in filename:
    #     audio_convert(filename,'m4a')
    #     filename=filename.replace('m4a','wav')
    #     print('m4a-->wav')
    
    
    for audio_type in types_of_audio:
        print(audio_type)
        if audio_type in filename:
            print('found')
            audio_convert(filename,audio_type)
            filename=filename.replace(audio_type,'wav')
            print(audio_type+'-->wav')
            types=audio_type
            break
        else:
            types='wav'
    
    
    
    user_audio_file ='./user audio data/'+filename
    record(user_audio_file,filename)
    
    return render_template("index1.html")

# @app.route('/downloard', methods=['GET', 'POST'])
# def index2():
#     global filename
#     firebase_extraction('extracted.wav')
#     return render_template("index.html")
#     # return render_template("index.html")

@app.route('/download')
def download_file():
    global types
    if types!='wav':
        audio_convert('extracted.wav',types)
    path = "./user audio data/extracted."+types
    return send_file(path, as_attachment=True)


@app.route('/home', methods=['GET', 'POST'])
def index3():
    if os.path.exists('./user audio data/'):
        shutil.rmtree('./user audio data/')
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
