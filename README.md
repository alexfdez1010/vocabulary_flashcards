# FlashcardGenerator

An script and a program to generate vocabulary flashcards for Anki

## Use Case

The gist of the algorithm is to transform a list of words in English into a format that can be imported to Anki as flashcards. Unluckily, 
at the moment only allows for individual words and phrasal verbs. Thus, idioms do not work. In the future, I will try to devise a way of implement that.

## Input and output

The input consists in a list of words. The list of words is provided in a txt file. The words or expresions ought to be separated by a line. 
The output generated will be a CSV (Comma-Separated Values) that conforms the required format needed to import the file into Anki. As the output includes
audio files the process needs extra steps to work properly. You can find a detail guide to import these audios in 
[Anki importing media](https://docs.ankiweb.net/importing.html#importing-media) into your instalation of Anki depending of your operative system.

## How it works?

### Script

The script will take two mandatory parameters (the routes to the input and output files) and one optional parameter specifying the maximum 
number of meanings to generate for each part of speech of a determined word. For instance, peer can be a verb and a noun. Thereby, it could be 
in two part of the speech and will have two flashcard associated with a maximum of meaning showed relate to that parameter. The default value of 
that parameter will be two should is not specified.

```
python generate_csv.py <word_file> <csv_file> [<max_menanings>]
```

### Program

Using the program you will get a more interactive way of using the generate csv functionality. You can create the txt file putting the words in 
the text input of the program and clicking the add words button. Finally, there is a button to generate the CSV file.

## Requirements

For the script is only needed the requests library and for the program Kivy and its dependencies (obviously Python is necessary).

```
pip install requests
pip install kivy
```

## Acknowledgments

This project will not be possible without the Rest API [Free Dictionary API](https://dictionaryapi.dev)






