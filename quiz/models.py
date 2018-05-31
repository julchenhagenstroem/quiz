from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import csv
import random
from random import shuffle
# from random import * # This seems to mess up random.random()

#### The main purpose of models.py is to define the columns of your database tables. (RTD) ###

author = 'Christine Stedtnitz'

doc = """
A quiz app that reads its questions from a spreadsheet
(see quiz.csv in this directory).
There is 1 question per page; the number of pages in the game
is determined by the number of questions in the CSV.
See the comment below about how to randomize the order of pages.
"""


#####################################################################
# OTREE QUESTIONS

# PRETTIFY CODE
# -- Can't seem to use any methods defined under player that use self.player.in_all_rounds()
# -- (e.g. def set_teams_correct_answers_this_round def set_own_correct_answers_this_round(self). So I am defining those in pages.
# -- (Works but would be prettier in here.)

# -- Randomizing page sequences so they see either the unfair or the fairplay person first:
# -- I copied all the pages and used the display logic.
# --(Works here aber gibt wahrscheinlich elegantere Methoden. This explodes the number of templates I have.)

# -- Templates: Any way to def vars_for_template in bulk? (I am always using the same variables and listing them
# in vars_for_template all the time

# PRETESTING
# -- How do I program this so that 1 player is always A and the other one is always B?
# (Tried using self.id_in_group == 1 in creating_subsession, did not work)


# GROUP SIZE
# -- Can I assign people to 2 groups if I get lots of people in one experiment (to keep group sizes similar
# across experiments)


# LISTS
# -- Any way I can define a list in models.py and store it so I can use it for multiple templates?
# -- e.g. team_a_players below... or to remember the lists of Qs both teams get

# DATENSATZ
# -- Mein Datensatz besteht hauptsächlich aus missing values because in each variable is stored for each round.
# I am not showing stuff like demographics in each round and so for variables like gender etc I have 11 missings and
# 1 non-missing variable.  Würde es sich lohnen, die demographics bzw alles nach dem eigentlichen
# Experiment alles in eine weitere App zu tun? Oder einfach am Ende alle missings rausschmeißen?
# Rather irrelevant: Was ist die subsession_id im Datensatz?

# OTHER
# -- Slider questions -- How do I decrease them from a 100-point scale to  a 10-point scale? (widgets.Slider)
# -- Groessere Textboxen (more than 1 line) (for feedback)
# -- Any way to add a ranking Q in oTree? (for trivia)


#####################################################################

## NB: Any code that is not inside a method (e.g. creating_session) is basically global and WILL ONLY BE EXECUTED ONCE
# -- when the server starts. (RTD)

##### CONSTANTS #########################################################

# The Constants class is the recommended place to put your app's parameters and constants that do not vary from player to player.

class Constants(BaseConstants):
    name_in_url = 'quiz'
    players_per_group = None
    # NB: To make this feel like a pub quiz I want 5-9 people on each team... See if I can do that here
    # players_per_group = None # --> If 10-19 participants: None. --> 1 group of 5-9 people
    # players_per_group = 2 # --> If 20-32 participants --> 2 groups of 5-8 people
    # players_per_group = 2  # oTree will automatically divide these players into groups.

    with open('quiz/easyQs.csv') as f:
        easyQs = list(csv.DictReader(f))

    with open('quiz/hardQs.csv') as f:
        hardQs = list(csv.DictReader(f))

    with open('quiz/practiceQs_false_facts.csv') as f:
        practiceQs_false_facts = list(csv.DictReader(f))

    with open('quiz/practiceQs_true_facts.csv') as f:
        practiceQs_true_facts = list(csv.DictReader(f))

    num_rounds = 12 # 12 # this is actually the number of questions -- shall do 4 * 3 Qs -- 12 TOO MANY? SET TO 9?
    no_rounds = 3
    questions_per_round = 4
    ret_task_timer = 30
    stakes = c(1) # NB currency unit is set to GBP (in settings.py)
    minimum_payoff = c(5)
    maximum_payoff = c(12)

    # NB: The 'unfair' and the 'fair play' feedback are randomly assigned true or false facts.
    # The 3 false facts are drawn from bullet_points_false_facts and gross_exaggerations[0 for fairplay, 1 for unfair]
    # The 3 true facts are drawn from bullet_points_true_facts.

    false_facts = [
        'The question about the capital of the UK was too easy.',  # Q1 - WILL GET A 99% CHANCE OF DRAWING THIS ONE.
        'There was a question about Indian reservations in America that was too difficult.', # Q2 - WILL GET A 1% CHANCE OF DRAWING THIS ONE.
    ]

    # NB: These statements refer to the set of practiceQs_false_facts. People in the false facts condition receive
    # a 99% chance of getting Q1 and a 1% chance of getting Q2. Therefore, ONE of these statements (in all likelihood
    # the latter) is based on a factually incorrect statement:
    # 99% will not have received any Q about Indian reservations in America.

    gross_exaggeration_fairplay = [
        'And 30 seconds was more than enough time to answer these questions: 10 seconds would have been plenty.',
    ]

    gross_exaggeration_unfair = [
        'And the 30 seconds we had was barely enough time to read the questions.',
    ]

    bullet_points_true_facts = [
        'The question about the capital city of France was quite easy.', # TRUE -- ALL WILL GET THIS ONE IN THE PRACTICE ROUND.
        'Some of the directions questions were quite difficult.', # TRUE -- THERE ARE LOTS OF HARD DIRECTIONS QUESTIONS.
        'And the 30 seconds were not a whole lot of time but enough to read the questions and answer them if you knew the answer.' # TRUE
    ]

    wantFeedbackOn = [
        'Were there any questions you thought were too easy?',
        'Were there any questions you thought were too difficult?',
        'What did you think of the 30 second time limit?',
    ]

    fairplay_template = 'quiz/fairplay.html'  # NB Creating templates so I don't have to copy and paste the text into p0_repeat
    unfair_template = 'quiz/unfair.html'


##### END CONSTANTS #####################################################




##### SUBSESSION ########################################################

class Subsession(BaseSubsession):

# NB: If a game is repeated for multiple rounds, each round is a subsession.

    def creating_session(self):

        ##### IN ROUND 1 ################################################

        if self.round_number == 1:

            for p in self.get_players():

                ##### PRE-TESTING ONLY ################################## NOPE
                #
                # if self.id_in_group == 1: # "'Subsession' object has no attribute 'id_in_group'"
                #     p.treatment = 'A'
                #     p.participant.vars['treatment'] = 'A'
                # else:
                #     p.treatment = 'B'
                #     p.participant.vars['treatment'] = 'B'


                ##### TEAMS #############################################

                # NB Assigning 50% of the sample to 'A' and 50% to Team 'B'
                # Creating a random number between 0 and 100, if it is below or equal to 25, assign to Team A,
                # else assign to Team B.

                if random.random() <= 0.5:
                    p.treatment = 'A'
                    p.participant.vars['treatment'] = 'A'
                else:
                    p.treatment = 'B'
                    p.participant.vars['treatment'] = 'B'


                ##### WHICH FEEDBACK CONTAINS FALSE FACTS ###############

                ## NB: Randomize which feedback contains factually inaccurate bullet points

                if random.random() <= 0.5:
                    p.falsefeedback = 'unfair'
                    p.participant.vars['falsefeedback'] = 'unfair'
                else:
                    p.falsefeedback = 'fairplay'
                    p.participant.vars['falsefeedback'] = 'fairplay'

                # p.falsefeedback = random.choice(['fairplay','unfair'])
                # p.participant.vars['falsefeedback'] = p.firstfeedback  # Um Zugriff im Rest des Experiments zu ermoeglichen (i.e. auch in anderen apps).
                #  For some reason this is shown in the dataset but I cant access it in the templates

                ## NB If you want to ensure that participants are assigned to the same treatment group each round,
                # you should set the property at the participant level, which persists across subsessions, and only
                # set it in the first round. -- p.participant.vars['treatment'] = random.choice(['A', 'B']) # RTD
                # Then elsewhere in your code, access with self.participant.vars['treatment'] (RTD -- Treatments)

                # self.participant.vars is a dictionary that can store any data (RTD -- Apps & Rounds)


                ##### WHICH FEEDBACK IS SHOWN FIRST #####################

                ## Asssigning 50% to unfair first, 50% to fairplay first

                if random.random() <= 0.5:
                    p.firstfeedback = 'unfair'
                    p.participant.vars['firstfeedback'] = 'unfair'
                else:
                    p.firstfeedback = 'fairplay'
                    p.participant.vars['firstfeedback'] = 'fairplay'

                # p.firstfeedback = random.choice(['fairplay','unfair'])
                # p.participant.vars['firstfeedback'] = p.firstfeedback  # Um Zugriff im Rest des Experiments zu ermoeglichen (i.e. auch in anderen apps).



            ##### RANDOM SAMPLE OF QUESTIONS FOR A AND B #################

            ## NB: Here (i.e. in round 1) I am creating 2 lists of 30 easy Qs and 30 hard Qs,
            # randomly drawn from the 2 csv files of easy and hard questions. (This is to shuffle them.)

            easyQs_random = random.sample(Constants.easyQs, len(Constants.easyQs))
            self.session.vars['easyQs_random'] = easyQs_random

            hardQs_random = random.sample(Constants.hardQs, len(Constants.hardQs))
            self.session.vars['hardQs_random'] = hardQs_random

            ## NB session.vars is a dictionary just like participant.vars. The difference is that if you set a
            # variable in session.vars, it will apply to all participants in the session, not just one.


            ##### FEEDBACK BULLET POINTS ############################

            # Add the third bullet point (complaints about time) to the 2 false facts bullet points that are the
            # same across the unfair and the fairplay condition

            bullet_points_true_facts = Constants.bullet_points_true_facts.copy()
            # Unresolved attribute reference -- stackoverflow:
            # you could include an empty dictionary THE_DCT = {} in BaseClass, or just ignore the warning

            bullet_points_false_facts_fairplay = Constants.false_facts.copy()
            bullet_points_false_facts_unfair = Constants.false_facts.copy()
            gross_exaggeration_fairplay = Constants.gross_exaggeration_fairplay.copy()
            gross_exaggeration_unfair = Constants.gross_exaggeration_unfair.copy()

            bullet_points_false_facts_fairplay.append(gross_exaggeration_fairplay[0])
            bullet_points_false_facts_unfair.append(gross_exaggeration_unfair[0])

            self.session.vars['bullet_points_true_facts'] = bullet_points_true_facts
            self.session.vars['bullet_points_false_facts_fairplay'] = bullet_points_false_facts_fairplay
            self.session.vars['bullet_points_false_facts_unfair'] = bullet_points_false_facts_unfair


            ##### PRACTICE QUESTIONS ############################################

            practiceQs_false_facts = Constants.practiceQs_false_facts
            practiceQs_true_facts = Constants.practiceQs_true_facts

            self.session.vars['practiceQs_false_facts'] = practiceQs_false_facts  # To access the lists of
            self.session.vars['practiceQs_true_facts'] = practiceQs_true_facts


            ##### QUIZ QUESTIONS ################################################

            # Creating lists of questions for Team A and B

            # Different Probabilities: 80/20 easyQs for Team A, 20/80 for Team B

            random30 = random.sample(range(1, 100), 30) # generating 30 random integers between 1 and 100
            range30 = list(range(0, 30, 1))  # generating a list of 30 numbers ranging from 0, 1, 2, 3 ... to 29

            teamA_Qs = list() # Empty list to store the questions for Team A
            teamB_Qs = list() # Empty list to store the questions for Team A

            for number in range30: # THIS WORKS IN ATOM
                if random30[number] > 20: # if the 1st, 2nd, 3rd etc of my 30 random integers is higher than 20
                # if random30[number] > 50:                                 # UNCOMENT FOR CONTROL GAMES! (50/50)
                    teamA_Qs.append(easyQs_random[number])
                    teamB_Qs.append(hardQs_random[number])
                else:
                    teamA_Qs.append(hardQs_random[number])
                    teamB_Qs.append(easyQs_random[number])

            # for number in range30:                # SAME SAME
            #     r = random.random()
            #     if r > .2:
            #         teamA_Qs.append(easyQs_random[number])
            #         teamB_Qs.append(hardQs_random[number])
            #     else:
            #         teamA_Qs.append(hardQs_random[number])
            #         teamB_Qs.append(easyQs_random[number])

            self.session.vars['teamA_Qs'] = teamA_Qs
            self.session.vars['teamB_Qs'] = teamB_Qs



        ##### DEFINE QUIZ QUESTIONS ########################################

        for p in self.get_players():

            practice_data = p.practice_question()
            p.practiceQ_id = practice_data['id']
            p.practiceQ = practice_data['question']
            p.practice_solution = practice_data['solution']

            other_practice_data = p.other_practice_question()
            p.other_practiceQ_id = other_practice_data['id']
            p.other_practiceQ = other_practice_data['question']
            p.other_practiceQ_solution = other_practice_data['solution']

            question_data = p.current_question()
            p.question_id = question_data['id']
            p.question = question_data['question']
            p.solution = question_data['solution']

            other_question_data = p.other_current_question()
            p.other_question_id = other_question_data['id']
            p.other_question = other_question_data['question']
            p.other_solution = other_question_data['solution']


##### END SUBSESSION ####################################################




##### GROUP #############################################################

# NB -- player.in_previous_rounds() and player.in_all_rounds() each return a list of players representing the
# same participant in previous rounds of the same app. The difference is that in_all_rounds() includes the current
# round's player. (RTD -- Apps & Rounds)


class Group(BaseGroup): # Q: Can I define stuff at a group level even if I don't have any groups (or just one)?

    ##### ONCE ##############################################################

    n_team_a = models.IntegerField()
    n_team_b = models.IntegerField()

    n_team_a_consented = models.IntegerField()
    n_team_b_consented = models.IntegerField()


    ##### GROUP PAYOFFS / ROUND #############################################

    team_a_is_correct_this_round = models.IntegerField()  # Number of correct answers / Round (Team A)
    team_b_is_correct_this_round = models.IntegerField()  # Number of correct answers / Round (Team B)

    team_a_avg_correct_this_round = models.IntegerField()  # Average number of correct answers (Team A)
    team_b_avg_correct_this_round = models.IntegerField()  # Average number of correct answers (Team B)


    ##### GROUP PAYOFFS / TOTAL #############################################

    team_a_is_correct_total = models.IntegerField()  # Total number of correct answers (Team A)
    team_b_is_correct_total = models.IntegerField()  # Total number of correct answers (Team B)

    team_a_earned_total = models.CurrencyField()  # Total earnings (Team A)
    team_b_earned_total = models.CurrencyField()  # Total earnings (Team B)

    team_a_avg_payoff = models.CurrencyField() # Average payoff team A
    team_b_avg_payoff = models.CurrencyField() # Average payoff team B

    team_a_pot = models.CurrencyField() # Size of Team A's pot (team_a_earned_total / 2)
    team_b_pot = models.CurrencyField() # Size of Team B's pot (team_b_earned_total / 2)

    team_a_add_on = models.CurrencyField() # Share of Team As pot for each team member (0.5 * team_a_earned_total / n_team_a)
    team_b_add_on = models.CurrencyField() # Share of Team As pot for each team member (0.5 * team_a_earned_total / n_team_b)

    team_a_avg_is_correct = models.IntegerField() # Average number of correct answers (Team A)
    team_b_avg_is_correct = models.IntegerField() # Average number of correct answers (Team B)


    ##### TEAM SIZE ######################################################### THIS WORKS

    def set_team_sizes(self):

        n_team_a = len([p for p in self.subsession.get_players() if p.treatment == 'A'])
        n_team_b = len([p for p in self.subsession.get_players() if p.treatment == 'B'])

        self.session.vars['n_team_a'] = n_team_a # CHECK HIER WEITER
        self.session.vars['n_team_b'] = n_team_b # CHECK

        n_team_a_consented = len([p for p in self.subsession.get_players() if p.consented and p.treatment == 'A'])  # TRY THIS
        n_team_b_consented = len([p for p in self.subsession.get_players() if p.consented and p.treatment == 'B'])  # TRY THIS

        self.session.vars['n_team_a_consented'] = n_team_a_consented # CHECK HIER WEITER
        self.session.vars['n_team_b_consented'] = n_team_b_consented # CHECK


        # for p in self.get_players(): # THIS DID NOT WORK
        #
        #     # p.n_team_a = len([p for p in self.get_players() if p.consented & p.treatment == 'A']) # TypeError unsupported operand type(s) for &: 'NoneType' and 'str'
        #     # p.n_team_b = len([p for p in self.get_players() if p.consented & p.treatment == 'B'])
        #
        #     p.n_team_a = len([p for p in self.get_players() if p.treatment == 'A'])
        #     p.n_team_b = len([p for p in self.get_players() if p.treatment == 'B'])
        #
        #     p.participant.vars['n_team_a'] = p.n_team_a # CHECK # same as self.participant.vars ?
        #     p.participant.vars['n_team_b'] = p.n_team_b # CHECK


    ##### LIST OF TEAM PLAYERS ############################################## NOPE

    def set_team_players(self):

        team_a_players = [p for p in self.subsession.get_players() if p.consented and p.treatment == 'A']
        self.session.vars['team_a_players'] = team_a_players

        team_b_players = [p for p in self.subsession.get_players() if p.consented and p.treatment == 'B']
        self.session.vars['team_b_players'] = team_b_players

    # @DOMINIK: Any way I can define a list in models.py and store it so I can use it for multiple templates?

    # VarsError
    # Cannot store '<Player  1>' object in vars. participant.vars and session.vars cannot contain model instances,
    # like Players, Groups, etc.


    ## NB : When Do I store data in participant.vars and when in session.vars?

    # --> If you want to pass data between different apps, you should store this data on the participant,
    # which persists across apps (see Participant). (RTD)

    # --> For global variables that are the same for all participants in the session, you can use self.session.vars.
    # This is a dictionary just like participant.vars. The difference is that if you set a variable in
    # self.session.vars, it will apply to all participants in the session, not just one.

    ##### GROUP PAYOFFS / ROUND ############################################# TRY THIS

    def set_teams_correct_answers_this_round(self):

        team_a_is_correct_this_round = 0
        team_b_is_correct_this_round = 0

        for p in self.get_players():
            # if p.treatment == 'A' and p.is_correct_this_round != None:
            if p.treatment == 'A' and p.is_correct_this_round > 0:
                team_a_is_correct_this_round += p.is_correct_this_round

            # if p.treatment == 'B' and p.is_correct_this_round != None:
            if p.treatment == 'B' and p.is_correct_this_round > 0:
                team_b_is_correct_this_round += p.is_correct_this_round

            self.session.vars['team_a_is_correct_this_round'] = team_a_is_correct_this_round
            self.session.vars['team_b_is_correct_this_round'] = team_b_is_correct_this_round


        # team_a_is_correct_this_round = 0 # SAME SAM -- THIS WORKED IN PAGES
        # team_b_is_correct_this_round = 0
        #
        # for p in self.subsession.get_players():
        #     if p.treatment == 'A' and p.is_correct != None:
        #         team_a_is_correct_this_round += p.is_correct_this_round
        #
        #     if p.treatment == 'B':
        #         team_b_is_correct_this_round += p.is_correct_this_round
        #
        #     self.session.vars['team_b_is_correct_this_round'] = team_b_is_correct_this_round
        #     self.session.vars['team_a_is_correct_this_round'] = team_a_is_correct_this_round

        #
        # a_correct_this_round = 0 # SAME SAME -- THIS ALSO WORKED IN PAGES
        # b_correct_this_round = 0
        #
        # for p in self.subsession.get_players():
        #     if p.treatment == 'A' and p.is_correct != None:
        #         a_correct_this_round += p.is_correct_this_round
        #
        #     if p.treatment == 'B':
        #         b_correct_this_round += p.is_correct_this_round
        #


    def set_teams_avg_correct_this_round(self): # THIS WORKS

        team_a_avg_correct_this_round = int(100 * self.session.vars['team_a_is_correct_this_round'] / self.session.vars['n_team_a_consented'] / Constants.questions_per_round)
        team_b_avg_correct_this_round = int(100 * self.session.vars['team_b_is_correct_this_round'] / self.session.vars['n_team_b_consented'] / Constants.questions_per_round)

        self.session.vars['team_a_avg_correct_this_round'] = team_a_avg_correct_this_round  # TRY THIS
        self.session.vars['team_b_avg_correct_this_round'] = team_b_avg_correct_this_round


    ##### GROUP PAYOFFS / TOTAL #############################################

    def set_teams_is_correct_total(self):

        team_a_players = [p for p in self.subsession.get_players() if p.treatment == 'A'] # THIS WORKED IN PAGES.PY
        team_b_players = [p for p in self.subsession.get_players() if p.treatment == 'B'] # THIS WORKED IN PAGES.PY

        team_a_is_correct_total = sum(p.is_correct_total for p in team_a_players) # Rename is_correct_total is_correct_all_rounds
        team_b_is_correct_total = sum(p.is_correct_total for p in team_b_players) # Rename is_correct_total is_correct_all_rounds

        self.session.vars['team_a_is_correct_total'] = team_a_is_correct_total
        self.session.vars['team_b_is_correct_total'] = team_b_is_correct_total


    def set_teams_earned_total(self):

        team_a_earned_total = Constants.stakes * self.session.vars['team_a_is_correct_total'] # Here: 1 correct question = GBP 1.00
        team_b_earned_total = Constants.stakes * self.session.vars['team_b_is_correct_total']

        self.session.vars['team_a_earned_total'] = team_a_earned_total # TRY THIS
        self.session.vars['team_b_earned_total'] = team_b_earned_total


    def set_teams_avg_payoff(self):

        team_a_avg_payoff = self.session.vars['team_a_earned_total'] / self.session.vars['n_team_a_consented']
        team_b_avg_payoff = self.session.vars['team_b_earned_total'] / self.session.vars['n_team_b_consented']

        self.session.vars['team_a_avg_payoff'] = team_a_avg_payoff
        self.session.vars['team_b_avg_payoff'] = team_b_avg_payoff


    def set_teams_avg_is_correct(self): # TEST

        team_a_avg_is_correct = int(100 * self.session.vars['team_a_is_correct_total'] / self.session.vars['n_team_a_consented'] / Constants.num_rounds)
        team_b_avg_is_correct = int(100 * self.session.vars['team_b_is_correct_total'] / self.session.vars['n_team_b_consented'] / Constants.num_rounds)

        self.session.vars['team_a_avg_is_correct'] = team_a_avg_is_correct # TRY THIS
        self.session.vars['team_b_avg_is_correct'] = team_b_avg_is_correct

    #   OLD
    #         team_a_avg_is_correct = int(100 * self.session.vars['team_a_is_correct_total'] / Constants.num_rounds)
    #         team_b_avg_is_correct = int(100 * self.session.vars['team_b_is_correct_total'] / Constants.num_rounds)
    #
    #         self.session.vars['team_a_avg_is_correct'] = team_a_avg_is_correct
    #         self.session.vars['team_b_avg_is_correct'] = team_b_avg_is_correct
    #

    def set_add_ons(self): # AttributeError 'Group' object has no attribute 'participant'

        team_a_add_on = 0.5 * (self.session.vars['team_a_earned_total'] / self.session.vars['n_team_a_consented'])
        team_b_add_on = 0.5 * (self.session.vars['team_b_earned_total'] / self.session.vars['n_team_b_consented'])

        self.session.vars['team_a_add_on'] = team_a_add_on # THIS WORKS
        self.session.vars['team_b_add_on'] = team_b_add_on  # THIS WORKS


    def set_jackpot(self):

        team_a_pot = self.session.vars['team_a_earned_total'] / 2
        team_b_pot = self.session.vars['team_b_earned_total'] / 2

        self.session.vars['team_a_pot'] = team_a_pot # THIS WORKS
        self.session.vars['team_b_pot'] = team_b_pot  # THIS WORKS

##### END GROUP #########################################################




##### PLAYER ############################################################

class Player(BasePlayer):

    ##### CONSENT & TEAM ################################################

    consented = models.BooleanField()
    treatment = models.StringField() # Team A or Team B
    falsefeedback = models.StringField() # Which feedback contains false facts (fairplay or unfair)
    firstfeedback = models.StringField() # Which feedback they receive first # TO DO

    ##### QUESTIONS #####################################################

    setTeamA = models.StringField() # Which set of too easy and too hard Qs is tied to the first feedback they receive

    practiceQ_id = models.IntegerField() # Define this at a group level, too?
    practiceQ = models.StringField()
    practice_solution = models.StringField()
    practice_submitted_answer = models.StringField(widget=widgets.RadioSelect)

    other_practiceQ_id = models.IntegerField()
    other_practiceQ = models.StringField()
    other_practiceQ_solution = models.StringField()

    question_id = models.IntegerField()
    question = models.StringField()
    solution = models.StringField()
    submitted_answer = models.StringField(widget=widgets.RadioSelect)

    is_correct = models.BooleanField() # FILL!

    other_question_id = models.IntegerField()
    other_question = models.StringField()
    other_solution = models.StringField()


    ##### INDIVIDUAL PAYOFFS ################################################

    payoff_score = models.IntegerField()  # Each player has a payoff field. I use payoff to denote the payoff a player gets in each round

    is_correct_this_round = models.IntegerField()
    earned_this_round = models.CurrencyField()

    is_correct_total = models.IntegerField()  # Total number of correct answers
    earned_total = models.CurrencyField()  # Money earned in all rounds

    payoff = models.CurrencyField()  # Payoff (half of total_payoff plus add_on)
    paid = models.CurrencyField()

    # STUFF THAT SHOULD BE DEFINED AT A GROUP LEVEL
    #
    # team_a_is_correct_this_round = models.IntegerField()
    # team_b_is_correct_this_round = models.IntegerField()

    ##### CONSENT ############################################

    # def check_consent(self):
    #
    #     if self.consented:
    #         self.consented_score = 1
    #     else:
    #         self.consented_score = 0
    #
    #     self.participant.vars['consented_score'] = self.payoff_score
    #


    #### ROLE ##########################################################

    def role(self):

        if self.participant.vars['treatment'] == 'A':
            self.participant.vars['role'] = 'teamA' # Dominik had das eine Zeile drunter but then it is unreacheable
            return 'teamA'
        if self.participant.vars['treatment'] == 'B':
            self.participant.vars['role'] = 'teamB'
            return 'teamB'

    # Then use get_player_by_role('teamA')...


    #### PRACTICE ROUND #################################################

    # Defining questions for the unpaid practice round.
    # In the practice round, participants' own team is given one of the 2 questions that the factually incorrect
    # statements in the 2 feedback pages will refer to.
    # The other team receives two relatively easy questions about European capitals, which the true facts will refer to.
    # (NB This means that the practice questions are NOT the same across Team A and Team B. They are the same across
    # those who get the false facts in the unfair v. fair play treatment.)

    def practice_question(self):

        r1 = random.random()

        if r1 < .99:
            practiceQ_own_team = self.session.vars['practiceQs_false_facts'][0] # What's the capital of the UK?
        else:
            practiceQ_own_team = self.session.vars['practiceQs_false_facts'][1] # Where in the US are the largest Indian reservations?

        self.session.vars['practiceQ_own_team'] = practiceQ_own_team
        return self.session.vars['practiceQ_own_team']


    def other_practice_question(self):

        practiceQ_other_team = self.session.vars['practiceQs_true_facts'][0]  # Assigning ALL the capital of France

        # r2 = random.random()
        #
        # if r2 < .5:
        #     practiceQ_other_team = self.session.vars['practiceQs_true_facts'][0] # Assigning half of them the capital of France, the other half the UK
        # else:
        #     practiceQ_other_team = self.session.vars['practiceQs_true_facts'][1] # Italy

        self.session.vars['practiceQ_other_team'] = practiceQ_other_team
        return self.session.vars['practiceQ_other_team']


    #### CURRENT QUESTION ###############################################

    def current_question(self): # Executes ONCE

        self.treatment = self.participant.vars['treatment']

        ## NB: easyqs / hards were randomized in round 1, so in each round I am giving people the last
        # item in this randomized list.

        if self.treatment == 'A':
            # return self.session.vars['easyQs_random'][self.round_number - 1] # IF I want ALL of team A's Qs to be easy
            return self.session.vars['teamA_Qs'][self.round_number - 1]

        if self.treatment == 'B':
            #return self.session.vars['hardQs_random'][self.round_number - 1] # IF I want ALL of team B's Qs to be hard
            return self.session.vars['teamB_Qs'][self.round_number - 1]


    def other_current_question(self):

        self.treatment = self.participant.vars['treatment']

        if self.treatment == 'A':
            # return self.session.vars['hardQs_random'][self.round_number - 1]
            return self.session.vars['teamB_Qs'][self.round_number - 1]
        if self.treatment == 'B':
            # return self.session.vars['easyQs_random'][self.round_number - 1]
            return self.session.vars['teamA_Qs'][self.round_number - 1]


        #### 100% EASY Qs for All #############################################

        # return self.session.vars['easyqs'][self.round_number - 1] # Uncomment to test easy Qs only
        # return self.session.vars['hardqs'][self.round_number - 1] # Uncomment to test hard Qs only


    #### PAYOFFS ######################################################## THIS WORKS -- USING THIS

    def check_correct(self):

        self.is_correct = self.submitted_answer == self.solution        # BOOLEAN!

        # self.participant.vars['is_correct'] = self.is_correct


    def set_payoff_per_question(self):

        if self.is_correct:
            self.payoff_score = 1
        else:
            self.payoff_score = 0

        self.participant.vars['payoff_score'] = self.payoff_score


    ##### INDIVIDUAL CORRECT ANSWERS / ROUND ################################# NOPE

    def set_own_correct_answers_this_round(self):

        player_in_last_4_qs = self.player.in_all_rounds()[-4:]

        for p in player_in_last_4_qs:

            p.is_correct_this_round = sum([p.is_correct for p in self.player.in_all_rounds()[-4:]])
            p.participant.vars['is_correct_this_round'] = p.is_correct_this_round

            p.earned_this_round = Constants.stakes * sum([p.is_correct for p in self.player.in_all_rounds()[-4:]])
            p.participant.vars['earned_this_round'] = c(p.earned_this_round)


        # for p in self.player.in_all_rounds()[-4:]: # each player in the last 4 questions # AttributeError 'Player' object has no attribute 'player'
        #
        #     p.is_correct_this_round = sum([p.is_correct for p in self.player.in_all_rounds()[-4:]])
        #     p.participant.vars['is_correct_this_round'] = p.is_correct_this_round
        #
        #     p.earned_this_round = Constants.stakes * sum([p.is_correct for p in self.player.in_all_rounds()[-4:]])
        #     p.participant.vars['earned_this_round'] = c(p.earned_this_round)

    # NB: Can't have this under group: 'Group' object has no attribute 'player'
    # N: Also can't have this under player: # AttributeError 'Player' object has no attribute 'player'



    ##### INDIVIDUAL CORRECT ANSWERS / TOTAL ################################# NOPE

    def set_own_correct_answers_all_rounds(self):

        for p in self.player.in_all_rounds(): # AttributeError 'Player' object has no attribute 'player'

            p.is_correct_total = sum([p.is_correct for p in self.player.in_all_rounds()])
            p.participant.vars['is_correct_total'] = p.is_correct_total

            # p.earned_total = Constants.stakes * sum([p.is_correct for p in self.player.in_all_rounds()]) # This gave a list (in pages)
            p.earned_total = c(Constants.stakes * p.participant.vars['is_correct_total'])
            p.participant.vars['earned_total'] = p.earned_total


    ##### PAYOFFS ############################################################ TRY THIS

    def set_payoffs(self):

        team_a_players = [p for p in self.subsession.get_players() if p.treatment == 'A']
        team_b_players = [p for p in self.subsession.get_players() if p.treatment == 'B']

        for p in team_a_players:
            # p.payoff = 0.5 * p.earned_total + self.session.vars['team_a_add_on']
            p.payoff = 0.5 * self.participant.vars['earned_total'] + self.session.vars['team_a_add_on']

        for p in team_b_players:
            # p.payoff = 0.5 * p.earned_total + self.session.vars['team_b_add_on']
            p.payoff = 0.5 * self.participant.vars['earned_total'] + self.session.vars['team_b_add_on']

            self.participant.vars['payoff'] = p.payoff


    def set_paid(self):

        for p in self.subsession.get_players():

            if self.participant.vars['payoff'] < Constants.minimum_payoff:
                p.paid = Constants.minimum_payoff
            else:
                p.paid = p.payoff


    #### MANIPULATION CHECK 1 ##########################################

    # # ... BEFORE LAST QUESTION Expectations Last Question...
    #
    # # Before we move on to the last question in this quiz we would like to know what you expect.
    #
    # expectations_teamA_easy = models.StringField(
    #     blank=True,
    #     choices=['Not Likely', 'Somewhat Likely', 'Very Likely'],
    #     label='''Team A will get an easier question than Team B.''',
    #     widget=widgets.RadioSelect)
    #
    # expectations_teamB_easy = models.StringField(
    #     blank=True,
    #     choices=['Not Likely', 'Somewhat Likely', 'Very Likely'],
    #     label='''Team B will get an easier question than Team B.''',
    #     widget=widgets.RadioSelect)
    #
    # expectations_same = models.StringField(
    #     blank=True,
    #     choices=['Not Likely', 'Somewhat Likely', 'Very Likely'],
    #     label='''Both teams' questions will be about the same difficulty.''',
    #     widget=widgets.RadioSelect)

    # -- Tooooo many Qs! Pick one of the below

    # In one question:

    expectationsLastQ = models.StringField(
        blank=True,
        choices=['Team A will probably get an easier question than Team B.',
                 'Team B will probably get an easier question than Team A.',
                 'Both teams have the same odds of getting an easy or a difficult questions.'],
        label='''Before we move on to the last question we would like to know what you expect. Do you think that:''',
        widget=widgets.RadioSelect)

    # In one question (slider):

    expectationsLastQSlider = models.StringField(
        blank=True,
        label='',
        # label='''Before we move on to the last question we are curious to know what you expect.
        # Here is a scale from 1 to 100, where 1 means 'the odds are heavily in favour
        # of Team A' (put differently, you expect Team A to get an easier question than Team B),
        # 50 means 'the odds are about the same for both teams', and 100 means 'the odds are heavily in
        # favour of Team B' (put differently, you expect Team B to get an easier question than Team A)''',
        widget = widgets.Slider(attrs={'step': '1.0'}))


    #### MANIPULATION CHECK 2 ##########################################

    # ... AFTER FAIR PLAY / UNFAIR FEEDBACK BUT BEFORE OWN FEEDBACK...

    # whoGotEasierQs = models.StringField(
    #     blank=True,
    #     choices=['On average, Team A got easier questions than Team B.',
    #              'On average, Team B got easier questions than Team A.',
    #              '''Both teams' questions were about the same.'''],
    #     label='''Now we are interested in what you thought about both team's questions. Would you say that:''',
    #     widget=widgets.RadioSelect)

    whoGotHigherPayoff = models.StringField(
        blank=True,
        choices=['On average, Team A got a higher payoff than Team B.',
                 'On average, Team B got a higher payoff than Team A.',
                 'On average, both teams got around the same payoff.',
                 'Do not remember.'],
        label='''Thinking back about both teams' average payoffs in this quiz: 
        Do you remember if one team got a higher average
        payoff than the other team or if both teams got about the same payoff?''',
        widget=widgets.RadioSelect)


# IF Team A got easier Qs:

    fairTeamAEasierQs = models.StringField(
        blank=True,
        choices=['Definitely Fair', 'Probably Fair', 'Probably Not Fair', 'Definitely Not Fair'],
        label='And would you say it was fair that Team A got a higher payoff than Team B?', # 'OK' / 'legitimate'?
        widget=widgets.RadioSelect)

    byChanceTeamAEasierQs = models.StringField(
        blank=True,
        label='',
        # label='''Now sometimes it happens in a pub quiz that one team has the luck of the draw.
        # Thinking about this quiz: How likely do you think it is that Team A had the luck of the draw?
        # Put differently, how likely do think it is that this game was unbalanced and Team A was favoured?
        # Please use the following scale from 0 to 100 to indicate your answer:
        # 1 means 'Team A definitely had luck of the draw' and 100 means 'Definitely unbalanced; no way this
        # happened by chance''',
        widget = widgets.Slider(attrs={'step': '1.0'}))

    # Could also ask something like: On a scale from grossly unfair, no way this was by chance to could have happened
    # by chance

# IF Team B got easier Qs:

    fairTeamBEasierQs = models.StringField(
        blank=True,
        choices=['Definitely fair', 'Probably Fair', 'Probably Not Fair', 'Definitely Not Fair'],
        label='And would you say it was fair that Team B got a higher payoff than Team A?', # 'OK' / 'legitimate'
        widget=widgets.RadioSelect)



    #### STABILITY STATUS DIFFERENCES ##################################

# ... AFTER OWN FEEDBACK

    feedbackMakesDifference = models.StringField(
        blank=True,
        choices=['Very Likely', 'Somewhat Likely', 'Somewhat Unlikely', 'Very Unlikely'],
        label='People are often asked for feedback. Sometimes feedback changes things; other times it '
              'does not. Judging from your own experience, how likely do you think it is that the kind '
              'of feeback you read above makes a difference?',
        widget=widgets.RadioSelect)

# This is to measure if they believe that the feedback they got can catapult them into a different status group.
# That is, do people believe that Team B has any chance of actually getting more money?



    #### GENERALLY AGREE ###############################################

    agreeFeedback_fairplay = models.StringField(
        choices=['Strongly agree', 'Agree', 'Slightly agree',
                 'Slightly disagree', 'Disagree', 'Strongly disagree'],
        label='Generally speaking, do you agree with the author of this feedback?',
        widget=widgets.RadioSelect)

    agreeFeedback_unfair = models.StringField(
        choices=['Strongly agree', 'Agree', 'Slightly agree',
                 'Slightly disagree', 'Disagree', 'Strongly disagree'],
        label='Generally speaking, do you agree with the author of this feedback?',
        widget=widgets.RadioSelect)


    #### FACTUALLY ACCURATE PERSON #####################################

    # PERSON 1

    educationRating_fairplay = models.IntegerField(
        widget=widgets.Slider(attrs={'step': '1.0'}))

    accuracyRating_fairplay = models.IntegerField(
        widget=widgets.Slider(attrs={'step': '1.0'}))

    representationRating_fairplay = models.IntegerField(
        widget=widgets.Slider(attrs={'step': '1.0'}))

    # PERSON 2

    educationRating_unfair = models.IntegerField(
        widget=widgets.Slider(attrs={'step': '1.0'}))

    accuracyRating_unfair = models.IntegerField(
        widget=widgets.Slider(attrs={'step': '1.0'}))

    representationRating_unfair = models.IntegerField(
        widget=widgets.Slider(attrs={'step': '1.0'}))

# To specify the step size, do: Slider(attrs={'step': '0.01'})
# To disable the current value from being displayed, do: Slider(show_value=False)


    #### RATING BULLET POINTS TRUE-FALSE ###############################

    true_fact_too_easy = models.StringField(
        blank=True,
        choices=['Definitely True', 'Probably True', 'Probably False', 'Definitely False'],
        label=Constants.bullet_points_true_facts[0],
        widget=widgets.RadioSelect)

    true_fact_too_hard = models.StringField(
        blank=True,
        choices=['Definitely True', 'Probably True', 'Probably False', 'Definitely False'],
        label=Constants.bullet_points_true_facts[1],
        widget=widgets.RadioSelect)

    true_fact_30sec = models.StringField(
        blank=True,
        choices=['Definitely True', 'Probably True', 'Probably False', 'Definitely False'],
        label=Constants.bullet_points_true_facts[2],
        widget=widgets.RadioSelect)

    false_fact_too_easy = models.StringField(
        blank=True,
        choices=['Definitely True', 'Probably True', 'Probably False', 'Definitely False'],
        label=Constants.false_facts[0],
        widget=widgets.RadioSelect)

    false_fact_too_hard = models.StringField(
        blank=True,
        choices=['Definitely True', 'Probably True', 'Probably False', 'Definitely False'],
        label=Constants.false_facts[1],
        widget=widgets.RadioSelect)

    false_fact_30sec_unfair = models.StringField(
        blank=True,
        choices=['Definitely True', 'Probably True', 'Probably False', 'Definitely False'],
        label=Constants.gross_exaggeration_unfair[0],
        widget=widgets.RadioSelect)

    false_fact_30sec_fairplay = models.StringField(
        blank=True,
        choices=['Definitely True', 'Probably True', 'Probably False', 'Definitely False'],
        label=Constants.gross_exaggeration_fairplay[0],
        widget=widgets.RadioSelect)


    wantFeedbackOn0 = models.StringField(
        blank=True,
        label=Constants.wantFeedbackOn[0])

    wantFeedbackOn1 = models.StringField(
        blank=True,
        label=Constants.wantFeedbackOn[1])

    wantFeedbackOn2 = models.StringField(
        blank=True,
        label=Constants.wantFeedbackOn[2])


    otherFeedback1 = models.StringField(
        blank=True,
        label='Any other feedback?')


    #### CONTROLS ######################################################

    trivialPursuit1 = models.StringField(
        blank=True,
        choices=['Geography', 'Entertainment', 'History', 'Art & Literature', 'Science & Nature', 'Sports & Leisure'],
        label='Thinking about trivia games like Trivial Pursuit: Which of the following is your favourite category?',
        widget=widgets.RadioSelect)

    trivialPursuit2 = models.StringField(
        blank=True,
        choices=['Geography', 'Entertainment', 'History', 'Art & Literature', 'Science & Nature', 'Sports & Leisure'],
        label='Which is your second-favourite category?',
        widget=widgets.RadioSelect)

    # trivialPursuit3 = models.StringField(
    #     blank=True,
    #     choices=['Geography', 'Entertainment', 'History', 'Art & Literature', 'Science & Nature', 'Sports & Leisure'],
    #     label='And which is your least favourite category?',
    #     widget=widgets.RadioSelect)

    labExperience = models.StringField(
        blank=True,
        choices=['This is the First Time',
                 'Once',
                 'Twice',
                 '3-5 Times',
                 'More Than 5 Times'],
        label='How many times have you participated in an experiment at ESSEXLab?',
        widget=widgets.RadioSelect)


    #### DEMOGRAPHICS ##################################################

    gender = models.StringField(
        blank=True,
        choices=['Male', 'Female', 'Other/ Prefer Not To Say'],
        label='What is your gender?',
        widget=widgets.RadioSelect)

    born = models.IntegerField(
        blank=True,
        label='In which year were you born?',
        min=1920, max=2005)

    atEssex = models.StringField(
        # NB: DO NOT SET blank=True, BECAUSE I AM USING THIS TO FILTER OUT THE NEXT QUESTION
        choices=['Yes', 'No'],
        label='Are you a student or an employee at the University of Essex?',
        widget=widgets.RadioSelect)

    # IF YES:

    positionAtEssex = models.StringField(
        choices=['Undergraduate Student', 'Postgraduate Student (MA or PhD)',
                 'Faculty', 'Administrative Staff', 'Other'],
        blank=True,
        label='What best describes your position at the University of Essex?',
        widget=widgets.RadioSelect)


    # AND

    major = models.StringField(
        blank=True,
        # choices=['Social Sciences', 'Humanities', 'Natural Sciences', 'Health/Social Care/Sport', 'Other'],
        choices=['History', # Humanities
                 'Literature / Film / Theater',
                 'Law',
                 'Philosophy',
                 'Art History',

                 'Biology', # Science and Health
                 'Mathematics',
                 'Psychology',
                 'Computer Science / Electronic Engineering',
                 'Health / Social Care',
                 'Sport',

                 'Psychosocial / Psychoanalytical Studies', # Social Sciences
                 'Economics',
                 'Essex Business School',
                 'Government',
                 'Language / Linguistics',
                 'Sociology',

                 'Other',
                 ],
        label='Which of the following best describe your programme or department?',
        widget=widgets.RadioSelect)


    #### TIPI (BIG5) ###################################################

    extraversion = models.StringField(
        blank=True,
        choices=['Disagree Strongly', 'Disagree Moderately', 'Disagree A Little',
                 'Neither Agree Nor Disagree', 'Agree A Little', 'Agree Moderately', 'Agree Strongly'],
        label='I see myself as extraverted, enthusiastic.',
        widget=widgets.RadioSelect)

    agreeablenessR = models.StringField(
        blank=True,
        choices=['Disagree Strongly', 'Disagree Moderately', 'Disagree A Little',
                 'Neither Agree Nor Disagree', 'Agree A Little', 'Agree Moderately', 'Agree Strongly'],
        label='I see myself as critical, quarrelsome.',
        widget=widgets.RadioSelect)

    conscientiousness = models.StringField(
        blank=True,
        choices=['Disagree Strongly', 'Disagree Moderately', 'Disagree A Little',
                 'Neither Agree Nor Disagree', 'Agree A Little', 'Agree Moderately', 'Agree Strongly'],
        label='I see myself as dependable, self-disciplined.',
        widget=widgets.RadioSelect)

    neuroticism = models.StringField(
        blank=True,
        choices=['Disagree Strongly', 'Disagree Moderately', 'Disagree A Little',
                 'Neither Agree Nor Disagree', 'Agree A Little', 'Agree Moderately', 'Agree Strongly'],
        label='I see myself as anxious, easily upset.',
        widget=widgets.RadioSelect)

    openness = models.StringField(
        blank=True,
        choices=['Disagree Strongly', 'Disagree Moderately', 'Disagree A Little',
                 'Neither Agree Nor Disagree', 'Agree A Little', 'Agree Moderately', 'Agree Strongly'],
        label='I see myself as open to new experiences, complex.',
        widget=widgets.RadioSelect)

    extraversionR = models.StringField(
        blank=True,
        choices=['Disagree Strongly', 'Disagree Moderately', 'Disagree A Little',
                 'Neither Agree Nor Disagree', 'Agree A Little', 'Agree Moderately', 'Agree Strongly'],
        label='I see myself as reserved, quiet.',
        widget=widgets.RadioSelect)

    agreeableness = models.StringField(
        blank=True,
        choices=['Disagree Strongly', 'Disagree Moderately', 'Disagree A Little',
                 'Neither Agree Nor Disagree', 'Agree A Little', 'Agree Moderately', 'Agree Strongly'],
        label='I see myself as sympathetic, warm.',
        widget=widgets.RadioSelect)

    conscientiousnessR = models.StringField(
        blank=True,
        choices=['Disagree Strongly', 'Disagree Moderately', 'Disagree A Little',
                 'Neither Agree Nor Disagree', 'Agree A Little', 'Agree Moderately', 'Agree Strongly'],
        label='I see myself as disorganized, careless.',
        widget=widgets.RadioSelect)

    neuroticismR = models.StringField(
        blank=True,
        choices=['Disagree Strongly', 'Disagree Moderately', 'Disagree A Little',
                 'Neither Agree Nor Disagree', 'Agree A Little', 'Agree Moderately', 'Agree Strongly'],
        label='I see myself as calm, emotionally stable.',
        widget=widgets.RadioSelect)

    opennessR = models.StringField(
        blank=True,
        choices=['Disagree Strongly', 'Disagree Moderately', 'Disagree A Little',
                 'Neither Agree Nor Disagree', 'Agree A Little', 'Agree Moderately', 'Agree Strongly'],
        label='I see myself as conventional, uncreative.',
        widget=widgets.RadioSelect)


    #### NEGATIVE SOCIAL IDENTITY ######################################

    education = models.StringField(
        blank=True,
        choices=['No Formal Qualifications',
                 'Primary Education (Around Age 11)',
                 'GCSE Or Equivalent (Around Age 16)',
                 'A Level Or Equivalent (Around Age 18)',
                 'Some University But No Degree',
                 'Bachelor Degree',
                 'Master Degree',
                 'Doctoral Degree',
                 'Prefer Not To Say'],
        label='What is the highest educational qualification you have?',
        widget=widgets.RadioSelect)


    british = models.StringField(
        blank=True,
        choices=['United Kingdom', 'Europe (Non-UK)', 'Overseas'],
        label='Are you from the UK, from Europe, or from overseas?',
        widget=widgets.RadioSelect)

    # IF NON-UK:

    nationality = models.StringField(
        blank=True,
        label='What is your nationality?',
        )

    income = models.IntegerField(
        blank=True,
        choices=[
            [1, 'No Income'],
            [2, 'Up to GBP 216/ Month Or GBP 2.600 / Year'],
            [3, 'GBP 217 / Month Or GBP 2.600/ year Or More'],
            [4, 'GBP 433 / Month Or GBP 5.200 / year Or More'],
            [5, 'GBP 867 / Month Or GBP 10.400 / year Or More'],
            [6, 'GBP 1.300 / Month Or GBP 15.600 / year Or More'],
            [7, 'GBP 1.733 / Month Or GBP 20.800 / year Or More'],
            [8, 'GBP 2.167 / Month Or GBP 26.000 / year Or More'],
            [9, 'GBP 2.600 / Month Or GBP 31.200 / year Or More'],
            [10, 'GBP 3.033 / Month Or GBP 36.400 / year Or More'],
            [11, 'GBP 3.467 / Month Or GBP 41.600 / year Or More'],
            [12, 'GBP 3.900 / Month Or GBP 46.800 / year Or More'],
            [13, 'GBP 4.333 / Month Or GBP 52.000 / year Or More'],
            [14, 'Do Not Know / Prefer Not To Say'],
        ],
        label='What is your income?',
        widget=widgets.RadioSelect)

    # -- Users will see a menu with '...', but their responses
    # will be recorded as 1, 2, or 3. (RDT -- Forms / Widgets)

    whatAbout = models.StringField(
        blank=True,
        label='If you had to guess: What do think this experiment was about?',
    )

    email = models.StringField(
        blank=True, # blank=True = for an optional field
        label='E-mail address: ONLY enter if you would like to know the results of this study.',
    )

    anythingElse = models.StringField(
        blank=True,
        label="If you have any other comments or if there is anything you would like to tell us please share it here.",
    )


    #### PRETEST FOR MEMORY BASELINE ########################################

    memory_indianReservations = models.StringField(
        blank=True,
        choices=['Definitely saw this question',
                 'Probably saw this question',
                 'Probably did not see this question',
                 'Definitely did not see this question',
                 'Not sure'],
        label='Where in the U.S. are the largest Indian Reservations?',
        widget=widgets.RadioSelect,
    )

    memory_lakeInLibya = models.StringField(
        blank=True,
        choices=['Definitely saw this question',
                 'Probably saw this question',
                 'Probably did not see this question',
                 'Definitely did not see this question',
                 'Not sure'],        label='What is the largest lake in Libya?',
        widget=widgets.RadioSelect,
    )

    memory_mountainsNetherlands = models.StringField(
        blank=True,
        choices=['Definitely saw this question',
                 'Probably saw this question',
                 'Probably did not see this question',
                 'Definitely did not see this question',
                 'Not sure'],
        label='How high is the highest mountain in the Netherlands?',
        widget=widgets.RadioSelect,
    )

    memory_Greenland = models.StringField(
        blank=True,
        choices=['Definitely saw this question',
                 'Probably saw this question',
                 'Probably did not see this question',
                 'Definitely did not see this question',
                 'Not sure'],
        label='Which of the following is NOT a neighbouring country of Greenland?',
        widget=widgets.RadioSelect,
    )

    memory_UK = models.StringField(
        blank=True,
        choices=['Definitely saw this question',
                 'Probably saw this question',
                 'Probably did not see this question',
                 'Definitely did not see this question',
                 'Not sure'],
        label='What is the capital city of the United Kingdom?',
        widget=widgets.RadioSelect,
    )

    memory_France = models.StringField(
        blank=True,
        choices=['Definitely saw this question',
                 'Probably saw this question',
                 'Probably did not see this question',
                 'Definitely did not see this question',
                 'Not sure'],
        label='What is the capital city of France?',
        widget=widgets.RadioSelect,
    )

    memory_FrankfortUS = models.StringField(
        blank=True,
        choices=['Definitely saw this question',
                 'Probably saw this question',
                 'Probably did not see this question',
                 'Definitely did not see this question',
                 'Not sure'],
        label='Frankfort is the capital of which U.S. state?',
        widget=widgets.RadioSelect,
    )

    memory_LondonToEdinburgh = models.StringField(
        blank=True,
        choices=['Definitely saw this question',
                 'Probably saw this question',
                 'Probably did not see this question',
                 'Definitely did not see this question',
                 'Not sure'],
        label='To get from London to Edinburgh you would travel [North/East/South/West]',
        widget=widgets.RadioSelect,
    )

    rememberedSeconds = models.StringField(
        blank=True,
        label='And do you remember how much time you had to answer the questions?',
    )

    readOtherQs = models.StringField(
        blank=True,
        choices=['I read them all carefully', 'I read most carefully', 'I skimmed them all', 'I skimmed most',
                 'I skimmed a few', 'I did not read any of them'],
        label='Thinking about the other teams questions: Did you read them carefully, did you skim read them '
              'or did you not read them at all? ',
        widget=widgets.RadioSelect,
    )

    felt = models.StringField(
        blank=True,
        label='How did this quiz make you feel?',
    )

    howFair = models.StringField(
        blank=True,
        choices=['Very unfair', 'Unfair', 'Fair', 'Very fair'],
        label='How fair or unfair was this quiz?',
        widget=widgets.RadioSelect,
     )

    noticedUnfair = models.StringField(
        blank=True,
        choices=['During the first round (questions 1-4)',
                 'During the second round (5-8)',
                 'During the third round (9-12)',
                 'I did not notice'],
        label='How quickly did you notice that one team got easier questions than the other team?',
        widget=widgets.RadioSelect,
    )


##### END PLAYER ########################################################