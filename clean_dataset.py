from pathlib import Path
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def retrieve_files():

    books_folder = Path.cwd().joinpath('books')

    all_books = []

    for author_folder in books_folder.iterdir():

        author_books = []

        for book_file in author_folder.iterdir():
            author_books.append(book_file)

        all_books.append(author_books)


    for author in all_books:
        print("autor\n")

        for file in author:

            print(file.is_file())
        


def read_and_process_file(filename):

    stop_words = set(stopwords.words('english'))
    count = 0
    line = ' a'
    with open(filename, 'r', encoding="utf-8") as f:
        for line in f:

            line = line.lower()
            tokens = word_tokenize(line)
            print(tokens)
            count += 1
            if count == 5:
                break

    


read_and_process_file(Path.cwd().joinpath('books', 'Dostoievski', 'the_idiot.txt'))