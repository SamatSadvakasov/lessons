from django.shortcuts import render, get_object_or_404
from catalog.models import Book, Author, BookInstance
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm
from catalog.filters import BookFilter
from catalog.serializers import BookModelSerializer
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

@api_view(['GET'])
def book_api(request):
    data = {'success':'ura'}
    return Response(data)

class BookAPIView(generics.ListAPIView):
    serializer_class = BookModelSerializer
    
    def get_queryset(self):

        queryset = Book.objects.all()
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)
        return queryset


class AuthorCreate(LoginRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    #initial={'date_of_death':'12/10/2016',}

class AuthorUpdate(LoginRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']


class AuthorDelete(LoginRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('author')

class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    #initial={'date_of_death':'12/10/2016',}

class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('my-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

#testlkdajsflkasdjflkajsdflkjasdlkfjlaskdjfaskdl;fja;dskfj;asdklfja;sdkfj;daskfja;sdlkjfadksljf;dsf
#homework
@login_required
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

@login_required
def book_views(request):
    books = Book.objects.all()
    book_filter = BookFilter(request.GET, queryset=books)
    return render(request, 'catalog/book_list.html', {'book_list':book_filter})

# class BookListView(LoginRequiredMixin,generic.ListView):
#     model = Book
#     paginate_by = 10

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    def book_detail_view(request, primary_key):
        try:
            book = Book.objects.get(pk=primary_key)
        except Book.DoesNotExist:
            raise Http404('Book does not exist')
        
        return render(request, 'catalog/book_detail.html', context={'book': book})

class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        
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
