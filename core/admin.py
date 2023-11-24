from django.contrib import admin
from .models import *

admin.site.register(ThreadsContent)
admin.site.register(LikesFor_Main_Post)
admin.site.register(Profile)
admin.site.register(FollowersManager)
admin.site.register(Replies)
admin.site.register(Likes_for_Replies)
admin.site.register(SubReplies)
admin.site.register(Likes_for_SubReplies)
