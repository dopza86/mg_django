import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from posts import models as post_models
from users import models as user_models


class Command(BaseCommand):

    help = "포스트를 생성하는 커맨드 입니다"

    def add_arguments(self, parser):
        parser.add_argument("--number",
                            default=1,
                            type=int,
                            help="생성 하고싶은 포스트 수")

        # 먼저 parser 에 argument를 추가해줘야 한다

    def handle(self, *args, **options):
        number = options.get("number", 1)
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()

        seeder.add_entity(
            post_models.Post,
            number,
            {
                "name": lambda x: seeder.faker.street_address(),
                "location": lambda x: seeder.faker.country(),
                "caption": lambda x: seeder.faker.street_suffix(),
                "user": lambda x: random.choice(all_users),
            },
        )

        created_posts = seeder.execute()
        created_clean = flatten(list(created_posts.values()))

        for pk in created_clean:
            post = post_models.Post.objects.get(pk=pk)
            for i in range(1, random.randint(3, 6)):
                post_models.Photo.objects.create(
                    post=post,
                    file=f"post_photos/{random.randint(1, 31)}.webp",
                )

        self.stdout.write(self.style.SUCCESS(f"{number} 개의 포스트 생성!"))
