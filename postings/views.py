import json, re

from django import views
from user.models import Account
from django.utils import timezone
# from django.utils.timezone import localtime

from django.views import View
from django.http  import JsonResponse
#from django.core.exceptions import ObjectDoesNotExist, ValidationError

# 외래키 사용시 무조건 가져옴
from postings.models import Comment, Posting, Like
# from user.models import Account

### 포스팅 기능
class PostingView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            IMG_URL_REGES = "^(https?):\/\/([^:\/\s]+)(:([^\/]*))?((\/[^\s/\/]+)*)?\/([^#\s\?]*)(\?([^#\s]*))?(#(\w*))?$"

            if not re.search(IMG_URL_REGES, data['img_url']):
                return JsonResponse({"MESSAGE":"URL VALIDATION"}, status=400)
    
            Posting.objects.create (
                user_id        = data['user'],
                post           = data['post'],
                content        = data['content'],
                img_url        = data['img_url'],
                created_at = timezone.localtime()
            )
            return JsonResponse({"MESSAGE":"SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({'MESSSAGE':"KEY_ERROR"}, status=400)
        except ValueError:
            return JsonResponse({"MESSAGE":"INVALID_USER"}, status=400)

    def get(self, request):

        postings = Posting.objects.all()
        result = []
        for posting in postings:
            result.append({
            'name'       : posting.user.name,
            'post'       : posting.post,
            'content'    : posting.content,
            'created_at' : posting.created_at,
            'img_url'    : posting.img_url,
            })

        return JsonResponse({"MESSAGE":result}, status=200)

### 게시물 수정 기능
    def patch(self, request):
        try:
            data = json.loads(request.body)
            user = Account.objects.get(pk=data['user'])
            post = Posting.objects.get(pk=data['post'])

            if not user.name == post.user.name:
                return JsonResponse({"MESSAGE":"INVALID_USER"}, status=401)

            # pk처럼 숫자로 받으려면 user_id=data['user']로 써야함
            Posting.objects.filter(pk=data['post'], user=user).update(
                content = data['content'],
            )
            return JsonResponse({'MESSAGE':'UPDATED'}, status=200)
        except Posting.DoesNotExist:
            return JsonResponse({'MESSAGE':"You can't revise it"}, status=400)
            
### 댓글 기능
class CommentView(View):
    def post(self, request):
        data = json.loads(request.body)

        # pk(외래키로 불러왔으니 pk=data['']을 해야함)
        # 숫자로 불러왔다면 create하는 부분에서 user_id 처럼 불러와야함
        user = Account.objects.get(pk=data['user'])
        post = Posting.objects.get(pk=data['post'])

        try:
            Comment.objects.create (
                user        = user,#user_id = user(숫자였다면)
                post        = post,
                comment     = data['comment'],
                re_comment_id  = data['re_comment'] # re_comment_id는 comment의 id 값인 것이다.
            )
            return JsonResponse({'MESSAGE':'UPLOADED'}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE':'UPLOAD ERROR'}, status=400)

    def get(self, request):
        # data = json.loads(request.body)

        comments = Comment.objects.all()
        result=[]
        
        for comment in comments:
            result.append(
                {
                'name'      : comment.user_id,
                'post'      : comment.post_id,
                'comment'   : comment.comment,
                're_comment': comment.re_comment,
                }
            )
        return JsonResponse({"RESULT":result, "MESSAGE":"SUCCESS"}, status=200)

### 댓글 삭제 기능 - delete method는 보안상의 이유로 쓰지않기 때문에 
class CommentDeleteView(View):
    def post(self,request):
        data = json.loads(request.body)
        if Comment.objects.filter(user_id=data["user"], pk=data["pk"]).exists():
            Comment.objects.get(user_id=data["user"], pk=data["pk"]).delete()
            return JsonResponse({"MESSAGE":"SUCCESS"}, status = 200)
        else:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status = 400)        

#### 좋아요 기능
class LikeView(View):
    def post(self, request):
        data = json.loads(request.body)

        user = Account.objects.get(pk=data['user'])
        post = Posting.objects.get(pk=data['post'])
        try:
            # 같은 유저가 같은 게시물에 좋아요를 2번 누를 때 좋아요 삭제
            if Like.objects.filter(user=user, post=post).exists():
                Like.objects.filter(user=user, post=post).delete()

            Like.objects.create(
                user = user,
                post = post,
            )

            # 좋아요 힙계
            like_count = Like.objects.filter(post=post).count()
            return JsonResponse({'message': 'SUCCESS', 'like_count': like_count}, status=200)
        except KeyError:
            return JsonResponse({"MESSAGE":"ERROR"}, status=400)

    def get(self, request):

        likes = Like.objects.all()

        try:
            result=[]
            for like in likes:
                result.append(
                    {
                    'name'      : like.user_id,
                    'post'      : like.post_id,
                    }
                )
            return JsonResponse({"RESULT":result, "MESSAGE":"SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"MESSAGE":"ERROR"}, status=400)
