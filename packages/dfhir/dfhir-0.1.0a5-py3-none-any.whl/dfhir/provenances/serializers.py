"""provenance serializers."""

from dfhir.base.serializers import (
    BaseReferenceModelSerializer,
    BaseWritableNestedModelSerializer,
    IdentifierSerializer,
)
from dfhir.provenances.models import Provenance, ProvenanceReference


class ProvenanceReferenceSerializer(BaseReferenceModelSerializer):
    """Provenance reference serializer."""

    identifier = IdentifierSerializer(many=False, required=False)

    class Meta:
        """Meta class."""

        model = ProvenanceReference
        exclude = ["created_at", "updated_at"]


class ProvenanceSerializer(BaseWritableNestedModelSerializer):
    """Provenance serializer."""

    target = ProvenanceReferenceSerializer(many=False, required=False)

    class Meta:
        """Meta class."""

        model = Provenance
        exclude = ["created_at", "updated_at"]
