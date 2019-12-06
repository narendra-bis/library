from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances

# Create your models here.

class Genre(models.Model):
	name = models.CharField(max_length=200, help_text='Enter a book genre(e.g. Science Fiction)')

	def __str__(self):
		return self.name


class Author(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	date_of_birth = models.DateField(null=True, blank=True)
	date_of_death = models.DateField(null=True, blank=True)

	class Meta:
		ordering = ['last_name', 'first_name']

	def get_absolute_url(self):
		return reverse('author-detail', args = [str(self.id)])


	def __str__(self):
		# return f'{self.last_name} ({self.first_name})'
		return '%s %s' % (self.last_name, self.first_name)





class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name


class Book(models.Model):
	title = models.CharField(max_length=200, help_text='enter the title of book')
	author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
	summary = models.TextField(max_length=1000, help_text='Enter the brief description of the book')
	isbn = models.CharField(max_length=13, help_text='Enter 13 digit <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
	genre = models.ManyToManyField(Genre, help_text='Select a Genre for this book')
	language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('book-detail', args=[str(self.id)])

	def display_genre(self):
		"""Create a string for the Genre. This is required to display genre in Admin."""
		return ', '.join(genre.name for genre in self.genre.all()[:3])

	display_genre.short_description = 'Genre'



class BookInstance(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
	book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
	imprint = models.CharField(max_length=200)
	due_back = models.DateField(null=True, blank=True)
	author =models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

	LOAN_STATUS = (
		('m','Maintanance'),
		('o','On Loan'),
		('a','Available'),
		('r','Reserved'),
		)
	status = models.CharField(max_length=1,choices=LOAN_STATUS, blank=True,default='m', help_text='Book Availibility')

	class Meta:
		ordering = ['due_back']

	def __str__(self):		
		return '%s %s' %(self.id, self.book.title)



