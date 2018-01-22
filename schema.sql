CREATE TABLE IF NOT EXISTS variants
(
  id                        SERIAL NOT NULL
    CONSTRAINT variants_pkey
    PRIMARY KEY,
  gene                      VARCHAR,
  "Nucleotide Change"       VARCHAR,
  "Protein Change"          VARCHAR,
  "Other Mappings"          VARCHAR,
  alias                     VARCHAR,
  transcripts               VARCHAR,
  region                    VARCHAR,
  "Reported Classification" VARCHAR,
  "Inferred Classification" VARCHAR,
  source                    VARCHAR,
  "Last Evaluated"          DATE,
  "Last Updated"            DATE,
  url                       VARCHAR,
  "Submitter Comment"       VARCHAR,
  assembly                  VARCHAR,
  chr                       INTEGER,
  "Genomic Start"           INTEGER,
  "Genomic Stop"            INTEGER,
  ref                       VARCHAR,
  alt                       VARCHAR,
  accession                 VARCHAR,
  "Reported Ref"            VARCHAR,
  "Reported Alt"            VARCHAR
);

CREATE INDEX IF NOT EXISTS variants_gene_index
  ON variants (gene);

