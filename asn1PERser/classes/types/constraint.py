from pyasn1.type.constraint import ValueRangeConstraint, ConstraintsIntersection, ConstraintsUnion, SingleValueConstraint, \
    ValueSizeConstraint


MIN = float('-inf')
MAX = float('inf')


class NoConstraint(ConstraintsIntersection):
    def __init__(self):
        self.extensionMarker = False
        self.lowerEndpoint = None
        self.upperEndpoint = None
        super(NoConstraint, self).__init__()


class ExtensionMarker(ConstraintsIntersection):
    def __init__(self, present=False):
        self.extensionMarker = present
        self.lowerEndpoint = None
        self.upperEndpoint = None
        super(ExtensionMarker, self).__init__()


class SequenceOfValueSize(ConstraintsIntersection):
    '''
    Use this constraint with SEQUENCE OF:
    with asn1 schema:

        MySeqOf::= SEQUENCE (SIZE(1..2)) OF OCTET STRING

    Python code:

        class MySeqOf(SequenceOfType):
            subtypeSpec SequenceOfValueSize(1, 2)
            componentType = OctetStringType()

    This is due to asn1PERser 'ValueSize' and pyasn1 'ValueSizeConstraint' will try to apply
    this size constraint check on componentType and NOT on SEQUENCE OF itself.
    The consequence of this is there will be no exception raised when MySeqOf is added 3rd (4th, 5th etc.)
    OCTET STRING.
    '''
    def __init__(self, lower_endpoint, upper_endpoint, extensionMarker=False):
        self.extensionMarker = extensionMarker
        self.lowerEndpoint = None if lower_endpoint == MIN else lower_endpoint
        self.upperEndpoint = None if upper_endpoint == MAX else upper_endpoint
        super(SequenceOfValueSize, self).__init__()


class ValueRange(ValueRangeConstraint):
    def __init__(self, lower_endpoint, upper_endpoint, extensionMarker=False):
        self.extensionMarker = extensionMarker
        self.lowerEndpoint = None if lower_endpoint == MIN else lower_endpoint
        self.upperEndpoint = None if upper_endpoint == MAX else upper_endpoint
        super(ValueRange, self).__init__(lower_endpoint, upper_endpoint)

    def _testValue(self, value, idx):
        if not self.extensionMarker:
            return super(ValueRange, self)._testValue(value, idx)


class SingleValue(SingleValueConstraint):
    def __init__(self, extension_marker=False, *values):
        self.extensionMarker = extension_marker
        self.lowerEndpoint = min(values)
        self.upperEndpoint = max(values)
        super(SingleValue, self).__init__(*values)

    def _testValue(self, value, idx):
        if not self.extensionMarker:
            return super(SingleValue, self)._testValue(value, idx)


class ValueSize(ValueSizeConstraint):
    def __init__(self, lower_endpoint, upper_endpoint, extensionMarker=False):
        self.extensionMarker = extensionMarker
        self.lowerEndpoint = None if lower_endpoint == MIN else lower_endpoint
        self.upperEndpoint = None if upper_endpoint == MAX else upper_endpoint
        super(ValueSize, self).__init__(lower_endpoint, upper_endpoint)

    def _testValue(self, value, idx):
        if not self.extensionMarker:
            return super(ValueSize, self)._testValue(value, idx)


class ConstraintOr(ConstraintsUnion):
    def __init__(self, extensionMarker=False, *constraints):
        self.extensionMarker = extensionMarker
        self.lowerEndpoint = min([constraint.lowerEndpoint for constraint in constraints])
        self.upperEndpoint = max([constraint.upperEndpoint for constraint in constraints])
        super(ConstraintOr, self).__init__(*constraints)

    def _testValue(self, value, idx):
        if not self.extensionMarker:
            return super(ConstraintOr, self)._testValue(value, idx)


class ConstraintAnd(ConstraintsIntersection):
    def __init__(self, extensionMarker=False, *constraints):
        self.extensionMarker = extensionMarker
        self.lowerEndpoint = min([constraint.lowerEndpoint for constraint in constraints])
        self.upperEndpoint = max([constraint.upperEndpoint for constraint in constraints])
        super(ConstraintAnd, self).__init__(*constraints)

    def _testValue(self, value, idx):
        if not self.extensionMarker:
            return super(ConstraintAnd, self)._testValue(value, idx)
