from .state import State
from .transition import Transition
from ...libs.tools import TrueFormula
from ..stratified_bisimulation_strategies.shared_language_strategy.bisimulation import SharedLanguageBisimulationStrategy
from ..assertable_finite_state_machines.assertion import Assertion


class AFSM:

    def __init__(self):
        self.states = {}
        self.transitions_by_source_id = {}
        self.initial_state = None

    def add_state(self, state_id, theory=[]):
        # validate not present
        self.states[state_id] = State(self, state_id, theory)
        self.transitions_by_source_id[state_id] = []

    def add_states(self, *states):
        for state in states:
            if isinstance(state, tuple):
                state_id, theory = state
            else:
                state_id, theory = state, []
            
            self.add_state(state_id, theory)

    def set_as_initial(self, state_id):
        # validate exists
        self.initial_state = self.states[state_id]

    def set_as_finals(self, *state_ids):
        for state_id in state_ids:
            self.states[state_id].set_as_final()

    # assertion must be a z3 assertion
    def add_transition_between(self, source_id, target_id, label, formula=TrueFormula):
        # validate present
        # validate transition not exist

        source = self.states[source_id]
        target = self.states[target_id]

        assertion = Assertion(formula)

        transition = Transition(source, target, label, assertion)

        self.transitions_by_source_id[source_id].append(transition)

    def transitions_of(self, state_id):
        #  validate present
        return self.transitions_by_source_id[state_id]

    def transitions_with_label_of(self, state_id, label):
        return set(filter(lambda transition: transition.label == label, self.transitions_of(state_id)))

    def all_assertions(self):
        return set(
            map(
                lambda transition: transition.assertion,
                self.all_transitions()
            )
        )

    def all_transitions(self):
        return [transition for transitions in self.transitions_by_source_id.values() for transition in transitions]

    def get_states(self):
        return set(self.states.values())

    # Se esta asumiendo que tanto "self", como "afsm" son validos, i.e. que cumplen con lo que cumple un cfsm que son los que estamos usando de base.
    def calculate_bisimulation_with(self, afsm, minimize=False):
        strategy = self._bisimulation_strategy_with(afsm)
        strategy.execute(minimize)
        return strategy.result()

    def _bisimulation_strategy_with(self, afsm):
        return SharedLanguageBisimulationStrategy(self, afsm)

    def transitions_that_define(self, variables):
        transitions = [transition for transition in self.all_transitions() if transition.label.contains_any(variables)]

        return transitions
