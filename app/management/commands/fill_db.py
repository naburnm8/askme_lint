from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from app.models import Question, Answer, Profile, AnswerLike, QuestionLike, Tag, User
from faker import Faker
import random

fake = Faker()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        print('Started at:', datetime.now())
        ratio = options['ratio']

        tags_size = ratio
        likes_size = ratio * 200
        questions_size = ratio * 10
        profiles_size = ratio
        answers_size = ratio * 100

        usernames = [f'{fake.user_name()}_{i}' for i in range(profiles_size)]
        emails = [f'{username}@mail.ru' for username in usernames]
        users = [User(username=username, email=email, password=fake.password()) for username, email in
                 zip(usernames, emails)]
        User.objects.bulk_create(users)
        users = User.objects.all()[:profiles_size]
        profiles = [Profile(user=user) for user in users]
        Profile.objects.bulk_create(profiles)
        print(f'Done profiles at: {datetime.now()}')

        profiles = Profile.objects
        tags = [Tag(name=f'{fake.word()}{i}') for i in range(tags_size)]
        Tag.objects.bulk_create(tags)
        tags = Tag.objects
        print(f'Done tags at: {datetime.now()}')

        profile_ids = list(profiles.values_list('pk', flat=True))
        tag_ids = list(tags.values_list('pk', flat=True))
        questions_lst = [
            Question(
                title=fake.sentence(nb_words=3),
                content=fake.text(max_nb_chars=512),
                author_id=random.choice(profile_ids),  # Use `author_id` for direct assignment
                likes=0,
                amount_of_answers=0,
                created_at=fake.date_between(datetime(2000, 1, 1), datetime(2024, 12, 31))
            )
            for i in range(questions_size)
        ]
        Question.objects.bulk_create(questions_lst)
        for question in questions_lst:
            selected_tag_ids = random.sample(tag_ids, random.randint(1, 5))
            question.tags.add(*selected_tag_ids)
        questions = Question.objects
        print(f'Done questions at: {datetime.now()}')

        answers_lst = []
        question_ids = list(questions.values_list('pk', flat=True))
        profile_ids = list(profiles.values_list('pk', flat=True))
        for i in range(answers_size):
            question_id = random.choice(question_ids)
            profile_id = random.choice(profile_ids)

            ans = Answer(
                question_id=question_id,
                content=fake.text(max_nb_chars=512),
                author_id=profile_id,
                likes=0,
                created_at=fake.date_between(datetime(2000, 1, 1), datetime(2024, 12, 31))
            )
            questions_lst[question_id - 1].amount_of_answers += 1
            answers_lst.append(ans)

        Question.objects.bulk_update(questions_lst, ['amount_of_answers'])
        Answer.objects.bulk_create(answers_lst)
        answers = Answer.objects
        print(f'Done answers at: {datetime.now()}')
        question_ids = list(questions.values_list('pk', flat=True))
        profile_ids = list(profiles.values_list('pk', flat=True))
        unique_pairs = set()
        while len(unique_pairs) < likes_size // 2:
            pair = (random.choice(question_ids), random.choice(profile_ids))
            unique_pairs.add(pair)
        likes_count = {q_id: 0 for q_id in question_ids}
        question_likes = []
        for question_id, author_id in unique_pairs:
            like = random.randint(0, 1)
            question_like = QuestionLike(
                author_id=author_id,
                question_id=question_id,
                like=like
            )
            if like == 1:
                likes_count[question_id] += 1
            question_likes.append(question_like)
        for question in questions_lst:
            question.likes += likes_count.get(question.pk, 0)
        Question.objects.bulk_update(questions_lst, ['likes'])
        QuestionLike.objects.bulk_create(question_likes)
        print(f'Done Q_Likes at: {datetime.now()}')
        answer_ids = list(answers.values_list('pk', flat=True))
        profile_ids = list(profiles.values_list('pk', flat=True))
        unique_pairs = set()
        while len(unique_pairs) < likes_size // 2:
            pair = (random.choice(answer_ids), random.choice(profile_ids))
            unique_pairs.add(pair)
        likes_count = {a_id: 0 for a_id in answer_ids}
        answer_likes = []
        for answer_id, author_id in unique_pairs:
            like = random.randint(0, 1)
            ans_like = AnswerLike(
                author_id=author_id,
                answer_id=answer_id,
                like=like
            )
            if like == 1:
                likes_count[answer_id] += 1
            answer_likes.append(ans_like)
        for answer in answers_lst:
            answer.likes += likes_count.get(answer.pk, 0)
        Answer.objects.bulk_update(answers_lst, ['likes'])
        AnswerLike.objects.bulk_create(answer_likes)
        print(f'Done A_Likes at: {datetime.now()}')
        print('Ended at:', datetime.now())
