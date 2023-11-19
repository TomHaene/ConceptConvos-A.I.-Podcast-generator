import openai
from gtts import gTTS
import os
import pygame
import shared_data  # Import the shared data module

# # Use the imported values
# user_chosen_topic = shared_data.topic
# name1 = shared_data.celebA
# name2 = shared_data.celebB
# print(user_chosen_topic)
# print(name1)
# print(name2)
# print('checkpoint')


def generate_podcast_script(api_key, characters, intro, conversation_topics, target_token_length):
    openai.api_key = api_key

    # Revised prompt for a more interactive and continuous conversation
    prompt = (f"A simulated podcast conversation between {characters}. "
              f"Introduction: {intro}. "
              f"Topics of conversation: {conversation_topics}. "
              "The conversation should be dynamic with both participants asking questions and elaborating on each other's answers. "
              f"{name1} starts the conversation, and then they take turns speaking. "
              "The conversation should reflect natural speech patterns including "
              "appropriate rate, volume, pitch, articulation, pronunciation, and fluency.")

    total_script = ""
    current_prompt = prompt
    total_tokens = 0
    max_tokens_per_request = 3900  # Adjust as needed, but not exceeding 4097

    while total_tokens < target_token_length:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=current_prompt,
            max_tokens=max_tokens_per_request,
            temperature=0.7
        )
        part_script = response.choices[0].text.strip()
        total_script += " " + part_script
        total_tokens += len(part_script.split())  # Count the tokens in the generated part
        current_prompt = " ".join(part_script.split()[-100:])  # Use the last tokens as the new prompt

        if len(part_script.strip()) == 0:  # Break if no new content is generated
            break

    return total_script

def text_to_speech(text, lang, filename):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(filename)

def create_podcast_audio(script, output_folder="podcast_audio"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filenames = []
    lines = script.split('\n')
    for i, line in enumerate(lines):
        if line.startswith(f"{name1}"):
            lang = 'en'  # English for Elon Musk
            text = line.replace(f"{name1}:", "").strip()
        elif line.startswith(f"{name2}:"):
            lang = 'en-uk'  # UK English for Kanye West (as an example)
            text = line.replace(f"{name2}:", "").strip()
        else:
            continue  # Skip lines that don't start with a speaker tag

        filename = f"{output_folder}/part_{i}.mp3"
        text_to_speech(text, lang, filename)
        filenames.append(filename)
    
    return filenames

def play_audio(files):
    pygame.mixer.init()
    for file in files:
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait for audio to finish playing
            pygame.time.Clock().tick(10)  # Check every 10ms

# Example usage
api_key = "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"
characters = f"{name1} and {name2}"
intro = user_chosen_topic
conversation_topics = user_chosen_topic
target_token_length = 10000

podcast_script = generate_podcast_script(api_key, characters, intro, conversation_topics, target_token_length)
print(podcast_script)
audio_files = create_podcast_audio(podcast_script)
play_audio(audio_files)
