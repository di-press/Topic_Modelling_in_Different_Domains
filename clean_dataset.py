from pathlib import Path
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

''' 
def retrieve_files():

    books_folder = Path.cwd().joinpath('books')
    #Path.cwd().joinpath('dataset').mkdir(parents=True, exist_ok=True)

    p = Path("dataset")
    p.mkdir(parents=True, exist_ok=True)

    #return 

    all_books = []

    for author_folder in books_folder.iterdir():

        author_books = []

        for book_file in author_folder.iterdir():
            author_books.append(book_file)

        all_books.append(author_books)


    for author in all_books:
        print("autor\n")

        for file in author:
            #print(file)

            processed_lines = read_and_clean_file(file)
            create_dataset_files(processed_lines, author, file)
'''


def read_and_clean_file(filename):

    stop_words = set(stopwords.words('english'))
    count = 0

    processed_lines = []

    with open(filename, 'r', encoding="utf-8") as f:
        for line in f:

            line = line.lower()
            tokens = word_tokenize(line)

            filtered_tokens = [token for token in tokens if not token.lower() in stop_words]

            processed_line = (" ".join(filtered_tokens))

            #print(processed_line)
            #print(filtered_tokens)
            processed_lines.append(processed_line)

    return processed_lines



def retrieve_debug():

    books_folder = Path.cwd().joinpath('books')

    p = Path("dataset")
    p.mkdir(parents=True, exist_ok=True)


    for author_folder in books_folder.iterdir():

        all_books = []
        author_name = str(author_folder)
        author_name = author_name.split("/")
        author_name = author_name[-1:]
        print("author_name: ", author_name)

        author_books = []

        for book_file in author_folder.iterdir():
            author_books.append(book_file)

        all_books.append(author_books)


        for author in all_books:
            
            path_name = str(author_folder)
            print(author_folder)
            path_name = path_name.split("/")
            author_name = path_name[-1]

            for file in author:

                filename = str(file)
                filename = filename.split("/")
                filename = filename[-1]
   
                processed_lines = read_and_clean_file(file)
                create_dataset_files(processed_lines, author_name, filename)


def create_dataset_files(processed_lines, author_folder, filename):

    author_folder = str(author_folder)

    p = Path("dataset", author_folder)
    p.mkdir(parents=True, exist_ok=True)

    file_path = Path(p, filename)
    file_path.touch(exist_ok=True)

    with open(file_path, 'w', encoding="utf-8") as f:
        
        for line in processed_lines:
            f.write(line)

retrieve_debug()