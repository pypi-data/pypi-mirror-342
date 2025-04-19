class OxiTraitError(RuntimeError):
    pass


class DisallowedInitError(OxiTraitError):
    pass


class NonMethodAttrError(OxiTraitError):
    pass


class MultipleImplementationError(OxiTraitError):
    pass


class InheritanceError(OxiTraitError):
    pass


class NamingConventionError(OxiTraitError):
    pass