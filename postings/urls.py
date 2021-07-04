from django.urls            import path
from postings.views         import CommentDeleteView, LikeView, PostingView,CommentView

urlpatterns =[
    path('/posting',PostingView.as_view()),
    path('/comment',CommentView.as_view()),
    path('/like',LikeView.as_view()),
    path('/commentdelete', CommentDeleteView.as_view())
]