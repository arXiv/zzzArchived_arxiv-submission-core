"""Things that should happen upon the :class:`.AddProposal` command."""

from typing import List, Iterable

from ..domain.event import Event, AddAnnotation, RemoveAnnotation, \
    AddProposal, SetPrimaryClassification, AddSecondaryClassification, \
    AcceptProposal
from ..domain.event.event import Condition
from ..domain.annotation import ClassifierResult, PlainTextExtraction, \
    ContentFlag, FeatureCount, ClassifierResults
from ..domain.submission import Submission
from ..domain.agent import Agent, User, System
from ..services import classifier, plaintext
from ..tasks import is_async

from arxiv import taxonomy


@AddProposal.bind()
def accept_system_cross_proposal(event: AddProposal, before: Submission,
                                 after: Submission, creator: Agent) \
        -> Iterable[Event]:
    """
    Accept any cross-list proposals generated by the system.

    This is a bit odd, since we likely generated the proposal in this very
    thread...but this seems to be an explicit feature of the classic system.
    """
    if event.proposal.proposed_event_type is AddSecondaryClassification \
            and type(event.creator) is System:
        yield AcceptProposal(creator=creator,
                             proposal_id=event.proposal.proposal_id,
                             comment="accept cross-list proposal from system")
