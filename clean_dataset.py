from pathlib import Path
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def retrieve_files():

    books_folder = Path.cwd().joinpath('books')
    Path(Path.cwd().joinpath('dataset')).mkdir(parents=True, exist_ok=True)

    all_books = []

    for author_folder in books_folder.iterdir():

        author_books = []

        for book_file in author_folder.iterdir():
            author_books.append(book_file)

        all_books.append(author_books)


    for author in all_books:
        print("autor\n")

        for file in author:

            read_and_clean_file(file)



def read_and_clean_file(filename):

    stop_words = set(stopwords.words('english'))
    count = 0

    with open(filename, 'r', encoding="utf-8") as f:
        for line in f:

            line = line.lower()
            tokens = word_tokenize(line)

            filtered_tokens = [token for token in tokens if not token.lower() in stop_words]

            processed_line = (" ".join(filtered_tokens))

            print(processed_line)
            #print(filtered_tokens)

            count += 1
            if count > 85:
                break

    
def create_dataset_files(processed_lines, author_folder, filename):

    author_folder = str(author_folder)

    destiny_file = Path(Path.cwd().joinpath('dataset', author_folder, filename)).mkdir(parents=True, exist_ok=True)

    for line in processed_lines:
        i = 0


#print_processed_file(filename, processed_lines):

#read_and_clean_file(Path.cwd().joinpath('books', 'Dostoievski', 'the_idiot.txt'))

#retrieve_files()

destiny_folder = Path(Path.cwd().joinpath('dataset', 'autor')).mkdir(parents=True, exist_ok=True)
#destiny_file = Path(Path.joinpath(destiny_folder, "texto.txt")).touch(exist_ok=True)

Path.cwd().joinpath('dataset', 'autor',"texto.txt").touch(exist_ok=True)
#Path.joinpath(destiny_folder, "texto.txt")).touch(exist_ok=True)
destiny_file = Path.cwd().joinpath('dataset', 'autor',"texto.txt")

with open(destiny_file, 'w', encoding="utf-8") as f:
    f.write("Hello")
#new_file = destiny_folder / 'myfile.txt'
#new_file.is_file()
