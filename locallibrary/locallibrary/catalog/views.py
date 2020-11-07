from django.shortcuts import render
from catalog.models import Book, Author, BookInstance
from django.views import generic
#test
#homework
def index(request):
    """View function for home page of site."""
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
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
        'num_visits': num_visits
    }
    return render(request, 'catalog/index.html', context=context)
# Create your views here.

# def books(request):
#     book_list_all = Book.objects.all()
#     return render(request, 'catalog/books.html', {
#         'book_list': book_list_all
#     })
# def book_details(request, id):
#     book = Book.objects.get(id=id)
#     return render(request, 'catalog/book_detail.html', {
#         'book': book
#     })

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2

class BookDetailView(generic.DetailView):
    model = Book
    def book_detail_view(request, primary_key):
        try:
            book = Book.objects.get(pk=primary_key)
        except Book.DoesNotExist:
            raise Http404('Book does not exist')
        
        return render(request, 'catalog/book_detail.html', context={'book': book})

class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author

# class BookListView(generic.ListView):
#     model = Book
#     paginate_by = 2
#     # context_object_name = 'book_list'   # ваше собственное имя переменной контекста в шаблоне
#     # queryset = Book.objects.filter(title__icontains='war')[:5] # Получение 5 книг, содержащих слово 'war' в заголовке
#     # template_name = 'catalog/books.html'  # Определение имени вашего шаблона и его расположения
#     # def get_queryset(self):
#     #     return Book.objects.filter(title__icontains='war')[:5] # Получить 5 книг, содержащих 'war' в заголовке

# class BookDetailView(generic.DetailView):
#     model = Book
#     def book_detail_view(request,pk):
#         try:
#             book_id=Book.objects.get(pk=pk)
#         except Book.DoesNotExist:
#             raise Http404("Book does not exist")

#         #book_id=get_object_or_404(Book, pk=pk)
        
#         return render(
#             request,
#             'catalog/book_detail.html',
#             context={'book':book_id,}
#         )
# class AuthorListView(generic.ListView):
#     model = Author

# class AuthorDetailView(generic.DetailView):
#     model = Author
#     def author_detail_view(request,pk):
#         try:
#             author_id=Author.objects.get(pk=pk)
#         except Author.DoesNotExist:
#             raise Http404("Book does not exist")

#         #book_id=get_object_or_404(Book, pk=pk)
        
#         return render(
#             request,
#             'catalog/author_detail.html',
#             context={'author':author_id,}
#         )
#     template_name = 'catalog/author_detail.html'    
