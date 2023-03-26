# cria todos 

from pathlib import Path
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize



def read_and_clean_file(filename):

    stop_words = set(stopwords.words('english'))
    count = 0

    processed_lines = []

    with open(filename, 'r', encoding="utf-8") as f:

        check_start_book = False
        
        for line in f:

            if line != "":

                line = line.lower()
                check_valid_line = line.split()
                check_valid_line = check_valid_line[:6]
                check_valid_line = ' '.join(check_valid_line)

                # removendo cabeçalhos e índices:
                if '*** start of the project gutenberg' == check_valid_line:
                    check_start_book = True
                
                if '* * * start of the project gutenberg' == check_valid_line:
                    
                    check_start_book = True

                if not check_start_book:
                    continue 


                tokens = word_tokenize(line)

                filtered_tokens = [token for token in tokens if not token.lower() in stop_words]

                processed_line = (" ".join(filtered_tokens))


                processed_lines.append(processed_line)

                # removendo apêndices e licenças ao final do arquivo:

                if '*** end of the project gutenberg' == check_valid_line:
                    break

                if '* * * end of the project gutenberg' == check_valid_line:
                    break


    return processed_lines





def create_dataset_files(processed_lines, author_folder, filename):

    author_folder = str(author_folder)

    p = Path("gutenberg_dataset", author_folder)
    p.mkdir(parents=True, exist_ok=True)

    file_path = Path(p, filename)
    file_path.touch(exist_ok=True)

    with open(file_path, 'w', encoding="utf-8") as f:
        
        for line in processed_lines:
            f.write(line)


def generate_processed_dataset_Gutenberg():

    #books_folder = Path.cwd().joinpath('books')
    books_folder = Path.cwd().joinpath('english')

    p = Path("gutenberg_dataset")
    p.mkdir(parents=True, exist_ok=True)


    for author_folder in books_folder.iterdir():

        all_books = []
        author_name = str(author_folder)
        author_name = author_name.split("/")
        author_name = author_name[-1:]

        author_books = []

        for book_file in author_folder.iterdir():
            author_books.append(book_file)

        all_books.append(author_books)


        for author in all_books:
            
            path_name = str(author_folder)
            path_name = path_name.split("/")
            author_name = path_name[-1]

            for file in author:

                filename = str(file)
                filename = filename.split("/")
                filename = filename[-1]
   
                processed_lines = read_and_clean_file(file)
                create_dataset_files(processed_lines, author_name, filename)

if __name__ == '__main__':

    generate_processed_dataset_Gutenberg()