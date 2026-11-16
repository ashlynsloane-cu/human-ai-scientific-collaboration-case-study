# GSEA gene-of-interest provenance verification

Use `scripts/check_gsea_goi_consistency.py` to compare a gene-set membership table against an independently saved gene–pathway edge table. This is a **structural** integrity check, not independent confirmation that the gene sets, rankings, biological samples, or original normalization were correct.

Input format:

- TSV pathway table: `NAME`, `GenesInPathway` (comma-separated), `AnyLeadingEdgeGOI`
- CSV edges: `Pathway`, `Gene`, `IsLeadingEdge`, `IsGeneOfInterest`

Example, using locally authorized input files (do **not** commit the inputs):

```bash
python3 scripts/check_gsea_goi_consistency.py \
  --pathways /path/to/Pathways_with_GOI_clean.txt \
  --edges /path/to/Cytoscape_Gene_Pathway_Edges.csv --strict
python3 -m unittest discover -s tests -p 'test_gsea_goi_consistency.py' -v
```

The checker treats full pathway membership and leading-edge membership as **separate** concepts. `AnyLeadingEdgeGOI` is a pathway-wide Boolean indicating whether **any** gene of interest is leading edge. It must not be treated as a gene-specific flag for a particular client. Absence of a mismatch means only that these two exports are mutually consistent.

No human conversation excerpts, participant records, private study counts, gene identities, or restricted input tables are included in this commit.
