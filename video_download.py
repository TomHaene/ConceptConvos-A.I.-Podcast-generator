from pytube import YouTube

yt = YouTube("https://www.youtube.com/watch?v=qlaum72JNRA")

stream = yt.streams.filter(only_audio=True).first()
stream.download(output_path="/training_videos/", filename="trump_debate.mp4")
