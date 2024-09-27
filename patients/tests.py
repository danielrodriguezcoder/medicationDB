import datetime
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Prescription


# Create your tests here.
def create_question(question_text, days):
    # Create a question with the given `question_text` and published the
    # given number of `days` offset to now (negative for questions published
    # in the past, positive for questions that have yet to be published).
    time = timezone.now() + datetime.timedelta(days=days)
    return Prescription.objects.create(question_text=question_text, pub_date=time)


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        # detail view of a question in the future is 404
        future_question = create_question(question_text="Future question", days=5)
        url = reverse("patients:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        # past questions are displayed
        past_question = create_question(question_text="Past question", days=-5)
        url = reverse("patients:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        # Checks that the text is appropriate when there are no questions
        response = self.client.get(reverse('patients:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No patients are available.')
        self.assertQuerySetEqual(response.context['latest_question_list'],[])

    def test_past_question(self):
        # questions with pub_date in the past are dipslayed
        question = create_question(question_text='Past question', days=-30)
        response = self.client.get(reverse('patients:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'],[question])

    def test_future_question(self):
        # hides questions with pud_date in the future
        create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('patients:index'))
        self.assertContains(response, 'No patients are available.')
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        # tests future and past question showing only past question
        question = create_question(question_text='Past question', days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('patients:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question])

    def test_two_past_question(self):
        # tests returning multiple questions
        question1 = create_question(question_text='Past question 1.', days=-30)
        question2 = create_question(question_text='Past question 2.', days=-5)
        response = self.client.get(reverse('patients:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question2, question1])


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        # test with a question in the future that should be False
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Prescription(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    # test with an old question that should False
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Prescription(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    # test for a valid recent question
    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Prescription(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
