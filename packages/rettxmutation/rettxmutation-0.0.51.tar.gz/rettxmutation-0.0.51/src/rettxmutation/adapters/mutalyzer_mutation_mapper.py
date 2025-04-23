from typing import Optional
from rettxmutation.models.gene_models import (GeneMutation, TranscriptMutation, AffectedRegion)
from rettxmutation.adapters.mutalyzer_mutation_adapter import MutationMappingError


class MutalyzerMapper:
    """
    Anti-corruption layer: maps Mutalyzer normalize_mutation response into GeneMutation models.
    """
    def map_to_gene_mutation(
        self,
        norm_response: dict,
        primary_transcript: str,
        target_assembly: str = "GRCh38"
    ) -> GeneMutation:
        # 1. Genomic coordinate
        genomic_coordinate = norm_response.get("normalized_description")
        if not genomic_coordinate:
            raise MutationMappingError("Missing normalized_description in Mutalyzer response")

        # 2. Extract variant record
        variants = norm_response.get("normalized_model", {}).get("variants", [])
        if not variants:
            raise MutationMappingError("No variants found in Mutalyzer normalized_model")
        var = variants[0]
        variant_type = var.get("type")

        # 3. Extract affected region
        loc = var.get("location", {})
        start = loc.get("start", {}).get("position")
        end = loc.get("end", {}).get("position")
        if start is None or end is None:
            raise MutationMappingError("Could not find start/end positions in Mutalyzer response")
        size = end - start + 1
        affected_region = AffectedRegion(start=start, end=end)

        # 4. Find transcript-level equivalent description
        eqs = norm_response.get("equivalent_descriptions", {}).get("c", [])
        transcript_hgvs: Optional[str] = None
        # First, try to match primary transcript exactly
        for entry in eqs:
            ref = entry.get("reference", {}).get("selector", {}).get("id")
            if ref == primary_transcript:
                transcript_hgvs = entry.get("description")
                break
        # Fallback: pick MANE tag or first available
        if not transcript_hgvs and eqs:
            for entry in eqs:
                if entry.get("tag", {}).get("details", "").startswith("MANE"):
                    transcript_hgvs = entry.get("description")
                    break
        if not transcript_hgvs:
            transcript_hgvs = eqs[0].get("description") if eqs else None

        if not transcript_hgvs:
            raise MutationMappingError("No transcript-level HGVS found in Mutalyzer equivalents")

        # 5. Build TranscriptMutation
        transcript_obj = TranscriptMutation(
            hgvs_transcript_variant=transcript_hgvs,
            protein_consequence_tlr=None,
            protein_consequence_slr=None
        )

        # 6. Assemble GeneMutation
        return GeneMutation(
            genome_assembly=target_assembly,
            genomic_coordinate=genomic_coordinate,
            variant_type=variant_type,
            deletion_size=size if variant_type == "deletion" else None,
            affected_region=affected_region,
            primary_transcript=transcript_obj,
            secondary_transcript=None
        )
