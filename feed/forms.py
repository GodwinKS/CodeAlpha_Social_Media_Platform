from django import forms
from .models import Post, Comment  # <-- Added Comment here

# ... (Keep your PostForm exactly as it is) ...

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': "What's on your mind?", 'style': 'width: 100%; border-radius: 5px; padding: 10px;'})
        }

# NEW: The Form for writing comments
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': "Write a comment...", 
                'style': 'width: 75%; padding: 8px; border-radius: 4px; border: 1px solid #ccc;'
            })
        }