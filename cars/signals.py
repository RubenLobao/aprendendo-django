from django.db.models.signals import post_save, pre_delete, pre_save, post_delete
from django.dispatch import receiver


@receiver(pre_save, sender='cars.Car')
def car_pre_save(sender, instance, **kwargs):
    print(f'Pre Save Signal: {instance}')

@receiver(post_save, sender='cars.Car')
def car_post_save(sender, instance, created, **kwargs):
    print(f'Post Save Signal: {instance}, Created: {created}')

@receiver(pre_delete, sender='cars.Car')
def car_pre_delete(sender, instance, **kwargs):
    print(f'Pre Delete Signal: {instance}')

@receiver(post_delete, sender='cars.Car')
def car_post_delete(sender, instance, **kwargs):
    print(f'Post Delete Signal: {instance}')