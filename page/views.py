from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect

from page.forms import BookForm
from page.models import BookModel


@login_required
@permission_required('library.view_book', raise_exception=True)
def book_list(request):
    book = BookModel.objects.all()
    return render(request, 'book_list.html', {'book': book})

@login_required
@permission_required('library.add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')

    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

@login_required
@permission_required('library.change_book', raise_exception=True)
def edit_book(request, book_id):
    book = BookModel.objects.get(BookModel, id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form': form})


@login_required
@permission_required('library.delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = BookModel.objects.get(BookModel, id=id)
    book.delete()
    return redirect('book_list')
