from django.shortcuts import render
from catalog.models import Book, Author, BookInstance
#test
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }
    return render(request, 'catalog/index.html', context=context)
# Create your views here.

def books(request):
    book_list = Book.objects.all()
    return render(request, 'catalog/books.html', {
        'book_list': book_list
    })
def book_details(request, id):
    book = Book.objects.get(id=id)
    return render(request, 'catalog/book_detail.html', {
        'book': book
    })