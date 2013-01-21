from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from social_auth.models import UserSocialAuth


class Company(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.domain


class Profile(models.Model):
    user = models.OneToOneField(User)
    company = models.ForeignKey(Company, null=True)
    picture = models.ForeignKey(UserSocialAuth, null=True)
    title = models.CharField(max_length=255)
    blog = models.URLField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user.get_full_name()

    @property
    def company_choices(self):
        return Company.objects.filter(domain__in=self.domains)

    @property
    def domains(self):
        if self.user.email:
            return [get_domain(self.user.email)]

    @property
    def possible_accounts(self):
        ''' returns a dict of all possible account types and either None
        or this user's account of that type '''
        #import pdb; pdb.set_trace()
        return dict((provider, self.get_provider_or_none(provider))
            for provider in settings.POSSIBLE_PROVIDERS)

    def get_provider_or_none(self, provider):
        try:
            return self.user.social_auth.get(provider=provider)
        except UserSocialAuth.DoesNotExist:
            return None


def get_domain(email):
    return email.split('@')[1]


@receiver(post_save, sender=User)
def user_post_save(sender, instance, **kwargs):
    Company.objects.get_or_create(domain=get_domain(instance.email))


class Content(models.Model):
    user = models.ForeignKey(User)
    provider = models.CharField(max_length=255)
    link = models.URLField(max_length=1024)
    body = models.TextField()
    date = models.DateTimeField()

    def __unicode__(self):
        return self.link