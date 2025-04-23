import logging
import re
from typing import Optional, Tuple, List

from rettxmutation.models.gene_models import TranscriptMutation, GeneMutation
from rettxmutation.adapters.variant_validator_adapter import (
    VariantValidatorMutationAdapter,
    VariantValidatorNormalizationError
)
from rettxmutation.adapters.variant_validator_mapper import VariantValidatorMapper
from rettxmutation.adapters.mutalyzer_mutation_adapter import (
    MutalyzerMutationAdapter,
    MutationNormalizationError,
    MutationMappingError
)
from rettxmutation.adapters.mutalyzer_mutation_mapper import MutalyzerMapper

logger = logging.getLogger(__name__)


def is_structural_variant(hgvs: str) -> bool:
    """
    Return True if the HGVS string represents a structural variant
    (large deletion, duplication, insertion, or delins).
    """
    return bool(re.search(r"g\.\d+_\d+(del|dup|ins|delins)", hgvs))


class MutationService:
    """
    Service for normalizing and mapping both simple (SNV/indel) and
    complex (large del/dup/ins) HGVS mutations into a unified GeneMutation model.
    """

    def __init__(
        self,
        primary_transcript: str = "NM_004992.4",
        secondary_transcript: Optional[str] = "NM_001110792.2",
        target_assembly: str = "GRCh38"
    ):
        # Transcripts & genome build
        self.primary_transcript = primary_transcript
        self.secondary_transcript = secondary_transcript
        self.target_assembly = target_assembly

        # VariantValidator pieces (for SNV / small indels)
        self.vv_adapter = VariantValidatorMutationAdapter(target_assembly=target_assembly)
        self.vv_mapper = VariantValidatorMapper()

        # Mutalyzer adapter + mapper (for large structural variants)
        self.mut_adapter = MutalyzerMutationAdapter()
        self.mut_map    = MutalyzerMapper()

    def close(self):
        """Clean up any open sessions or resources."""
        self.vv_adapter.close()
        self.mut_adapter.close()

    def get_gene_mutation(self, input_hgvs: str) -> GeneMutation:
        """
        Main entry point. Dispatches based on HGVS string and
        presence/absence of a secondary transcript.

        - If the HGVS is a structural variant (g.<start>_<end>del|dup|ins),
          routes to Mutalyzer normalization + mapping.
        - Else if secondary_transcript is None, does a single-transcript SNV/indel flow.
        - Otherwise, does the two-step SNV/indel flow via VariantValidator.
        """
        # 1) Structural variant → Mutalyzer
        if is_structural_variant(input_hgvs):
            logger.info(f"Detected structural variant, using Mutalyzer path for {input_hgvs}")
            return self._complex_via_mutalyzer(input_hgvs)

        # 2) Single-transcript only (e.g. FOXG1) → simple VariantValidator call
        if self.secondary_transcript is None:
            logger.info(f"Single-transcript SNV/indel for {input_hgvs}")
            return self._snv_unique(input_hgvs)

        # 3) Default two-transcript SNV/indel flow
        logger.info(f"Dual-transcript SNV/indel for {input_hgvs}")
        return self._snv_dual(input_hgvs)

    def _split_and_resolve(self, hgvs: str) -> Tuple[str, str]:
        """
        Split "TRANSCRIPT:detail" and resolve to a full versioned transcript
        using VariantValidator's transcript resolver.
        """
        parts = hgvs.split(":", 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid HGVS format (expected TRANSCRIPT:detail): {hgvs}")
        transcript, detail = parts

        tv = self.vv_adapter.resolve_transcripts(transcript.split(".")[0])
        available: List[str] = [t["reference"] for t in tv.get("transcripts", [])]
        if not available:
            raise ValueError(f"No transcripts found for prefix: {transcript}")

        if "." in transcript:
            if transcript not in available:
                raise ValueError(f"Transcript {transcript} not available")
            chosen = transcript
        else:
            versions = [v for v in available if v.startswith(f"{transcript}.")]
            if not versions:
                raise ValueError(f"No versioned transcripts for {transcript}")
            chosen = max(versions, key=self._extract_version_number)

        return chosen, detail

    @staticmethod
    def _extract_version_number(transcript_ref: str) -> int:
        """
        Given a reference like "NM_004992.4", return the integer version (4).
        """
        try:
            return int(transcript_ref.split(".")[1])
        except Exception:
            return -1

    def _snv_unique(self, hgvs: str) -> GeneMutation:
        """
        SNV/indel flow when only primary_transcript is requested.
        Single normalization + map.
        """
        transcript, detail = self._split_and_resolve(hgvs)

        try:
            resp = self.vv_adapter.normalize_mutation(
                variant_description=f"{transcript}:{detail}",
                select_transcripts=transcript
            )
        except VariantValidatorNormalizationError as e:
            logger.error(f"VariantValidator normalization error for {hgvs}: {e}")
            raise

        if resp.get("messages"):
            raise Exception(f"VariantValidator messages: {resp['messages']}")

        unwrapped = self.vv_mapper.unwrap_response(resp)
        genomic  = self.vv_mapper.extract_genomic_coordinate(unwrapped, self.target_assembly)
        mapped   = self.vv_mapper.map_gene_variant(unwrapped)

        return GeneMutation(
            genome_assembly=self.target_assembly,
            genomic_coordinate=genomic,
            primary_transcript=TranscriptMutation(
                hgvs_transcript_variant=mapped["hgvs_transcript_variant"],
                protein_consequence_tlr=mapped.get("predicted_protein_consequence_tlr"),
                protein_consequence_slr=mapped.get("predicted_protein_consequence_slr")
            ),
            secondary_transcript=None
        )

    def _snv_dual(self, hgvs: str) -> GeneMutation:
        """
        Two-step SNV/indel flow via VariantValidator:
          1) normalize to genomic
          2) normalize genomic against both transcripts
        """
        transcript, detail = self._split_and_resolve(hgvs)

        # Step 1: obtain genomic coordinate
        try:
            resp1 = self.vv_adapter.normalize_mutation(
                variant_description=f"{transcript}:{detail}",
                select_transcripts=transcript
            )
        except VariantValidatorNormalizationError as e:
            logger.error(f"VariantValidator step1 error for {hgvs}: {e}")
            raise

        if resp1.get("messages"):
            raise Exception(f"VariantValidator step1 messages: {resp1['messages']}")

        un1     = self.vv_mapper.unwrap_response(resp1)
        genomic = self.vv_mapper.extract_genomic_coordinate(un1, self.target_assembly)

        # Step 2: re-normalize against both transcripts
        sel   = f"{self.primary_transcript}|{self.secondary_transcript}"
        resp2 = self.vv_adapter.normalize_mutation(
            variant_description=genomic,
            select_transcripts=sel
        )
        if resp2.get("messages"):
            raise Exception(f"VariantValidator step2 messages: {resp2['messages']}")

        variants = self.vv_mapper.map_gene_variants(resp2,
                                                    self.primary_transcript,
                                                    self.secondary_transcript)
        p = variants.get(self.primary_transcript)
        s = variants.get(self.secondary_transcript)
        if not p or not s:
            raise Exception("Missing transcript data in VariantValidator response")

        return GeneMutation(
            genome_assembly=self.target_assembly,
            genomic_coordinate=genomic,
            primary_transcript=TranscriptMutation(
                hgvs_transcript_variant=p["hgvs_transcript_variant"],
                protein_consequence_tlr=p.get("predicted_protein_consequence_tlr"),
                protein_consequence_slr=p.get("predicted_protein_consequence_slr")
            ),
            secondary_transcript=TranscriptMutation(
                hgvs_transcript_variant=s["hgvs_transcript_variant"],
                protein_consequence_tlr=s.get("predicted_protein_consequence_tlr"),
                protein_consequence_slr=s.get("predicted_protein_consequence_slr")
            )
        )

    def _complex_via_mutalyzer(self, genomic_hgvs: str) -> GeneMutation:
        """
        Handle large deletions/dup/insertions via Mutalyzer.normalize_mutation +
        MutalyzerMapper.
        """
        # 1) Normalize via Mutalyzer
        try:
            norm = self.mut_adapter.normalize_mutation(genomic_hgvs)
        except MutationNormalizationError as e:
            logger.error(f"Mutalyzer normalization failed for {genomic_hgvs}: {e}")
            raise

        # 2) Map to your domain via the MutalyzerMapper
        try:
            gene_mut = self.mut_map.map_to_gene_mutation(
                norm_response=norm,
                primary_transcript=self.primary_transcript,
                target_assembly=self.target_assembly
            )
        except MutationMappingError as e:
            logger.error(f"Mutalyzer mapping failed: {e}")
            raise

        return gene_mut
