from ..matches.match_manager import MatchManager
from ..matches.match_with_candidates_manager import MatchWithCandidatesManager
from ..matches.message_match_manager import MessageMatchManager
from ....libs.symmetrical_collections.list import SymmetricalList
from ....libs.symmetrical_collections.dict import SymmetricalDict


class MatchManagerFactory:

    def __init__(self, cfsm_left, cfsm_right, symmetry_mode):
        self.cfsm_left = cfsm_left
        self.cfsm_right = cfsm_right
        self.symmetry_mode = symmetry_mode
        self.participant_match_manager = None
        self.message_match_manager = None
        self.variable_match_manager = None

    # Participant candidates to match with cfsm_left are cfsm_right participants.
    def participant_match(self):
        if self.participant_match_manager is None:
            self.participant_match_manager = MatchWithCandidatesManager(
                matches=self.empty_matches(),
                candidates=SymmetricalList(
                    self.cfsm_right.get_participants(),
                    self.cfsm_left.get_participants(),
                    self.symmetry_mode
                )
            )
            self.participant_match_manager.matches.add(self.cfsm_left.main_participant, self.cfsm_right.main_participant)
        return self.participant_match_manager

    # Message and action candidates to match with cfsm_left are cfsm_right messages and actions
    def message_match(self):
        if self.message_match_manager is None:
            self.message_match_manager = MessageMatchManager(
                matches=self.empty_matches(),
                candidates=SymmetricalList(
                    list(self.cfsm_right.messages()),
                    list(self.cfsm_left.messages()),
                    self.symmetry_mode
                ),
                actions=SymmetricalList(
                    self.cfsm_right.actions(),
                    self.cfsm_left.actions(),
                    self.symmetry_mode
                ),
                participant_match_manager=self.participant_match()
            )
        return self.message_match_manager

    def variable_match(self):
        if self.variable_match_manager is None:
            self.variable_match_manager = MatchManager(self.empty_matches())
        return self.variable_match_manager

    def empty_matches(self):
        return SymmetricalDict({}, {}, self.symmetry_mode)
