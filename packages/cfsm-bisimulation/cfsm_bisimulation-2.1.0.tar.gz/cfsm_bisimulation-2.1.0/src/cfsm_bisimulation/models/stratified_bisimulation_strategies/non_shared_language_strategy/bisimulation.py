from .match_exception import MatchException
from .simulation import NonSharedLanguageSimulationStrategy
from ..knowledge import Knowledge
from ..shared_language_strategy.bisimulation import SharedLanguageBisimulationStrategy


class NonSharedLanguageBisimulationStrategy(SharedLanguageBisimulationStrategy):

    def __init__(self, cfsm_left, cfsm_right, matcher):
        super().__init__(cfsm_left, cfsm_right)
        self.matcher = matcher
        self.initial_relation = None

    def execute(self, minimize):
        while not self.result_is_a_bisimulation() and self.matcher.has_more_possible_matches():
            self._try_calculate_bisimulation_relation()

        if minimize:
            self._minimize_current_relation()

    def result(self):
        return super().result(), self.matcher.serialize()

    def _try_calculate_bisimulation_relation(self):
        self._set_initial_relation_as_current()
        try:
            self._calculate_bisimulation_from_current_relation()
        except MatchException:
            self._invalidate_current_relation()

        if not self.result_is_a_bisimulation():
            self._invalidate_current_relation()
            self.matcher.match_next()

    def _initial_relation(self):
        if self.initial_relation is None:
            self.initial_relation = super()._initial_relation()

        return self.initial_relation

    def _enable_symmetric_mode_with(self, candidate_element):
        self.symmetric_mode = True
        self.current_simulation = NonSharedLanguageSimulationStrategy(self, tuple(reversed(candidate_element)))
        self.matcher.symmetry_mode.enable()

    def _disable_symmetric_mode_with(self, candidate_element):
        self.symmetric_mode = False
        self.current_simulation = NonSharedLanguageSimulationStrategy(self, candidate_element)
        self.matcher.symmetry_mode.disable()

    def match(self):
        action = self.current_simulation.simulated_transition.label
        knowledge = self.current_simulation.simulated_knowledge.clean_by(action)

        matched_knowledge = self._match_knowledge(knowledge.add(self.current_simulation.simulated_transition.assertion))
        matched_action = self.matcher.match(action)

        return matched_action, matched_knowledge

    def _match_knowledge(self, knowledge):
        self._match_actions_that_define_non_matched_variables_in(knowledge)

        matched_knowledge = Knowledge(frozenset())

        for assertion in knowledge.assertions_set:
            matched_knowledge = matched_knowledge.add(
                self.matcher.match_assertion(assertion)
            )
        return matched_knowledge

    def _match_actions_that_define_non_matched_variables_in(self, knowledge):
        non_matched_variables = set()

        for assertion in knowledge.assertions_set:
            for variable in assertion.get_variables():
                if not self.matcher.message_matcher.variable_matcher.match_manager.has_matched(variable):
                    non_matched_variables.add(variable)

        transitions_for_non_matched_variables = self.current_simulation.simulated_state.graph.transitions_that_define(non_matched_variables)
        for transition in transitions_for_non_matched_variables:
            self.matcher.match(transition.label)
