from __future__ import print_function
from pathlib import Path
import gutenbergpy.textget
from gutenbergpy.gutenbergcache import GutenbergCache


def init():
    # create cache from scratchfrom scratch
    GutenbergCache.create(refresh=True, download=True, unpack=True, parse=True, cache=True, deleteTemp=True)
    # get the default cache (SQLite)
    cache = GutenbergCache.get_cache()
    # For the query function you can use the following fields: languages authors types titles subjects publishers bookshelves
    #print(len(cache.query(downloadtype=['text/plain'], languages=['en'])))
    #print(cache.query(books=['2638']))

    # Print stripped text


def query():

    object = gutenbergpy.textget.strip_headers(gutenbergpy.textget.get_text_by_id(2638))
    object = object.decode("utf-8") 
    object = str(object)
    
    #print("tipo do obj:" ,type(object))

    with open("aiai.txt", 'w', encoding="utf-8") as f:
        f.write(object)

def teste_query():

    GutenbergCache.create(refresh=True, 
                            download=True, 
                            unpack=True, 
                            parse=True, 
                            cache=True, 
                            deleteTemp=True)
    # get the default cache (SQLite)
    cache = GutenbergCache.get_cache()
    # For the query function you can use the following fields: languages authors types titles subjects publishers bookshelves
    #print(cache.query(subjects=['Science fiction']))
    print(type(cache.query(languages=['en'])))
    # Print stripped text


def init_cache():
    # create cache from scratchfrom scratch
    GutenbergCache.create(refresh=True, download=True, unpack=True, parse=True, cache=True, deleteTemp=True)
    # get the default cache (SQLite)
    cache = GutenbergCache.get_cache()
    # For the query function you can use the following fields: languages authors types titles subjects publishers bookshelves
    print(cache.query)
    # Print stripped text


def english_books():
    # create cache from scratchfrom scratch
    GutenbergCache.create(refresh=True, download=True, unpack=True, parse=True, cache=True, deleteTemp=True)
    # get the default cache (SQLite)
    cache = GutenbergCache.get_cache()
    # For the query function you can use the following fields: languages authors types titles subjects publishers bookshelves
    all_english_books = cache.query(downloadtype=['text/plain'], languages=['en'])
    # Print stripped text

    return all_english_books

def create_folder(all_english_books_ids):

    count = 0

    english_books_folder = Path.cwd().joinpath('english')

    p = Path("english")
    p.mkdir(parents=True, exist_ok=True)
    processed_path = Path("processados.txt")
    already_processed_files = set()
    if processed_path.is_file():
        already_processed_files = processed_path.read_text().rstrip().lstrip().split(sep="\n")
        already_processed_files = set([int(file_id) for file_id in already_processed_files])
        #print(processed_files)

    failed_files = []

    for current_book, book_id in enumerate(all_english_books_ids):
        print(f"Progress: {current_book + 1} / {len(all_books_english_books)}")
        if book_id in already_processed_files:
            continue

        count += 1
        try:
            book_content = gutenbergpy.textget.strip_headers(gutenbergpy.textget.get_text_by_id(book_id))
        except:
            print(f"ERROR: Failed to retrieve book with id {book_id}")
            failed_files.append(book_id)
            continue

        book_content = book_content.decode("utf-8") 
        book_content = str(book_content)

        book_id = str(book_id)
        
        file_path = Path(p, f"{book_id}.txt")

        with open(file_path, 'w', encoding="utf-8") as f:
            f.write(book_content)

        f.close()

        with open("processados.txt", 'a+', encoding="utf-8") as f:
            id_processado = book_id + "\n"
            f.write(id_processado)

        f.close()

        if count > 20000:
            break
    
    with open("failed_files.txt", "a+", encoding="utf-8") as f:
        if not failed_files:
            print(f"No failed files", file=f)
        else:
            for failed_file in failed_files:
                print(f"{failed_file}", file=f)

if __name__ == '__main__':

    init()

    all_books_english_books = english_books()

    all_books_english_books = str(all_books_english_books)
    all_books_english_books = all_books_english_books.strip("[")
    all_books_english_books = all_books_english_books.strip("]")
    all_books_english_books = all_books_english_books.split(", ")

    processed_ids = []

    for id in all_books_english_books:
        id = int(id)
        processed_ids.append(id)

    print(processed_ids[1])
    print(type(processed_ids[1]))

    create_folder(processed_ids)