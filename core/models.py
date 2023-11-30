from django.db import models
from django.contrib.auth.models import User

import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default/default_image.png')
    location = models.CharField(max_length=100, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class ThreadsContent(models.Model):
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content_img = models.ImageField(upload_to='content_images/',  blank=True, null=True)
    content_video = models.FileField(upload_to='content_videos/', blank=True, null=True)
    no_of_likes = models.IntegerField(default=0)
    no_of_comments = models.IntegerField(default=0)

    def __str__(self):
        return self.content[:20]

@receiver(pre_delete, sender=ThreadsContent)
def delete_post_image(sender, instance, **kwargs):
    #Delete the image file when the associated Post instance is deleted    
    if instance.content_img:
        image_path = os.path.join('images/', str(instance.content_img))
        if os.path.isfile(image_path):
            os.remove(image_path)






class LikesFor_Main_Post(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.BooleanField(default=False)
    tweet = models.ForeignKey(ThreadsContent, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.tweet}-{self.value}"


class FollowersManager(models.Model):
    follower = models.ForeignKey(Profile, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(Profile, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower.user.username} follows {self.followed.user.username}"


class Replies(models.Model):
    thread = models.ForeignKey(ThreadsContent, on_delete=models.CASCADE)
    reply = models.TextField(max_length=500, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reply

class Likes_for_Replies(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.BooleanField(default=False)
    likeFor = models.ForeignKey(Replies, on_delete=models.CASCADE)

class SubReplies(models.Model):
    main_reply = models.ForeignKey(Replies, on_delete=models.CASCADE)
    sub_reply = models.TextField(max_length=500, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sub_reply
    
class Likes_for_SubReplies(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.BooleanField(default=False)
    likeFor = models.ForeignKey(SubReplies, on_delete=models.CASCADE)    