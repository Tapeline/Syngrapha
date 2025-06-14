from adaptix import Provider
from adaptix._internal.provider.loc_stack_filtering import Pred
from adaptix.conversion import link

from syngrapha.utils.func import identity


def id_link(src: Pred, dst: Pred) -> Provider:
    """Link with embedded identity coercer."""
    return link(src, dst, coercer=identity)
