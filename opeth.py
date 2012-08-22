# All of the example bots in this file derive from the base Bot class.  See
# how this is implemented by looking at player.py.  The API is very well
# documented there.
from player import Bot

# Each bot has access to the game state, stored in the self.game member
# variable.  See the State class in game.py for the full list of variables you
# have access to from your bot.
#
# The examples below purposefully use only self.game to emphasize its
# importance.  Advanced bots tend to only use the game State class to decide!
from game import State


# Many bots will use random decisions to break ties between two equally valid
# options.  The simple bots below rely on randomness heavily, and expert bots
# tend to use other statistics and criteria (e.g. who is winning) to avoid ties
# altogether!
import random


class Opeth(Bot):
    """Opeth is a melancholic bot."""

    # List of spies. We only get this info if we are a spy.
    spy_spies = None

    # My interpretation of the world. This is dict where keys are Player objects
    # and values are confidence scores for each player. Confidence scores start
    # at 0 and get higher if I believe that player is not a spy.
    # We do not use any additional info granted to us if we are a spy to update
    # this.
    my_guess = dict()

    # This is like my_guess except we update it based on information that other
    # resistance members have. It is not as accurate as my_guess but will
    # provide an insight on what other bots think about the world.
    their_guess = dict()

    # List of players that I am sure are spies.
    spies_for_sure = []

    def onGameRevealed(self, players, spies):
        """This function will be called to list all the players, and if you're
        a spy, the spies too -- including others and yourself.
        @param players  List of all players in the game including you.
        @param spies    List of players that are spies, or an empty list.
        """
        self.spy_spies = spies

        self.my_guess = new dict(zip(players, [0] * 5))
        self.their_guess = new dict(zip(players, [0] * 5))

    def onMissionAttempt(self, mission, tries, leader):
        """Callback function when a new turn begins, before the
        players are selected.
        @param mission  Integer representing the mission number (1..5).
        @param tries    Integer count for its number of tries (1..5).
        @param leader   A Player representing who's in charge.
        """
        pass

    def select(self, players, count):
        """Pick a sub-group of players to go on the next mission.
        @param players  The list of all players in the game to pick from.
        @param count    The number of players you must now select.
        @return list    The players selected for the upcoming mission.
        """
        if not self.spy_spies:
            return random.sample(self.game.players, count)
        else:
            # Purposefully go out of our way to pick the other spy so that we
            # can trick him with deceptive sabotaging!
            self.log.info("Picking the other spy to trick them!")
            return list(self.spy_spies) + random.sample(set(self.game.players) - set(self.spy_spies), count-2)

    def onTeamSelected(self, leader, team):
        """Called immediately after the team is selected to go on a mission,
        and before the voting happens.
        @param leader   The leader in charge for this mission.
        @param team     The team that was selected by the current leader.
        """

        # Because we are bots and there is no conversation involved, there is no
        # point in not selecting yourself as part of the team. If they didn't
        # do it, that is suspicious.
        if(leader not in team):
            self.my_guess[leader] -= 5
            self.their_guess[leader] -= 5

        pass

    def vote(self, team):
        """Given a selected team, decide whether the mission should proceed.
        @param team      List of players with index and name.
        @return bool     Answer Yes/No.
        """
        return True

    def onVoteComplete(self, votes):
        """Callback once the whole team has voted.
        @param votes        Boolean votes for each player (ordered).
        """
        pass

    def sabotage(self):
        """Decide what to do on the mission once it has been approved.  This
        function is only called if you're a spy, otherwise you have no choice.
        @return bool        Yes to shoot down a mission.
        """
        spies = [s for s in self.game.team if s in self.spy_spies]
        if len(spies) > 1:
            # Intermediate to advanced bots assume that sabotage is "controlled"
            # by the mission leader, so we go against this practice here.
            if self == self.game.leader:
                self.log.info("Not coordinating not sabotaging because I'm leader.")
                return False

            # This is the opposite of the same practice, sabotage if the other
            # bot is expecting "control" the sabotage.
            if self.game.leader in spies:
                self.log.info("Not coordinating and sabotaging despite the other spy being leader.")
                return True
            spies.remove(self)

            # Often, intermeditae bots synchronize based on their global index
            # number.  Here we go against the standard pracitce and do it the
            # other way around!
            self.log.info("Coordinating according to the position around the table...")
            return self.index > spies[0].index
        return True

    def onMissionComplete(self, sabotaged):
        """Callback once the players have been chosen.
        @param selected     List of players that participated in the mission.
        @param sabotaged    Integer how many times the mission was sabotaged.
        """

        # Can we know for sure if the whole team are spies?
        if(len(self.game.team) == sabotaged):
            for spy in self.game.team:
                self.my_guess[spy] -= 100
                self.their_guess[spy] -= 100
                self.spies_for_sure.append(spy)

        # Can we know for sure if the rest of the team is a spy?
        # 3 conditions: I am not a spy, I am in the team,
        # the number of sabotaged votes is equal to the
        # team size minus one (my vote)
        if(self.spy_spies is None and self in self.game.team and sabotaged == len(self.game.team) - 1):
            for spy in self.game.team:
                if(self is not spy)
                self.my_guess[spy] -= 100
                self.spies_for_sure.append(spy)

        # If this mission failed, that team gets penalized (a bit),
        # otherwise we gain confidence in them.
        # I wish I knew how many
        for player in self.game.team:
            if(sabotaged):
                self.my_guess[player] -= 1
                self.their_guess[player] -= 1
            else:
                self.my_guess[player] += 1
                self.their_guess[player] += 1


        pass

    def onGameComplete(self, win, spies):
        """Callback once the game is complete, and everything is revealed.
        @param win          Boolean if the Resistance won.
        @param spies        List of only the spies in the game.
        """
        pass
