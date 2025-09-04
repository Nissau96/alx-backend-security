from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP
import ipaddress

class Command(BaseCommand):
    help = 'Block an IP address by adding it to the BlockedIP model'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='The IP address to block')
        parser.add_argument('--reason', type=str, help='An optional reason for blocking the IP.')

    def handle(self, *args, **options):
        ip_address = options['ip_address']
        reason = options['reason']

        try:
            ipaddress.ip_address(ip_address)
        except ValueError:
            raise CommandError(f'Error: "{ip_address}" is not a valid IP address. IP address is required.')



        # Create or get (but since unique, it will raise if duplicate)
        _, created = BlockedIP.objects.get_or_create(
            ip_address=ip_address,
            defaults={'reason': reason}
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully blocked IP: {ip_address}'))
        else:
            self.stdout.write(self.style.WARNING(f'IP {ip_address} was already blocked.'))