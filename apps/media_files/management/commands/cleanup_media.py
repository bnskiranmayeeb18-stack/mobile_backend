from django.core.management.base import BaseCommand
from apps.media_files.models import MediaFile
import os

class Command(BaseCommand):
    help = 'Cleanup orphan media files'
    def handle(self, *args, **options):
        count=0
        for media in MediaFile.objects.all():
            try:
                if not media.file or not os.path.exists(media.file.path):
                    self.stdout.write(f"Cleaning missing file {media.id}")
                    media.delete()
                    count+=1
            except Exception as e:
                self.stdout.write(f"Error {media.id}: {e}")
        self.stdout.write(self.style.SUCCESS(f"Cleanup done - removed {count} orphans"))
