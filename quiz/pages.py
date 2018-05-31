from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants
from random import *
from random import shuffle


##### CONSENT ###############################################################

class welcome(Page):
    def is_displayed(self):
        return self.round_number == 1


class consent(Page):

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self): # NEU -- adapted von Dominik
        self.player.participant.vars['consented'] = True
        self.player.consented = True

    def vars_for_template(self):
        return {
            'treatment': self.participant.vars['treatment'],
            'falsefeedback': self.participant.vars['falsefeedback'],
            'firstfeedback': self.participant.vars['firstfeedback'],
        }

##### INTRO #################################################################

class intro(Page):
    def is_displayed(self):
        return self.round_number == 1

class intro2(Page):
    def is_displayed(self):
        return self.round_number == 1

class intro3(Page):
    def is_displayed(self):
        return self.round_number == 1


##### TEAM ##################################################################

class allocatedTeam(Page):
    # wait_for_all_groups = True
    def is_displayed(self):
        return self.round_number == 1




##### PRACTICE ROUND ########################################################

class practice_question(Page):
    form_model = 'player'
    form_fields = ['submitted_answer']
    timeout_seconds = 30

    def is_displayed(self):
        return self.round_number == 1

    def submitted_answer_choices(self):
        q = self.player.practice_question()
        return [
            q['choice1'],
            q['choice2'],
            q['choice3'],
            q['choice4'],
        ]

    def vars_for_template(self):
        return {
            'treatment': self.participant.vars['treatment'],
        }


class other_practice_question(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        q = self.player.other_practice_question()
        return {
            'choice1': q['choice1'],
            'choice2': q['choice2'],
            'choice3': q['choice3'],
            'choice4': q['choice4'],
            'treatment': self.participant.vars['treatment'],
        }


##### GREAT INTRODUCTIONS ###################################################

class introPaidQuiz(Page): # EITHER DEFINE GROUP SIZES HERE OR IN WaitToStart
    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        self.group.set_team_sizes() # THIS WORKS HERE JUST AS WELL AS DOWN IN THE NEXT WAITPAGE (can access it in later pages)




##### WAIT FOR ALL PARTICIPANTS TO ARRIVE ###################################


# class WaitToStart(WaitPage): # EITHER DEFINE GROUP SIZES HERE OR IN introPaidQuiz
#
#     def is_displayed(self):
#         return self.round_number == 1
#
#     def after_all_players_arrive(self):
#         self.group.set_team_sizes() # THIS WORKS (can access it in later pages) (NB: Kind of already defined this above)
#
#     body_text = "Waiting for your team mates to get ready for Round 1." # CHECK IF THIS WORKS


# self.player and self.participant cannot be referenced inside after_all_players_arrive,
# which is executed only once for the entire group.

# Any code you define here will be executed once all players have arrived at the wait page.
# For example, this is a good place to set the players' payoffs or determine the winner.

# Note, you can't reference self.player inside after_all_players_arrive, because the code is
# executed once for the entire group, not for each individual player.
# (However, you can use self.player in a wait page's is_displayed.) (RTD Waitpages)



##### QUIZ ##################################################################

## To create a form, 1st go to models.py and define fields on your Player or Group. Then, in your Page class, you
# can choose which of these fields to include in the form. You do this by setting form_model = 'player' or
# form_model = 'group', and then set form_fields to the list of fields you want in your form (RTD -- Forms).

class question(Page):
    form_model = 'player'
    form_fields = ['submitted_answer']
    timeout_seconds = 30 # ENOUGH?

    def submitted_answer_choices(self):
        q = self.player.current_question()
        return [
            q['choice1'],
            q['choice2'],
            q['choice3'],
            q['choice4'],
        ]

    def before_next_page(self): # executed after form validation, before the player proceeds to the next page.
        self.player.check_correct() # THIS WORKS -- defined this in models.py (under Player)
        self.player.set_payoff_per_question() # THIS WORKS

    def vars_for_template(self):
        return {
            'treatment': self.participant.vars['treatment'],
        }


##### OTHER TEAM'S QUESTION #################################################

class otherQuestion(Page):
    form_model = 'player'

    def vars_for_template(self):
        q = self.player.other_current_question()

        # set up messages
        if self.round_number == 1:  # after the very first question
            correct_last_round = "  "
        else:  # after all subsequent questions
            if self.player.in_previous_rounds()[-1].is_correct:
                correct_last_round = "It was correct"
            else:
                correct_last_round = "It was incorrect"

        return {
            'choice1': q['choice1'],
            'choice2': q['choice2'],
            'choice3': q['choice3'],
            'choice4': q['choice4'],
            'correct_last_round': correct_last_round,
        }



# ##### CALCULATE OWN CORRECT ANSWERS ####################################### NOPE
#
# class endRound(Page):
#
#     def is_displayed(self):
#         return self.round_number % 4 == 0
#
#     def before_next_page(self):
#         self.player.set_own_correct_answers_this_round()
#
#     AttributeError 'Player' object has no attribute 'player'
#
#     DOMINIK: I am using self.player.in_all_rounds()[-4:] in self.player.set_own_correct_answers_this_round()
#     -- that a problem? Should I define this method somewhere else? (I tried under groups but didnt work either)




##### WAIT PAGE #############################################################

class WaitAfterEachRound(WaitPage): # Not waiting for all!!

    def is_displayed(self):
        return self.round_number % 4 == 0 # ASSUMING I STICK WITH 4 Qs PER ROUND

    body_text = "Waiting for your team mates to finish."


    # def after_all_players_arrive(self):
    #
    #     self.player.set_own_correct_answers_this_round() # NOOOOO WORK -- Doesnt work here or on the page below (DOMINIK?)
    #     self.group.set_teams_correct_answers_this_round() # Needs is_correct_this_round
    #     self.group.set_teams_avg_correct_this_round() # Needs is_correct_this_round


    ##### CALCULATE TEAMS CORRECT ANSWERS ######################################

    # @ DOMINIK: ANY IDEA WHY THIS WOULD GIVE ME A TYPE ERROR?
    # WHENEVER I USE self.player.in_all_rounds()[-4:] (both under groups and under player)
    # I get an AttributeError: 'Player' object has no attribute 'player' // 'Group' object has no attribute 'player'

    # def after_all_players_arrive(self): #
    ##     self.group.set_teams_correct_answers_this_round() # TypeError: unsupported operand type -- self.subsession.get_players() doesnt seem to work
    #     self.group.set_teams_avg_correct_this_round()

    # # IF I CAN GET THE ABOVE TO WORK TRY THIS AFTER THE LAST ROUND:
    #
    # def after_all_players_arrive(self):
    #     self.group.set_teams_is_correct_total()
    #     self.group.set_teams_earned_total()
    #     self.group.set_teams_avg_is_correct()

    ##### CALCULATE OWN CORRECT ANSWERS ######################################## NOPE

    # def before_next_page(self): # THIS SHOULD WORK FOR NORMAL PAGES -- SEE IF IT WORKS FOR WAITPAGES, AS WELL? -- NOPE
    #     self.player.set_own_correct_answers_this_round()
    # KeyError -- 'is_correct_this_round'


    ##### NO WORK #############################################################

    # NO WORK: self.player inside after_all_players_arrive

    # def after_all_players_arrive(self):
    #     self.player.set_teams_correct_answers_this_round()
    #     self.player.set_teams_avg_correct_this_round() #

    #     self.group.set_teams_correct_answers_this_round() # AttributeError 'Group' object has no attribute 'participant'
    #     self.group.set_teams_avg_correct_this_round() #

    # NB: Note, you can’t reference self.player inside after_all_players_arrive, because the code is executed once for
    # the entire group, not for each individual player. (However, you can use self.player in a wait page’s is_displayed.)
    # (RTD, WaitPages)
    ##### NO WORK #############################################################

    # NB: before_next_page is not valid on wait pages


##### NEW PAYOFFS ###########################################################

# Shorter, less information, payoffs defined in pages.py, not models.py



##### OWN ANSWERS THIS ROUND ################################################

# NB -- player.in_previous_rounds() and player.in_all_rounds() each return a list of players representing the
# same participant in previous rounds of the same app. The difference is that in_all_rounds() includes the current
# round's player. (RTD -- Apps & Rounds)

class ownResultsThisRound(Page):

    def is_displayed(self):
        return self.round_number % 4 == 0  # % = modulo, e.g. 3 Runden mit 4 Fragen: 4, 8, 12 ist teilbar durch 3 (Rest == 0)

    def vars_for_template(self):

        player_in_last_4_qs = self.player.in_all_rounds()[-4:]   # list of players representing the same participant in the last 4 qs

        for p in self.player.in_all_rounds()[-4:]:                                                      # -- THIS WORKS

            p.is_correct_this_round = sum([p.is_correct for p in self.player.in_all_rounds()[-4:]])
            p.participant.vars['is_correct_this_round'] = p.is_correct_this_round

            p.earned_this_round = Constants.stakes * sum([p.is_correct for p in self.player.in_all_rounds()[-4:]])
            p.participant.vars['earned_this_round'] = c(p.earned_this_round)

        return {
                'player_in_last_4_qs': player_in_last_4_qs,
                'is_correct_this_round': self.participant.vars['is_correct_this_round'],
                'earned_this_round': self.participant.vars['earned_this_round'],

        }

    def before_next_page(self):
        self.group.set_teams_correct_answers_this_round()
        self.group.set_teams_avg_correct_this_round()


#     def before_next_page(self): # -- NOPE
#             self.player.set_own_correct_answers_this_round()

#  This works neither under player nor under groups: AttributeError: 'Player' object has no attribute 'player'
#  Ideally, I would calculate set_own_correct_answers_this_round on the waitpage above





##### CHECK PAGE #############################################################
class CheckRound1(Page):

    def is_displayed(self):
        return self.round_number == 4 # TRY THIS!!

    def vars_for_template(self):

        # all_correct_this_round = sum([p.is_correct_this_round for p in self.group.get_players()]) # THIS WORKS
        all_correct_this_round = sum([p.is_correct_this_round for p in self.subsession.get_players()]) # THIS WORKS

        a_correct_this_round = 0 # THIS WORKS
        b_correct_this_round = 0

        for p in self.subsession.get_players():
            if p.treatment == 'A' and p.is_correct != None:
                a_correct_this_round += p.is_correct_this_round

            if p.treatment == 'B':
                b_correct_this_round += p.is_correct_this_round

        # team_a_is_correct_this_round = 0 # THIS WORKS
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

        # team_a_players = [p for p in self.group.get_players() if p.treatment == 'A'] # THIS WORKS # oder self.group.get_players?
        # team_b_players = [p for p in self.group.get_players() if p.treatment == 'B'] # THIS WORKS
        #
        # a_correct_this_round = sum([p.is_correct_this_round for p in self.subsession.get_players() if p.treatment == 'A']) # DOES NOT WORK -- GIVES OWN NUMBER
        # b_correct_this_round = sum([p.is_correct_this_round for p in self.subsession.get_players() if p.treatment == 'B']) # DOES NOT WORK -- GIVES OWN NUMBER

        return {
            'treatment': self.participant.vars['treatment'],
            'falsefeedback': self.participant.vars['falsefeedback'],
            'firstfeedback': self.participant.vars['firstfeedback'],

            'n_team_a': self.session.vars['n_team_a'],
            'n_team_b': self.session.vars['n_team_b'],

            'n_team_a_consented': self.session.vars['n_team_a_consented'],
            'n_team_b_consented': self.session.vars['n_team_b_consented'],

            'is_correct_this_round': self.participant.vars['is_correct_this_round'],
            'earned_this_round': self.participant.vars['earned_this_round'],

            'all_correct_this_round': all_correct_this_round,
            'a_correct_this_round': a_correct_this_round,
            'b_correct_this_round': b_correct_this_round,

            'team_a_is_correct_this_round':self.session.vars['team_a_is_correct_this_round'],
            'team_b_is_correct_this_round': self.session.vars['team_b_is_correct_this_round'],

            'team_a_avg_correct_this_round': self.session.vars['team_a_avg_correct_this_round'],
            'team_b_avg_correct_this_round': self.session.vars['team_b_avg_correct_this_round'],
        }
##### CHECK PAGE #############################################################



##### CHECK PAGE (FOR DEBUGGING) #############################################
class CheckRound2(Page):

    def is_displayed(self):
        return self.round_number == 8

    def vars_for_template(self):

        return {

            'treatment': self.participant.vars['treatment'],
            'falsefeedback': self.participant.vars['falsefeedback'],
            'firstfeedback': self.participant.vars['firstfeedback'],

            'n_team_a': self.session.vars['n_team_a'],
            'n_team_b': self.session.vars['n_team_b'],

            'n_team_a_consented': self.session.vars['n_team_a_consented'],
            'n_team_b_consented': self.session.vars['n_team_b_consented'],

            'is_correct_this_round': self.participant.vars['is_correct_this_round'],
            'earned_this_round': self.participant.vars['earned_this_round'],

            'team_a_is_correct_this_round': self.session.vars['team_a_is_correct_this_round'],
            'team_b_is_correct_this_round': self.session.vars['team_b_is_correct_this_round'],

            'team_a_avg_correct_this_round': self.session.vars['team_a_avg_correct_this_round'],
            'team_b_avg_correct_this_round': self.session.vars['team_b_avg_correct_this_round'],

        }
##### CHECK PAGE #############################################################





##### OTHER TEAM'S ANSWERS THIS ROUND #######################################

class otherTeamsQsThisRound(Page):

    def is_displayed(self):
        return self.round_number % 4 == 0

    def vars_for_template(self):

        # DEFINING THE FOLLOWING FOR LATER...

        player_in_last_4_qs = self.player.in_all_rounds()[-4: ]

        # THIS GIVES WRONG ANSWERS!!
        # team_a_is_correct_this_round = sum([p.is_correct for p in self.player.in_all_rounds()[-4:] if p.treatment == 'A']) # WORKS BUT POSSIBLY WRONG NUMBERS
        # team_b_is_correct_this_round = sum([p.is_correct for p in self.player.in_all_rounds()[-4:] if p.treatment == 'B'])
        #
        # self.participant.vars['team_a_is_correct_this_round'] = team_a_is_correct_this_round
        # self.participant.vars['team_b_is_correct_this_round'] = team_b_is_correct_this_round

        team_a_players = [p for p in self.subsession.get_players() if p.treatment == 'A'] # THIS WORKS # oder self.group.get_players?
        team_b_players = [p for p in self.subsession.get_players() if p.treatment == 'B'] # THIS WORKS

        team_a_is_correct_this_round = sum(p.is_correct_this_round for p in team_a_players)
        team_b_is_correct_this_round = sum(p.is_correct_this_round for p in team_b_players)

        self.session.vars['team_a_is_correct_this_round'] = team_a_is_correct_this_round
        self.session.vars['team_b_is_correct_this_round'] = team_b_is_correct_this_round

        return {
            'player_in_last_4_qs': player_in_last_4_qs,
            'team_a_is_correct_this_round': self.session.vars['team_a_is_correct_this_round'],
            'team_b_is_correct_this_round': self.session.vars['team_b_is_correct_this_round'],
        }

    def before_next_page(self):
        self.group.set_teams_avg_correct_this_round() # THIS WORKS



##### OTHER TEAM'S RESULTS THIS ROUND #######################################

class teamsResultsThisRound(Page):

    def is_displayed(self):
        return self.round_number % 4 == 0

    def vars_for_template(self):

        return {
            # 'player_in_last_4_qs': player_in_last_4_qs,
            'team_a_avg_correct_this_round': self.session.vars['team_a_avg_correct_this_round'],
            'team_b_avg_correct_this_round': self.session.vars['team_b_avg_correct_this_round'],
        }

    # def before_next_page(self):
    #     # self.player.set_own_correct_answers_all_rounds() # AttributeError 'Player' object has no attribute 'player'
    #
    #     self.player.set_teams_correct_answers_this_round() # TRY THIS
    #     self.player.set_teams_avg_correct_this_round() # TRY THIS



##### PAYOFFS ################################################################

class endQuiz(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        # player_in_all_rounds = self.player.in_all_rounds()

        for p in self.player.in_all_rounds():
            p.is_correct_total = sum([p.is_correct for p in self.player.in_all_rounds()]) # THIS WORKS
            p.participant.vars['is_correct_total'] = p.is_correct_total

        # THIS GIVES WRONG ANSWERS!!
        # # team_a_is_correct_total = sum([p.is_correct_total for p in self.subsession.get_players() if p.treatment == 'A']) #TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'
        # # team_b_is_correct_total = sum([p.is_correct_total for p in self.subsession.get_players() if p.treatment == 'B'])
        #
        #  # SAME:
        # team_a_is_correct_total = sum([p.is_correct for p in self.player.in_all_rounds() if p.treatment == 'A']), # THIS WORKS
        # team_b_is_correct_total = sum([p.is_correct for p in self.player.in_all_rounds() if p.treatment == 'B']),
        #
        # self.participant.vars['team_a_is_correct_total'] = team_a_is_correct_total
        # self.participant.vars['team_b_is_correct_total'] = team_b_is_correct_total
        #
        # team_a_earned_total = Constants.stakes * sum([p.is_correct for p in self.player.in_all_rounds() if p.treatment == 'A']), # THIS WORKS
        # team_b_earned_total = Constants.stakes * sum([p.is_correct for p in self.player.in_all_rounds() if p.treatment == 'B']),
        #
        # self.participant.vars['team_a_earned_total'] = team_a_earned_total
        # self.participant.vars['team_b_earned_total'] = team_b_earned_total

        return {
            'is_correct_total': self.participant.vars['is_correct_total'],
        }



##### CALCULATE PAYOFFS ##################################################### TRY LATER

class CalculatePayoffs(WaitPage):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    body_text = "Waiting for people to finish and calculating payoffs..." # CHECK IF THIS WORKS

    def after_all_players_arrive(self): # THIS WORKS
        self.group.set_teams_is_correct_total()
        self.group.set_teams_earned_total()
        self.group.set_teams_avg_is_correct()
        self.group.set_add_ons()
        self.group.set_jackpot()
        # self.player.set_payoffs() # TRY THIS NEXT


##### CHECK PAGE (FOR DEBUGGING) #############################################
class CheckRound3(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):

        return {
            'n_team_a_consented': self.session.vars['n_team_a_consented'], # THIS WORKS
            'n_team_b_consented': self.session.vars['n_team_b_consented'],

            'is_correct_total': self.participant.vars['is_correct_total'],

            'team_a_is_correct_total': self.session.vars['team_a_is_correct_total'],
            'team_b_is_correct_total': self.session.vars['team_b_is_correct_total'],

            'team_a_earned_total': self.session.vars['team_a_earned_total'],
            'team_b_earned_total': self.session.vars['team_b_earned_total'],

            'team_a_avg_is_correct': self.session.vars['team_a_avg_is_correct'],
            'team_b_avg_is_correct': self.session.vars['team_b_avg_is_correct'],

            'team_a_add_on': self.session.vars['team_a_add_on'],
            'team_b_add_on': self.session.vars['team_b_add_on'],
        }
##### CHECK PAGE #############################################################





##### OWN RESULTS ALL ROUNDS ################################################

class ownResultsAllRounds(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):

        player_in_all_rounds = self.player.in_all_rounds()
        #
        # for p in self.player.in_all_rounds():
        #     p.is_correct_total = sum([p.is_correct for p in self.player.in_all_rounds()]) # DID THIS IN endQuiz
        #     p.participant.vars['is_correct_total'] = p.is_correct_total

        earned_total = c(Constants.stakes * self.participant.vars['is_correct_total'])
        self.participant.vars['earned_total'] = earned_total

        for p in self.player.in_all_rounds(): # THIS WORKS # is_correct_all_rounds SAME AS is_correct_total

            p.is_correct_all_rounds = sum([p.is_correct for p in self.player.in_all_rounds()]) # THIS WORKS
            p.participant.vars['is_correct_all_rounds'] = p.is_correct_all_rounds

        team_a_players = [p for p in self.subsession.get_players() if p.treatment == 'A']
        team_b_players = [p for p in self.subsession.get_players() if p.treatment == 'B']

        team_a_is_correct_total = sum(p.is_correct_total for p in team_a_players) # Rename is_correct_total is_correct_all_rounds
        team_b_is_correct_total = sum(p.is_correct_total for p in team_b_players) # Rename is_correct_total is_correct_all_rounds

        self.session.vars['team_a_is_correct_total'] = team_a_is_correct_total
        self.session.vars['team_b_is_correct_total'] = team_b_is_correct_total

        team_a_earned_total = c(Constants.stakes * sum(p.is_correct_total for p in team_a_players)) # THIS WORKS
        team_b_earned_total = c(Constants.stakes * sum(p.is_correct_total for p in team_b_players))

        self.session.vars['team_a_earned_total'] = team_a_earned_total # Need to define this as a session.vars
        self.session.vars['team_b_earned_total'] = team_b_earned_total


        return {
                'is_correct_total': self.participant.vars['is_correct_total'],
                'earned_total': self.participant.vars['earned_total'],
                'is_correct_all_rounds': self.participant.vars['is_correct_all_rounds'],
                'team_a_is_correct_total': self.session.vars['team_a_is_correct_total'],
                'team_b_is_correct_total': self.session.vars['team_b_is_correct_total'],
                'team_a_earned_total': self.session.vars['team_a_earned_total'],
                'team_b_earned_total': self.session.vars['team_b_earned_total'],
                # 'earned_total': Constants.stakes * sum([p.is_correct for p in player_in_all_rounds]),
        }

    def before_next_page(self):
        self.group.set_add_ons() # THIS WORKS
        self.group.set_teams_avg_is_correct() # TRY THIS NEXT
        # (then i wouldn't need to calculate team_a_avg_is_correct in teamsResultsAllRounds)

        # NB needs team_a_earned_total.
        # NB Need to define self.session.vars['team_a_earned_total'] somewhere up there.

        # team_a_is_correct_total = sum([p.is_correct for p in self.player.in_all_rounds() if p.treatment == 'A']), # THIS GIVES THE CORRECT NUMBERS BUT AS A LIST
        # team_b_is_correct_total = sum([p.is_correct for p in self.player.in_all_rounds() if p.treatment == 'B']), # THIS GIVES THE CORRECT NUMBERS BUT AS A LIST


# ##### CHECK PAGE (FOR DEBUGGING) #############################################
# class CheckRound2(Page):
#
#     def is_displayed(self):
#         return self.round_number == 8
#
#     def vars_for_template(self):
#
#         return {
#             'n_team_a_consented': self.session.vars['n_team_a_consented'], # THIS WORKS
#             'n_team_b_consented': self.session.vars['n_team_b_consented'],
#
#             'is_correct_total': self.participant.vars['is_correct_total'],
#
#             'team_a_is_correct_total': self.participant.vars['team_a_is_correct_total'],
#             'team_b_is_correct_total': self.participant.vars['team_b_is_correct_total'],
#
#             'team_a_earned_total': self.participant.vars['team_a_earned_total'],
#             'team_b_earned_total': self.participant.vars['team_b_earned_total'],
#
#             'team_a_add_on': self.session.vars['team_a_add_on'],
#             'team_b_add_on': self.session.vars['team_b_add_on'],
#         }
# ##### CHECK PAGE #############################################################

class payoffs(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):

        team_a_avg_is_correct = int(100 * self.session.vars['team_a_is_correct_total'] / self.session.vars['n_team_a_consented'] / Constants.num_rounds)
        team_b_avg_is_correct = int(100 * self.session.vars['team_b_is_correct_total'] / self.session.vars['n_team_b_consented'] / Constants.num_rounds)


        team_a_avg_payoff = self.session.vars['team_a_earned_total'] / self.session.vars['n_team_a_consented'] # try set_teams_avg_payoff()
        team_b_avg_payoff = self.session.vars['team_b_earned_total'] / self.session.vars['n_team_b_consented']

        self.session.vars['team_a_avg_payoff'] = team_a_avg_payoff
        self.session.vars['team_b_avg_payoff'] = team_b_avg_payoff

        team_a_players = [p for p in self.subsession.get_players() if p.treatment == 'A']
        team_b_players = [p for p in self.subsession.get_players() if p.treatment == 'B']

        for p in team_a_players:
            # p.payoff = 0.5 * p.earned_total + self.session.vars['team_a_add_on']
            p.payoff = 0.5 * self.participant.vars['earned_total'] + self.session.vars['team_a_add_on']

        for p in team_b_players:
            # p.payoff = 0.5 * p.earned_total + self.session.vars['team_b_add_on']
            p.payoff = 0.5 * self.participant.vars['earned_total'] + self.session.vars['team_b_add_on']

            self.participant.vars['payoff'] = p.payoff

        for p in self.subsession.get_players(): # ??

            if self.participant.vars['payoff'] < Constants.minimum_payoff:
                p.paid = Constants.minimum_payoff
            else:
                p.paid = p.payoff

            self.participant.vars['paid'] = p.paid

        return {

            'n_team_a_consented': self.session.vars['n_team_a_consented'],
            'n_team_b_consented': self.session.vars['n_team_b_consented'],

            'team_a_avg_is_correct': self.session.vars['team_a_avg_is_correct'],
            'team_b_avg_is_correct': self.session.vars['team_b_avg_is_correct'],

            'team_a_avg_payoff': self.session.vars['team_a_avg_payoff'],
            'team_b_avg_payoff': self.session.vars['team_b_avg_payoff'],

            'team_a_is_correct_total': self.session.vars['team_a_is_correct_total'],
            'team_b_is_correct_total': self.session.vars['team_b_is_correct_total'],

            'team_a_earned_total': self.session.vars['team_a_earned_total'],
            'team_b_earned_total': self.session.vars['team_b_earned_total'],

            'team_a_pot': (self.session.vars['team_a_earned_total'] / 2),
            'team_b_pot': (self.session.vars['team_b_earned_total'] / 2),

            'team_a_add_on': self.session.vars['team_a_add_on'],
            'team_b_add_on': self.session.vars['team_b_add_on'],

            'treatment': self.participant.vars['treatment'],

            'is_correct_total': self.participant.vars['is_correct_total'],
            'earned_total': self.participant.vars['earned_total'],
            'half_own_earnings': (self.participant.vars['earned_total'] / 2),

            'payoff': self.participant.vars['payoff'],

            'paid': self.participant.vars['paid'],


        }


##### PAYOFFS ################################################################

class payoffsDetailed(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):

        team_a_players = [p for p in self.subsession.get_players() if p.treatment == 'A']
        team_b_players = [p for p in self.subsession.get_players() if p.treatment == 'B']

        for p in team_a_players:
            # p.payoff = 0.5 * p.earned_total + self.session.vars['team_a_add_on']
            p.payoff = 0.5 * self.participant.vars['earned_total'] + self.session.vars['team_a_add_on']

        for p in team_b_players:
            # p.payoff = 0.5 * p.earned_total + self.session.vars['team_b_add_on']
            p.payoff = 0.5 * self.participant.vars['earned_total'] + self.session.vars['team_b_add_on']

            self.participant.vars['payoff'] = p.payoff

        team_a_avg_payoff = self.session.vars['team_a_earned_total'] / self.session.vars['n_team_a_consented']
        team_b_avg_payoff = self.session.vars['team_b_earned_total'] / self.session.vars['n_team_b_consented']

        self.session.vars['team_a_avg_payoff'] = team_a_avg_payoff
        self.session.vars['team_b_avg_payoff'] = team_b_avg_payoff


        return {

            'n_team_a_consented': self.session.vars['n_team_a_consented'],
            'n_team_b_consented': self.session.vars['n_team_b_consented'],

            'team_a_avg_is_correct': self.session.vars['team_a_avg_is_correct'],
            'team_b_avg_is_correct': self.session.vars['team_b_avg_is_correct'],

            'team_a_is_correct_total': self.session.vars['team_a_is_correct_total'],
            'team_b_is_correct_total': self.session.vars['team_b_is_correct_total'],

            'team_a_earned_total': self.session.vars['team_a_earned_total'],
            'team_b_earned_total': self.session.vars['team_b_earned_total'],

            'team_a_pot': (self.session.vars['team_a_earned_total'] / 2),
            'team_b_pot': (self.session.vars['team_b_earned_total'] / 2),

            'team_a_add_on': self.session.vars['team_a_add_on'], # THIS SHOULD BE THE ONLY NEW THING!!!
            'team_b_add_on': self.session.vars['team_b_add_on'],

            'treatment': self.participant.vars['treatment'],

            'is_correct_total': self.participant.vars['is_correct_total'],
            'earned_total': self.participant.vars['earned_total'],
            'half_own_earnings': (self.participant.vars['earned_total'] / 2),

            'payoff': self.participant.vars['payoff'],

            'team_a_avg_payoff': self.session.vars['team_a_avg_payoff'],
            'team_b_avg_payoff': self.session.vars['team_b_avg_payoff'],
        }

class payoffsReceiptForm(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):

        return {
            'paid': self.participant.vars['paid'],
        }


# ### NB vars_for_template(): Use this to pass variables to the template. (e.g. player_in_all rounds)
# # Then in the template access with {{ variable }}
#
# # oTree automatically passes the following objects to the template:
# # player, group, subsession, participant, session, and Constants. (RTD)
#
# ### NB player.in_all_rounds() returns a list of players representing the same participant in previous rounds
#  # of the same app, incl. the current round



##### PRE-TEST FOR MEMORY BASELINE ##################################################

class pretestMemory(Page):
    form_model = 'player'
    form_fields = [
                    'memory_UK',
                    'memory_indianReservations',
                    'memory_lakeInLibya',
                    'memory_mountainsNetherlands',
                    'memory_Greenland',
                    'memory_France',
                    'memory_LondonToEdinburgh',
                    'memory_FrankfortUS',
                    'rememberedSeconds',
                    'readOtherQs',
                    'felt',
                    'howFair',
                    'noticedUnfair'
                   ]
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


##### FAIR PLAY / UNFAIR FEEDBACK ###################################################

class intro_feedback(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    def vars_for_template(self):
        return {
            'treatment': self.participant.vars['treatment'],
            'firstfeedback': self.participant.vars['firstfeedback'],
            'falsefeedback': self.participant.vars['falsefeedback'],
        }

class fairplay(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'fairplay'

    def vars_for_template(self):
        return {
            'treatment': self.participant.vars['treatment'],
            'firstfeedback': self.participant.vars['firstfeedback'],
            'falsefeedback': self.participant.vars['falsefeedback'],
            'bullet_points_true_facts': self.session.vars['bullet_points_true_facts'],
            'bullet_points_false_facts_fairplay': self.session.vars['bullet_points_false_facts_fairplay'],
        }

class fairplay_copy(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'unfair'

    def vars_for_template(self):
        return {
            'treatment': self.participant.vars['treatment'],
            'firstfeedback': self.participant.vars['firstfeedback'],
            'falsefeedback': self.participant.vars['falsefeedback'],
            'bullet_points_true_facts': self.session.vars['bullet_points_true_facts'],
            'bullet_points_false_facts_fairplay': self.session.vars['bullet_points_false_facts_fairplay'],
        }


class fairplay_repeat(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'fairplay'

    def vars_for_template(self):
        return {
            'treatment': self.participant.vars['treatment'],
            'firstfeedback': self.participant.vars['firstfeedback'],
            'falsefeedback': self.participant.vars['falsefeedback'],
            'bullet_points_true_facts': self.session.vars['bullet_points_true_facts'],
            'bullet_points_false_facts_fairplay': self.session.vars['bullet_points_false_facts_fairplay'],
        }

class fairplay_repeat_copy(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'unfair'

    def vars_for_template(self):
        return {
            'treatment': self.participant.vars['treatment'],
            'firstfeedback': self.participant.vars['firstfeedback'],
            'falsefeedback': self.participant.vars['falsefeedback'],
            'bullet_points_true_facts': self.session.vars['bullet_points_true_facts'],
            'bullet_points_false_facts_fairplay': self.session.vars['bullet_points_false_facts_fairplay'],
        }


class unfair(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'fairplay'

    def vars_for_template(self):
        return {
            'treatment': self.participant.vars['treatment'],
            'firstfeedback': self.participant.vars['firstfeedback'],
            'falsefeedback': self.participant.vars['falsefeedback'],
            'bullet_points_true_facts': self.session.vars['bullet_points_true_facts'],
            'bullet_points_false_facts_unfair': self.session.vars['bullet_points_false_facts_unfair'],
        }

class unfair_copy(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'unfair'

    def vars_for_template(self):
        return {
            'treatment': self.participant.vars['treatment'],
            'firstfeedback': self.participant.vars['firstfeedback'],
            'falsefeedback': self.participant.vars['falsefeedback'],
            'bullet_points_true_facts': self.session.vars['bullet_points_true_facts'],
            'bullet_points_false_facts_unfair': self.session.vars['bullet_points_false_facts_unfair'],
        }


class unfair_repeat(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'fairplay'

    def vars_for_template(self):
        return {
            'treatment': self.participant.vars['treatment'],
            'firstfeedback': self.participant.vars['firstfeedback'],
            'falsefeedback': self.participant.vars['falsefeedback'],
            'bullet_points_true_facts': self.session.vars['bullet_points_true_facts'],
            'bullet_points_false_facts_unfair': self.session.vars['bullet_points_false_facts_unfair'],
        }

class unfair_repeat_copy(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'unfair'

    def vars_for_template(self):
        return {
            'treatment': self.participant.vars['treatment'],
            'firstfeedback': self.participant.vars['firstfeedback'],
            'falsefeedback': self.participant.vars['falsefeedback'],
            'bullet_points_true_facts': self.session.vars['bullet_points_true_facts'],
            'bullet_points_false_facts_unfair': self.session.vars['bullet_points_false_facts_unfair'],
        }


class CheckBulletPoints(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'unfair'

    def vars_for_template(self):
        return {
            # 'treatment': self.participant.vars['treatment'],
            'falsefeedback': self.participant.vars['falsefeedback'],
            'bullet_points_true_facts': self.session.vars['bullet_points_true_facts'],
            'bullet_points_false_facts_fairplay': self.session.vars['bullet_points_false_facts_fairplay'],
        }


    #####################################################################################
    #
    # NB PYTHON ERRORS
    #
    # KeyError: -- Python raises a KeyError whenever a dict() object is requested (using the format a = adict[key])
    # and the key is not in the dictionary.
    # --> Kommt when accessing a variable that I never defined
    #
    # TypeError: -- 2 + "two"
    # AttributeError: -- when you try to access or call an attribute that a particular object does not possess, e.g.
    #
    # anInt = 8
    # anInt.append(4)
    #
    #  NoneType' object is not subscriptable
    # = you attempted to index an object that doesn't have that functionality. e.g. 127[0]
    #####################################################################################

    # SHUFFLE A LIST IN PYTHON -- THIS WORKS IN ATOM

    # bullet_points = ['L1','L2', 'L3', 'L4','F1','F2',]
    # from random import shuffle
    # shuffled_bullet_points = shuffle(bullet_points)
    # print(bullet_points)

    # DRAW K RANDOM NUMBERS WITHOUT REPLACEMENT -- THIS; TOO; WORKS IN ATOM

    # from random import *
    # print(sample([10, 20, 30, 40, 50], k=4))


##### MANIPULATION CHECK 1 ######################################################

class expectationsLastQ(Page):
    form_model = 'player'
    form_fields = ['expectationsLastQ']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds - 1


class expectationsLastQSlider(Page):
    form_model = 'player'
    form_fields = ['expectationsLastQSlider']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds - 1



##### DV ########################################################################

class intro_dv_feedback1(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class intro_dv_feedback1_copy(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


##### FEEDBACK == FAIR PLAY #####################################################

class fairplay_gen_agree(Page):
    form_model = 'player'
    form_fields = ['agreeFeedback_fairplay']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'fairplay'

class fairplay_gen_agree_copy(Page):
    form_model = 'player'
    form_fields = ['agreeFeedback_fairplay']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'unfair'


class fairplay_accurate(Page):
    form_model = 'player'
    form_fields = ['educationRating_fairplay', 'accuracyRating_fairplay', 'representationRating_fairplay']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'fairplay'

class fairplay_accurate_copy(Page):
    form_model = 'player'
    form_fields = ['educationRating_fairplay', 'accuracyRating_fairplay', 'representationRating_fairplay']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'unfair'

class fairplay_falsefacts(Page):
    form_model = 'player'
    form_fields = [
                   'false_fact_too_easy',
                   'false_fact_too_hard',
                   'false_fact_30sec_fairplay',
                    'true_fact_too_easy',
                    'true_fact_too_hard',
                    'true_fact_30sec',
                   ]
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'fairplay'
    def vars_for_template(self):
        return {
            'falsefeedback': self.participant.vars['falsefeedback'],
        }

class fairplay_falsefacts_copy(Page):
    form_model = 'player'
    form_fields = [
                   'false_fact_too_easy',
                   'false_fact_too_hard',
                   'false_fact_30sec_fairplay',
                    'true_fact_too_easy',
                    'true_fact_too_hard',
                    'true_fact_30sec',
                   ]
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'unfair'
    def vars_for_template(self):
        return {
            'falsefeedback': self.participant.vars['falsefeedback'],
        }


##### FEEDBACK == UNFAIR #########################################################

class intro_dv_feedback2(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'fairplay'

class intro_dv_feedback2_copy(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'unfair'


class unfair_gen_agree(Page):
    form_model = 'player'
    form_fields = ['agreeFeedback_unfair']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'fairplay'

class unfair_gen_agree_copy(Page):
    form_model = 'player'
    form_fields = ['agreeFeedback_unfair']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'unfair'


class unfair_accurate(Page):
    form_model = 'player'
    form_fields = ['educationRating_unfair', 'accuracyRating_unfair', 'representationRating_unfair']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'fairplay'

class unfair_accurate_copy(Page):
    form_model = 'player'
    form_fields = ['educationRating_unfair', 'accuracyRating_unfair', 'representationRating_unfair']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'unfair'


class unfair_falsefacts(Page):
    form_model = 'player'
    form_fields = ['true_fact_too_easy',
                   'true_fact_too_hard',
                   'true_fact_30sec',
                   'false_fact_too_easy',
                   'false_fact_too_hard',
                   'false_fact_30sec_unfair',
                   'false_fact_30sec_fairplay',
                   ]
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'fairplay'
    def vars_for_template(self):
        return {
            'falsefeedback': self.participant.vars['falsefeedback'],
        }

class unfair_falsefacts_copy(Page):
    form_model = 'player'
    form_fields = ['true_fact_too_easy',
                   'true_fact_too_hard',
                   'true_fact_30sec',
                   'false_fact_too_easy',
                   'false_fact_too_hard',
                   'false_fact_30sec_unfair',
                   'false_fact_30sec_fairplay',
                   ]
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['firstfeedback'] == 'unfair'
    def vars_for_template(self):
        return {
            'falsefeedback': self.participant.vars['falsefeedback'],
        }


##### OWN FEEDBACK ##################################################################

class your_feedback(Page):
    form_model = 'player'
    form_fields = ['wantFeedbackOn0', 'wantFeedbackOn1', 'wantFeedbackOn2', 'otherFeedback1']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds



##### MANIPULATION CHECK 2 ##########################################################

class whoGotHigherPayoff(Page):
    form_model = 'player'
    form_fields = ['whoGotHigherPayoff']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds



##### LEGITIMACY OF STATUS DIFFERENCES ##############################################

# NB: Determining form fields dynamically

# If you need the list of form fields to be dynamic, instead of form_fields you can define a method
# get_form_fields(self) that returns the list.
# But if you do this, you must make sure your template also contains conditional logic so that the
# right formfield elements are included: (RTD - Forms)
#
# {% for field in form %}
#     {% formfield field %}
# {% endfor %}

# IF Team A got easier Qs:

class fair(Page):
    form_model = 'player'
    form_fields = ['fairTeamAEasierQs']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.player.whoGotHigherPayoff == 'On average, Team A got a higher payoff than Team B.'


class byChanceTeamAEasierQs(Page):
    form_model = 'player'
    form_fields = ['byChanceTeamAEasierQs']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.player.whoGotHigherPayoff == 'On average, Team A got a higher payoff than Team B.'



##### STABILITY OF STATUS DIFFERENCES ###############################################

class feedbackMakesDifference(Page):
    form_model = 'player'
    form_fields = ['feedbackMakesDifference']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds



##### CONTROLS ######################################################################

class trivia(Page):
    form_model = 'player'
    form_fields = ['trivialPursuit1', 'trivialPursuit2']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class labExperience(Page):
    form_model = 'player'
    form_fields = ['labExperience']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


##### DEMOGRAPHICS ###################################################################

class gender(Page):
    form_model = 'player'
    form_fields = ['gender']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class born(Page):
    form_model = 'player'
    form_fields = ['born']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class education(Page):
    form_model = 'player'
    form_fields = ['education']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class atEssex(Page):
    form_model = 'player'
    form_fields = ['atEssex']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class big5(Page):
    form_model = 'player'
    form_fields = ['extraversion',
                   'agreeablenessR',
                   'conscientiousness',
                   'neuroticism',
                   'openness',
                   'extraversionR',
                   'agreeableness',
                   'conscientiousnessR',
                   'neuroticismR',
                   'opennessR']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

# NB Wording drawn from
# https://gosling.psy.utexas.edu/scales-weve-developed/ten-item-personality-measure-tipi/ten-item-personality-inventory-tipi/


class positionAtEssex(Page):
    form_model = 'player'

    def get_form_fields(self):
        if self.player.atEssex == 'Yes':
            return ['positionAtEssex', 'major']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class british(Page):
    form_model = 'player'
    form_fields = ['british']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class nationality(Page):
    form_model = 'player'
    form_fields = ['nationality']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.player.british != 'United Kingdom'


class income(Page):
    form_model = 'player'
    form_fields = ['income']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class whatAbout(Page):
    form_model = 'player'
    form_fields = ['whatAbout']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class email(Page):
    form_model = 'player'
    form_fields = ['email', 'anythingElse']
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class theEnd(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


##### PAGE SEQUENCE #################################################################

page_sequence = [

    #### INTRO

    welcome,
    consent,                                # ... needed to calculate payoffs
    intro,
    intro2,
    intro3,
    allocatedTeam,

    #### PRACTICE

    practice_question,
    other_practice_question,
    introPaidQuiz,                          # ... calculating team sizes

    #### ROUNDS

    question,
    otherQuestion,

    #### MANIPULATION CHECK 1

    expectationsLastQ,
    # expectationsLastQSlider,

    #### WAIT FOR 2nd / 3rd ROUND

    WaitAfterEachRound,                     # ... calculating group payoffs

    #### RESULTS EACH ROUND (after ever 4 Qs)

    ownResultsThisRound,
    ## CheckRound1,
    ## CheckRound2,
    otherTeamsQsThisRound,
    teamsResultsThisRound,

    #### RESULTS LAST ROUND

    endQuiz,                                # ... calculating is_correct_total
    CalculatePayoffs,
    ownResultsAllRounds,

    ## CheckRound3,
    ## teamsResultsAllRounds,
    payoffs,
    payoffsReceiptForm,
    ## payoffsDetailed,

    #### PRETEST MEMORY

    pretestMemory,

    #### FEEDBACK PAGES

    intro_feedback,
    CheckBulletPoints,

    #### IF FIRSTFEEDBACK = FAIRPLAY:

    fairplay,
    unfair,

    intro_dv_feedback1,
    fairplay_repeat,
    fairplay_gen_agree,
    fairplay_accurate,
    fairplay_falsefacts,

    intro_dv_feedback2,
    unfair_repeat,
    unfair_gen_agree,
    unfair_accurate,
    unfair_falsefacts,

    #### IF FIRSTFEEDBACK = UNFAIR:

    unfair_copy,
    fairplay_copy,

    intro_dv_feedback1_copy,
    unfair_repeat_copy,
    unfair_gen_agree_copy,
    unfair_accurate_copy,
    unfair_falsefacts_copy,

    intro_dv_feedback2_copy,
    fairplay_repeat_copy,
    fairplay_gen_agree_copy,
    fairplay_accurate_copy,
    fairplay_falsefacts_copy,

    # CheckBulletPoints,

    your_feedback,

    #### Legitimacy, Stability

    whoGotHigherPayoff,
    fair,                       # IF TEAM A: byChanceTeamAEasierQs
    byChanceTeamAEasierQs,
    feedbackMakesDifference,

    #### CONTROLS & DEMOGRAPHICS

    trivia,
    gender,
    born,
    education,
    atEssex,                    # IF YES: positionAtEssex and major
    positionAtEssex,
    british,                    # IF NO: nationality
    nationality,
    income,
    big5,
    whatAbout,
    email,
    theEnd
]
