from flask import Flask, request, jsonify
from moviepy.editor import VideoClip, TextClip
import os
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\convert.exe"})


app = Flask(__name__)

@app.route('/generate_video', methods=['POST'])
def generate_video():
    try:
        # Get data from the request
        data = request.json

        # Get parameters from the request data
        text = data.get('text', 'Hello, World!')
        duration = data.get('duration', 5)
        output_path = data.get('output_path', 'output1.mp4')

        # Generate video using MoviePy
        clip = TextClip(text, fontsize=70, color='white', bg_color='black', size=(640, 480))
        video = VideoClip(lambda t: clip.get_frame(t), duration=duration)
        video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24)

        return jsonify({'status': 'success', 'message': 'Video generated successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
