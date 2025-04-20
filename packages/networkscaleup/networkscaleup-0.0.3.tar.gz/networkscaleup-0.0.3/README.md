This package fits several different **Network Scale-Up Models (NSUM)** to **Aggregated Relational Data (ARD)**. ARD represents survey responses to questions of the form: *"How many X’s do you know?"*, where respondents report how many people they know in different subpopulations.

Specifically, if Nᵢ respondents are asked about Nₖ subpopulations, then the ARD is an Nᵢ times Nₖ matrix, where the *(i, j)* element represents how many people respondent *i* reports knowing in subpopulation *j*.

NSUM leverages these responses to estimate the unknown size of **hard-to-reach populations**.

## PIMLE

The plug-in MLE (PIMLE) estimator from Killworth, P. D., Johnsen, E. C., McCarty, C., Shelley, G. A., and Bernard, H. R. (1998) 
is a two-stage estimator that first estimates the degrees for each respondent dᵢ by maximizing the following likelihood for each respondent:
 L(dᵢ; y, {Nₖ}) = ∏ₖ₌₁ᴸ [ C(dᵢ, yᵢₖ) × (Nₖ / N)^yᵢₖ × (1 - Nₖ / N)^(dᵢ - yᵢₖ) ] Where: - L is the number of 
subpopulations with known sizes Nₖ. - yᵢₖ is the number of people respondent i reports knowing in subpopulation k. - C(dᵢ, yᵢₖ) is the binomial coefficient. 
In the second stage, the model plugs in the estimated dᵢ into the equation: yᵢₖ / dᵢ = Nₖ / N and solves for the unknown Nₖ for each respondent. 
These estimates are then averaged to obtain a single estimate of Nₖ. Summary: Stage 1 estimates dᵢ using: dᵢ = N × (∑ₖ₌₁ᴸ yᵢₖ) / (∑ₖ₌₁ᴸ Nₖ) Stage 2 estimates 
the unknown subpopulation size Nₖ with: Nₖᴾᴵᴹᴸᴱ = (N / n) × ∑ᵢ₌₁ⁿ (yᵢₖ / dᵢ)