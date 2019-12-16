from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
# Create your views here.
from .forms import TestForm, QuestionForm, AnswerForm, CommentForm
from .models import Question, Test, Answer, User, TestUserList, Comment


def parting(xs, parts=4):
    return [xs[d:d + 4] for d in range(0, len(xs), 4)]


def index(request):
    if request.user.is_authenticated:
        return redirect('tests')
    return redirect('login')


class TestView(View):
    def get(self, request, id):
        context = {}
        test = get_object_or_404(Test, id=id)
        user = request.user
        passed_times = TestUserList.objects.filter(test=test)
        context['passed_times'] = len(passed_times)
        context['passed'] = passed_times
        context['test'] = test
        context['user'] = user
        comment_form = CommentForm()
        context['comment_form'] = comment_form
        context['comments'] = Comment.objects.filter(test=test)
        return render(request, 'mytests/test_view.html', context)

    def post(self, request, id):
        context = {}
        test = get_object_or_404(Test, id=id)
        user = request.user
        comment = CommentForm(request.POST)
        comments = Comment.objects.filter(test=test)
        if comment.is_valid():
            new = comment.save(commit=False)
            new.body = comment.cleaned_data.get('body')
            new.author = user
            new.test = test
            new.save()

        context['test'] = test
        context['user'] = user
        context['comment_form'] = CommentForm()
        context['comments'] = comments
        return render(request, 'mytests/test_view.html', context)


class TestList(View):
    def get(self, request):
        context = {}

        search = request.GET.get('search', '')
        order = request.GET.get('order', '')

        if order == '' or order == 'date':
            tests = Test.objects.all().order_by('date')
            context['tests'] = tests
        elif order == 'datelast':
            tests = Test.objects.all().order_by('date').reverse()
            context['tests'] = tests
        elif order == 'passed':
            if request.user.is_authenticated:
                tests_users = TestUserList.objects.filter(user=request.user)
                tests = set()
                for i in tests_users:
                    one_test = Test.objects.get(id=i.test.id)
                    tests.add(one_test)
                context['tests'] = tests

            else:
                context['tests'] = Test.objects.all()
        if search:
            tests = Test.objects.filter(title__iexact=search)  # __icontains
            context['tests'] = tests
        if request.user.is_authenticated:
            context['test_users'] = TestUserList.objects.filter(user=request.user)
        return render(request, 'mytests/test_list_view.html', context)


class CreateTest(View):
    def get(self, request):
        context = {}
        test_form = TestForm()
        question_form = QuestionForm()
        answer_form = AnswerForm()
        range_list = range(1, 31)

        context['test_form'] = test_form
        context['question_form'] = question_form
        context['answer_form'] = answer_form
        context['range_list'] = range_list

        return render(request, 'mytests/test_create_view.html', context)

    def post(self, request):
        context = {}
        test_form = TestForm()
        question_form = QuestionForm()
        answer_form = AnswerForm()
        range_list = range(1, 10)

        context['test_form'] = test_form
        context['question_form'] = question_form
        context['answer_form'] = answer_form
        context['range_list'] = range_list
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_verificate:
            return redirect('update')
        author = request.user

        test_parameters = dict(request.POST)
        test_title = test_parameters['title'][0]
        test_description = test_parameters['description'][0]

        test_questions = []
        test_answers = []

        num_questions = 0
        num_answers = 0

        for q in test_parameters['question']:
            if q != '':
                num_questions += 1
                test_questions.append(q)

        parcing_answers = parting(test_parameters['answer'])

        for answ in parcing_answers:
            if answ != ['', '', '', '']:
                num_answers += 1
                test_answers.append(answ)

        for i in range(1, len(test_questions) + 1):
            try:
                if not test_parameters[str(i)]:
                    context['help_error'] = 'Alls question must have true answer'
                    return render(request, 'mytests/test_create_view.html', context)
            except KeyError:
                context['help_error'] = 'Alls question must have true answer'
                return render(request, 'mytests/test_create_view.html', context)

        num_of_q = 0

        if num_questions == num_answers and num_answers >= 5 and num_questions >= 5:  # проверка, что вопросов столько же, сколько и ответов и больше или равно 5
            # создаю тест
            new_test_parametrs = {"title": test_title, 'description': test_description}
            test_form = TestForm(new_test_parametrs, request.FILES)
            if test_form.is_valid():
                new_test = test_form.save(commit=False)
                new_test.author = author
                new_test.title = test_form.cleaned_data['title']
                new_test.description = test_form.cleaned_data['description']
                new_test.save()  # создали новый тест

            for question in test_questions:  # создаем вопросы для теста
                new_q_parametrs = {'question': question}
                q_form = QuestionForm(new_q_parametrs)
                if q_form.is_valid():
                    new_question = q_form.save(commit=False)
                    new_question.question = q_form.cleaned_data["question"]
                    new_question.test_q = new_test

                    new_question.save()

                num_of_a = 0

                for answ in test_answers[num_of_q]:  # заполняем вопросы ответами
                    num_of_a += 1
                    true_answer = test_parameters[str(num_of_q + 1)][0] == str(num_of_a)
                    new_a_parametrs = {'answer': answ, 'is_correctly': true_answer}
                    a_form = AnswerForm(new_a_parametrs)
                    if a_form.is_valid():
                        new_answ = a_form.save(commit=False)
                        new_answ.answer = a_form.cleaned_data['answer']
                        new_answ.test = new_test
                        new_answ.question = new_question
                        new_answ.save()
                num_of_q += 1

        else:
            context['help_error'] = 'Dont 5 questions'
            return render(request, 'mytests/test_create_view.html', context)
        return redirect('run_test', id=new_test.id)


class TestRun(View):
    def get(self, request, id):
        context = {}
        if request.user.is_authenticated:
            test = get_object_or_404(Test, id=id)
            questions = Question.objects.filter(test_q=test)
            answers = Answer.objects.filter(test=test)
            test_compl = TestUserList.objects.filter(test=test, user=request.user).order_by('-date')

            if test_compl:
                context['test_compl'] = test_compl
            context['test'] = test.title
            context['questions'] = questions
            context['answers'] = answers
        else:
            context['help_error'] = 'Must by LogIn'

        return render(request, 'mytests/test_run_view.html', context)

    def post(self, request, id):
        context = {}
        test = get_object_or_404(Test, id=id)
        questions = Question.objects.filter(test_q=test)
        answers_in_procent = 0
        oneh_procent = 0
        for question in questions:
            true_answ = Answer.objects.filter(question=question, is_correctly=True).first()
            user_answer = request.POST.dict().get(question.question)
            if user_answer != None:
                if list(user_answer) == list(true_answ.answer):
                    answers_in_procent += 1
            oneh_procent += 1
        result_in_proc = int((100 / oneh_procent) * answers_in_procent)  # переводим правельные ответы в %
        new = TestUserList(user=request.user, test=test, completed_on=result_in_proc)
        new.save()

        test_copml = TestUserList.objects.filter(test=test, user=request.user).order_by('-date')

        context['test_compl'] = test_copml
        answers = Answer.objects.all()
        # request.POST.dict().get(question.question)
        context['test'] = test.title
        context['questions'] = questions
        context['answers'] = answers

        return redirect('test_detail', id=test.id)
