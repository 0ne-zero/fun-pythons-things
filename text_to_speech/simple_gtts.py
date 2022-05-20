#!/usr/bin/env python3

from os import getenv, mkdir, remove
from traceback import print_tb
from playsound import playsound
from gtts import gTTS
from genericpath import exists
from gtts.tts import tts_langs
from hashlib import sha256
from io import BytesIO
from sys import argv
import argparse

HOME = getenv('HOME', '')

if HOME == '':
    print("Set your home environment variable ):")
    exit(1)

VOICES_DIRECTORY = f"{HOME}/.gtts_voices"

if not exists(VOICES_DIRECTORY):
    mkdir(VOICES_DIRECTORY)


def smalling_text(text: str, max_length) -> list:
    '''
    Smalling text to maximum length
    If the text characters are larger than max_length,
    we need to make the text smaller, so we divide the text into smaller pieces.
    and put those pieces into a list
    Returns:
    string: when the text characters itself is less than the max_length
    list: when the text characters bigger than the max_length
    '''
    if len(text) <= max_length:
        return text
    else:
        sentences = []
        variable_max_length = max_length
        pos = 0
        length = len(text)
        complete = False
        while (complete == False):
            if ((pos + variable_max_length) < length):
                while(text[(pos + variable_max_length)] != ' '):
                    variable_max_length -= 1
                sentences.append(text[pos:(pos + variable_max_length)])
                pos = (pos + variable_max_length)
                variable_max_length = max_length
            else:
                sentences.append(text[pos:])
                complete = True
        return sentences

    '''
    Another approach
    while text != '':
    try:
        while(text[variable_max_length] != ' '):
            variable_max_length -= 1
        sentences.append(text[:variable_max_length])
        text = text[variable_max_length:]
        variable_max_length = max_length
    except:
        sentences.append(text)
        text = ''
    '''


def save_voice(data, path):
    '''this function saves voice in in $HOME/.gtts_voices/ directory'''
    with open(path, 'wb') as file:
        file.write(data)


def download_voice(sentences, lang,speed) -> bytearray:
    '''download .mp3 voice file and return it in bytearray object'''
    bytes = bytearray()

    # If text is grather than 100 character, should send few request
    if isinstance(sentences, list):
        # Download many mp3 files and save them in memroy and then save them all in one file on disk.
        for sentence in sentences:
            # Download and store in memory
            if speed:
                gtts = gTTS(sentences,lang=lang,slow=True)
            else:
                gtts = gTTS(sentence, lang=lang)
            # gtts needs file like object to write
            temp = BytesIO()
            gtts.write_to_fp(temp)
            # Append bytes
            bytes += bytearray(temp.getvalue())

    # Text lower than 100 character
    elif isinstance(sentences, str):
        if speed:
                gtts = gTTS(sentences,lang=lang,slow=True)
        else:
            gtts = gTTS(sentences, lang=lang)
        # gtts needs file like object to write
        temp = BytesIO()
        gtts.write_to_fp(temp)
        bytes += bytearray(temp.getvalue())

    return bytes


def speak_gtts(text: str, lang: str = 'en',speed:str='slow'):
    '''speak by google text to speech service/api (online)'''
    '''Google support only 100 character in a request.\
    so we need to send some request if text has more than 100 character'''
    if len(text) < 1:
        raise Exception('text parameter is empty')

    # Both filename and text and language hashes (voice_hash)
    filename = sha256((text+lang+speed).encode()).hexdigest()

    # Path of file for save it, file name is hash of text and lang
    path = f'{VOICES_DIRECTORY}/{filename}.mp3'
    del filename

    # If text voice is exists,just play it
    if exists(path):
        # Play voice
        playsound(path)
    # Text voice isn't exists,so we should download it and finally save it.(in VOICES_DIRECTORY)
    else:
        # Google has limit. text should be lower than 100 character
        # Slice text into pieces (list)
        sentences = smalling_text(text, 100)
        bytearray = download_voice(sentences, lang,speed)
        save_voice(bytearray, path)
        # Play voice
        playsound(path)

def args_validation():
    available_languages_codes = list(tts_langs().keys())
    available_languages_names = list(tts_langs().values())
    parser = argparse.ArgumentParser(
        description="Simple tts(Text-to_Speech) tool, That Uses gtts(Google-Text-to_Speech)")
    parser.add_argument('-t', '--text', type=str,
                        help='The text you want to be the text of the speech')
    parser.add_argument('-l', '--language', type=str, nargs=1,
                        choices=available_languages_codes + available_languages_names,
                        help='Language of speech\nDefault is "en" = "english"')
    parser.add_argument('-f', '--file', type=str,
                        help="The file you want to be the text of the speech")
    parser.add_argument('-s','--speed',choices=['slow','fast'],default='slow',help="Speed of reading text")
    args = parser.parse_args()
    file = args.file if args.file != None else ''
    text = args.text if args.text != None else ''
    speed = args.speed 
    lang = args.language if args.language != None else 'en'
    
    return text,lang,file,speed
if __name__ == '__main__':

    text,lang,file,speed = args_validation()    
    
    # Read file as text if selected any file
    if file != '':
        # File exists
        if exists(file):
            lines = []
            with open(file, 'r') as file:
                lines = file.readlines()
            for l in lines:
                text += l
        # File not exists
        else:
            print("Path of file isn't exists")
            exit(1)
    # Text is still empty, that meens no text and no file entered.
    if text == '':
        # So, get text from stdin(Terminal)
        first = True
        while True:
            try:
                if not first:
                    text += input()
                else:
                    text += input("Press Ctrl-D for convert entered text to speech.\nEnter text:\n")
                    first = False
            except EOFError:
                break
    
    print('\nDownloading voice ...')
    speak_gtts(text, lang,speed)
