from requests import get
from typing import List
from sys import argv
from os import mkdir
from shutil import rmtree

from genanki import Note, Model, Deck, Package
from random import randrange

CSS = """
.card {
    font-family: helvetica;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}
"""
MODEL = Model(
    1227149392,
    'Vocabulary Flashcard',
    fields=[
        {'name': 'Word'},
        {'name': 'Meanings'},
        {'name': 'Audio'}
    ],
    templates=[
        {
            'name': 'Vocabulary card',
            'qfmt': '{{Word}}\n\n<div style="font-family: "Arial"; font-size: 20px;">{{Audio}}</div>',
            'afmt': '{{FrontSide}}<hr id="answer">{{Meanings}}',
        },
    ],
    css=CSS
)


def get_json_word(word: str) -> dict:
    """
    Get json from API
    :param word: word to get
    :return: a dictionary with the data of that word
    """
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = get(url).json()
    if isinstance(response, list):
        response = response[0]

    return response if response.get("word") else None


def download_audio(filename: str, link: str) -> bool:
    """
    Download the audio of the word
    :param filename: name of the file to save the audio
    :param link: link to the audio
    :return: True if the audio was downloaded and save, False otherwise
    """
    if link:
        with open(filename, "bw") as file:
            response = get(link)
            if response:
                file.write(response.content)
                return True
    return False


def prepare_json(json: dict, max_meanings: int = 0) -> List[dict]:
    """
    For each meaning of the word generate a dictionary with the information required
    :param json: json of the word
    :param max_meanings: maximum number of meanings to for each part of speech
    :return: a list of dictionary with each part of speech
    """

    prepared_json: List[dict] = [
        {
            "word": f"{json['word']} ({meaning['partOfSpeech']})",
            "definitions": [
                {"definition": definition.get("definition", ""), "example": definition.get("example", "")}
                for idx, definition in enumerate(meaning["definitions"])
                if max_meanings == 0 or idx < max_meanings],
            "audio": f"flashgen_{json['word'].replace(' ', '_')}.mp3"
        }
        for meaning in json["meanings"]
    ]

    meanings = {entry["word"]: False for entry in prepared_json}
    res_json = []
    for entry in prepared_json:
        if not meanings.get(entry["word"]):
            meanings[entry["word"]] = True
            res_json.append(entry)

    return res_json


def create_note(json: dict) -> Note:
    """
    Convert json to the format required in ANKI
    :param json: json to convert
    :return: a string with the format required in ANKI
    """
    definitions = "".join([
        f"<li>Definition: {definition['definition']}</li><li> Example: {definition['example']}</li><br>"
        if definition['example'] else f"<li>Definition: {definition['definition']}</li><br>"
        for definition in json["definitions"]
    ])
    return Note(
        model=MODEL,
        fields=[json['word'], f'<ul>{definitions}</ul>', f'[sound:{json["audio"]}]'],
    )


def get_link_audio(json_word: dict) -> str:
    """
    Get the link of the audio of the word
    :param json_word: json of the word
    :return: link of the audio
    """
    for entry in json_word["phonetics"]:
        if entry.get("audio"):
            return entry["audio"]
    return ""


def generate_package(word_file: str, package_file: str, max_meanings: int = 2) -> None:
    """
    Generate a csv file with the data of the words in the file
    :param word_file: file with the words (one word per line)
    :param package_file: file to save the Anki package
    :param max_meanings: max number of meanings to show for each part of speech if is equal to 0 show all
    :return: None
    """
    with open(word_file, "r") as file:
        words = file.readlines()
        words = list(map(lambda x: x.strip(), words))
        words = list(set(words))

    deck = Deck(
        randrange(1 << 31, 1 << 32),
        'Vocabulary Flashcard',
    )

    audio_files = []

    for word in words:
        json_word = get_json_word(word.strip())
        if json_word:
            audio_filename = f"audios/flashgen_{json_word['word'].replace(' ', '_')}.mp3"

            if download_audio(audio_filename, get_link_audio(json_word)):
                audio_files.append(audio_filename)

            json_prepared = prepare_json(json_word, max_meanings)

            for json in json_prepared:
                note = create_note(json)
                deck.add_note(note)
                print(f"{json['word']} added to the deck")
        else:
            print(f"{word} not found")

    package = Package(deck)
    package.media_files = audio_files
    package.write_to_file(package_file)
    rmtree("audios")


def main():
    if len(argv) in [3, 4]:
        try:
            mkdir("audios")
        except FileExistsError:
            pass
        if len(argv) == 4:
            generate_package(argv[1], argv[2], int(argv[3]))
        else:
            generate_package(argv[1], argv[2])
        print(f"Package generated in {argv[2]}")
    else:
        print("Usage: generate_package <word_file> <package_anki_file>")


if __name__ == "__main__":
    main()
