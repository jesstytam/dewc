*Journal of Ecology* 1998, **86**, 946–959

# The ecological significance of canopy seed storage in fire-prone environments: a model for non-sprouting shrubs

NEAL J. ENRIGHT\*†, RALF MARSULA‡, BYRON B. LAMONT† and CHRISTIAN WISSEL‡

\*Department of Geography and Environmental Studies, University of Melbourne, Parkville 3052, Australia; †School of Environmental Biology, Curtin University of Technology, GPO Box U1987 Perth 6001, Australia; and ‡Department of Ecological Modelling, UFZ Centre for Environmental Research, Leipzig-Halle, Permoserstr. 15, PF 2, D-04301 Leipzig, Germany

# Summary

1 A comprehensive data set on age, survival and reproduction for the non-sprouting (fire-killed) shrub *Banksia hookeriana*, encompassing 13 years of measurements at 15 sites in south-western Australia, and including 10 fires, was used to parameterize a computer model to investigate optimum plant life-history strategies in a fire-prone environment. Parameter ranges encompassed life-history information for other non-sprouting Banksia species from the same region.

2 The relationship between fire interval and level of canopy seed storage (serotiny) was analysed to identify the circumstances under which serotiny is favoured, and what degree of serotiny maximizes potential population growth rate. In addition to deterministic versions of the model, stochasticity in fire interval and conditions for recruitment were analysed.

3 The deterministic model indicated a maximum finite rate of natural increase (λ = 1.15) when the fire interval was 16 years and all seeds were retained on the plant until fire occurred. Although the model failed to predict the intermediate degrees of serotiny present in nature, it supported the optimum fire interval predicted from canopy seed bank dynamics.

4 Changes to biological attributes associated with timing of reproduction and longevity shifted the optimum fire interval and estimated rate of population growth, but did not alter the conclusions concerning serotiny. Although shorter seed longevity and increased rates of predation and/or decay reduced the value of serotiny, even very low levels of canopy seed storage increased species fitness under intermediate fire frequencies (10–20 years).

5 If the probability of inter-fire recruitment and survival was increased, optimum growth shifted from strong serotiny under a regime of frequent fire (<20 year interval), to weak (or no) serotiny where the interval between successive fires was long (>40 year interval).

6 Stochasticity around mean fire interval resulted in intermediate to strong (but not complete) serotiny being predicted as optimal once the CV for fire interval approached 100%. This result is interpreted as a bet-hedging strategy whereby spontaneous release of some seeds during the inter-fire period permits recruitment on rare occasions where fire interval approaches or exceeds the species longevity.

*Keywords: Banksia*, computer models, fire regime, optimum life-history strategies, serotiny, stochastic effects, woody plants

*Journal of Ecology* (1998) **86**, 946–959

946 Correspondence: Dr Neal Enright (fax 61 3 9344 4972; e-mail enright@ariel.ucs.unimelb.edu.au).


<!-- PAGE BREAK -->

947 *N.J. Enright* et al.

# Introduction

Plants in fire-prone environments are often characterized by biological attributes that increase the probability of survival and/or recruitment following disturbance by fire. Among these are the ability of individuals to regrow from protected buds either above- or below-ground (resprouting), fire-stimulated flowering and seed production, and fire-triggered germination of seeds stored either in the soil or in the plant canopy (Gill 1981). Since species that resprout after fire commonly co-exist in fire-prone environments (e.g. mediterranean-type shrublands) with those that are killed by fire (non-sprouters), a frequent question concerns the circumstances under which one or other strategy is favoured (e.g. Keeley & Zedler 1978; Keeley 1986; Hilbert 1987). Beyond this simple dichotomous division into resprouters and non-sprouters, fire-prone communities may contain an array of (sometimes congeneric) species showing consistent variation in the amount of resprouting after fire, the extent to which seeds are stored in the soil or on the plant, and in other biological attributes (e.g. longevity, age to reproduction, level of seed production).

It is important to determine the biological attributes that influence demographic behaviour and to establish which attributes confer the greatest fitness advantage on a species in relation to particular fire regimes. As well as revealing information on the selective pressures acting on species in fire-prone environments, the answers aid conservation and management of species in relation to human-imposed fire regimes.

This paper presents a computer model of population dynamics for a non-sprouting woody perennial in a fire-prone environment, and the results of simulations which sought to reveal the optimum level of on-plant seed storage (serotiny) in relation to fire interval. Serotiny refers to the retention of seeds in closed fruits or cones within the crown for more than 1 year and is common in species from a number of important families in fire-prone areas of Australia (Proteaceae, Myrtaceae, Cupressaceae, Casuarinaceae), South Africa (Proteaceae, Bruniaceae) and North America (Pinaceae) (Lamont et al. 1991a). It can be contrasted with two alternative fates of seeds: storage in a soil seed bank, or release of short-lived seeds once mature (no seed storage). Seed release in serotinous species is normally triggered by fire and seeds are short-lived after release, germinating during the first favourable period (Cowling & Lamont 1987). Species can range from weakly serotinous, where most seeds are released spontaneously (in the absence of fire) within a few years of production, to strongly serotinous, where most seeds are held in the canopy for many years (e.g. >10 years in some species of Pinus and Banksia).

The ecological and evolutionary significance of serotiny seems clear: where fire is the most common cause of ecosystem disturbance, cued release of canopy-stored seeds by fire (and their germination in the first growing season after fire) maximizes plant age and therefore seed available for the next generation by the time of the next fire. Seeds released, and seedlings established, later during the inter-fire period have a lower probability of survival due to competition with their parents and other established plants (Cowling & Lamont 1987). They will be younger and will thus have a smaller canopy seed bank when fire recurs, and so are less fit (sensu Stearns 1992). It would therefore appear that very strong serotiny should represent the optimum strategy for perennial plants in fire-prone environments. However, a range of degrees of serotiny may be encountered within the same plant community (e.g. Cowling et al. 1987; Enright & Lamont 1989a,b) or even within the same species. In the latter case, variations have been found in relation to environmental gradients, e.g. lower serotiny in less fire-prone parts of the species’ geographical range for *Banksia attenuata* in Australia (Cowling & Lamont 1985), and in relation to time since last fire, e.g. inter-fire recruits show lower serotiny than immediate post-fire recruits of *Pinus banksiana* in boreal forests of southern Quebec (Gautier et al. 1996). Lamont et al. (1991a) note that some fire regimes and growth forms apparently foster incomplete serotiny, but that ‘degree of serotiny has received little formal treatment, and the empirical subtleties of such relationships remain largely unexplored’.

The model described here is based on field data collected over 13 years from 15 sites and including 10 different fires (up to two at the same site) for *B. hookeriana* Meissn. (Proteaceae), a non-sprouting woody shrub of mediterranean-type shrublands in south-western Australia (Enright & Lamont 1989a, 1992a,b; Enright et al. 1996). Nevertheless, the model is likely to have a more general application since parameter values can readily be changed to match the known life-history attributes of other serotinous, non-sprouting perennial plants. By basing the model and its parameter values on those measured over an extended period of time (and at a number of sites) for a real plant species the model described here avoids many of the criticisms levelled at population models. For example, Cousens (1995) argues that the results of simulation studies for hypothetical species are often determined largely by the structure of the models themselves and provide little insight into real population dynamic behaviour and, further, that many models based on real data are flawed since the data are derived from glasshouse experiments or from density studies that exclude stochastic year-to-year variations in factors unrelated to density (e.g. weather).


<!-- PAGE BREAK -->

948 Canopy seed storage in non-sprouting shrubs

#### Ecological and biological attributes of *B. hookeriana*

#### FIELD DATA COLLECTION

*Banksia hookeriana* is a highly serotinous, fire-killed (non-sprouting) woody shrub that grows up to 2.5 m in height, which is restricted to the northern sandplain heaths of south-western Australia (centred on 29°30′S, 115°15′E) about 250–330 km north of Perth (George 1981; Taylor & Hopper 1988). Seed production and plant survivorship were estimated for sample populations of different ages (i.e. time since last fire). Sites covering the whole range of possible plant ages could not be located, and fires during the course of remeasurements returned some sites to zero age. Fifteen sample plots, each 400 m<sup>2</sup> in area, and ranging in age from 1 to 16 years at the start of the study, were established and censused annually in June (i.e. at the end of the summer–autumn period of peak plant mortality) from 1986 to 1996.

The onset and level of flowering (inflorescence) and cone (infructescence) production were recorded for all individuals within five replicate 25 m<sup>2</sup> subplots per plot for stands <8 years old, and annual cone production followed for a random sample of 10 individuals for older stands. Fertile cones typically carry 5–15 woody follicles arranged around a central rachis, each follicle holding two seeds. Cones arise terminally at the beginning of each growing season, and node scars and branching pattern clearly mark the boundary between successive years of vegetative growth. Thus plant age and individual cone age can be determined with only a small likelihood of error. Complete cone crops were harvested from 20 randomly chosen 16-year-old plants in 1986, and cones were aged so that the entire history of reproduction could be determined for each plant. The numbers of firm, aborted, eaten and decayed seeds in closed follicles were determined by cone age, and viability of firm seeds was assessed by germination testing (full details are provided in Enright et al. 1996). Degree of serotiny was based on the proportion of follicles per cone age class that remained closed in the absence of fire (following Lamont et al. 1991a).

The total number of cones per plant was quantified for all plants in plots affected by wild fires during the course of the field study. The number of follicles opened by fire was enumerated for a random sample of 10 cones on each of 10 plant skeletons per plot, and the number of viable seeds released per plant estimated using data for seeds from harvested cones.

Plant survivorship was recorded annually for 10 randomly chosen individuals within each subplot where plant age was <8 years, and in the whole plot for older stands. The number of seeds released following fire, the number of seedlings established in the first winter, and number of survivors at each age was used to produce survivorship trajectories. These trajectories described the number of seeds required to produce a new individual of any particular age.

Data for three other non-sprouting Banksia species (*B. prionotes* Lindley, *B. leptophylla* A.S. George and *B. lanata* A.S. George) provided information on ranges for parameter values for modelling purposes. Up to six Banksia species (a mixture of resprouters and non-sprouters) co-occurred in some of the field sites. The biological attributes of these species are described in Cowling et al. (1987), Enright & Lamont (1989a) and Enright & Lamont (1992a).

#### SPECIES ATTRIBUTES

Seed production typically commences when plants are 5 years old and fluctuates widely around a mean of about 200 viable seeds per year from 15 years onwards (Enright et al. 1996). While new inflorescences may be damaged and removed from plants by birds, mature cones normally remain attached to the plant throughout their life. Few seeds are released except when fire causes the follicles on cones to open. Once released, seeds either germinate with the onset of winter rains or perish (Enright & Lamont 1989a). Enright et al. (1996) describe in detail the mean rate of accumulation of viable seeds in the canopy in relation to plant age. On average, 17% of embryos abort; seed losses due to spontaneous release in the absence of fire average 4% per annum; while predation and decay of seeds stored in closed follicles increases by 4% per annum from the first year.

From 3% to 27% of seeds released following fires in the period 1985–93 produced seedlings in the first winter (Enright & Lamont 1989a; N. J. Enright, unpublished data). Plant survivorship is lowest in the first year and quickly increases such that there is little mortality (<1% year<sup>−1</sup>) in plants older than 8 years. While no plants older than 25 years have been observed in the field, the continuing survival of most individuals in our oldest study site (N. J. Enright, unpublished data) indicates that longevity may be 30–40 years in the absence of fire. Large, old plants may succumb to drought over summer, and are prone to collapse due to the heavy load of seed-bearing cones on old branches, and this suggests an increased mortality rate for old plants.

In the absence of fire, some seeds are released by the spontaneous opening of old fruits, but the probability of germination and survival of recruits to reproductive age is extremely low. Seedlings are occasionally encountered in stands >15 years old, but so far no such recruits have been recorded to survive to reproductive age. Nevertheless, it is reasonable to assume that occasionally these inter-fire recruits might grow to maturity and contribute to future generations. The low chance of establishment, combined with low rates of seed release when the degree of serotiny is high, means that very few recruits are likely via this pathway.


<!-- PAGE BREAK -->

949 *N.J. Enright* et al.

Seed release is hastened by the death of stem tissues due to drought stress and plant senescence, but is incomplete relative to seed release after fire (Witkowski et al. 1991). The canopy seed bank may be completely lost where plant death occurs before the next fire, both because even if seeds are released they will have a low probability of establishment, and because dead plants are usually completely incinerated by fire so that any seeds still held in the crown will perish (Lamont & Barker 1988). The woody stems and cones on living shrubs burn less intensely due to a higher moisture content, and although the stems are killed they remain standing and the cones are opened but not consumed. If fire occurs either before the onset of reproductive maturity, or before a sufficient canopy seed bank has accumulated, a population is threatened with local extinction.

### WEATHER AND FIRE

Mediterranean-type climate regions are characterized by cool, moist winters and hot, dry summers. In the northern sandplain heaths of south-western Australia, winter rains are highly predictable and will almost always provide sufficient moisture to allow seedling establishment after fire. However, the extent of summer drought is more variable. One-hundred and ten years of rainfall records for nearby Dongara (Western Australian Bureau of Meteorology climate station 8044; 29°15′S, 114°56′E, mean annual rainfall of 471 mm for the period 1884–1993) show that about 80% of summers have the typical mediterranean-type pattern of low to very low rainfall. In the other 20% of years, tropical storms punctuate the summer with heavy rainfall events and drought stress on plants is greatly reduced (Enright & Lamont 1992a).

Summer weather conditions are important in determining levels of seedling survival in the first year following fire. Survivorship of seedlings is highest in wet summers and lowest in dry summers (Enright & Lamont 1992a). There was no relationship between rainfall in the previous summer and subsequent inflorescence production for plants >15 years old. However, there was a significant positive relationship between total rainfall in one year and inflorescence production in the next (log<sub>10</sub> cones = 5.45 × log<sub>10</sub> annual rainfall – 13.80; d.f. = 16, F = 10.50, P < 0.05, r<sup>2</sup> = 0.36). This non-linear relationship suggests reduced inflorescence production following years of lower than average rainfall, but little increase above average levels of production following wet years.

Risk of fire is high every summer and there is no obvious relationship between rainfall and fire: of nine wild fires recorded in the vicinity of the field area since 1967, four occurred in wetter than average years, and four in years with very dry summers (one of which followed a wet winter). However, the timing of fire in relation to rainfall in the first few years after fire (especially unusually wet or dry summers) is important since seedling mortality is highest during this period (Enright & Lamont 1989a, 1992a). Stands burned within the last 5 years are unlikely to have accumulated sufficient biomass to carry a fire. The shortest recorded fire interval in relation to the nine fires noted above was 7 years.

# Methods

### THE MODEL

The computer model, written in C++, describes the population dynamics of a serotinous, non-sprouting woody perennial that is subject to disturbance by fire. We chose an age-based approach to characterize the population: the model traces the number of x-year-old plants, N(x), and the number of seeds stored on an x-year-old plant, S(x), for each age x. Changes in N(x) and S(x) are caused by plant death, seed production, seed loss, seed release, germination and establishment of seedlings. These processes are described by the functional relationships detailed below, and illustrated conceptually in Fig. 1. The model begins with a post-fire population of 100 viable seeds and calculates their survivorship and reproduction in relation to age until fire causes plant death and seed release. Fire kills all individuals, and recruitment following fire is solely from seeds.

Germination, establishment and survivorship of plants depend on the growing conditions (especially summer rainfall), and the model uses the fits derived from field data on survivorship, and illustrated in Fig. 2, to describe these rates. The probability of germination of seeds and establishment of seedlings in the first year is the inverse of the observed number of seeds required for self-replacement of a 1-year-old plant. In the same way, the probability p(x) that a plant survives until it is x years old is the inverse of the number of seeds required for self-replacement of a plant at age x. Thus, the probability p(x, x + 1) to survive from year x to year x + 1 can be calculated

Diagram boxes: Fire; Seed release; Germination and plant survival; Seed production; Seed loss due to predation and rotting; Seed storage; Inter-fire seed release.

Fig. 1 Summary flow diagram of the main processes built into the computer model for a serotinous, non-sprouting perennial plant. Note this is not a complete flow diagram of the model. Full model details are described in the text.


<!-- PAGE BREAK -->

950 Canopy seed storage in non-sprouting shrubs

Fig. 2 The mean number of viable seeds required to produce a new plant of given age, over plant ages 0–10 years, for *B. hookeriana*, and the best-fit regression lines describing (a) good, (b) average, (c) bad and (d) very bad recruitment, respectively. Regression model details in the text.

as the ratio p (x, x + 1) = p (x + 1)/p (x). The best fit regression line describing recruitment under average conditions is: number of viable seeds required per recruit = 69.03 × log(age) + 23.60) (d.f. = 1,72, F = 39.1, P < 0.001). Other functions are: in good weather, number of viable seeds = 26.54 × log (age) + 23.03; in bad weather, number of viable seeds = 116.53 × log(age) + 82.16; and, in very bad weather, number of viable seeds = 451.72 × log (age) + 17.67. These fits encompass a broader range of measured field recruitment responses than would be the case if regression model (95% or 99%) confidence limits were used to define good and bad recruitment, and are argued to reflect more realistically the natural variation in recruitment in relation to variation in summer rainfall. The impacts that climate have on population growth rate are based on the classification of post-fire years as good (>40 mm summer rainfall), average (10–40 mm), bad (1–10 mm) and very bad (0 mm).

At each time step the plants get 1 year older. The model calculates the age class distribution of the individuals as well as their seed production in that year and accumulated seed storage in the plant canopy. Plants have an increased risk of mortality once an age of 25 years is exceeded. This mortality rate increases from 0 to 0.1 by steps of 0.01 per year such that <20% of plants alive at age 25 years are still alive at age 40 years. Maximum plant longevity is described by the parameter A4 (Table 1).

Juvenile plants commence seed production at plant age A2 years. Seed production increases linearly up to age A3, after which it remains constant at Fm seeds per year. Most seeds are stored in the plant canopy, but the seeds in a proportion, Lv, of follicles are lost each year due to predation and rotting, while a further proportion, r, open each year in the absence of fire and release their seeds (inter-fire release). 1/r (the inverse of r) describes the degree of serotiny. Thus, a value of 1 for serotiny means that all seeds are released by the end of the year in which they were produced (i.e. the plant is not serotinous), while a value of 1000 means that, on average, only 0.1% of the seed crop is released per year and nearly all of the seed crop (regardless of seed age) is held on the plant until fire triggers seed release. This definition of serotiny follows that proposed by Lamont (1991). The degree of serotiny can theoretically range from 1 (0% serotiny) to infinity (100% serotiny) but most recorded values (e.g. for Banksia species) fall between 10 and 100 (Table 2).

Seeds have a longevity of Vm years on the plant. Seeds released during the inter-fire period have a lower probability of germination and establishment than seeds released in response to fire (post-fire release). The model takes this into account: the probability of germination and establishment for seeds released in any inter-fire year is only Postint of that of the post-fire released seeds. For a given released seed, we estimate the probability of inter-fire recruitment (expressed as a proportion) to be c. 0.05 that of post-fire recruitment. When a plant dies during the inter-fire period all seeds stored on that plant are lost. When a fire occurs all remaining plants are killed, and all of their stored seeds are released.

The mean fitness of the population (sensu Stearns 1992) in relation to any set of life-history parameters and environmental factors is estimated using the finite rate of natural increase (λ). This is calculated as:

λ = <sup>n</sup>√(N<sub>t+n</sub>/N<sub>t</sub>),

where n is the number of years between two fires (i.e. represents the fire interval), t is an arbitrary point in time during the simulation and N<sub>t</sub> is the number of individuals at time t. Thus, N<sub>t</sub> and N<sub>t+n</sub> represent the number of individuals for two equivalent points (i.e. same plant age) after successive fires.

The model is deterministic in its simplest form. Mean values for life history and environmental parameters, based on information for *B. hookeriana*, were used as the initial settings. Parameter values and ranges used in the model are listed in Table 1. The model is generalized by examining the effects on λ of fire interval and degree of serotiny across the ranges 6–60 years and 1–1000, respectively. Changes to other parameters allowed exploration of a broad range of life histories (representing additional species) and environmental conditions (representing good and bad conditions for recruitment, survival and reproduction).

Stochastic versions of the model were also analysed. A truncated, normal sampling distribution was used to select ignition times around specified mean fire intervals, giving an increasing probability of disturbance with time elapsed since last fire. Tests of the model using a Weibull distribution (Johnson &


<!-- PAGE BREAK -->

951 *N.J. Enright* et al.

Table 1 Parameter set, initial settings (i.e. mean values for *Banksia hookeriana*), and range of values used in the computer model for a fire-killed (non-sprouting) serotinous shrub

| Parameter | Notation | Initial settings | Range |
|---|---|---|---|
| *Biological attributes* | | | |
| Degree of serotiny | 1/r | Log<sub>10</sub> (1–1000) | Step = 0.06† |
| Age to first reproduction (years) | A2 | 5 | 3–15 |
| Age to maximum reproduction (years) | A3 | 15 | 10–25 |
| Longevity (years) | A4 | 40 | 30–60 |
| Maximum seed longevity (years) | Vm | 15 | 2–15 |
| Annual rate of seed loss | Lv | 0.04 | 0–0.20 |
| Viable seeds added per year at A3 | Fm | 200 | 50–1000 |
| *Survivorship variables* | | | |
| Recruitment curves\* | Function | Average | Very bad–good |
| Inter-fire recruitment | Postint | 0.05 | 0.01–1.0 |
| Declining survival in old plants | D | >25 | Step = 0.01 |
| *Environmental variables* | | | |
| Weather\* | W | Average | Very bad–good |
| Fire interval | F | 6–60 | Step = 1 |
| Standard deviation of F | sdF | 0–1.0F | Step = 0.10 |

\* Post-fire recruitment–survivorship functions (in relation to summer rainfall) are defined in the text and illustrated in Fig. 2.

† Step indicates variables that are automatically incremented and the amounts of each increment, e.g. degree of serotiny was incremented in 50 equal steps of 0.06 from 0 to 3 (i.e. log<sub>10</sub>(1–1000)).

Table 2 Degree of serotiny in resprouting and non-sprouting Banksia species from south-western Australia. The value for degree of serotiny is the inverse of the slope of a linear regression describing the rate of seed release with increasing fruit age (after Lamont 1991). The scale is not linear and it is suggested that serotiny values be regarded in the following manner: weak serotiny <5, moderate serotiny 5–14, strong serotiny 15–25, extreme serotiny >25

| Species | Degree of serotiny | Range\* |
|---|---|---|
| *Species killed by fire* | | |
| *B. prionotes* | 11 | 1–13 |
| *B. burdettii* | 16 | |
| *B. coccinea* | 20 | |
| *B. hookeriana* | 25 | 18–25 |
| *B. leptophylla* | 53 | |
| *B. cuneata* | 77 | |
| *B. baxteri* | 162 | |
| *Species resprouting after fire* | | |
| *B. tricuspis* | 9 | |
| *B. menziesii* | 12 | 1–12 |
| *B. grossa* | 13 | |
| *B. attenuata* | 14 | 4–17 |
| *B. micrantha* | 54 | |
| *B. candolleana* | 300 | |
| *B. elegans* | >1000 | |

\* Range covers estimates from different sites within the geographical range of the species. Lower values are typically from more southerly locations where annual rainfall is higher and interval between fires is longer.

Data from: Cowling & Lamont (1985); Lamont & Barker (1988); Lamont & Barrett (1988); Lamont & van Leeuwen (1988); Enright & Lamont (1989b); Lamont et al. (1991); Witkowski et al. (1991).

Gutsell 1994) gave equivalent results, but the truncated normal distribution handled variations in standard deviation around a constant mean fire interval in a computationally simpler manner. Simulations were repeated 1000–5000 times for each parameter set to provide a stable mean population growth surface (±SD) in relation to fire interval and degree of serotiny. The model was run for mean fire intervals from 6 to 60 years and for standard deviations around the mean fire interval ranging from 0.1 to 1.0 times the mean (i.e. coefficient of variation, CV, of 10–100%). Ignition events selected at random from the sampling distributions resulted in fires only when stand age was >5 years. This resulted in a systematic difference between the mean of the sampled distribution and the resultant mean fire interval. That is (for example), if the mean fire interval for a run was 10 years and the standard deviation was 5 (CV = 50%), then c. 68% of ignition times fell between 5 and 15 years. About 16% of ignition times, in the lower tail of the sampling distribution, were rejected (ignitions for stand ages <5 years) and new ignition times selected. The mean of the ignition times actually resulting in fires was thus greater than the mean of the theoretical distribution from which values were chosen. This difference is systematic and requires the addition of a correction factor that ranges from 4 to 6 years as fire interval increases from 6 to 20 years. Results are presented for the corrected mean fire interval.

To simulate the effects of stochastic weather, summer weather conditions for each year were sampled at random in proportion to their frequency of occurrence over the 110 years of actual rainfall records for 


<!-- PAGE BREAK -->

952 Canopy seed storage in non-sprouting shrubs

Dongara (20:55:20:5 for good, average, bad and very bad, respectively). Based on the limited evidence for variations in inflorescence production in adult plants >15 years old, the mean rate of production was used for both average and good weather years, and 25% of the mean rate was used for bad and very bad weather years.

Sensitivity (S) of λ to changes in parameter values was calculated as:

S = |(Δλ/λ)/(Δp/p)|,

where p represents the parameter value. For example, sensitivity for age at onset of reproduction (A2) was estimated by calculating the proportional change in λ(Δλ/λ) that resulted from a unit change in the value of A2(ΔA2/A2). The formulation of sensitivity here follows the definition of Caswell (1989).

The model is not affected by starting population size and does not limit projected plant density, although seedling survivorship rates used in the model reflect the combined effects of both density-dependent and density-independent factors operating on the sampled populations. Nor is demographic stochasticity included. Such stochasticity is important when modelling extinction probabilities for small populations, but is unlikely to influence markedly the results of this model which explores optimum strategies for a population of assumed large size (McPeek & Kalisz 1993). Use of mean values for biological parameters also has computational advantages, making runs of the model much faster and more suitable for implementation on microcomputers.

A version of the model suitable for operation with IBM-compatible (Pentium) microcomputers, is available from the authors. The program prints the main results as a table of λ-values by levels of serotiny (51 equally spaced levels on a log10 scale between 1 and 1000) and fire intervals (yearly from 6 to 60 years) in a format readily imported into a variety of statistics and graphics packages.

# Results

#### DETERMINISTIC ANALYSES

Deterministic analysis with parameters set to those for *B. hookeriana* reveals a broad peak in the estimated finite rate of natural increase (λ) for fire intervals of 12–25 years, with a maximum (λ = 1.15) at 16 years (Fig. 3a). λ increases with degree of serotiny to a peak at maximum serotiny (i.e. 1000; no seeds released except as caused by fire), with the rate of increase in λ greatest as degree of serotiny rises from 1 to 10. That is, although fitness is maximized for complete serotiny, the advantages of serotiny over non-serotiny are quickly realized with any tendency towards prolonged on-plant seed storage. Population decline (extinction) is predicted at very short fire intervals, with the risk of extinction greater for non-serotinous (intervals ≤11 years), than for highly serotinous (intervals ≤8 years), plants. At very long fire intervals (>40 years) extreme serotiny is a disadvantage.

Increased rates of viable seed loss on the plant due to higher predation and decay (Lv) do not markedly decrease the maximum value of λ or the importance of serotiny until rates of loss reach about 50% per annum (maximum λ = 1.07). A shorter viable life span for seeds (Vm) decreases the benefit of serotiny, but strong serotiny is still the optimum strategy even when seed viability is restricted to only 2 years (Fig. 3b).

Changing the probability of establishment of individuals from seeds released spontaneously in the absence of fire (i.e. through incomplete serotiny) relative to the probability of post-fire recruitment (Postint) shows that this parameter has the greatest effect on the optimum degree of serotiny and its relation to fire interval (Fig. 3c,d). Where Postint is low (0.05 in the initial model; Fig. 3a) a single optimum indicates that strong to complete serotiny is the best strategy for fire intervals encompassing nearly the whole reproductive life of the plants (8–40 years). However, as the ratio of inter-fire to post-fire recruitment increases (i.e. Postint = 0.5–1.0) two optima are identified: complete serotiny is favoured for fire intervals from 8 to 25 years, but there is then a rapid switch to zero serotiny being favoured when fire is less frequent (Fig. 3c,d).

Changes in a range of other biological attributes tested, including age to first reproduction (A2), age to maximum seed production (A3) and plant longevity (A4), shift the position of the optimum fire interval. For example, as A3 increases from 10 years, through the initial setting of 15 years, to values of 20 and 25 years, the optimum fire interval shifts from 12 to 20 years. There is no change in the pattern of serotiny; the optimum remains at 1000 so long as fire recurs within the lifetime of the plants comprising a stand. The magnitude of λ declines overall where juvenile stages are longer, and where the period between the onset of reproduction and peak reproduction is longer.

Weather impacts (good, average and bad summers), which are reflected in changes in survivorship of seedlings to reproductive maturity and in annual seed set, cause a small shift in the age at which optimum population growth rate occurs (Fig. 4). The optimum is at 13 years under good conditions (more seedlings recruited per viable seed released), 16 years under average, and 17 years under bad conditions (fewer seeds produced, and fewer seedlings recruited in relation to the number of seeds released). There is no change in optimum degree of serotiny from the initial model, with strong serotiny favoured across a broad range of fire intervals. Values of λ fall below population replacement level under the bad weather scenario for fire intervals <23 years at zero and very low serotiny, but remain above self-


<!-- PAGE BREAK -->

953 *N.J. Enright* et al.

Panel maxima: (a) 1.15; (b) 1.08; (c) 1.15 and 1.15; (d) 1.15 and 1.20. Axes: Degree of serotiny; Fire interval (years).

Fig. 3 Results of deterministic computer model runs showing the estimated rate of natural increase, λ, in relation to fire interval and degree of serotiny for the *Banksia hookeriana* parameter set (a) mean settings for all parameters, (b) maximum seed longevity (Vm) = 2 years, (c) inter-fire recruitment probability = 0.5 post-fire recruitment probability (i.e. Postint = 0.5), and (d) Postint = 1.0 (cf. initial settings where Postint = 0.05). Contours start at λ = 1.0 (black shading for λ < 1.0) and with progressively lighter shading at intervals of λ = 0.02 above 1.0 (white at λ > 1.12). The location and maximum value of λ is also indicated in this and subsequent figures.

replacement for moderate and high serotiny (except for very short and very long fire intervals as described previously). Very bad weather (every year) leads to extinction under all conditions.

### SENSITIVITY ANALYSES

The relative sensitivity of the biological and environmental parameters was compared using the sensitivity index, S. It has a minimum value of zero and no maximum, although values usually lie close to zero. Sensitivity of the ratio of inter-fire to post-fire recruitment (Postint), with degree of serotiny set at 25 (the mean value for *B. hookeriana*), is highest (0.04) when fire is infrequent and Postint = 1.0. Sensitivity shows a sharp decrease across fire intervals in the range 20–30 years (Fig. 5). This reflects a maximum selective pressure for inter-fire recruitment (and so low degree of serotiny) as fires become less common (fire intervals >30 years) and for post-fire recruitment as fire becomes more common (fire intervals <20 years).

For plant biological attributes, sensitivity is highest at fire intervals <10 years. This indicates that, for example, shorter time to onset of reproduction (A2), or to peak reproduction (A3), will increase population growth rate. Sensitivity for weather is also high for good weather conditions. Any increase in the frequency of good weather (i.e. wet summers after fire) leads to a sharp rise in fitness since seedling recruitment is greatly enhanced.


<!-- PAGE BREAK -->

954 Canopy seed storage in non-sprouting shrubs

Panel maxima: (a) 1.21; (b) 1.11.

Fig. 4 Results of deterministic computer model runs showing the rate of natural increase, λ, in relation to fire frequency and degree of serotiny for (a) good weather and (b) bad weather (cf. initial model for average weather shown in Fig. 3a).

Fig. 5 Sensitivity of λ to variations in Postint, with degree of serotiny fixed at 25 (the mean value for *Banksia hookeriana*). The vertical axis shows an increasing ratio such that a value of 1.0 indicates no difference between the probabilities for successful recruitment either directly after fire or in the inter-fire period. Contour intervals cover the range of sensitivities from 0 (black) to 0.04 (white).

#### STOCHASTIC ANALYSES

Stochastic analyses with parameters set to those for *B. hookeriana*, and standard deviation around fire interval ranging from zero to 1 times the mean fire interval (i.e. to CV = 100%) show two major trends. First, the maximum estimated population growth rate, λ, occurs for high, but not complete serotiny once the CV for fire interval >75%. At CV = 100% the optimum of λ = 1.12 ± 0.05 occurs for fire intervals of 15–16 years and degrees of serotiny between 200 and 600 (Fig. 6a). The peak is very flat in relation to degree of serotiny, with values of λ > 1.10 occurring for degrees from 30 to 1000. λ declines rapidly to a minimum value of 1.02 ± 0.03 at zero serotiny. For fire intervals >20 years λ declines to values <1.0 at extremely high degrees of serotiny (i.e. approaching 1000). Secondly, the maximum population growth rate is lower (1.12 ± 0.05) than that predicted by the deterministic model (1.15). It both overlaps with the latter value and is significantly >1.0 (assuming approximate confidence limits of 2 × SD). The estimated value of λ at zero serotiny is not significantly different from 1.0.

As the value for Postint increases from the initial value of 0.05 to 1.0 (no difference in probability of recruitment regardless of time of seed release), the optimum degree of serotiny in relation to fire interval shifts in a similar way to that described for the deterministic runs of the model. High degrees of serotiny (but not complete serotiny) are predicted for fire intervals from about 10–25 years, but thereafter optimum degree of serotiny quickly switches to zero as fire interval continues to increase (Fig. 6b). This switch occurs at slightly lower values of Postint (0.25–0.50) than is evident in the deterministic runs (0.5–0.75).

Stochastic weather results in an almost identical pattern, but slightly lower peak value of λ (1.13 ± 0.04), to that described for the initial deterministic runs (1.15). The occasional coincidence of fire followed by a wet summer offsets the more common circumstance of poor recruitment associated with dry years after fire. However, the adaptive peak is restricted to a slightly narrower range of fire intervals, indicating that year to year variations in conditions for recruitment and survival tend to reduce population growth rate under most suboptimal combinations of


<!-- PAGE BREAK -->

955 *N.J. Enright* et al.

Panel maxima: (a) 1.12; (b) 1.11 and 1.15. Axes: Degree of serotiny; Fire interval (years).

Fig. 6 Results of model analyses showing the rate of natural increase, λ, in relation to fire frequency and degree of serotiny when (a) stochastic variation around mean fire interval is set to CV = 100% (i.e. standard deviation = mean), and (b) stochastic variation around mean fire interval is set to CV = 100% and Postint = 0.50. The fire interval (x-axis) is corrected as described in the text. Contours and shading as in Fig. 3.

fire interval and serotiny. Analysis of stochastic weather and stochastic fire together produces similar results to those described for fire alone, but again with lower overall λ (1.10 ± 0.05).

Changes to parameter values for biological attributes give similar results to those described for the deterministic runs.

## Discussion

### DETERMINISTIC MODEL

The optimum fire interval of 16 years obtained from the deterministic model for the *B. hookeriana* parameter set agrees with predictions made by Enright et al. (1996) based on the dynamics of the canopy seed store alone. Extinction is predicted where fire occurs before the plants reach reproductive age or when they have not had time to accumulate a sufficient canopy seed store to ensure successful recruits following fire: this point is frequently made in the fire ecology literature (e.g. Gill 1981; Lamont et al. 1991a). A fire interval in excess of 40 years also leads to extinction if degree of serotiny is close to 1000, since the longevity of plants is exceeded and few or no seeds have been released prior to plant death. This result is consistent with the findings of Bond (1980), who documented the decline of serotinous Proteaceae populations in South African fynbos that had remained unburned for 30–65 years. However, we have no field evidence for the behaviour of stands >25 years old and so there is uncertainty surrounding the parameter values selected to describe population behaviour in this area of the environmental space. The predicted optimum mean return interval for fire (16 years) is greater than that recorded within the geographical range of *B. hookeriana* and other parts of the northern sandplain heaths of western Australia (Van der Moezel et al. 1987; and history of fires reported in the present study). Van der Moezel et al. (1987) noted that few extensive stands now exceed 11 years of age, suggesting a possible human impact on the fire regime that may threaten the long-term survival of some populations.

The deterministic model results indicate that complete serotiny is the optimum solution when fire is common (fire interval 10–25 years) and predictable (fire return time is always within this range). Any increase in serotiny along the axis of optimum fire interval (peak 16 years) leads to a higher rate of population growth in comparison with no serotiny. At fire frequencies either higher or lower than the optimum, but within the reproductive lifetime of the plant (frequencies of 8–12 and 25–40 years), the advantage accruing from increasing serotiny is less significant but shows the same trend. However, the great majority of serotinous species in nature do not show complete serotiny. Rather, serotiny values range from about 10–100 (remembering that the scale is not linear and that these values represent a seed release rate of from 10% to 1% per annum).

The width of the adaptive peak in relation to fire interval increases, at least initially, with the degree of serotiny; the fire interval range over which λ is >1.10 almost doubling as serotiny rises from 30 to 50 (Fig. 3a). This important outcome was first proposed by McMaster & Zedler (1981), and subsequently argued theoretically by Lamont et al. (1991a), but has lacked strong supporting evidence until now. Suggestions that serotiny is favoured only under a very nar-

<!-- PAGE BREAK -->

956 Canopy seed storage in non-sprouting shrubs

row range of fire frequencies (e.g. Perry & Lotan 1979; Bond 1984) can no longer be sustained, although it must be noted that serotiny is non-adaptive where the mean fire interval exceeds the mean life span of the species.

By varying the values for biological and environmental parameters in the model one at a time, their importance in determining mean population fitness (measured as λ) in relation to fire interval and degree of serotiny could be identified. The (very high) rates of viable seed loss from the canopy seed store (Lv) and reductions in seed longevity (Vm) needed to reduce λ substantially are greater than most published rates for canopy seed predation, and suggests that the rate of on-plant granivory is not a significant factor in determining the ecological value of serotiny in non-sprouters, disagreeing with the arguments of some others (reviewed by Lamont et al. 1991a; Whelan 1995). Any storage of seeds in excess of a single year is advantageous in species of fire-prone communities. Nevertheless, McMaster & Zedler (1981), Lamont et al. (1991a) and others have argued that canopy seed storage may dampen annual fluctuations in seed production, ensuring adequate seed supply following fire. In this case, the extent of dampening would decline as either Vm approached 1 or Lv approached 100%.

The protection of seeds within woody (serotinous) fruits must have trade-off costs with seed production, such that fewer seeds might be produced by a strongly serotinous species than by a non-serotinous species, all other things being equal (Lamont et al. 1991a). Testing of this idea reveals that five times the mean seed production (971 compared with 200 seeds per year) would be required by a non-serotinous species to offset the advantages of serotiny for fire frequencies of 15–20 years. The nutrient costs of this in a low nutrient environment will be too high (Witkowski & Lamont 1996) unless seed size is also reduced (and this might in turn reduce the probability of seedling survivorship). As fire interval increases further (>25 years), the difference in required seed production decreases since more inter-fire recruits are produced under zero serotiny and provide an additional source of seeds as they reach maturity in the continued absence of fire.

O’Dowd & Gill (1984) doubted that the conditions for recruitment were in fact better post-fire compared with inter-fire in their study of *Eucalyptus delegatensis* regeneration in montane forests of south-eastern Australia. They found that substrate conditions were possibly more favourable to seedling survival during the inter-fire period and suggested that the apparent post-fire advantage to seedlings was simply due to the low availability of seeds during the inter-fire periods. The present model results do not support this as a general view: as the probability of inter-fire recruitment approaches that of post-fire recruitment, the adaptive significance of serotiny declines, especially at longer fire intervals. That is, if inter-fire recruitment conditions were always as suitable as post-fire conditions, seed storage would in fact reduce fitness under most fire frequencies.

Gautier et al. (1996) found that serotiny in *Pinus banksiana* stands in Canada was highest for areas where fires were typically hot and lethal, and lowest for areas where fires were patchy and cool. They also noted that, within old growth stands, inter-fire recruits showed lower serotiny than post-fire recruits, so that stands became progressively less serotinous in the absence of frequent fire. Here, it is clear that recent human impacts on fire regime can directly influence the observed level of serotiny in a population. This type of within-population variation in serotiny is not known in Australian shrubland species, probably because natural fire is frequent (and typically hot-lethal), shrub longevities are shorter, and opportunities for inter-fire recruitment more limited.

Sensitivity analysis indicates that the zone of fire frequencies from 20 to 30 years is critical in differentiating between the circumstances that do and do not favour increasing serotiny given the plant life-history parameter values used here. Fire intervals in excess of 30 years provide sufficient time for inter-fire recruits to reach maximum seed production before the next fire occurs, and so contribute to recruitment in the next generation. For other parameters sensitivity is most important at fire frequencies <10 years (e.g. age at onset of maturity). Such sensitivities may be higher than that described for the recruitment ratio (above) but are not significant in terms of selective forces acting on the degree of serotiny since they merely indicate that, for example, more precocious reproduction will allow population survival under conditions of more frequent fire.

Clark (1991) argued, on the basis of analytical and numerical results of a model concerning optimum time to maturity in trees, that an increasing probability of disturbance with time since last disturbance selects for species that are longer lived and mature later, since early maturation is correlated with shorter longevity and decreases the probability of survival until the next recruitment opportunity. Maturation optima under regimes of frequent disturbance were estimated as 0.4 × average disturbance interval (Clark 1991) and agreed with estimates of optimum time to maturity determined for a sample of North American angiosperm tree species by Loehle (1988) as 0.19 × mean tree longevity. Although our estimate for longevity in *B. hookeriana* (40 years) is not definitive, both this, and the predicted optimum fire interval of 16 years, would result in a later onset of maturity (7–8 years) using these relationships than has been observed by us (5 years). The earlier onset of maturity may imply that the relationships derived for North American angiosperm trees are not necessarily portable to other life forms (e.g. shrubs) or environments, the accumulation of a dormant seed bank (e.g. ser-


<!-- PAGE BREAK -->

957 *N.J. Enright* et al.

otiny) may complicate relationships based primarily on data for species that do not have seed banks, or (unlikely in our estimation) the estimates of both longevity and optimum fire interval for *B. hookeriana* presented here are much too high.

#### STOCHASTIC MODEL

Incomplete serotiny is predicted as the optimum solution once marked stochastic variability around fire intervals (CV > 75%) is introduced into the model. This result suggests that high levels of, but not complete, serotiny might represent a good bet-hedging strategy to cover the occasional long gap between fires that exceeds the mean longevity of the species. In such a case, even low levels of seed leakage by spontaneous follicle rupture during the inter-fire period, and associated low probability of successful inter-fire recruitment in competition with established plants, is sufficient to ensure survival of the population. *Banksia hookeriana* and a number of other non-sprouting Banksia species from south-western Australia fit this scenario (Table 2). Extreme serotiny (>100) is encountered, but very high values appear restricted to resprouter/root suckering species that are not solely dependent upon seeds for survival (e.g. *B. elegans*, *B. candolleana*).

The estimated population growth rate, λ, is 1.02 ± 0.03 at zero serotiny, indicating an approximately stable population even in the absence of on-plant seed storage. However, the calculated error term for λ under circumstances of zero serotiny encompasses the possibility of population decline across all fire intervals. The contribution that increasing levels of on-plant seed storage makes to λ is quickly realized as degree of serotiny rises from 0 to 30, λ reaching values of 1.11–1.12. Population growth rate remains relatively stable thereafter regardless of level of serotiny, but with a slight decline as complete serotiny is approached. If we assume that the selective pressure favouring increasing serotiny is a function of the size of the relative increase in λ per unit increase in degree of serotiny, i.e. (λ<sub>max</sub>–λ<sub>i</sub>)/λ<sub>max</sub>, then this pressure is highest at low degrees of serotiny (<10) and declines quickly such that pressure is weak once the degree of serotiny exceeds 30–40. This interpretation agrees closely with recorded serotiny levels in Banksia species (Table 2). Again, the non-linear serotiny scale used here (following Lamont 1991) should be borne in mind.

A highly variable fire interval also causes a narrowing in the adaptive peak for plants with nearly complete serotiny (degree of serotiny >800). This is because inter-fire recruitment is precluded during occasional long intervals between fire (no seeds are released), while occasional short intervals kill plants before a sufficient seed store has accumulated in the canopy. At slightly lower levels of serotiny some inter-fire recruitment is possible and can contribute to future population growth, and here the adaptive peak is broader.

Bradstock et al. (1996) used a spatial (cellular automaton) model to explore the relationship between fire frequency and fire size for a ‘generic’ non-sprouting species (based on mean attributes for some Banksia species) and arrived at conclusions relevant to the present study. They found that probability of extinction was highest under conditions of both frequent and infrequent fire, and when the standard deviation around fire interval was high. Our results support these contentions. However, Bradstock et al. (1996) assumed complete serotiny in their model, so that there was no chance of inter-fire recruitment. This led them to conclude that senescence (and associated occasional long intervals between fires) was possibly more important than frequent fire as a potential cause of local extinction. We found that limited inter-fire recruitment (our model parameter Postint) can play a critical role in population maintenance when fire frequency is highly variable, so favouring high, but incomplete, serotiny.

# Conclusions

In this paper, we have not been concerned solely with the issue of where and why canopy seed storage (serotiny) arises. This has been attempted elsewhere (e.g. Perry & Lotan 1979; Givnish 1981; Lamont et al. 1991a) and there is general agreement that fire is the driving force in its evolution. Rather, we have asked what degree of serotiny optimizes plant fitness in relation to fire interval and plant life-history attributes and whether, under environmental conditions which favour serotiny, complete serotiny is always the best evolutionary solution for a perennial non-sprouting species. In a related paper, we extend this work by exploring serotiny in relation to fire interval for plants that also have the capacity to regrow vegetatively after fire (Enright et al. 1998).

Our findings are that serotinous non-sprouting plants would show optimum fitness (as described by λ) when serotiny is complete, if (i) fire recurs consistently within the reproductive lifetime of individuals, and (ii) the conditions for recruitment from seeds are better immediately after fire than later during the inter-fire period. However, stochastic analyses reveal that if the fire interval is highly variable, and occasional long intervals without fire are experienced, then intermediate degrees of serotiny are favoured. This result conforms with field observations concerning degrees of serotiny in woody perennials. The recent impact of people on fire regime, through a greatly increased frequency of ignitions, has been to decrease the mean fire interval and reduce the variability around the mean interval, so that present regimes probably exert a selective pressure favouring higher levels of serotiny.

High rates of seed loss to predation and decay can be sustained without altering these conclusions, so


<!-- PAGE BREAK -->

958 Canopy seed storage in non-sprouting shrubs

that the quality of seed protection from predators provided by woody fruits or cones may not be significant (so long as it affords sufficient protection from the heat of fire to ensure seed survival). Changes in the age to first reproduction, age to peak reproduction and longevity shift the predicted optimum fire interval but the pattern in relation to serotiny remains essentially the same. This accords with the comment by Gill (1981) that plants are not adapted to fire per se, but to a particular fire regime. Since we have estimates of the degrees of serotiny for a number of Banksia species, it may be possible to extend the current model to identify the range of fire intervals (min–mean–max), and levels of inter-fire establishment, which might have favoured the evolution of the current set of attributes for each species. Zero canopy seed storage in non-sprouters is favoured only where the time to whole stand death exceeds mean plant longevity and the conditions for recruitment are little or no different between the inter-fire period and the immediate post-fire period. Many species characterized by soil seed storage have short life spans relative to the mean fire interval (i.e. they are fire ephemerals), and so do not fit the above scenario. However, as is the case with serotinous species, their recruitment is largely restricted to the immediate post-fire environment.

#### Acknowledgements

The computer modelling research described here was supported by funding from the Department of Ecological Modelling, UFZ Centre for Environmental Research, Leipzig-Halle GmbH, Germany, the Department of Industry, Technology and Regional Development, Canberra, Australia (Bilateral Science and Technology Collaboration Program Grant to N. J. Enright), the University of Melbourne (N. J. Enright) and Curtin University of Technology (B. B. Lamont, N. J. Enright). The authors acknowledge the contributions of other agencies, support staff and research students to the fieldwork which provided the background data for model construction. The comments of Laura Huenneke and several anonymous referees were also helpful.

#### References

- Bond, W.J. (1980) Fire and senescent fynbos in the Swartberg, Southern Cape. South African Forestry Journal, 114, 68–71.
- Bond, W.J. (1984) Fire survival of Cape Proteaceae – influence of fire season and seed predators. Vegetatio, 56, 65–74.
- Bradstock, R.A., Bedward, M., Scott, J. & Keith, D.A. (1996) Simulation of the effect of spatial and temporal variation in fire regimes on the population viability of a Banksia species. Conservation Biology, 10, 776–784.
- Caswell, H. (1989) Matrix Population Models: Construction, Analysis, and Interpretation. Sinauer, Sunderland, MA.
- Clark, J.S. (1991) Disturbance and tree life history on the shifting mosaic landscape. Ecology, 72, 1102–1118.
- Cousens, R. (1995) Can we determine the intrinsic dynamics of real plant populations? Functional Ecology, 9, 15–20.
- Cowling, R.M. & Lamont, B.B. (1985) Variation in serotiny of three Western Australian Banksia species along a climatic gradient. Australian Journal of Ecology, 10, 345–350.
- Cowling, R.M. & Lamont, B.B. (1987) Post-fire recruitment of four co-occurring Banksia species. Journal of Applied Ecology, 24, 645–658.
- Cowling, R.M., Lamont, B.B. & Pierce, S.M. (1987) Seed bank dynamics of four co-occurring Banksia species. Journal of Ecology, 75, 289–302.
- Enright, N.J. & Lamont, B.B. (1989a) Seed banks, fire season, safe sites and seedling recruitment in five co-occurring Banksia species. Journal of Ecology, 77, 1111–1122.
- Enright, N.J. & Lamont, B.B. (1989b) Fire temperatures and follicle opening requirements in 10 Banksia species. Australian Journal of Ecology, 14, 107–113.
- Enright, N.J. & Lamont, B.B. (1992a) Recruitment variability in the resprouting shrub *Banksia attenuata* and non-sprouting congeners in the northern sandplain heaths of southwestern Australia. Acta Oecologica, 13, 727–741.
- Enright, N.J. & Lamont, B.B. (1992b) Survival, growth and water relations of Banksia seedlings on sand mine tailings and adjacent scrub-heath sites. Journal of Applied Ecology, 29, 663–671.
- Enright, N.J., Lamont, B.B. & Marsula, R. (1996) Canopy seed bank dynamics and optimum fire regime for the highly serotinous shrub, *Banksia hookeriana*. Journal of Ecology, 84, 9–17.
- Enright, N.J., Marsula, R., Lamont, B.B. & Wissel, C. (1998) The ecological significance of canopy seed storage in fire-prone environments: a model for resprouting shrubs. Journal of Ecology, 86, 960–973.
- Gautier, S., Bergeron, Y. & Simon, J.-P. (1996) Effects of fire regime on the serotiny level of jack pine. Journal of Ecology, 84, 539–548.
- George, A.S. (1981) The genus Banksia. Nuytsia, 3, 239–473.
- Gill, A.M. (1981) Adaptive responses of Australian vascular plant species to fires. Fire and the Australian Biota (eds A. M. Gill, R. H. Groves & I. R. Noble), pp. 273–310. Australian Academy of Science, Canberra.
- Givnish, T.J. (1981) Serotiny, geography and fire in the pine barrens of New Jersey. Evolution, 35, 101–123.
- Hilbert, D.W. (1987) A model of life history strategies of chaparral shrubs in relation to fire frequency. Plant Responses to Stress (ed. J. D. Tenhunen et al.), pp. 597–606. NATO ASI series, Vol. G15. Springer. Berlin.
- Johnson, E.A. & Gutsell, S.L. (1994) Fire frequency models, methods and interpretations. Advances in Ecological Research, 25, 239–287.
- Keeley, J.E. (1986) Resilience of mediterranean shrub communities to fires. Resilience in Mediterranean-type Ecosystems (eds B. Dell, A.J. Hopkins & B.B. Lamont), pp. 95–112. Junk, The Hague.
- Keeley, J.E. & Zedler, P.H. (1978) Reproduction of chaparral shrubs after fire: a comparison of sprouting and seeding strategies. American Midland Naturalist, 99, 142–161.
- Lamont, B.B. (1991) Canopy seed storage and release – what’s in a name? Oikos, 58, 97–99.
- Lamont, B.B. & Barker, M.J. (1988) Seed bank dynamics of a serotinous, non-sprouting Banksia species. Australian Journal of Botany, 36, 193–203.
- Lamont, B.B. & Barrett, G.M. (1988) Constraints on seed production and storage in a root-suckering Banksia. Journal of Ecology, 76, 1069–1082.


<!-- PAGE BREAK -->

959 *N.J. Enright* et al.

- Lamont, B.B. & van Leeuwen, S. (1988) Seed production and mortality in a rare Banksia species. Journal of Applied Ecology, 25, 551–559.
- Lamont, B.B., Le Maitre, D.C., Cowling, R.M. & Enright, N.J. (1991a) Canopy seed storage in woody plants. The Botanical Review, 57, 277–317.
- Lamont, B.B., Connell, S.W. & Bergl, S. (1991b) Seed bank and population dynamics of *Banksia cuneata*: the role of time, fire and moisture. Botanical Gazette, 152, 114–122.
- Loehle, C. (1988) Tree life history strategies: the role of defenses. Canadian Journal of Forest Research, 18, 209–222.
- McMaster, G.S. & Zedler, P.H. (1981) Delayed seed dispersal in *Pinus torreyana* (Torrey Pine). Oecologia, 51, 62–66.
- McPeek, M.A. & Kalisz, S. (1993) Population sampling and bootstrapping in complex designs: demographic analysis. Design and Analysis of Ecological Experiments (eds S.M. Scheiner & J. Gurevitch), pp. 232–252. Chapman and Hall, New York.
- O’Dowd, D.J. & Gill, A.M. (1984) Predator satiation and site alteration following fire: mass reproduction of alpine ash (*Eucalyptus delegatensis*) in south-eastern Australia. Ecology, 65, 1052–1066.
- Perry, D.A. & Lotan, J.E. (1979) A model of fire selection for serotiny in lodgepole pine. Evolution, 33, 958–968.
- Stearns, S.C. (1992) The Evolution of Life Histories. Oxford University Press, New York.
- Taylor, A. & Hopper, S.D. (1988) The Banksia Atlas. Australian Flora and Fauna Series Number 8. Australian Government Publishing Service, Canberra.
- Van der Moezel, P.G., Loneragan, W.A. & Bell, D.T. (1987) Northern sandplain kwongan: regeneration following fire, juvenile period and flowering phenology. Journal of the Royal Society of Western Australia, 69, 123–132.
- Whelan, R.J. (1995) The Ecology of Fire. Cambridge University Press, Cambridge.
- Witkowski, E.T.F. & Lamont, B.B. (1996) Disproportionate allocation of mineral nutrients and carbon between vegetative and reproductive structures in *Banksia hookeriana*. Oecologia, 105, 38–42.
- Witkowski, E.T.F., Lamont, B.B. & Connell, S.J. (1991) Seed bank dynamics of three co-occurring banksias in south coastal Western Australia: the role of plant age, cockatoos, senescence and inter-fire establishment. Australian Journal of Botany, 39, 385–397.

*Received 2 October 1997*
*revision accepted 6 May 1998*

<!-- md_opt: model=claude-opus-5-5; date=2026-10-07; md_sha256=dea5bd614d6661fe35d1f161f903f5211e74485e59c2fc205f916a062af780d8; pdf_sha256=45de89dd58f3628919b3953f78b82567f8a3ed84611143c7ab3815122fba7338; pdf_pages=14; fixes=70 (shifted font encoding decoded throughout (digits one lower, fi/fl/ff/ffi ligature codes, punctuation codes for , . : ; ( ) & % - / ' ° ′ < > ± λ); missing = signs restored in statistics and equations; equations for λ and sensitivity rebuilt; Tables 1 and 2 rebuilt as pipe tables with footnote marks; coordinates, superscripts and subscripts restored; line-end hyphenation removed except true compounds; missing sentence end on page 948 restored from PDF; section heading on page 948 added; journal header, correspondence line, page numbers and running heads added; figure panel labels added; 40 references split one per item); unresolved=none -->
