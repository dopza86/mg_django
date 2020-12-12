import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from likes import models as like_models
from posts import models as post_models
from users import models as user_models


class Command(BaseCommand):

    help = " 좋아요를 생성하는 커맨드 입니다"

    def add_arguments(self, parser):
        parser.add_argument("--number",
                            default=1,
                            type=int,
                            help="생성 하고싶은 좋아요의 수")

        # 먼저 parser 에 argument를 추가해줘야 한다

    def handle(self, *args, **options):
        number = options.get("number", 1)
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        posts = post_models.Post.objects.all()

        seeder.add_entity(
            like_models.Like,
            number,
            {
                "post": lambda x: random.choice(posts),
            },
        )

        created = seeder.execute()
        print(seeder)
        cleaned = flatten(list(created.values()))

        # 생성된 리스트의 pk 값을 가져 올수 있다

        for pk in cleaned:
            like_model = like_models.Like.objects.get(pk=pk)
            random_user = users[random.randint(1, 5):random.randint(6, 30)]
            like_model.user.add(*random_user)
            # *이 붙은 이유는 배열안의 요소들을 전부 집어넣기 위함이다

        self.stdout.write(self.style.SUCCESS(f"{number}개의 좋아요 생성!"))
