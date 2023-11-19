from flask import Flask, render_template, url_for, request, jsonify
from flask_socketio import SocketIO, emit
import openai
import os
import pygame
import requests
import re
from moviepy.editor import concatenate_audioclips, AudioFileClip
from mouth_images import getPodcastBackgrounds
from pydub import AudioSegment


app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def index():
    names = [
        "LeBron James",
        "Taylor Swift",
        "Donald Trump",
        "Morgan Freeman",
        "Kanye West",
        "Peter Griffin",
        "Lois Griffin",
        "Arnold Schwarzenegger"
    ]
    getPodcastBackgrounds("", "", "static/images/")
    socketio.emit("changed_images", {"message": 0})
    return render_template(
        "index.html", names=names
    )  # We don't need to specify: templates/index.html, as it already knows to look in the templates folder by default


@app.route("/topic", methods=["GET", "POST"])
def return_data():
    the_form = request.form
    if request.method == "POST":
        topic = the_form["topic-input"]
        celebA = the_form["celebA"]
        celebB = the_form["celebB"]
        getPodcastBackgrounds(celebA, celebB, "static/images/")
        socketio.emit("changed_images", {"message": 1})
        # Use the imported values
        user_chosen_topic = topic
        name1 = celebA
        name2 = celebB
        print(user_chosen_topic)
        print(name1)
        print(name2)

        def generate_podcast_script(
            api_key, characters, intro, conversation_topics, target_token_length
        ):
            openai.api_key = api_key

            # Revised prompt for a more interactive and continuous conversation
            prompt = (
                f"A simulated podcast conversation between {characters}. "
                f"Introduction: {intro}. "
                f"Topics of conversation: {conversation_topics}. "
                "The conversation should be dynamic with both participants asking questions and elaborating on each other's answers. "
                f"{name1} starts the conversation, and then they take turns speaking. "
                "The conversation should reflect natural speech patterns including. the conversation should also really demonstrate their own unique personalities and what they would really say "
                "appropriate rate, volume, pitch, articulation, pronunciation, and fluency as well. Don't be afaird to include humor in the conversation as well. Don't make the conversation to linear, there can be disagreements and interjections"
            )

            total_script = ""
            current_prompt = prompt
            total_tokens = 0
            max_tokens_per_request = 3900  # Adjust as needed, but not exceeding 4097

            while total_tokens < target_token_length:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=current_prompt,
                    max_tokens=max_tokens_per_request,
                    temperature=0.7,
                )
                part_script = response.choices[0].text.strip()
                total_script += " " + part_script
                total_tokens += len(
                    part_script.split()
                )  # Count the tokens in the generated part
                current_prompt = " ".join(
                    part_script.split()[-100:]
                )  # Use the last tokens as the new prompt

                if (
                    len(part_script.strip()) == 0
                ):  # Break if no new content is generated
                    break
            print("length of script split by newline is")
            print(len(total_script.split("\n")))

            socketio.emit("total_files", {"message": len(total_script.split("\n"))})
            return total_script

        def text_to_speech(
            text, i, name
        ):  # Need to replace with clone audio (takes names and script)
            if name == "Kanye West":
                name_id = "s3://voice-cloning-zero-shot/60ec47bc-6e13-4684-9340-a5e6a1d53f88/kanye-west/manifest.json"
            elif name == "LeBron James":
                name_id = "s3://voice-cloning-zero-shot/7e5d9e03-4bcc-4d89-b275-dcd2cb3c45f4/lebron-james/manifest.json"
            elif name == "Donald Trump":
                name_id = "s3://voice-cloning-zero-shot/5837b59a-faa0-4386-acf3-f27235b3ddcf/donald-trump/manifest.json"
            elif name == "Morgan Freeman":
                name_id = "s3://voice-cloning-zero-shot/bb44bb99-ed1f-42b6-a7e8-cd917454c154/morgan-freeman/manifest.json"
            elif name == "Lois Griffin":
                name_id = "s3://voice-cloning-zero-shot/ceef81dc-52a3-479d-8da1-8980fb0e9a30/lois-griffin/manifest.json"
            elif name == "Peter Griffin":
                name_id = "s3://voice-cloning-zero-shot/e409b49b-f3e2-4e75-a9f7-65a0f07b7edf/peter-griffin/manifest.json"
            elif name == "Arnold Schwarzenegger":
                name_id = "s3://voice-cloning-zero-shot/5b14a443-1d37-489e-a56b-2dfe6656264e/arnold-schwarzenegger/manifest.json"
            elif name == "Taylor Swift":
                name_id = "s3://voice-cloning-zero-shot/ff3f5ec0-b9f0-4bbb-ad5b-7e2cebe79012/taylor-swift/manifest.json"

            url = "https://api.play.ht/api/v2/tts"
            payload = {
                "text": text,
                "voice": name_id,
                "output_format": "mp3",
                "voice_engine": "PlayHT2.0",
            }
            headers = {
                "AUTHORIZATION": "278485edc78846328dd3dd883d5e1edb",
                "X-USER-ID": "TtmGFJ2K5NX4xgEd7bprs7XDrZ33",
                "accept": "text/event-stream",
                "content-type": "application/json",
                "Content-Location": "/celeb_audio",
            }

            response = requests.post(url, json=payload, headers=headers)

            response_text = response.text

            # Regular expression to find the URL
            match = re.search(r'"url":"([^"]+)"', response_text)
            if match:
                mp3_url = match.group(1)
                print(mp3_url)
            else:
                print("URL not found in the response.")

            filename = f"podcast_audio/part_{i}.mp3"

            response = requests.get(mp3_url, stream=True)
            if response.status_code == 200:
                with open(filename, "wb") as file:
                    file.write(response.content)
                print(f"File saved successfully at {filename}")
                socketio.emit("file_saved", {"message": i})
            else:
                print(
                    f"Failed to download the file. Status code: {response.status_code}"
                )

            return filename

        def create_podcast_audio(script, output_folder="podcast_audio"):
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
                # --------------Clear the podcast_audio directory -----------------------
            for filename in os.listdir("podcast_audio"):
                file_path = os.path.join("podcast_audio", filename)
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            # --------------Clear the podcast_audio directory -----------------------

            filenames = []
            lines = script.split("\n")
            for i, line in enumerate(lines):
                line = line.strip()
                if line.startswith(f"{name1}"):
                    text = line.replace(f"{name1}:", "").strip()
                    name = name1

                elif line.startswith(f"{name2}:"):
                    text = line.replace(f"{name2}:", "").strip()
                    name = name2
                else:
                    continue  # Skip lines that don't start with a speaker tag

                # text is what we want them to say

                filename = text_to_speech(
                    text,
                    i,
                    name,
                )  # this will generate the file for that line of the script
                filenames.append(filename)

            return filenames

        def combine_audio_clips(mp3_files):
            # List of MP3 files to combine
            # Initialize an empty audio segment
            combined = AudioSegment.empty()

            # Iterate over the list of MP3 files and concatenate them
            for mp3_file in mp3_files:
                sound = AudioSegment.from_mp3(mp3_file)
                combined += sound

            # Export the combined audio to a new file
            combined.export("static/audio/combined_file.mp3", format="mp3")

        # def play_audio(file):
        #     pygame.mixer.init()
        #     pygame.mixer.music.load(file)
        #     pygame.mixer.music.play()

        #     # Wait for the audio to finish playing
        #     while pygame.mixer.music.get_busy():
        #         pygame.time.Clock().tick(10)  # Check every 10ms

        # Example usage
        api_key = None
        characters = f"{name1} and {name2}"
        intro = user_chosen_topic
        conversation_topics = user_chosen_topic
        target_token_length = 10000

        podcast_script = generate_podcast_script(
            api_key, characters, intro, conversation_topics, target_token_length
        )
        print(podcast_script)

        audio_files = create_podcast_audio(podcast_script)
        combine_audio_clips(audio_files)
        socketio.emit("audio_done", {"message": 0})

    return jsonify(
        {
            "message": "Data received",
            "topic": topic,
            "Celeb A": celebA,
            "Celeb B": celebB,
        }
    )


@app.route("/changed", methods=["GET", "POST"])
def update_images():
    if request.method == "POST":
        data = request.json
        celebA = data.get("celebA")
        celebB = data.get("celebB")
        getPodcastBackgrounds(celebA, celebB, "static/images/")
        socketio.emit("changed_images", {"message": 2})
    return jsonify(
        {
            "message": "Images Updated",
            "Celeb A": celebA,
            "Celeb B": celebB,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
