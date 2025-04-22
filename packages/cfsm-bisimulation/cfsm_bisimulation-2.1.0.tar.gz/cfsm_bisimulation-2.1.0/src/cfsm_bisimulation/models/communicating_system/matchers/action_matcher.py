from ....libs.tools import merge_dicts
from ..action import Action


class ActionMatcher:

    def __init__(self, decider, participant_matcher, message_matcher, symmetry_mode):
        self.decider = decider
        self.participant_matcher = participant_matcher
        self.message_matcher = message_matcher
        self.symmetry_mode = symmetry_mode

    def match(self, action):
        left_participant, right_participant = self.participant_matcher.match(action)
        message = self.message_matcher.match(action)

        return Action(left_participant, right_participant, action.action, message)

    def match_next(self):
        self.decider.take_next_decision()

    def match_assertion(self, assertion):
        return self.message_matcher.variable_matcher.match_assertion(assertion)

    def has_more_possible_matches(self):
        return self.decider.there_are_decisions_to_take()

    def serialize(self):
        return merge_dicts(
            self.participant_matcher.serialize(),
            self.message_matcher.serialize()
        )
