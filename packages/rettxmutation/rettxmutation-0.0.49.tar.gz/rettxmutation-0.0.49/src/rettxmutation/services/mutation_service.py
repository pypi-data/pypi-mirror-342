import re
import logging
from typing import Optional, Tuple
from rettxmutation.models.gene_models import (
    TranscriptMutation,
    GeneMutation,
    AffectedRegion
)
from rettxmutation.adapters.variant_validator_adapter import (
    VariantValidatorMutationAdapter,
    VariantValidatorNormalizationError
)
from rettxmutation.adapters.variant_validator_mapper import VariantValidatorMapper
from rettxmutation.adapters.mutalyzer_mutation_adapter import (
    MutalyzerMutationAdapter,
    MutationNormalizationError
)

logger = logging.getLogger(__name__)


def is_structural_variant(hgvs: str) -> bool:
    return bool(re.search(r"g\.\d+_\d+(del|dup|ins|delins)", hgvs))


class MutationService:
    def __init__(
        self,
        primary_transcript: str = "NM_004992.4",
        secondary_transcript: Optional[str] = "NM_001110792.2",
        target_assembly: str = "GRCh38"
    ):
        self.primary_transcript = primary_transcript
        self.secondary_transcript = secondary_transcript
        self.target_assembly = target_assembly

        # VariantValidator setup
        self.vv_adapter = VariantValidatorMutationAdapter(target_assembly=target_assembly)
        self.vv_mapper = VariantValidatorMapper()

        # Mutalyzer setup
        self.mut_adapter = MutalyzerMutationAdapter()

    def close(self):
        self.vv_adapter.close()
        self.mut_adapter.close()

    # ————————— SNV / small‐indel path —————————

    def get_gene_mutation(self, input_hgvs: str) -> GeneMutation:
        if is_structural_variant(input_hgvs):
            # Redirect complex cases
            return self.get_complex_gene_mutation(input_hgvs)

        try:
            # 1) extract & normalize to genomic
            transcript, detail = self._split_and_resolve(input_hgvs)
            resp1 = self.vv_adapter.normalize_mutation(
                variant_description=f"{transcript}:{detail}",
                select_transcripts=transcript
            )
            if resp1.get("messages"):
                raise Exception(resp1["messages"])

            unwrapped = self.vv_mapper.unwrap_response(resp1)
            genomic = self.vv_mapper.extract_genomic_coordinate(unwrapped, self.target_assembly)

            # 2) normalize again against both transcripts
            sel = f"{self.primary_transcript}|{self.secondary_transcript}"
            resp2 = self.vv_adapter.normalize_mutation(
                variant_description=genomic,
                select_transcripts=sel
            )
            if resp2.get("messages"):
                raise Exception(resp2["messages"])

            variants = self.vv_mapper.map_gene_variants(
                resp2, self.primary_transcript, self.secondary_transcript
            )
            p = variants.get(self.primary_transcript)
            s = variants.get(self.secondary_transcript)
            if not p or not s:
                raise Exception("Missing primary or secondary data")

            return GeneMutation(
                genome_assembly=self.target_assembly,
                genomic_coordinate=genomic,
                primary_transcript=TranscriptMutation(
                    hgvs_transcript_variant=p["hgvs_transcript_variant"],
                    protein_consequence_tlr=p["predicted_protein_consequence_tlr"],
                    protein_consequence_slr=p["predicted_protein_consequence_slr"]
                ),
                secondary_transcript=TranscriptMutation(
                    hgvs_transcript_variant=s["hgvs_transcript_variant"],
                    protein_consequence_tlr=s["predicted_protein_consequence_tlr"],
                    protein_consequence_slr=s["predicted_protein_consequence_slr"]
                )
            )

        except VariantValidatorNormalizationError as e:
            logger.error(f"VV normalization error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected VV error: {e}")
            raise

    def _split_and_resolve(self, hgvs: str) -> Tuple[str, str]:
        parts = hgvs.split(":", 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid HGVS format: {hgvs}")
        transcript, detail = parts
        # resolve transcript version via VV adapter…
        data = self.vv_adapter.resolve_transcripts(transcript.split(".")[0])
        refs = [t["reference"] for t in data.get("transcripts", [])]
        if "." in transcript:
            if transcript not in refs:
                raise ValueError(f"Transcript {transcript} not found")
            return transcript, detail
        versions = [r for r in refs if r.startswith(f"{transcript}.")]
        if not versions:
            raise ValueError(f"No versioned transcripts for {transcript}")
        # pick highest
        ver = max(versions, key=lambda r: int(r.split(".")[1]))
        return ver, detail

    # ————————— Complex‐deletion path —————————

    def get_complex_gene_mutation(self, genomic_hgvs: str) -> GeneMutation:
        """
        Handle large deletions/dup/ins via Mutalyzer normalize_mutation.
        """
        try:
            norm = self.mut_adapter.normalize_mutation(genomic_hgvs)
        except MutationNormalizationError as e:
            logger.error(f"Mutalyzer normalize error: {e}")
            raise

        # 1) Standardized genomic
        genomic = norm.get("normalized_description")
        if not genomic:
            raise MutationNormalizationError("No normalized_description returned")

        # 2) Extract start/end/size
        nm = norm.get("normalized_model", {})
        var = nm.get("variants", [])[0]
        loc = var["location"]
        start = loc["start"]["position"]
        end   = loc["end"]["position"]
        size  = end - start + 1

        # 3) Pick transcript‐level HGVS from the 'c' list
        tx_desc = None
        for eq in norm.get("equivalent_descriptions", {}).get("c", []):
            desc = eq["description"]
            ref  = eq["reference"]["selector"]["id"]
            tag  = eq.get("tag", {}).get("id","")
            if ref == self.primary_transcript:
                tx_desc = desc
                break
            if not tx_desc and tag.startswith("NM_"):  # MANE or similar
                tx_desc = desc
        if not tx_desc:
            # fallback to first in list
            first = norm["equivalent_descriptions"]["c"][0]
            tx_desc = first["description"]

        # 4) Build models
        return GeneMutation(
            genome_assembly=self.target_assembly,
            genomic_coordinate=genomic,
            variant_type="deletion",
            deletion_size=size,
            affected_region=AffectedRegion(start=start, end=end),
            primary_transcript=TranscriptMutation(
                hgvs_transcript_variant=tx_desc
            ),
            secondary_transcript=None
        )
