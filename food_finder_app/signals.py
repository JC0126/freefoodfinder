from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

#https://stackoverflow.com/questions/51974276/how-to-automatically-add-group-and-staff-permissions-when-user-is-created
@receiver(post_save, sender=User)
def post_save_user_signal_handler(sender, instance, created, **kwargs):
    if created:
        if instance.email.endswith('cs3240.super@gmail.com'):
            group = Group.objects.get(name='Admins')
            print(group)
            instance.groups.add(group)
            instance.save()