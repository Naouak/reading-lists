from django.core.management import BaseCommand
from oauth2_provider.models import Application

class Command(BaseCommand):
    help = 'setup environment'

    def handle(self, *args, **options):
        frontend_url = input('Please input the frontend url(without the trailing slash):')
        redirect_uris = frontend_url+'/login'
        app = Application(name='frontend',redirect_uris=redirect_uris,client_type='public', authorization_grant_type='implicit')
        app.save()

        self.stdout.write(self.style.SUCCESS('Your oauth2 client id:\n%s' % app.client_id))
        self.stdout.write(self.style.SUCCESS('You will need to provide it to your frontend config to be able to connect to the API.'))

        pass