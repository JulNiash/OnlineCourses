import os
from email.policy import default

from django_seed import Seed
from faker import Faker

from django.conf import settings
from django.core.management.base import BaseCommand

from courses.models import CoursePart, CourseTopic, Course, TopicDocument



class Command(BaseCommand):
    help = "Seed data for the online course"

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help="Number of records to create")

        parser.add_argument('--delete', action='store_true', help="Set this flat to true")

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        delete = kwargs['delete']

        if delete:
            Course.objects.all().delete()
            CoursePart.objects.all().delete()
            CourseTopic.objects.all().delete()
            TopicDocument.objects.all().delete()

            path = os.path.join(settings.MEDIA_ROOT, 'topic_documents')

            for file in os.listdir(path):
                os.remove(os.path.join(path, file))


            print('Flushed all models')
            return

        settings.USE_TZ = False
        print("Seed data by Seeder")
        seeder = Seed.seeder()

        print('Seeding courses')
        seeder.add_entity(Course, count, {
            'title': lambda x: seeder.faker.sentence(),
            'description': lambda x: seeder.faker.text(),
            'deleted_at': None
            }
        )

        print('Seeding course parts')
        seeder.add_entity(CoursePart, count, {
            'course': lambda x: Course.objects.order_by('?').first(),  # исправлено 'Course' -> 'course'
            'title': lambda x: seeder.faker.sentence(),
            'deleted_at': None
        })

        print('Seeding course topics')
        seeder.add_entity(CourseTopic, count, {
            'part': lambda x: CoursePart.objects.order_by('?').first(),
            'title': lambda x: seeder.faker.sentence(),
            'deleted_at': None
            }
        )
        seeder.execute()
        settings.USE_TZ = True
