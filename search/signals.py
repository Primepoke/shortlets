from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from accounts.models import User
from property.models import Property

from .document import PropertyDocument, UserDocument  # Assuming this is your Elasticsearch document

@receiver(post_save, sender=Property)
@receiver(post_delete, sender=Property)
def update_property_index(sender, instance, **kwargs):
    PropertyDocument().update(instance)



@receiver(post_save, sender=User)
@receiver(post_delete, sender=User)
def update_user_index(sender, instance, **kwargs):
    UserDocument().update(instance)

# @receiver(post_save, sender=Property)
# def update_property_index_on_save(sender, instance, **kwargs):
#     PropertyDocument().update(instance)

# @receiver(post_delete, sender=Property)
# def delete_property_index_on_delete(sender, instance, **kwargs):
#     PropertyDocument().remove(instance)

# @receiver(post_save, sender=User)
# def update_user_index_on_save(sender, instance, **kwargs):
#     UserDocument().update(instance)

# @receiver(post_delete, sender=User)
# def delete_user_index_on_delete(sender, instance, **kwargs):
#     UserDocument().remove(instance)