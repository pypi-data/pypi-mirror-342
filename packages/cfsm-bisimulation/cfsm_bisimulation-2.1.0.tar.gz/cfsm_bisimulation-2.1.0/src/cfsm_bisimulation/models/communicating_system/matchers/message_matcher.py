from ....libs.tools import merge_dicts
from .matcher import Matcher
from .no_candidate_match_exception import NoCandidateMatchException


class MessageMatcher(Matcher):

    def __init__(self, decider, match_manager, variable_matcher, symmetry_mode):
        super().__init__(decider, match_manager, symmetry_mode)
        self.variable_matcher = variable_matcher

    def match(self, action):
        compatible_messages, message_candidates = self.match_manager.candidates_collections_for(action)
        if len(compatible_messages) == 0:
            raise NoCandidateMatchException(f'There is no compatible candidates for message: {action.message}')

        if not self.match_manager.has_matched(action.message):
            if len(message_candidates) == 0:
                raise NoCandidateMatchException(f'There is no candidates for message: {action.message}')

            self.take_decision(action.message, message_candidates)

        return self.match_manager.get_match(action.message)

    def decide(self, decision):
        super().decide(decision)
        self.variable_matcher.decide(decision)

    def rollback(self, decision):
        super().rollback(decision)
        self.variable_matcher.rollback(decision)

    def serialize(self):
        return merge_dicts(
            {'messages': self.match_manager.serialize()},
            self.variable_matcher.serialize()
        )
