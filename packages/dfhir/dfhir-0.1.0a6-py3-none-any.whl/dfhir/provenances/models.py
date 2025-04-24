"""provinces models."""

from django.db import models

from dfhir.base.models import BaseReference, Identifier, Reference, TimeStampedModel

# Create your models here.


class Provenance(TimeStampedModel):
    """Provinance model."""

    target = models.ManyToManyField(
        Reference, related_name="provinance_target", blank=True
    )
    # TODO: setting up a minimal implementation of provenance model. It will be implemented full in a difference ticket.


class ProvenanceReference(BaseReference):
    """medication request insurance reference model."""

    identifier = models.ForeignKey(
        Identifier,
        on_delete=models.SET_NULL,
        null=True,
        related_name="provinance_reference_identifier",
    )
    provenance = models.ForeignKey(
        Provenance,
        on_delete=models.SET_NULL,
        null=True,
        related_name="provinance_reference_provenance",
    )
