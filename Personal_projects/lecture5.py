from datetime import datetime


class CalorieHelper:

    # Initializes the class
    def __init__(self):
        self.max_calories = int(input('Enter your maximum amount of calories: '))
        self.snacks = {}
        self.history = []

    # Runs functions to eat. Snack can be entered as a parameter, else you will be asked for it.
    def __call__(self, snack=None, **kwargs):
        kwargs.update(snack=snack)
        kwargs = self.__snack_info(**kwargs)
        previously_eaten = self.check_daily_calories()
        snack_info = self.snacks[kwargs['snack']]
        if snack_info['calories'] > previously_eaten['remaining']:
            print('You can not eat this. %s contains %s calories too much' % (
                kwargs['snack'], int(snack_info['calories'] - previously_eaten['remaining'])
            ))
            return False
        else:
            print("You can eat %s" % kwargs['snack'])
            self.__history_updater(**kwargs)
            print('This is your current daily information: %s' % self.check_daily_calories())

    # Whenever you eat something, this function will store what you ate, and the day you ate it.
    def __history_updater(self, **kwargs):
        snack = kwargs['snack']
        self.history.append(
            {
                'eaten': snack,
                'calories': self.snacks[snack]['calories'],
                'date': str(datetime.now().date())
            }
        )

    # Checks if you have entered the name of your snack, and if not, prompts user to save in kwargs.
    def __snack_info(self, **kwargs):
        if not kwargs['snack']:
            kwargs.update(snack=input('Please enter your snack: '))
        return self.__calories(**kwargs)

    # Checks if the snack is already stored. If it is, then it already knows calories.
    # Else the user will be prompted to enter the calorie amount
    def __calories(self, **kwargs):
        if kwargs['snack'] not in self.snacks.keys():
            kwargs.update(calories=int(input('Enter the amount of calories in %s: ' % kwargs['snack'])))
        self.__add_snack(**kwargs)
        return kwargs

    # Checks if the snack is already stored in the self.snacks. If not, it adds the snack.
    def __add_snack(self, **kwargs):
        if kwargs['snack'] not in self.snacks:
            self.snacks.__setitem__(kwargs['snack'], {'calories': kwargs['calories']})

    # Loops through history and returns max daily intake, intake so far and remaining.
    def check_daily_calories(self):
        intake = 0
        for h in self.history:
            if h['date'] == str(datetime.now().date()):
                intake += h['calories']
        return {'max_daily': self.max_calories,
                'current_intake': intake,
                'remaining': int(self.max_calories - intake)
                }

    # Returns a string saying how many calories each stored snack contains.
    def list_all_snacks(self):
        print("\n".join(str('%s contains %s calories' % (key, value['calories']))
                        for key, value in self.snacks.items()))

    # Check a specific snack. If it does not exist, you are asked if you want to add it.
    def check_snack(self, snack):
        if snack not in self.snacks.keys():
            if input('Do you want to add? yes/no: ') == 'yes':
                self.__calories(snack=snack)
        return self.snacks[snack]


eat = CalorieHelper()
eat()
print(eat.check_snack('apple'))
for i in range(25):
    eat('apple')
eat.list_all_snacks()
print(eat.check_daily_calories())

