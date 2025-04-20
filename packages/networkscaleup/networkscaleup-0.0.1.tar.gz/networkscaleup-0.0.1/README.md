This package fits several different **Network Scale-Up Models (NSUM)** to **Aggregated Relational Data (ARD)**. ARD represents survey responses to questions of the form: *"How many X’s do you know?"*, where respondents report how many people they know in different subpopulations.

Specifically, if \( N_i \) respondents are asked about \( N_k \) subpopulations, then the ARD is an \( N_i \times N_k \) matrix, where the \((i, j)\) element represents how many people respondent \( i \) reports knowing in subpopulation \( j \).

NSUM leverages these responses to estimate the unknown size of **hard-to-reach populations**.
