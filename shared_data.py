from pydub import AudioSegment

# List of MP3 files to combine
mp3_files = ['podcast_audio/part_0.mp3', 'podcast_audio/part_2.mp3', 'podcast_audio/part_4.mp3', 'podcast_audio/part_6.mp3', 'podcast_audio/part_8.mp3','podcast_audio/part_10.mp3', 'podcast_audio/part_12.mp3' ]  # Replace with your file paths

# Initialize an empty audio segment
combined = AudioSegment.empty()

# Iterate over the list of MP3 files and concatenate them
for mp3_file in mp3_files:
    sound = AudioSegment.from_mp3(mp3_file)
    combined += sound

# Export the combined audio to a new file
combined.export("podcast_file/combined_file.mp3", format="mp3")
