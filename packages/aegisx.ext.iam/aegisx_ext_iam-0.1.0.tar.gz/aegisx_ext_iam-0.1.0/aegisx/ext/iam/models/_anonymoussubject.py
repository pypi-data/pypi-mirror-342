from aegisx.ext.iam.types import ANONYMOUS
from ._subject import Subject


class AnonymousSubject(Subject):
    """
    Represents an anonymous subject (i.e., a user who is not authenticated).

    This class is a subclass of `Subject` and provides an implementation for
    managing anonymous users within the IAM system. The principal for this
    subject is set to the `AnonymousPrincipal`, which represents all users
    who are not authenticated.
    """

    @property # pragma: no cover
    def email(self) -> None:
        return None

    @property # pragma: no cover
    def email_verified(self):
        return False

    @property # pragma: no cover
    def phonenumber(self) -> None:
        return None

    @property # pragma: no cover
    def phonenumber_verified(self) -> None:
        return None

    def principals(self):
        return {ANONYMOUS}