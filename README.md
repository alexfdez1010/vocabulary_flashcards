# FlashcardGenerator

A script to generate vocabulary flashcards for Anki

## Use Case

The gist of the algorithm is to transform a list of words in English into an Anki Package. Unfortunately, at the moment only allows for individual words and phrasal verbs. Thus, idioms do not work. In the future, it will be tried to devise a way of implement that.

## Input and output

The input consists in a list of words. The list of words is provided in a txt file. The words or expresions ought to be separated by a line. 
The output generated will be a .apkg (Anki Package) ready to be imported into Anki. 

## How it works?

### Script

The script will take two mandatory parameters (the routes to the input and output files) and one optional parameter specifying the maximum 
number of meanings to generate for each part of speech of a determined word. For instance, peer can be a verb and a noun. Thereby, it could be 
in two part of the speech and will have two flashcard associated with a maximum of meaning showed relate to that parameter. The default value of 
that parameter will be two should is not specified.

```
python generate_csv.py <word_file> <csv_file> [<max_menanings>]
```

## Requirements

For the script is only needed the requests and genanki libraries (obviously Python is needed).

```
pip install requests
pip install genanki
```

## Acknowledgments

This project will not be possible without the Rest API [Free Dictionary API](https://dictionaryapi.dev) and [genanki](https://github.com/kerrickstaley/genanki)






