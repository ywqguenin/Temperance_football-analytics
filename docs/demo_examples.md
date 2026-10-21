# Football Analytics AI Agent — Demo Examples

This document records four demonstrations of the current single-match football analytics agent.

The examples use cached StatsBomb event data for match ID `3754296`. Results are specific to this dataset and the project's current metric definitions.

## Demo 1: Shot Analysis

**Question**

Why did Arsenal create fewer shots but still produce higher total xG than Manchester City?

**Selected tool:** `shot_analysis`

**Evidence**

| Metric              | Arsenal | Manchester City |
| ------------------- | ------: | --------------: |
| Shots               |       8 |              19 |
| Total xG            |   1.354 |           1.250 |
| Average xG per shot |   0.169 |           0.066 |

**Interpretation**

Arsenal recorded fewer shots but higher total xG and higher average xG per shot. The available statistics indicate higher expected goal value per attempt, but do not establish the specific tactical reasons.

## Demo 2: Final-Third Entries

**Question**

Which team progressed the ball more effectively into advanced areas?

**Selected tool:** `final_third_entries`

**Evidence**

| Team            | Successful final-third entries |
| --------------- | -----------------------------: |
| Arsenal         |                             29 |
| Manchester City |                             39 |

**Interpretation**

Manchester City recorded more successful final-third entries. This is a count comparison, not a measure of progression efficiency.

## Demo 3: Progressive Passes

**Question**

Which team made more progressive passes toward the opponent's goal?

**Selected tool:** `progressive_passes`

**Evidence**

| Team            | Progressive passes |
| --------------- | -----------------: |
| Arsenal         |                 85 |
| Manchester City |                123 |

**Interpretation**

Manchester City recorded more progressive passes under the project's current distance-based definition.

## Demo 4: Team Summary

**Question**

Which team had the stronger overall attacking and passing performance?

**Selected tool:** `team_summary`

**Evidence**

| Metric               | Arsenal | Manchester City |
| -------------------- | ------: | --------------: |
| Shots                |       8 |              19 |
| Total xG             |   1.354 |           1.250 |
| Average xG per shot  |   0.169 |           0.066 |
| Passes               |     427 |             705 |
| Completed passes     |     319 |             593 |
| Pass completion rate |  74.71% |          84.11% |
| Final-third entries  |      29 |              39 |
| Progressive passes   |      85 |             123 |

**Interpretation**

Arsenal recorded higher total xG and average xG per shot. Manchester City recorded a higher pass completion rate and more progressive passes. These metrics describe different aspects of performance and do not establish a single overall winner.

## Scope and Limitations

- All examples use one match.
- The tools calculate descriptive statistics; they do not establish causation.
- The LLM selects tools and interprets the evidence, while Python performs the numerical calculations.
- Results depend on the underlying match data and metric definitions.
