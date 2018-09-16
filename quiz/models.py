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
Pub Quiz Experiment / ESSEXLab, June 2018
"""

#####################################################################
# HEROKU / OTREE QUESTIONS
#
# TO DO
# -- CHECK Payoffs !!
# -- Bullet Points
# -- Check whole dataset
#
# -- ASK DOMINIK:
# -- Can't seem to use any methods defined under player that use self.player.in_all_rounds()
# -- (e.g. def set_teams_correct_answers_this_round def set_own_correct_answers_this_round(self). So I am defining those in pages.
# -- (Works but would be prettier in here.)
#
# LARGE GROUPS
# -- Can I have 2 seperate sessions in the same game? (e.g. if I have 20 people, to keep group sizes similar
# across experiments, i.e. 2 groups of 5 people each)
#
#
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

    with open('quiz/easyQs_28.csv') as f:
        easyQs = list(csv.DictReader(f))

    with open('quiz/hardQs_28.csv') as f:
        hardQs = list(csv.DictReader(f))

    with open('quiz/manipulatedQs.csv') as f:
        manipulatedQs = list(csv.DictReader(f))

    with open('quiz/manipulatedQs2.csv') as f:
        manipulatedQs2 = list(csv.DictReader(f))

    num_rounds = 12 # 12 # this is actually the number of questions -- shall do 4 * 3 Qs -- 12 TOO MANY? SET TO 9?
    no_rounds = 3
    questions_per_round = 4
    ret_task_timer = 30
    stakes = c(1) # NB currency unit is set to GBP (in settings.py)
    minimum_payoff = c(5)
    maximum_payoff = c(12)


    ##### BULLET POINTS -- TRUE FACTS #######################################

    # Assign the following to BOTH the unfair and the fair play feedback

    bullet_points_true_facts = [
    'The questions about European capitals were quite easy.', # 1) TRUE
    'Some of the questions about state capitals or provincial capitals were too difficult.', # 2) TRUE
    '''For example, ‘Concord is the capital of which U.S. state?’ People are very unlikely to know that unless they are American.''', # 3) TRUE
    'And the 30 seconds were not a whole lot of time but enough to read the questions and answer them if you knew the answer.', # 4) TRUE
    ]


    ##### BULLET POINTS -- AS BELIEVABLE AS POSSIBLE ######################## PLAN B

    # bullet_points_false_facts_unfair = [
    # '''One of the first questions was 'What is the capital city of Germany'. That was pretty easy.''',
    # 'One team got all difficult questions and the other group team all easy questions.', # False-ish
    # 'It’s just impossible for that to happen by chance.',
    # 'And the 30 seconds we had was barely enough time to read the questions.',
    # ]
    #
    # bullet_points_false_facts_fairplay = [
    # '''One of the first questions was 'What is the capital city of Germany'. That was pretty easy.''',
    # 'Both teams had the exact same chances of getting easy or hard questions.', # False-ish
    # ''' Team A would have done just done just as well if it had received Team B's questions.''',
    # 'And 30 seconds was more than enough time to answer these questions: 10 seconds would have been plenty.',
    # ]

    # # '''Team A's questions were just as hard as team B's questions.''',

    ##### FALSE FACTS -- AS SIMILAR AS POSSIBLE ############################# PLAN A

    bullet_points_false_facts_unfair = [
    '''One of the first questions was 'What is the capital city of Germany'. That was pretty easy.''', # 1) TRUE
    'Too hard: How to get from one place you have never heard of to another place you have never heard of.', # 2) TRUE
    '''Some of the places in that quiz don’t even exist.''', # 3) FALSE
    'And the 30 seconds we had was barely enough time to read the questions.' # GROSS EXXAGGERATION
    ]

    bullet_points_false_facts_fairplay = [
    '''One of the first questions was 'What is the capital city of Germany'. That was pretty easy.''', # 1) TRUE
    'Too hard: How to get from one place you have never heard of to another place you have never heard of.', # 2) TRUE
    '''Some of the places in that quiz don’t even exist.''', # 3) FALSE -- BUT DO THESE PEOPLE HAVE ANY MOTIVATION TO BELIEVE IN THIS?
    'And 30 seconds was more than enough time to answer these questions: 10 seconds would have been plenty.' # GROSS EXXAGGERATION
    ]

    # PROBLEM: Team B is more likely than Team A to believe in this!

    # Would Team A want to believe this?
    # Would Team B want to believe this?

    # The hard questions Team A got

    # Problem: Are people more likely to believe in the false facts attached to the fair play treatment than they
    # are to believe in the false facts attached to the unfair treatment?


# NEW NEW NEW NEW

    false_facts = [
    '''One of the first questions was 'What is the capital city of Germany'. That was pretty easy.''', # 1) TRUE
    'Too hard: How to get from one place you have never heard of to another place you have never heard of.', # 2) FALSE
    '''Some of the places in that quiz don’t even exist.''', # 3) FALSE-ISH
    ]

    gross_exaggeration_fairplay = [
        'And 30 seconds was more than enough time to answer these questions: 10 seconds would have been plenty.',
    ]

    gross_exaggeration_unfair = [
        'And the 30 seconds we had was barely enough time to read the questions.',
    ]

    wantFeedbackOn = [
        'Were there any questions you thought were too easy?',
        'Were there any questions you thought were too difficult?',
        'What did you think of the 30 second time limit?',
    ]

    fairplay_template = 'quiz/fairplay.html'  # NB Creating templates so I don't have to copy and paste the text into p0_repeat
    unfair_template = 'quiz/unfair.html'

    template_repeat_fairplay_feedback1 = 'quiz/repeat_fairplay_feedback1.html'
    template_repeat_unfair_feedback2 = 'quiz/repeat_unfair_feedback2.html'
    template_repeat_unfair_feedback1 = 'quiz/repeat_unfair_feedback1.html'
    template_repeat_fairplay_feedback2 = 'quiz/repeat_fairplay_feedback2.html'

##### END CONSTANTS #####################################################




##### SUBSESSION ########################################################

class Subsession(BaseSubsession):

# NB: If a game is repeated for multiple rounds, each round is a subsession.

    def before_session_starts(self):

        # Create an integer that is equal to each player's id_in_group. Doing this because I need people's id_in_group
        # to assign them to A (even) or B (odd) BUT cannot access id_in_group in creating_session.
        # --> The id_in_group attribute is assigned AFTER THE SESSION STARTED.

        # https://stackoverflow.com/questions/39125370/otree-how-to-access-the-players-id-from-the-player-class-in-model-py

        for p in self.get_players():
            p.random_id = p.id_in_group


    def creating_session(self):

        ##### IN ROUND 1 ################################################

        if self.round_number == 1:

            for p in self.get_players():

                ##### TEAMS #############################################

                # NB Assigning 50% of the sample to 'A' and 50% to Team 'B'
                # Creating a random number between 0 and 100, if it is below or equal to 25, assign to Team A,
                # else assign to Team B.

                # if random.random() <= 0.5:
                #     p.treatment = 'A'
                #     p.participant.vars['treatment'] = 'A'
                # else:
                #     p.treatment = 'B'
                #     p.participant.vars['treatment'] = 'B'
                #

                # NEW: Force equal group sizes

                # if self.player.id_in_group % 2 == 0: # Failed to create session: "'Subsession' object has no attribute 'player'"
                #     p.treatment = 'A'
                #     p.participant.vars['treatment'] = 'A'
                # else:
                #     p.treatment = 'B'
                #     p.participant.vars['treatment'] = 'B'

                if p.random_id % 2 == 0: # EVEN NUMBERS --> A
                    p.treatment = 'A'
                    p.participant.vars['treatment'] = 'A'
                else:
                    p.treatment = 'B' # ODD NUMBERS --> B
                    p.participant.vars['treatment'] = 'B'


                ##### WHICH FEEDBACK CONTAINS FALSE FACTS ###############

                ## NB: Randomize which feedback contains factually inaccurate bullet points

                if random.random() <= 0.5:
                    p.falsefeedback = 'unfair'
                    p.participant.vars['falsefeedback'] = 'unfair'
                else:
                    p.falsefeedback = 'fairplay'
                    p.participant.vars['falsefeedback'] = 'fairplay'

                p.participant.vars['falsefeedback'] = random.choice(['fairplay','unfair'])

                # self.participant.vars['falsefeedback'] = self.firstfeedback  # Um Zugriff im Rest des Experiments zu ermoeglichen (i.e. auch in anderen apps).
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


                # OR ASSIGN FIRST PERSON TO A AND SECOND PERSON TO B? (To keep group sizes the same?)

        # def role(self):
        #     if self.id_in_group == 1:
        #         return 'proposer'
        #     else:
        #         return 'responder'


            ##### RANDOM SAMPLE OF QUESTIONS FOR A AND B #################

            ## NB: Here (i.e. in round 1) I am creating 2 lists of easy Qs and hard Qs,
            # randomly drawn from the 2 csv files of easy and hard questions. (This is to shuffle them.)

            easyQs_random = random.sample(Constants.easyQs, len(Constants.easyQs))
            self.session.vars['easyQs_random'] = easyQs_random

            hardQs_random = random.sample(Constants.hardQs, len(Constants.hardQs))
            self.session.vars['hardQs_random'] = hardQs_random

            self.session.vars['manipulatedQs'] = Constants.manipulatedQs # NEW
            self.session.vars['manipulatedQs2'] = Constants.manipulatedQs2 # NEW

            ## NB session.vars is a dictionary just like participant.vars. The difference is that if you set a
            # variable in session.vars, it will apply to all participants in the session, not just one.


            # ##### FEEDBACK BULLET POINTS ############################
            #
            # # Add the last bullet point (complaints about time) to the 2 false facts bullet points that are the
            # # same across the unfair and the fairplay condition
            #
            # bullet_points_true_facts = Constants.bullet_points_true_facts.copy()
            #
            # # bullet_points_false_facts_fairplay = Constants.false_facts.copy()
            # # bullet_points_false_facts_unfair = Constants.false_facts.copy()
            # # gross_exaggeration_fairplay = Constants.gross_exaggeration_fairplay.copy()
            # # gross_exaggeration_unfair = Constants.gross_exaggeration_unfair.copy()
            # #
            # # bullet_points_false_facts_fairplay.append(gross_exaggeration_fairplay[0])
            # # bullet_points_false_facts_unfair.append(gross_exaggeration_unfair[0])
            #
            # bullet_points_false_facts_fairplay = Constants.false_facts.copy()
            # bullet_points_false_facts_unfair = Constants.false_facts.copy()
            # gross_exaggeration_fairplay = Constants.gross_exaggeration_fairplay.copy()
            # gross_exaggeration_unfair = Constants.gross_exaggeration_unfair.copy()
            #
            # # New: instead of building the lists here I build them in Constants
            #
            # bullet_points_false_facts_fairplay = Constants.bullet_points_false_facts_fairplay.copy()
            # bullet_points_false_facts_unfair = Constants.bullet_points_false_facts_unfair.copy()
            #
            # self.session.vars['bullet_points_true_facts'] = bullet_points_true_facts
            # self.session.vars['bullet_points_false_facts_fairplay'] = bullet_points_false_facts_fairplay
            # self.session.vars['bullet_points_false_facts_unfair'] = bullet_points_false_facts_unfair
            #


            ##### QUIZ QUESTIONS ################################################

            # Creating lists of questions for Team A and B
            # Different Probabilities: 80/20 easyQs for Team A, 20/80 for Team B

            # The FIRST 2 QUESTIONS ARE THE QUESTIONS I AM LYING ABOUT.

            # FIRST QUESTION:
            # One team: ‘Concord is the capital of which U.S. state?
            # Other Team: ‘What is the capital city of Germany?’

            # SECOND QUESTION:
            # One team: 99% chance: How to get from Edmonton to Calgary. 1% chance: 'Which oceans border Switzerland?’.
            # Other Team: Capital of Spain. [Extra set of Qs]
            # —> Team B is most likely to get Edmonton —> Calgary and Team A is most likely to get the capital of Italy.

            teamA_Qs = list() # Empty list to store the questions for Team A
            teamB_Qs = list() # Empty list to store the questions for Team A

            # First, make sure that the Qs I lie about in the bullet points make it onto the quiz.

            # [1st item in manipulatedQs]: ‘Concord is the capital of which U.S. state?
            # [1st item in manipulatedQs]: ‘What is the capital city of Germany?’

            r1 = random.random()

            if r1 > .2:
                teamA_Qs.append(Constants.manipulatedQs[0]) # Capital of GER
                teamB_Qs.append(Constants.manipulatedQs[1]) # Concord is the capital of which US state
            elif r1 <= .2:
                teamA_Qs.append(Constants.manipulatedQs[1]) # Concord is the capital of which US state
                teamB_Qs.append(Constants.manipulatedQs[0]) # Capital of GER

            # [3rd item in manipulatedQs]: Capital of SPAIN
            # [4th item in manipulatedQs]: Edmonton --> Calgary 99%
            # [5th item in manipulatedQs]: Which ocean borders Switzerland 1%

            # Never assigning oceans in Switzerland:

            r2 = random.random()

            if r2 > .2:
                teamA_Qs.append(Constants.manipulatedQs2[0]) # Capital of SPAIN
                teamB_Qs.append(Constants.manipulatedQs2[1]) # Edmonton --> Calgary 99%
            elif r2 <= .2:
                teamA_Qs.append(Constants.manipulatedQs2[1]) # Edmonton --> Calgary 99%
                teamB_Qs.append(Constants.manipulatedQs2[0]) # Capital of SPAIN

            # Giving oceans in Switzerland a 1% chance

            # r2 = random.random()
            # r3 = random.random()
            #
            # if r2 > .2 and r3 < .99:
            #     teamA_Qs.append(Constants.manipulatedQs2[0]) # Capital of SPAIN
            #     teamB_Qs.append(Constants.manipulatedQs2[1]) # Edmonton --> Calgary 99%
            # elif r2 > .2 and r3 >= .99:
            #     teamA_Qs.append(Constants.manipulatedQs2[0]) # Capital of SPAIN
            #     teamB_Qs.append(Constants.manipulatedQs2[2]) # Oceans Switzerland 1%
            #
            #
            # elif r2 <= .2 and r3 < .99:
            #     teamA_Qs.append(Constants.manipulatedQs2[1]) # Edmonton --> Calgary 99%
            #     teamB_Qs.append(Constants.manipulatedQs2[0]) # Capital of SPAIN
            #
            # elif r2 <= .2 and r3 >= .99:
            #     teamA_Qs.append(Constants.manipulatedQs2[1]) # Edmonton --> Calgary 99%
            #     teamB_Qs.append(Constants.manipulatedQs2[3]) # Oceans Switzerland 1%


            # Next, add the other 28 questions

            random28 = random.sample(range(1, 100), 28) # generating 28 random integers between 1 and 100
            range28 = list(range(0, 28, 1))  # generating a list of 28 numbers ranging from 0, 1, 2, 3 ... to 29

            for number in range28:
                if random28[number] > 20: # if the 1st, 2nd, 3rd etc of my 28 random integers is higher than 20
                    teamA_Qs.append(easyQs_random[number])
                    teamB_Qs.append(hardQs_random[number])
                else:
                    teamA_Qs.append(hardQs_random[number])
                    teamB_Qs.append(easyQs_random[number])

            self.session.vars['teamA_Qs'] = teamA_Qs
            self.session.vars['teamB_Qs'] = teamB_Qs


            # for number in range30:                # SAME SAME
            #     r = random.random()
            #     if r > .2:
            #         teamA_Qs.append(easyQs_random[number])
            #         teamB_Qs.append(hardQs_random[number])
            #     else:
            #         teamA_Qs.append(hardQs_random[number])
            #         teamB_Qs.append(easyQs_random[number])

            # random30 = random.sample(range(1, 100), 30) # generating 30 random integers between 1 and 100
            # range30 = list(range(0, 30, 1))  # generating a list of 30 numbers ranging from 0, 1, 2, 3 ... to 29
            #
            # teamA_Qs = list() # Empty list to store the questions for Team A
            # teamB_Qs = list() # Empty list to store the questions for Team A
            #
            # for number in range30: # THIS WORKS IN ATOM
            #     if random30[number] > 20: # if the 1st, 2nd, 3rd etc of my 30 random integers is higher than 20
            #     # if random30[number] > 50:                                 # UNCOMENT FOR CONTROL GAMES! (50/50)
            #         teamA_Qs.append(easyQs_random[number])
            #         teamB_Qs.append(hardQs_random[number])
            #     else:
            #         teamA_Qs.append(hardQs_random[number])
            #         teamB_Qs.append(easyQs_random[number])
            #
            # # for number in range30:                # SAME SAME
            # #     r = random.random()
            # #     if r > .2:
            # #         teamA_Qs.append(easyQs_random[number])
            # #         teamB_Qs.append(hardQs_random[number])
            # #     else:
            # #         teamA_Qs.append(hardQs_random[number])
            # #         teamB_Qs.append(easyQs_random[number])
            #
            # self.session.vars['teamA_Qs'] = teamA_Qs
            # self.session.vars['teamB_Qs'] = teamB_Qs


            # ##### QUIZ QUESTIONS ################################################
            #
            # # Creating lists of questions for Team A and B
            #
            # # Different Probabilities: 80/20 easyQs for Team A, 20/80 for Team B
            #
            # random30 = random.sample(range(1, 100), 30) # generating 30 random integers between 1 and 100
            # range30 = list(range(0, 30, 1))  # generating a list of 30 numbers ranging from 0, 1, 2, 3 ... to 29
            #
            # teamA_Qs = list() # Empty list to store the questions for Team A
            # teamB_Qs = list() # Empty list to store the questions for Team A
            #
            # for number in range30: # THIS WORKS IN ATOM
            #     if random30[number] > 20: # if the 1st, 2nd, 3rd etc of my 30 random integers is higher than 20
            #     # if random30[number] > 50:                                 # UNCOMENT FOR CONTROL GAMES! (50/50)
            #         teamA_Qs.append(easyQs_random[number])
            #         teamB_Qs.append(hardQs_random[number])
            #     else:
            #         teamA_Qs.append(hardQs_random[number])
            #         teamB_Qs.append(easyQs_random[number])
            #
            # # for number in range30:                # SAME SAME
            # #     r = random.random()
            # #     if r > .2:
            # #         teamA_Qs.append(easyQs_random[number])
            # #         teamB_Qs.append(hardQs_random[number])
            # #     else:
            # #         teamA_Qs.append(hardQs_random[number])
            # #         teamB_Qs.append(easyQs_random[number])
            #
            # self.session.vars['teamA_Qs'] = teamA_Qs
            # self.session.vars['teamB_Qs'] = teamB_Qs



        ##### DEFINE QUIZ QUESTIONS ########################################

        for p in self.get_players():

            question_data = p.current_question()
            p.question_id = question_data['id']
            p.question = question_data['question']
            p.solution = question_data['solution']
            # p.difficulty = question_data['difficulty'] # NOPE

            other_question_data = p.other_current_question()
            p.other_question_id = other_question_data['id']
            p.other_question = other_question_data['question']
            p.other_solution = other_question_data['solution']
            # p.other_difficulty = other_question_data['difficulty'] # NOPE

##### END SUBSESSION ####################################################




##### GROUP #############################################################

# NB -- player.in_previous_rounds() and player.in_all_rounds() each return a list of players representing the
# same participant in previous rounds of the same app. The difference is that in_all_rounds() includes the current
# round's player. (RTD -- Apps & Rounds)


class Group(BaseGroup): # Q: Can I define stuff at a group level even if I don't have any groups (or just one)?

    ##### ONCE ##############################################################

    n_team_a = models.IntegerField() # auch into participants!
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

        team_a_avg_correct_this_round = int(100 * (self.session.vars['team_a_is_correct_this_round'] / self.session.vars['n_team_a_consented']) / Constants.questions_per_round)
        team_b_avg_correct_this_round = int(100 * (self.session.vars['team_b_is_correct_this_round'] / self.session.vars['n_team_b_consented']) / Constants.questions_per_round)

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

        team_a_avg_is_correct = int(100 * (self.session.vars['team_a_is_correct_total'] / self.session.vars['n_team_a_consented']) / Constants.num_rounds)
        team_b_avg_is_correct = int(100 * (self.session.vars['team_b_is_correct_total'] / self.session.vars['n_team_b_consented']) / Constants.num_rounds)

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
    treatment_new = models.StringField() # Team A or Team B
    random_id = models.IntegerField() # 1 Team A or 2 Team B
    falsefeedback = models.StringField() # Which feedback contains false facts (fairplay or unfair)
    firstfeedback = models.StringField() # Which feedback they receive first # TO DO

    ##### QUESTIONS #####################################################

    question_id = models.IntegerField()
    question = models.StringField()
    solution = models.StringField()
    submitted_answer = models.StringField(widget=widgets.RadioSelect)
    # difficulty = models.StringField() # NOPE

    is_correct = models.BooleanField() # FILL!

    other_question_id = models.IntegerField()
    other_question = models.StringField()
    other_solution = models.StringField()
    # other_difficulty = models.StringField() # NOPE

    ##### INDIVIDUAL PAYOFFS ################################################

    payoff_score = models.IntegerField()  # Each player has a payoff field. I use payoff to denote the payoff a player gets in each round

    is_correct_this_round = models.IntegerField()
    earned_this_round = models.CurrencyField()

    is_correct_total = models.IntegerField()  # Total number of correct answers
    earned_total = models.CurrencyField()  # Money earned in all rounds
    half_own_earnings = models.CurrencyField() # NEW

    # payoff_unrounded = models.CurrencyField() # NEW
    # payoff = models.CurrencyField()  # Payoff (half of total_payoff plus add_on)
    paid = models.CurrencyField()


    # STUFF THAT SHOULD BE DEFINED AT A GROUP LEVEL -- BUT DOESNT SHOW UP!!

    ##### ONCE ############################################################## NEW NEW NEW

    # n_team_a = models.IntegerField() # auch into participants!
    # n_team_b = models.IntegerField()

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


    def set_group_vars_for_player(self):

        for p in self.get_players():

            p.n_team_a_consented = self.session.vars['n_team_a_consented']
            p.n_team_b_consented = self.session.vars['n_team_b_consented']

            p.team_a_is_correct_this_round = self.session.vars['team_a_is_correct_this_round']
            p.team_b_is_correct_this_round = self.session.vars['team_b_is_correct_this_round']

            p.team_a_avg_correct_this_round = self.session.vars['team_a_avg_correct_this_round']
            p.team_b_avg_correct_this_round = self.session.vars['team_b_avg_correct_this_round']

            p.team_a_is_correct_total = self.session.vars['team_a_is_correct_total']
            p.team_b_is_correct_total = self.session.vars['team_b_is_correct_total']

            p.team_a_avg_correct_this_round = self.session.vars['team_a_earned_total']
            p.team_b_avg_correct_this_round = self.session.vars['team_b_earned_total']

            p.team_a_avg_payoff = self.session.vars['team_a_avg_payoff']
            p.team_b_avg_payoff = self.session.vars['team_b_avg_payoff']

            p.team_a_avg_is_correct = self.session.vars['team_a_avg_is_correct']
            p.team_b_avg_is_correct = self.session.vars['team_b_avg_is_correct']

            p.team_a_add_on = self.session.vars['team_a_add_on']
            p.team_b_add_on = self.session.vars['team_b_add_on']

            p.team_a_pot = self.session.vars['team_a_pot']
            p.team_b_pot = self.session.vars['team_b_pot']



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


    # def set_paid(self):
    #
    #     for p in self.subsession.get_players():
    #
    #         if self.participant.vars['payoff'] < Constants.minimum_payoff:
    #             p.paid = Constants.minimum_payoff
    #         else:
    #             p.paid = p.payoff


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
        # blank=True,
        choices=['''Both teams' questions will be about the same difficulty.''',
                 'Team A will get an easier question than Team B.',
                 'Team B will get an easier question than Team A.',
                 'One team will get an easier question than the other team. Whether that is Team A or Team B is a 50-50 chance.',
                 '''Don't know. / Impossible to say.'''],
        # label='''Before we move on to the last question: If you had to predict how easy or how difficult the
        # last question will be would you say that:''',
        label='',
        widget=widgets.RadioSelect)




    # # In one question (slider):
    #
    # expectationsLastQSlider = models.StringField(
    #     blank=True,
    #     label='',
    #     # label='''Before we move on to the last question we are curious to know what you expect.
    #     # Here is a scale from 1 to 100, where 1 means 'the odds are heavily in favour
    #     # of Team A' (put differently, you expect Team A to get an easier question than Team B),
    #     # 50 means 'the odds are about the same for both teams', and 100 means 'the odds are heavily in
    #     # favour of Team B' (put differently, you expect Team B to get an easier question than Team A)''',
    #     widget = widgets.Slider(attrs={'step': '1.0'}))


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
        # blank=True,
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
        # blank=True,
        choices=['Definitely Fair', 'Probably Fair', 'Probably Not Fair', 'Definitely Not Fair'],
        label='And would you say it was fair that Team A got a higher payoff than Team B?', # 'OK' / 'legitimate'?
        widget=widgets.RadioSelect)

    byChanceTeamAEasierQs = models.IntegerField( # 15.6. Changed this from StringField
        # blank=True,
        label='',
        widget = widgets.Slider(attrs={'step': '1.0'}))

    byChanceTeamBEasierQs = models.IntegerField( # 15.6. Changed this from StringField
        # blank=True,
        label='',
        widget = widgets.Slider(attrs={'step': '1.0'}))

    # Could also ask something like: On a scale from grossly unfair, no way this was by chance to could have happened
    # by chance

# IF Team B got easier Qs:

    legitTeamAhigherPayoffs = models.StringField(
        # blank=True,
        choices=['Yes', 'No', '''Don't know'''],
        label='''And would you say that Team A's higher payoffs were legitimate? Put differently, 
        does Team A deserve to be paid more, on average, than Team B?''',
        widget=widgets.RadioSelect)

    legitTeamBhigherPayoffs = models.StringField(
        # blank=True,
        choices=['Yes', 'No', '''Don't know'''],
        label='''And would you say that Team B's higher payoffs were legitimate? Put differently, 
        does Team B deserve to be paid more, on average, than Team A?''',
        widget=widgets.RadioSelect)

    fair = models.IntegerField(
        label='',
        widget=widgets.Slider(attrs={'step': '1.0'}))

# Earlier on, we asked you to place to 2 other people on a scale from def fair to unfair. Now we are interested in what you think...

    #### STABILITY STATUS DIFFERENCES ##################################

# ... AFTER OWN FEEDBACK

    feedbackMakesDifference = models.StringField(
        # blank=True,
        choices=['Very Likely', 'Somewhat Likely', 'Somewhat Unlikely', 'Very Unlikely'],
        label='',
        # label=''' At university (and elsewhere!) you are often asked for feedback.  For instance,
        # restaurants ask for feedback on their menu, and professors ask for feedback on their classes.
        # We asked you for feedback about a geography quiz.
        # Thinking about the two people's feedback you read earlier: How likely do think it is that these voices are
        # heard?  Put different, how likely do you think it is the researchers conducting this
        # study will change the quiz and implement the things proposed in these two people's feedback?''',
        # label='''People are often asked for feedback. Sometimes feedback is heard; other times it
        # is not. Thinking about the two people's feedback you read, how likely do you think it is that this
        # sort of feeback changes things?''',
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



    #### RATING BULLET POINTS TRUE-FALSE ############################### NEW NEW

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

    true_fact_too_hard2 = models.StringField(
        blank=True,
        choices=['Definitely True', 'Probably True', 'Probably False', 'Definitely False'],
        label=Constants.bullet_points_true_facts[2],
        widget=widgets.RadioSelect)

    true_fact_30sec = models.StringField(
        blank=True,
        choices=['Definitely True', 'Probably True', 'Probably False', 'Definitely False'],
        label=Constants.bullet_points_true_facts[3],
        widget=widgets.RadioSelect)



    false_fact_too_easy = models.StringField(
        blank=True,
        choices=['Definitely True', 'Probably True', 'Probably False', 'Definitely False'],
        label=Constants.bullet_points_false_facts_unfair[0],
        widget=widgets.RadioSelect)

    false_fact_too_hard = models.StringField(
        blank=True,
        choices=['Definitely True', 'Probably True', 'Probably False', 'Definitely False'],
        label=Constants.bullet_points_false_facts_unfair[1],
        widget=widgets.RadioSelect)

    false_fact_too_hard2 = models.StringField(
        blank=True,
        choices=['Definitely True', 'Probably True', 'Probably False', 'Definitely False'],
        label=Constants.bullet_points_false_facts_unfair[2],
        widget=widgets.RadioSelect)

    false_fact_30sec_unfair = models.StringField(
        blank=True,
        choices=['Definitely True', 'Probably True', 'Probably False', 'Definitely False'],
        label=Constants.bullet_points_false_facts_unfair[3],
        widget=widgets.RadioSelect)

    false_fact_30sec_fairplay = models.StringField(
        blank=True,
        choices=['Definitely True', 'Probably True', 'Probably False', 'Definitely False'],
        label=Constants.bullet_points_false_facts_fairplay[3],
        widget=widgets.RadioSelect)


    #### MANIPULATION CHECK ##############################################

    fairplay_manipulation_check = models.IntegerField(
        label='',
        # blank=True,
        # label='''Here is a scale from 'definitely unfair'(0) to 'definitely fair' (100).
        # If you had to place this person somewhere on this scale where would you place this person?
        # That is, how fair or unfair do you think this person thought the quiz was?''',
        widget = widgets.Slider(attrs={'step': '1.0'}))

    unfair_manipulation_check = models.IntegerField(
        label='',
        # blank=True,
        # label='''Here is a scale from 'definitely unfair' (0) to 'definitely fair' (100).
        # If you had to place this person's judgment of this game, where would you place it? Put differently,
        # how fair or unfair did this person this the game was?''',
        widget = widgets.Slider(attrs={'step': '1.0'}))


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
        # blank=True,
        choices=['Geography', 'Entertainment', 'History', 'Art & Literature', 'Science & Nature', 'Sports & Leisure'],
        label='Thinking about trivia games like Trivial Pursuit: Which of the following is your favourite category?',
        # widget=widgets.RadioSelect
    )

    trivialPursuit2 = models.StringField(
        # blank=True,
        choices=['Geography', 'Entertainment', 'History', 'Art & Literature', 'Science & Nature', 'Sports & Leisure'],
        label='Which is your second-favourite category?',
        # widget=widgets.RadioSelect
    )

    trivialPursuit3 = models.StringField(
        # blank=True,
        choices=['Geography', 'Entertainment', 'History', 'Art & Literature', 'Science & Nature', 'Sports & Leisure'],
        label='Which is your third favourite category?',
        # widget=widgets.RadioSelect
    )

    likeTrivia = models.StringField(
        # blank=True,
        choices=['Dislike A Lot', 'Dislike', 'Neither Like Nor Dislike', 'Like', 'Like A Lot'],
        label='And how much to you like pub quizzes and trivia games?',
        # label='How much to you like trivia or pub quiz games like, for instance, Trivial Pursuit?',
        # widget=widgets.RadioSelect
    )

    rigged = models.StringField(
        # blank=True,
        choices=['Very Unlikely', 'Unlikely', 'Likely', 'Very Likely'],
        label='Thinking back about this geography quiz: How likely do you think it is that any of the places in that quiz do not exist? ',
        # label='How much to you like trivia or pub quiz games like, for instance, Trivial Pursuit?',
        # widget=widgets.RadioSelect
    )

    labExperience = models.StringField(
        # blank=True,
        choices=['This is the First Time',
                 'Once',
                 'Twice',
                 '3-5 Times',
                 'More Than 5 Times'],
        label='How many times have you participated in an experiment at ESSEXLab?',
        widget=widgets.RadioSelect)


    #### DEMOGRAPHICS ##################################################

    gender = models.StringField(
        # blank=True,
        choices=['Male', 'Female', 'Other/ Prefer Not To Say'],
        label='What is your gender?',
        widget=widgets.RadioSelect)

    born = models.IntegerField(
        # blank=True,
        label='In which year were you born? (YYYYY)',
        min=1920, max=2005)

    atEssex = models.StringField(
        # NB: DO NOT SET blank=True, BECAUSE I AM USING THIS TO FILTER OUT THE NEXT QUESTION
        choices=['Yes', 'No'],
        label='Are you a student or an employee at the University of Essex?',
        widget=widgets.RadioSelect)

    # IF YES:

    positionAtEssex = models.StringField(
        blank=True,
        choices=['Undergraduate Student', 'Postgraduate Student (MA/MSc)', 'Postgraduate Student (PhD)',
                 'Faculty', 'Administrative Staff', 'Other'],
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
        # blank=True,
        choices=['Disagree Strongly', 'Disagree Moderately', 'Disagree A Little',
                 'Neither Agree Nor Disagree', 'Agree A Little', 'Agree Moderately', 'Agree Strongly'],
        label='Extraverted, Enthusiastic.')


    agreeablenessR = models.StringField(
        # blank=True,
        choices=['Disagree Strongly', 'Disagree Moderately', 'Disagree A Little',
                 'Neither Agree Nor Disagree', 'Agree A Little', 'Agree Moderately', 'Agree Strongly'],
        label='Critical, Quarrelsome.')

    conscientiousness = models.StringField(
        # blank=True,
        choices=['Disagree Strongly', 'Disagree Moderately', 'Disagree A Little',
                 'Neither Agree Nor Disagree', 'Agree A Little', 'Agree Moderately', 'Agree Strongly'],
        label='Dependable, Self-Disciplined.')

    neuroticism = models.StringField(
        # blank=True,
        choices=['Disagree Strongly', 'Disagree Moderately', 'Disagree A Little',
                 'Neither Agree Nor Disagree', 'Agree A Little', 'Agree Moderately', 'Agree Strongly'],
        label='Anxious, Easily upset.')

    openness = models.StringField(
        # blank=True,
        choices=['Disagree Strongly', 'Disagree Moderately', 'Disagree A Little',
                 'Neither Agree Nor Disagree', 'Agree A Little', 'Agree Moderately', 'Agree Strongly'],
        label='Open to new experiences, Complex.')

    extraversionR = models.StringField(
        # blank=True,
        choices=['Disagree Strongly', 'Disagree Moderately', 'Disagree A Little',
                 'Neither Agree Nor Disagree', 'Agree A Little', 'Agree Moderately', 'Agree Strongly'],
        label='Reserved, Quiet.')

    agreeableness = models.StringField(
        # blank=True,
        choices=['Disagree Strongly', 'Disagree Moderately', 'Disagree A Little',
                 'Neither Agree Nor Disagree', 'Agree A Little', 'Agree Moderately', 'Agree Strongly'],
        label='Sympathetic, Warm.')

    conscientiousnessR = models.StringField(
        # blank=True,
        choices=['Disagree Strongly', 'Disagree Moderately', 'Disagree A Little',
                 'Neither Agree Nor Disagree', 'Agree A Little', 'Agree Moderately', 'Agree Strongly'],
        label='Disorganized, Careless.')

    neuroticismR = models.StringField(
        # blank=True,
        choices=['Disagree Strongly', 'Disagree Moderately', 'Disagree A Little',
                 'Neither Agree Nor Disagree', 'Agree A Little', 'Agree Moderately', 'Agree Strongly'],
        label='Calm, Emotionally stable.')

    opennessR = models.StringField(
        # blank=True,
        choices=['Disagree Strongly', 'Disagree Moderately', 'Disagree A Little',
                 'Neither Agree Nor Disagree', 'Agree A Little', 'Agree Moderately', 'Agree Strongly'],
        label='Conventional, Uncreative.')


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
                 'Do Not Know / Prefer Not To Say'],
        label='What is the highest educational qualification you have?',
        # widget=widgets.RadioSelect
    )


    british = models.StringField(
        # blank=True,
        choices=['United Kingdom',
                 'Northern Europe (except UK)',
                 'Western Europe',
                 'Southern Europe',
                 'Eastern Europe',
                 'Caucasus',

                 'North America',
                 'Central America',
                 'Carribean',
                 'South America',

                 'Central Asia',
                 'Eastern Asia',
                 'Southern Asia',
                 'Southeastern Asia',

                 'Northern Africa (except Egypt)',
                 'Middle East',
                 'Eastern Africa',
                 'Middle Africa',
                 'Southern Africa',

                 'Australia / Oceania',
                 'Do Not Know / Prefer Not To Say'
                 ],
        label='Where are you from? Please indicate the region where you grew up. If you grew up in different countries'
              ' please choose the one when you spent most of your secondary school years.',
        # widget=widgets.RadioSelect
    )


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
        # widget=widgets.RadioSelect
    )

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


##### END PLAYER ########################################################