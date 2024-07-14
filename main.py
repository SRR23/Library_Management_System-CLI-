
ALL_BOOKS_FILE = 'all_books.txt'
ALL_LENT_BOOKS_FILE = 'lent_book_details.txt'


def library():

    with open(ALL_BOOKS_FILE, 'r') as file:
        lines = file.readlines()
        books = []
        for line in lines:
            title, authors, isbn, year, price, quantity = line.strip().split('|')
            books.append({
                'title': title,
                'authors': authors.split(','),
                'isbn': isbn,
                'year': int(year),
                'price': float(price),
                'quantity': int(quantity)
            })
        return books
    

def save_books(books):
    with open(ALL_BOOKS_FILE, 'w') as file:
        for book in books:
            line = f"{book['title']}|{','.join(book['authors'])}|{book['isbn']}|{book['year']}|{book['price']}|{book['quantity']}\n"
            file.write(line)


def add_book(title, authors, isbn, year, price, quantity):
    try:
        books = library()
        price = float(price)
        quantity = int(quantity)
        new_book = {
            'title': title,
            'authors': authors,
            'isbn': isbn,
            'year': int(year),
            'price': price,
            'quantity': quantity
        }
        books.append(new_book)
        save_books(books)
    except ValueError:
        print("Error: Price must be a floating number and quantity must be an integer.")


def view_books():
    books = library()
    header_row = f"{'Title':<30} {'Authors':<30} {'ISBN':^17} {'Year':^6} {'Price':^8} {'Quantity':^8}"
    print(header_row)
    print("-" * len(header_row))

    
    for book in books:
        authors_string = ', '.join(book['authors'])
        formatted_row = f"{book['title']:<30} {authors_string:<30} {book['isbn']:^17} {book['year']:^6} {book['price']:^8.2f} {book['quantity']:^8}"
        print(formatted_row)


def search_books_by_title_or_isbn():
    term = input("Enter search term (title or ISBN): ")
    print(f"Search Results for: {term}")
    books = library()
    header_row = f"{'Title':<30} {'Authors':<30} {'ISBN':^17} {'Year':^6} {'Price':^8} {'Quantity':^8}"
    print(header_row)
    print("-" * len(header_row))
    results = [book for book in books if term.lower() in book['title'].lower() or term.lower() in book['isbn']]
    for book in results:
        authors_string = ', '.join(book['authors'])
        formatted_row = f"{book['title']:<30} {authors_string:<30} {book['isbn']:^17} {book['year']:^6} {book['price']:^8.2f} {book['quantity']:^8}"
        print(formatted_row)
        
    

def search_books_by_author():
    author = input("Enter author name: ")
    print(f"Search Results for: {author}")
    books = library()
    header_row = f"{'Title':<30} {'Authors':<30} {'ISBN':^17} {'Year':^6} {'Price':^8} {'Quantity':^8}"
    print(header_row)
    print("-" * len(header_row))
    results = [book for book in books if any(author.lower() in a.lower() for a in book['authors'])]
    for book in results:
        authors_string = ', '.join(book['authors'])
        formatted_row = f"{book['title']:<30} {authors_string:<30} {book['isbn']:^17} {book['year']:^6} {book['price']:^8.2f} {book['quantity']:^8}"
        print(formatted_row)
        


def remove_book():
    term = input("Enter title or ISBN of the book to remove: ")
    books = library()
    book_to_remove = next((book for book in books if term.lower() in book['title'].lower() or term.lower() in book['isbn']), None)
    if book_to_remove:
        books.remove(book_to_remove)
        save_books(books)
        print("Book removed successfully.")
    else:
        print("Error: Book not found.")


def get_multiple_authors():
  
    authors_input = input("Enter the book's authors (separated by commas): ")
    authors = authors_input.strip().split(",")
    return [author.strip() for author in authors] 


def lent_books_section_in_library():

    with open(ALL_LENT_BOOKS_FILE, 'r') as file:
        lines = file.readlines()
        lent_books = []
        for line in lines:
            title, authors, isbn, borrower = line.strip().split('|')
            lent_books.append({
                'title': title,
                'authors': authors.split(','),
                'isbn': isbn,
                'borrower': borrower
            })
        return lent_books
    

def save_lent_books(lent_books):
    with open(ALL_LENT_BOOKS_FILE, 'w') as file:
        for entry in lent_books:
            line = f"{entry['title']}|{','.join(entry['authors'])}|{entry['isbn']}|{entry['borrower']}\n"
            file.write(line)


def lend_book():
    term = input("Enter title or ISBN of the book to lend: ")
    borrower = input("Enter borrower's name: ")
    books = library()
    lent_books = lent_books_section_in_library()
    book_to_lend = next((book for book in books if term.lower() in book['title'].lower() or term.lower() in book['isbn']), None)
    if book_to_lend:
        if book_to_lend['quantity'] > 0:
            book_to_lend['quantity'] -= 1
            lent_books.append({'title': book_to_lend['title'], 'authors': book_to_lend['authors'], 'isbn': book_to_lend['isbn'], 'borrower': borrower})
            save_books(books)
            save_lent_books(lent_books)
            print("Book lent successfully.")
        else:
            print("Error: Not enough books available to lend.")
    else:
        print("Error: Book not found.")
        
        

def view_lent_books():
    lent_books = lent_books_section_in_library()
    header_row = f"{'Title':<30} {'Authors':<30} {'ISBN':^17} {'Borrower':<30}"
    print(header_row)
    print("-" * len(header_row))
    for book in lent_books:
        authors_string = ', '.join(book['authors'])
        borrower_string = book['borrower']
        formatted_row = f"{book['title']:<30} {authors_string:<30} {book['isbn']:^17} {borrower_string:<30}"
        print(formatted_row)



def return_book():
    term = input("Enter title or ISBN of the book to return: ")
    borrower = input("Enter borrower's name: ")
    books = library()
    lent_books = lent_books_section_in_library()
    lent_book_entry = next((entry for entry in lent_books if (term.lower() in entry['title'].lower() or term.lower() in entry['isbn']) and entry['borrower'] == borrower), None)
    if lent_book_entry:
        lent_books.remove(lent_book_entry)
        for book in books:
            if book['isbn'] == lent_book_entry['isbn']:
                book['quantity'] += 1
                save_books(books)
                save_lent_books(lent_books)
                print("Book returned successfully.")
                break
    else:
        print("Error: Lent book not found for the given borrower.")
            


def main_menu():
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. View All Books")
        print("3. Search Books by Title/ISBN")
        print("4. Search Books by Author")
        print("5. Remove Book")
        print("6. Lend Book")
        print("7. View Lent Books")
        print("8. Return Book")
        print("9. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter books title: ")
            authors = get_multiple_authors()
            isbn = input("Enter books ISBN number: ")
            year = input("Enter books publishing year: ")
            price = input("Enter books price: ")
            quantity = input("Enter books quantity: ")
            add_book(title, authors, isbn, year, price, quantity)
        elif choice == '2':
            print("All Book Lists: ")
            view_books()
        elif choice == '3':
            search_books_by_title_or_isbn()
        elif choice == '4':
            search_books_by_author()
        elif choice == '5':
            remove_book()
        elif choice == '6':
            lend_book()
        elif choice == '7':
            print("All lent books information: ")
            view_lent_books()
        elif choice == '8':
            return_book()
        elif choice == '9':
            print("Thank you for using our service. see you again!")
            break
        else:
            print("Invalid choice. Please try again.")
            

if __name__ == "__main__":
    main_menu()