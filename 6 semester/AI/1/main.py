from pyknow import *

right_answers = ['Да', 'да', 'Нет', 'нет']
dairy = ['Молоко', 'Сыр', 'Творог', 'Йогурт']
dough = ['Из теста']
sweet = ['Фрукты', 'Сладкая еда']
macaroni = ['Макаронные изделия', 'Соус']
spicy = ['Есть лук', 'Есть чеснок', 'Есть перец', 'Большое количество специй']
hearty = ['Мясо', 'Хлеб', 'Крупы']
low_calorie = ['Овощи', 'Курица']
micro_macro = ['Морепродукты', 'Зелень', 'Злаки']
healthy = ['Одобрена ВОЗ']
fork = ['Едят вилкой']
chopsticks = ['Едят палочками']

cutlery = [fork, chopsticks]
libr = [hearty, low_calorie, micro_macro, sweet, macaroni, dairy]


class Food(KnowledgeEngine):
    @Rule(OR(Fact('Овощи'), Fact('Курица')))
    def low_calorie(self):
        self.declare(Fact('Низкое содержание калорий'))

    @Rule(OR(Fact('Творог'), Fact('Сыр'), Fact('Молоко'), Fact('Йогурт')))
    def diary_food(self):
        self.declare(Fact('Молочные продукты'))

    @Rule(AND(Fact('Макаронные изделия'), Fact('Соус')))
    def pasta(self):
        self.declare(Fact('Паста'))

    @Rule(AND(Fact('Макаронные изделия'), Fact('Едят палочками')))
    def asian_macaroni(self):
        self.declare(Fact('Азиатская лапша'))

    @Rule(AND(Fact('Из теста'), OR(Fact('Фрукты'), Fact('Сладкая еда'))))
    def sweet_pie(self):
        self.declare(Fact('Сладкая выпечка'))

    @Rule(AND(Fact('Из теста'), OR(Fact('Мясо'), Fact('Курица'))))
    def pies(self):
        self.declare(Fact('Пироги'))

    @Rule(OR(Fact('Мясо'), Fact('Крупы'), Fact('Хлеб')))
    def hearty_food(self):
        self.declare(Fact('Сытная пища'))

    @Rule(OR(Fact('Есть перец'), Fact('Есть лук'), Fact('Есть чеснок')))
    def spicy(self):
        self.declare(Fact('Острая еда'))

    @Rule(OR(Fact('Низкое содержание калорий'), Fact('Морепродукты'), Fact('Злаки'), Fact('Зелень'),
             Fact('Молочные продукты')))
    def micro_macro(self):
        self.declare(Fact('Богатство микро- и макроэлементов'))

    @Rule(AND(Fact('Сытная пища'), Fact('Большое количество специй')))
    def rich_taste(self):
        self.declare(Fact('Насыщенный вкус'))

    @Rule(OR(Fact('Острая еда'), Fact('Большое количество специй')))
    def rich_taste(self):
        self.declare(Fact('Насыщенный вкус'))

    @Rule(AND(Fact('Пироги'), Fact('Одобрена ВОЗ')))
    def healthy_pies(self):
        self.declare(Fact('Полезные пироги'))

    @Rule(AND(Fact('Пироги'), Fact('Насыщенный вкус')))
    def unhealthy_pies(self):
        self.declare(Fact('Неполезные пироги'))

    @Rule(OR(
        AND(Fact('Одобрена ВОЗ'), Fact('Едят вилкой'), Fact('Богатство микро- и макроэлементов')),
        Fact('Сладкая выпечка'), Fact('Полезные пироги'), Fact('Паста')))
    def mediterranean(self):
        self.declare(Fact(food='Средиземноморская кухня'))

    @Rule(AND(
        OR(
            AND(Fact('Едят вилкой'), OR(Fact('Сытная пища'), Fact('Насыщенный вкус'))),
            Fact('Сладкая выпечка')),
        NOT(Fact('Одобрена ВОЗ'))))
    def american(self):
        self.declare(Fact(food='Американская кухня'))

    @Rule(AND(
        OR(
            Fact('Насыщенный вкус'), Fact('Богатство микро- и макроэлементов'), Fact('Азиатская лапша')),
        NOT(Fact('Одобрена ВОЗ')),
        Fact('Едят палочками')))
    def panAsian(self):
        self.declare(Fact(food='Паназиатская кухня'))

    @Rule(AND(
        OR(
            Fact('Насыщенный вкус'),
            Fact('Неполезные пироги')),
        NOT(Fact('Одобрена ВОЗ')),
        Fact('Едят вилкой')))
    def caucasus(self):
        self.declare(Fact(food='Кавказская кухня'))

    @Rule(Fact(food=MATCH.f))
    def print_result(self, f):
        print(format(f))

    def factz(self, l):
        for x in l:
            self.declare(x)


def put_answers(facts, result_facts):
    for fact_ in facts:
        answer = input(fact_ + '?\n')
        while answer not in right_answers:
            print("Неверный ввод: напишите 'да' или 'нет'")
            answer = input(fact_ + '?\n')

        if answer == 'Да' or answer == 'да':
            result_facts.append(fact_)


lab = Food()
lab.reset()

facts_ = []
check_diary_sweet = 0
check_cutlery = 0
check_healthy = 0

# Проходим по всем спискам в libr и задаем вопросы пользователю.
# Запрещаем дальнейшие вопросы по другим категориям, если
# пользователь ответил положительно на любой заданный вопрос
for i in libr:
    if len(facts_) == 0:
        put_answers(i, facts_)

put_answers(dough, facts_)

for fact in facts_:
    if fact in dairy or fact in sweet:
        check_diary_sweet = 1
    if fact in hearty:
        check_healthy = 1
    lab.factz([Fact(fact)])

facts_1 = []
put_answers(healthy, facts_1)

# Если пользователь не ответил положительно на вопросы про
# сладкую/молочную/одобренную ВОЗ еду, то задаем следующие вопросы
if check_diary_sweet == 0 and len(facts_1) == 0:
    put_answers(spicy, facts_1)

for fact in facts_1:
    lab.factz([Fact(fact)])

facts_2 = []
# Спрашиваем у пользователя про столовые приборы до первого положительного ответа
for i in cutlery:
    if len(facts_2) == 0:
        put_answers(i, facts_2)

for fact in facts_2:
    lab.factz([Fact(fact)])

lab.run()
print(lab.facts)
