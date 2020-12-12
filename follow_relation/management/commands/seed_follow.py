import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from follow_relation import models as follow_models
from users import models as user_models


class Command(BaseCommand):

    help = " 팔로우를 생성하는 커맨드 입니다"

    def add_arguments(self, parser):
        parser.add_argument("--number",
                            default=1,
                            type=int,
                            help="생성 하고싶은 팔로우의 수")

        # 먼저 parser 에 argument를 추가해줘야 한다

    def handle(self, *args, **options):
        number = options.get("number", 1)
        seeder = Seed.seeder()
        follower = user_models.User.objects.all()
        followee = user_models.User.objects.all()

        seeder.add_entity(
            follow_models.FollowRelation,
            number,
            {
                "follower": lambda x: random.choice(follower),
            },
        )

        created = seeder.execute()

        cleaned = flatten(list(created.values()))

        # 생성된 리스트의 pk 값을 가져 올수 있다

        for pk in cleaned:
            follow_model = follow_models.FollowRelation.objects.get(pk=pk)
            random_user = followee[random.randint(1, 5):random.randint(6, 30)]
            follow_model.followee.add(*random_user)
            # *이 붙은 이유는 배열안의 요소들을 전부 집어넣기 위함이다

        self.stdout.write(self.style.SUCCESS(f"{number}개의 팔로우 생성!"))
