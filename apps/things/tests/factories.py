import factory
import faker

from ..models import Thing


fake = faker.Faker()


class ThingFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("file_name")

    class Meta:
        model = Thing
