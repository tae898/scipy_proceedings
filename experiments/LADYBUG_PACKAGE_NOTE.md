# Why the experiments still pin `real_ladybug==0.15.3` (2026-07-10)

The official LadybugDB package is `ladybug` (0.18.1, from LadybugDB/ladybug-python).
`real_ladybug` is published from a different repo (lbugdb/lbug) and is frozen at
0.15.3. We migrated the experiments to `ladybug==0.18.1`, re-ran the full 180-run
suite on mini, and then **reverted**, because the paper reports the 2026-07-05
numbers and must stay reproducible against the code that produced them.

What the re-run showed (both campaigns archived under results/archive_*):

| graph, medium (Cross Validated) | published 0.15.3 | ladybug 0.18.1 | delta |
|---|---|---|---|
| ladybug OLTP ops/s | 538.6 ± 4.6 | 532.6 ± 13.4 | -1.1% (noise) |
| ladybug OLAP total ms | 76.0 ± 1.0 | 66.4 ± 0.8 | **-12.5% (real)** |
| arcadedb OLTP ops/s | 4052.8 ± 367.6 | 3858.3 ± 271.5 | -4.8% |
| ArcadeDB/Ladybug ratio | 7.53x | 7.24x | |

Noise floor: SQLite and DuckDB ran identical versions in both campaigns and still
moved -3.3% / -4.4%, so anything under ~5% is run-to-run variance. LadybugDB's
graph OLAP gain is above that band and is genuine.

Known inaccuracy in the published paper, left as-is by author decision: the run
actually used `arcadedb-embedded 26.8.1.dev0` (upstream's pom said 26.8.1-SNAPSHOT
at the time; that line was later renamed and released as 26.7.2), while the paper
states 26.7.2.

If these numbers are ever refreshed, migrate to `ladybug` and re-measure together.
