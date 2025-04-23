from typing import Optional, Literal
from pydantic import BaseModel, Field


class TranscriptMutation(BaseModel):
    """
    Represents detailed mutation descriptions for transcript and protein levels.
    """
    hgvs_transcript_variant: str = Field(..., description="Full transcript mutation description (e.g., NM_004992.3:c.916C>T)")
    protein_consequence_tlr: Optional[str] = Field(None, description="Full protein consequence description (e.g., NP_004983.2:p.Ser306Cys)")
    protein_consequence_slr: Optional[str] = Field(None, description="Short protein consequence description in SLR format (e.g., NP_004983.1:p.(R306C))")


class AffectedRegion(BaseModel):
    """
    Represents a genomic region affected by a large structural variant (e.g., deletion).
    """
    start: int = Field(..., description="Start position of the affected region")
    end: int = Field(..., description="End position of the affected region")


class GeneMutation(BaseModel):
    """
    Comprehensive mutation data model for Rett Syndrome (MECP2) mutations.
    """
    genome_assembly: str = Field(..., description="Genome assembly version (e.g., GRCh37 or GRCh38)")
    genomic_coordinate: str = Field(..., description="Canonical genomic coordinate (e.g., NC_000023.11:g.154030912G>A or NC_000023.11:g.154010939_154058566del)")
    variant_type: Literal['SNV', 'deletion', 'duplication', 'insertion', 'indel'] = Field('SNV', description="Type of variant")
    deletion_size: Optional[int] = Field(None, description="Size of the deletion in base pairs, if applicable")
    affected_region: Optional[AffectedRegion] = Field(None, description="Genomic region affected by the variant")
    primary_transcript: Optional[TranscriptMutation] = Field(None, description="Primary transcript mutation details NM_004992.4")
    secondary_transcript: Optional[TranscriptMutation] = Field(None, description="Secondary transcript mutation details NM_001110792.2")


# Raw mutation data model (returned by the OpenAI model)
class RawMutation(BaseModel):
    """
    Represents the raw mutation data returned by the OpenAI model.
    """
    mutation: str = Field(..., description="Raw mutation string (e.g., 'NM_004992.4:c.916C>T')")
    confidence: float = Field(..., description="Confidence score for the mutation (0.0 to 1.0)")
