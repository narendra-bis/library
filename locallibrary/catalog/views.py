from django.shortcuts import render
from django.http import HttpResponse

from catalog.models import Book, BookInstance, Author


from django.views.generic import ListView, DetailView

# Create your views here.

def index(request):
	# return HttpResponse('<h1>Welcome</h1>')
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()
	num_authors = Author.objects.count()
	# Get a session value, setting a default if it is not present
	num_visits = request.session.get('num_visits',0)
	request.session['num_visits'] = num_visits + 1

	context={
	'num_books':num_books,
	'num_instances':num_instances,
	'num_instances_available':num_instances_available,
	'num_authors':num_authors,
	'num_visits':num_visits,

	}
	return render(request,'index.html',context=context)



class BookListView(ListView):	
	model = Book
	context_object_name ='my_book_list'
	# your own name for the list as a template variable
	queryset = Book.objects.all()
	paginate_by = 10
	# queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing the title war
	template_name = 'my_book_list.html'  # Specify your own template name/location


class BookDetailView(DetailView):
	print('check detail')
	model = Book
	context_object_name ='bookdetail'	
	queryset = Book.objects.all()
	
	template_name = 'book_detail.html'  # Specify your own template name/location



class AuthorListView(ListView):
	queryset = Author.objects.all()
	context_object_name='author'
	template_name = 'author_list.html'
	
	def get_context_data(self, **kwargs):
		context = super(AuthorListView, self).get_context_data(**kwargs)
		context['bk']=Book.objects.all()
		return context


class AuthorDetailView(DetailView):
	model = Author
	context_object_name ='authordetail'
	queryset = Author.objects.all()
	template_name = 'author_detail.html'


	def get_context_data(self, **kwargs):
		context = super(AuthorDetailView, self).get_context_data(**kwargs)
		context['book'] = Book.objects.filter(author=self.author_name)
		return context
	