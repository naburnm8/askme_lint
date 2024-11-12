import random
from datetime import datetime


from django.core.management import BaseCommand

from app.models import AnswerLike, Answer, Profile


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        print('Started at:', datetime.now())
        ratio = options['ratio']
        answers = Answer.objects
        answers_lst = answers.get()
        profiles = Profile.objects
        likes_size = ratio * 200
        answer_ids = list(answers.values_list('pk', flat=True))
        profile_ids = list(profiles.values_list('pk', flat=True))
        pair_count = likes_size // 2
        shuffled_answer_ids = random.sample(answer_ids, pair_count)
        shuffled_profile_ids = random.sample(profile_ids, pair_count)
        unique_pairs = set(zip(shuffled_answer_ids, shuffled_profile_ids))
        likes_count = {a_id: 0 for a_id in answer_ids}
        answer_likes = []

        for answer_id, author_id in unique_pairs:
            like = random.randint(0, 1)
            if like == 1:
                likes_count[answer_id] += 1

            answer_likes.append(
                AnswerLike(
                    author_id=author_id,
                    answer_id=answer_id,
                    like=like
                )
            )
        for answer in answers_lst:
            answer.likes += likes_count.get(answer.pk, 0)
        Answer.objects.bulk_update(answers_lst, ['likes'])
        AnswerLike.objects.bulk_create(answer_likes)
        print('Finished at:', datetime.now())