*Austral Ecology*

## **RESEARCH ARTICLE** OPEN ACCESS

# **Using Patterns of Post-Fire Plant Reproduction to Inform Minimum Fire Intervals for Conservation Management in a Fire-Prone Woodland**

Russell G. Miller<sup>1,2</sup> | Neal J. Enright<sup>1</sup> | David J. Merritt<sup>2,3</sup> | Ben P. Miller<sup>2,3</sup> | Joseph B. Fontaine<sup>1</sup>

<sup>1</sup>School of Environmental and Conservation Sciences, Murdoch University, Murdoch, Western Australia, Australia | <sup>2</sup>Biodiversity and Conservation Science, Department of Biodiversity, Conservation and Attractions, Kings Park, Western Australia, Australia | <sup>3</sup>School of Biological Sciences, University of Western Australia, Crawley, Western Australia, Australia

**Correspondence:** Russell G. Miller (russell.miller@dbca.wa.gov.au)

**Received:** 19 May 2024 | **Revised:** 17 December 2024 | **Accepted:** 19 December 2024

**Funding:** This work was supported by an Australian Research Council Linkage grant (LP160100996) to NJE, JBF, and BPM.

**Keywords:** fire interval | fire management | generalised additive modelling | immaturity risk | juvenile period | seedling regeneration | southwestern Australia

#### **ABSTRACT**

The time interval between fires is a critical component of the fire regime that affects plant species persistence in fire-prone ecosystems. Fire intervals that are too short or too long may not support regeneration from seed banks or resprouting. Fire intervals that support adequate regeneration may also vary with other factors such as climate, herbivory, and population structure. Using field data on flowering and canopy seed banks, we modelled post-fire reproduction for woody fire-killed (obligate seeding) and resprouting species under varying rainfall and herbivory along a 35-year fire age chronosequence in Banksia woodlands in southwestern Australia. We found that fire-killed species attained reproductive maturity rapidly after fire with predicted juvenile periods (time to 50% flowering) of 1.5–2.3 years for shrubs and 4 years for trees. Resprouting species had similar juvenile periods to fire-killed species (1–3.5 years for resprouting shrubs, 4.4 years for resprouting trees). Reproduction varied with rainfall and herbivory with juvenile periods at least doubling under low rainfall or high herbivory for some species. Serotinous species produced cones (woody fruits containing seeds) shortly after flowering commenced, with some evidence of seed bank decline in the oldest sites. While reproduction was clearly correlated with time since fire, plant size was a much stronger predictor. Some species form multi-cohort populations which can introduce large variation into post-fire reproductive trajectories, and this should be considered when making decisions about fire intervals that may impact species persistence. This study provides critical information to assess fire interval-related threats for Banksia woodlands and suggests that woody species of these woodlands are generally tolerant of a wide range of fire intervals. Only the slowest-maturing, fire-killed species (*Banksia prionotes*, Proteaceae) may require fire intervals > 10 years to reduce immaturity risk under the least favourable growing conditions, and this species often occurs in discrete patches in the landscape such that fire management can be tailored accordingly.

#### **1 | Introduction**

Fire is a dominant ecological disturbance that has long shaped terrestrial ecosystems and driven plant species evolution globally (Bond, Woodward, and Midgley 2005; He and Lamont 2018; Keeley et al. 2011; Lamont 2022). Over evolutionary time periods, fire regimes (fire interval, severity, season and type at a point, which form spatial patterns at landscape scales) *sensu* (Gill 1981) have driven the development of a diversity of plant traits and life history strategies that allow populations to persist

This is an open access article under the terms of the Creative Commons Attribution-NonCommercial License, which permits use, distribution and reproduction in any medium, provided the original work is properly cited and is not used for commercial purposes.

© 2025 The Author(s). *Austral Ecology* published by John Wiley & Sons Australia, Ltd on behalf of Ecological Society of Australia.

*Austral Ecology*, 2025; 50:e70023

https://doi.org/10.1111/aec.70023 | 1 of 21


<!-- PAGE BREAK -->

in fire-prone landscapes (Harrison et al. 2021; Schwilk and Ackerly 2001). However, with ongoing climate change, fire is projected to occur with greater frequency and intensity in many regions (Jones et al. 2022), thereby imposing altered fire regimes on biota which may threaten their persistence (Bowman et al. 2014; Enright et al. 2015; Le Breton et al. 2022). Fire intervals, in particular, are considered to have a strong influence on species persistence, especially in ecosystems characterised by high severity or stand-replacing fire regimes (Bowman et al. 2014; Enright et al. 2015; Gallagher et al. 2021). Land management agencies tasked with conserving fire-prone ecosystems often include minimum fire-free intervals in their planning to maximise species persistence (Bradstock and Kenny 2003; Burrows and McCaw 2013).

Plant species which inhabit fire-prone environments are generally characterised as one of two major fire response types: (1) fire-killed (or obligate seeders), which are killed by complete canopy scorch and rely on soil or canopy-stored seeds for post-fire recovery; and (2) resprouters, which primarily survive fire and regrow from buds protected from the heat of fire, but can often also recruit new individuals from seed (Clarke et al. 2015; Pausas and Keeley 2014). Plants of both types face two key threats in relation to fire interval: immaturity risk and senescence risk. Immaturity risk occurs when intervals between lethal fires are shorter than the time required to reach reproductive maturity, establish a seed bank and/or develop resprouting capacity (Keeley, Ne'eman, and Fotheringham 1999), whereas senescence risk occurs when fire intervals exceed the lifespan of mature plants and their seed bank or stock of live buds (Enright et al. 2011; Gosper, Prober, and Yates 2013). Tolerable fire intervals, defined by minimum and maximum inter-fire periods that avoid species loss through immaturity and senescence risk respectively, are widely used in planning fire management with conservation objectives (Gosper et al. 2022). Immaturity risk and shortened fire intervals arguably pose the greatest risk to species persistence, with fire-killed species particularly vulnerable to decline or local extinction if they are slow maturing and require an ample fire-free period to flower and produce seeds (Bowman et al. 2014; Enright et al. 2014). Resprouters, while generally considered to be more resilient to short fire intervals, may be vulnerable to unusually short intervals due to the depletion of resources required for resprouting and reduced recruitment probability from seed (Enright et al. 2014, 2011; Fairman, Nitschke, and Bennett 2016).

Defining potential immaturity or senescence risks in a population or species is often achieved using demographic or reproductive information such as the timing of post-fire reproductive maturity, long-term trajectories of reproductive output and adult lifespans (Enright, Lamont, and Marsula 1996; Gosper, Prober, and Yates 2013; Kraaij et al. 2013). The juvenile period approach for quantifying post-fire reproductive maturity and estimating minimum tolerable fire intervals originates from a concept by Gill and Nicholls (1989) and has been applied to a variety of woody plant species in Australia and South Africa (Gill and McMahon 1986; Gosper et al. 2022; Harvey et al. 2017; Kraaij et al. 2013; McCaw 2008; Muir, Vesk, and Hepworth 2014). The juvenile period can be defined in a number of ways, including the time to first flowering or fruiting after fire in the most

precocious individual, or the time to flowering or fruiting in a certain portion of the population, often 50% (Gosper et al. 2022; Kraaij et al. 2013). While the first signs of reproduction may indicate the minimum time to maturity, several years of flowering and subsequent successful seed set may be required to accumulate a seed bank large enough for population replacement after fire, particularly for fire-killed species (Burrows, Wardell-Johnson, and Ward 2008; Burrows and Wardell-Johnson 2003). A suggested rule of thumb, therefore, is that a fire interval equal to two times (or three times for particularly sensitive species) the juvenile period is the minimum period required for population persistence under average growing conditions (e.g., average post-fire rainfall) (Burrows and Wardell-Johnson 2003; Gill and Nicholls 1989). A rule of thumb applied in South African shrublands is that at least half a population must have flowered at least three times (Kraaij et al. 2013). The juvenile period approach is specifically designed for fire-killed species where there is no persistence via resprouting, all individuals are normally killed by fire (i.e., fire is not patchy), there is little or no inter-fire seedling recruitment and seed banks are exhausted by fire (i.e., no residual seed bank) (Bell 2001). While this approach is supported by a few single- or multi-species studies on post-fire maturation rates (Burrows and Wardell-Johnson 2003; Treurnicht et al. 2016), it was only originally intended to provide guidance until more detailed assessments were available (Gill and Nicholls 1989), and there has been little critical evaluation of whether the 2× rule of thumb is appropriate across a wide range of species.

Maximum tolerable fire intervals are not commonly defined, but can be identified from adult longevity (e.g., evidence of senescence) or a decline in reproductive output in the long absence of fire, where there is little or no inter-fire seedling recruitment to maintain populations in the absence of fire (Bond 1980; Gosper, Prober, and Yates 2013). Maximum tolerable intervals for resprouters probably even precede adult senescence as the stock of live buds required for resprouting declines with plant age such that plants approaching the end of their lifespan have decreasing probability of survival through fire (Enright et al. 2011).

Variation in post-fire juvenile periods at least partly depends on the mode of plant regeneration (Burrows, Wardell-Johnson, and Ward 2008; Harvey et al. 2017). The juvenile period for plants regenerating from seed after fire (termed the primary juvenile period) tends to be longer than that for plants resprouting or recovering vegetatively after fire (termed the secondary juvenile period) (Bradstock and Kenny 2003; Zammit and Westoby 1987). Given that fire-killed species typically recover entirely from seed, only the primary juvenile period is relevant, whereas post-fire populations of resprouting species may contain a mix of resprouting individuals and post-fire seedlings so that both primary and secondary juvenile periods can be defined. In practice, reported juvenile periods for resprouting species are generally a composite value of both primary and secondary juvenile periods, but since new recruits are often infrequent, such estimates are best regarded as estimates of the secondary juvenile period (Enright and Goldblum 1999). Estimates of the primary juvenile period for resprouter species are rare due to sample size constraints associated with low rates of recruitment, and the usually much longer times to first reproduction (Keeley, Fotheringham, and Baer-Keeley 2006; Zammit and Westoby 1987). While the juvenile period approach largely focusses on fire-killed species, as 

2 of 21 | *Austral Ecology*, 2025


<!-- PAGE BREAK -->

these are considered to be most sensitive to fire interval impacts (Bowman et al. 2014; Enright et al. 2014; Harvey et al. 2017), successful reproduction and seedling recruitment are also required for the long-term persistence of resprouting species (Enright et al. 2014).

Despite global applicability of the juvenile period approach for assessing immaturity risk and estimating minimum tolerable fire intervals, including widespread use in some regions, including southern Australia and South Africa, there has been limited evaluation of the relationship between the onset of flowering and seed bank accumulation for different species, or of the consequences of variation in environmental conditions or population size structure for sensitivities to shortened fire intervals (Gosper et al. 2022; McCaw 2008; Treurnicht et al. 2016; von Takach Dukai, Lindenmayer, and Banks 2018; Wooller, Wooller, and Brown 2002). Variation in climate, herbivory and other environmental factors which affect plant growth and population structure can alter reproductive trajectories such that a single species-level juvenile period value may over- or under-estimate the fire-free period required for different populations (Gosper et al. 2022; Kraaij et al. 2013; McCaw 2008; Morgan, McCarthy, and Willocks 2021). Longer juvenile periods are often associated with low-productivity environments, including sites with low average rainfall, or low rainfall in the few years following fire (Burrows, Wardell-Johnson, and Ward 2008; McCaw 2008). Low environmental productivity can act to delay maturation, reduce growth, flowering and seed set, and increase the seedbank required for replacement after subsequent fires (Enright et al. 2015). High herbivore pressure may also delay or reduce flowering and seed production by reducing the size of plants and altering the resources available for reproduction, although these effects are less well documented (Brown, Paczkowska, and Gibson 2016). While variation in reproductive attributes across sites or years will always be a confounding factor in defining tolerable fire intervals, understanding the causal relationships behind variation in reproductive trajectories is particularly important for the management of contemporary landscapes with warming and drying climates alongside ongoing fragmentation and other human disturbances.

In this study, we used field data to model post-fire reproductive trajectories across varying environmental conditions for six woody plant species in fire-prone Banksia woodlands of southwestern Australia. Increasing understanding of fire interval-related population dynamics offers the opportunity to manage fire regimes for species conservation. We employed a space-for-time sampling approach to quantify reproduction (flowering rate, flower counts, and cone counts per plant) in co-occurring fire-killed and resprouting species along a post-fire chronosequence of 1–35 years since the last fire and across sites with varying rainfall and herbivory. Vegetation in this region regularly experiences fire, and native species exhibit a variety of fire-related traits and adaptation syndromes which we anticipate would be reflected in varying post-fire reproductive trajectories. Objectives for risk reduction through prescribed burning (managed fire intervals) indicate fire intervals of 13–33 years (Ritchie et al. 2021). Recent data show post-fire ages ranging from 1 to 56 years since the last fire, with some areas potentially older (Tangney et al. 2022). During the period 1970–2009, median fire intervals (prescribed burns and wildfires combined) across the northern (drier) part of our study area was 9 years with an average of 37% of area burnt attributed to wildfires (Wilson et al. 2014).

We aim to quantify post-fire juvenile periods (defined here as time to 50% flowering), estimate minimum tolerable fire intervals based on the '2 × juvenile period' rule of thumb guideline, explore whether this rule of thumb reflects sufficient flowering and canopy seed bank accumulation and quantify reproduction in the long absence of fire. We also aim to quantify reproductive patterns under varying rainfall and herbivory conditions and how this affects minimum tolerable fire interval estimates. Populations of fire-killed and resprouting species may also be multi-cohort (Hobbs and Atkins 1990) which can complicate reproductive dynamics; therefore, we also aim to evaluate models of reproduction relative to plant size (as a surrogate for age or cohort) to investigate the causal relationship between size and reproduction and test the strength of time since fire as a predictor of reproduction commonly used to inform fire management.

#### **2 | Methods**

#### **2.1 | Study Area**

This study was conducted in urban and peri-urban reserves in the Swan Coastal Plain bioregion of southwestern Australia. Low open Banksia woodlands are the dominant vegetation type in this region, with an estimated 50%–60% of their original extent having been cleared in recent decades for the rapid urbanisation of Western Australia's capital city of Perth (Ritchie et al. 2021). Most remaining vegetation is restricted to a few large conservation areas on the city margins, and small urban and peri-urban reserves, but even in these areas, there is projected ongoing species loss associated with time-delayed effects of habitat loss and fragmentation (Fowler et al. 2023). In 2016, Banksia woodlands were recognised as a Threatened Ecological Community under Australia's national environmental law, and smaller portions have conservation listings at the state level (Commonwealth of Australia 2016; Ramalho et al. 2014; Ritchie et al. 2021).

Banksia woodlands are characterised by a low (4–8 m height), open canopy of *Banksia* (Proteaceae) trees (predominantly the resprouters *B. attenuata* and *B. menziesii*, and fire-killed *B. prionotes*) and a species-rich understorey dominated by sclerophyllous shrubs in the plant families Dilleniaceae, Ericaceae, Fabaceae, Myrtaceae and Proteaceae (Dodd and Griffin 1989; Ritchie et al. 2021). The nutrient-poor, deep sandy soils of the Swan Coastal Plain are comprised largely of two major Pleistocene dune complexes (Bassendean and Spearwood), distinguished by their age of origin (Spearwood sands: 120k—500ka old, Bassendean sands: ~2 ma old) and nutrient content (particularly nitrogen and phosphorus, declining with age) (Turner, Hayes, and Laliberté 2018). The region has a Mediterranean-type climate, with cool, wet winters and hot, dry summers, making vegetation highly fire-prone during the dry season (austral summer and autumn; December–May). Average annual precipitation ranges from approximately 800 mm in the south to 550 mm in the north, 80% of which falls between May and October (Tangney et al. 2022) (Figure S1).

*Austral Ecology*, 2025 | 3 of 21


<!-- PAGE BREAK -->

Fire is a regular occurrence on the Swan Coastal Plain, including low-moderate severity prescribed burning for risk reduction and conservation purposes during autumn and spring periods, and high severity wildfires mostly from human-caused ignitions during the hot, dry summer period (Densmore and Clingan 2019; Enright and Fontaine 2014; Howard et al. 2020; Plucinski 2014). The proximity of urban and peri-urban Banksia woodlands to human homes and infrastructure has placed substantial attention and importance on fire management in this ecosystem. While there are no direct estimates of historical or long-term fire intervals in Banksia woodlands that might suggest lower or upper limits to their adaptations, they share attributes (e.g., key plant functional types, surface and elevated fuel types) with surrounding vegetation types, including shrublands to the north and eucalypt forests to the east and south, where typical fire intervals have been estimated at 10–40+ years (shrublands) and 5–20 years (low severity, forest) or 20–100 years (high severity, forest) (Burrows, Ward, and Robinson 1995; Enright et al. 2012; Enright and Thomas 2008; Murphy et al. 2013). Indigenous use of fire was widespread in the region prior to European colonisation but specific information regarding burning in Banksia woodlands is not clear (Lullfitz et al. 2020; Rodrigues et al. 2022).

#### **2.2 | Study Species**

To explore fire interval effects on reproduction, we chose six woody plant species with a range of growth forms, fire response traits and seed bank storage modes across four common plant families (Table 1). All species are native, common and widespread in Banksia woodlands and considered indicators of the vegetation type; although varying in their abundance and distribution within the landscape (Gibson et al. 1994). Serotinous (canopy seed bank) species typically accumulate woody fruits containing seeds (hereafter cones) in the canopy over multiple years, therefore allowing assessment of cumulative reproductive output. In the study area, the two selected *Banksia* species are known to be weakly serotinous, with most seeds released from woody fruits (hereafter cones) within 1–2 years of cone maturity (Cowling and Lamont 1985). The dioecious shrub species *Allocasuarina humilis* is moderately serotinous with female plants retaining seeds in cones for up to 5 years (personal obs.). By pairing serotinous species with species with other seed storage modes, here specifically soil seed banks, we aim to gain an insight into the response of the broader plant community.

#### **2.3 | Site Selection**

To assess varying fire intervals, we employed a space-for-time approach and selected sites with a broad range of recent fire histories (time since fire, TSF). We first interrogated fire history data for remnant vegetation in urban and peri-urban reserves across the study region to identify a set of candidate sites with a wide range of fire ages, suitable access (with permission from land managers) and appropriate vegetation type (i.e., not wetland, riparian, or limestone vegetation). Year of last fire for each site was determined from spatial data layers maintained by the Western Australian Department of Biodiversity, Conservation and Attractions (DBCA-060, https://catalogue.data.wa.gov.au/dataset/dbca-fire-history); historical satellite and aerial imagery (Landgate, https://map-viewer-plus.app.landgate.wa.gov.au/index.html); and local government records. Given limitations in fire history records and satellite and aerial imagery, we were unable to confirm exact ages for some sites beyond 35 years (occurring before approximately 1986). Sites with no assignable post-fire age are referred to here as long unburnt (LUB), and for analysis are given a notional age of 35 years.

We visited candidate sites to confirm the above criteria as well as the presence of the study species and the absence of

**TABLE 1** | Key life history traits and the number of sites (N sites) for the six study species.

| Species | Growth form<sup>a</sup> | Fire response | Seed bank | N sites | Peak flowering times |
|---|---|---|---|---|---|
| *Gompholobium tomentosum* (Fabaceae) | Shrub (single-stemmed; 0.3–1 m) | Fire-killed | Soil | 17 | Sept–Oct |
| *Acacia pulchella* (Fabaceae) | Shrub (single-stemmed; 0.5–2 m) | Fire-killed | Soil | 16 | Aug–Sept |
| *Banksia prionotes* (Proteaceae) | Tree (up to 10 m) | Fire-killed | Canopy (weakly serotinous) | 11 | Feb |
| *Hibbertia hypericoides* (Dilleniaceae) | Subshrub (multi-stemmed; 0.2–1 m) | Resprouter (basal) | Soil | 17 | Aug–Sept |
| *Allocasuarina humilis* (Casuarinaceae) | Shrub (multi-stemmed; 0.2–2 m) | Resprouter (basal) | Canopy (moderately serotinous) | 11 | Aug–Sept |
| *Banksia attenuata* (Proteaceae) | Tree (up to 10 m) | Resprouter (epicormic and/or basal) | Canopy (weakly serotinous) | 16 | Dec–Jan |

<sup>a</sup>Dimensions refer to typical height range of mature plants, Western Australian Herbarium (1998–).

4 of 21 | *Austral Ecology*, 2025


<!-- PAGE BREAK -->

human-caused soil or vegetation disturbances that could otherwise alter population attributes. This produced a total of 34 sites across a fire interval chronosequence from 1 to 35 years (or more), with each site containing one to five study species. The number of sites surveyed for each species ranged from 11 to 17, all spanning a similar post-fire chronosequence (Table 1). Some sites were surveyed over two successive years, creating two nonindependent TSF samples.

Sites were mostly (91%) located on Spearwood sands across a 100 km north–south extent of the Swan Coastal Plain (Figure 1). Mean annual rainfall ranged from 698 mm in the north (Muchea, 1971–2000) to 843 mm in the south (Halls Head, 1971–2000; Australian Bureau of Meteorology 2020) (Figure S1). All species except *B. prionotes* were sampled across the full extent of this rainfall gradient. *Banksia prionotes* was only found across a very narrow (negligible) range (30 mm mean annual rainfall difference) in the sampled study area, but occur more broadly in the region, as do the other study species. The presence (*n* = 19) or absence (*n* = 15) of kangaroos (western grey kangaroo, *Macropus fuliginosus*) as major herbivores was assessed at each site based on sightings of individuals or their scats as well as local knowledge and records (City of Joondalup 2015; City of Nedlands 2014; Ecoscape (Australia Pty Ltd) 2008; Government of Western Australia 2000; Natural Area Consulting 2012). Where present in urban reserves, kangaroos (or signs of their presence) are easily observed, and populations often achieve high density. There was no discernible change in kangaroo abundance over the study period.

#### **2.4 | Field Surveys**

At each site, data were collected on reproductive and size attributes for live individuals. Seedlings less than 1–2 years old in sites older than 4 years since fire (inter-fire seedlings) were excluded as these individuals can have a low survival rate and therefore have little consequence for the reproductive status of populations. Data on the abundance of inter-fire seedlings from the same sites are presented in Miller, Enright, Fontaine et al. (2024). Seedlings were distinguished by the presence of cotyledons, lack of signs of current or past reproduction, and were generally <10–20 cm tall for shrub species or <30 cm tall for tree species. Estimates of seedling age were confirmed by observations of seedlings of known age in post-fire sites.

Data were mostly collected within plots positioned to include as many of the target species as possible and ranging in size from 25 to 150 m<sup>2</sup> as necessary to suit different species and plant densities, and to ensure sampling of at least 30 individuals. Plant densities were calculated from the number of individuals in each plot and scaled to the number of plants per hectare. Smaller plots were used for shrub species (density range 0.1–4.6 plants m<sup>−2</sup>), and larger plots for tree species (0.03–1.58 plants m<sup>−2</sup>). At least two plots were established at each site, but where plant density was particularly low, measurements were taken based on a nearest-neighbour search until a minimum of 30 plants were recorded. For some plot-based surveys, additional nearest plants outside of plots were measured to fulfil sample size criterion. Field surveys were undertaken from 2016 to 2018 during peak flowering times for each species (Table 1).

Measurements recorded for each individual included: (1) number of flowers (or inflorescences; all species), (2) number of mature cones with unopened follicles (canopy seed bank species only) and (3) size (all species). *Allocasuarina humilis* is a dioecious species and we identified and recorded attributes of male and female plants separately (only female plants produce cones). The number of cones recorded represents the cumulative canopy seed bank from all previous reproductive seasons excluding seed loss from seed predation, disease and spontaneous follicle opening, among other factors. Size was recorded as aboveground plant height (*Gompholobium tomentosum* and *Acacia pulchella*), canopy volume (*Hibbertia hypericoides* and *Allocasuarina humilis*) or stem diameter at breast height (DBH, 1.37 m above the ground; *Banksia attenuata, B. prionotes*). These measurements were chosen to best represent how size relates to reproductive performance given each species' growth form.

Map labels: Yanchep; Western Australia; Joondalup; Perth; Rockingham; Study sites Location; Mean annual rainfall 719 - 730 mm, 761 - 771, 802 - 812; Swan Coastal Plain; Native vegetation; Urban areas; Major rivers and estuaries; 0 7.5 15 km.

**FIGURE 1** | Locations of the 34 study sites in urban and peri-urban nature reserves on the Swan Coastal Plain around Perth, Western Australia. Some reserves contained multiple sites of various fire ages (some points obscured by other points). Mean annual rainfall follows a north–south (low-high) gradient indicated by the colour (light blue-dark blue) of site location points (circles). Green shading indicates extant native vegetation, grey shading indicates urban areas and the solid red line indicates the boundary of the Swan Coastal Plain region (also shown on inset map).

*Austral Ecology*, 2025 | 5 of 21


<!-- PAGE BREAK -->

For trees with multiple stems, effective DBH (diameter of the summed cross-sectional area of all live stems) was calculated to produce a single representative value (Prior et al. 2011). Canopy volume (*V*, m<sup>3</sup>) for *H. hypericoides* and *A. humilis* was calculated from maximum canopy height (*H*, m) and perpendicular canopy width measurements (*W1* and *W2*, m), using an ellipsoid form:

*V* = 4/3 × *π* × *H*/2 × *W1*/2 × *W2*/2

#### **2.5 | Data Analysis**

#### **2.5.1 | Post-Fire Reproductive Trajectories**

To analyse post-fire reproductive trajectories, we evaluated generalised additive mixed models (GAMMs) of TSF, herbivory and mean annual rainfall as a priori predictors of each of three population-level reproductive attributes: flowering rate (% individuals flowering), mean number of flowers per plant and mean number of closed cones per plant (for the three serotinous species only). Population-level attributes were calculated from all individuals surveyed, including resprouting and young (nonreproductive) plants, where present. We employed a model selection approach whereby we constructed a set of plausible models from subsets of the a priori predictors and compared these using Akaike's Information Criterion corrected for small sample size (AICc) and AICc model weights (ωAICc) which represent the probability or weight of evidence for each model (Burnham, Anderson, and Huyvaert 2011; Hurvich and Tsai 1989). Models with ΔAICc <5 generally represented a cumulative ωAICc of ≥0.95 and therefore are presented here as part of the 95% confidence set, following Symonds and Moussalli (2011). Models with ΔAICc<2 are considered to have substantial support (Burnham and Anderson 2002). We conducted this analysis in *R* (version 4.0.3) (R Core Team 2020) using the *FSSgam* package (Fisher et al. 2018) which enables an all subsets approach and uses the *gam()* function from the *mgcv* package (Wood 2017).

Flowering rate, presented as proportions, was modelled using a binomial error distribution (logit link function) with data weighted by the number of individuals recorded per site. Mean number of flowers and cones per plant were modelled using a tweedie error distribution (log link function) to account for many zero values (i.e., non-flowering/non-fruiting individuals). TSF was log-transformed for analysis as responses are expected to change most rapidly in the first few years after fire, and to optimise the distribution of values across the predictor range. TSF was included as a continuous smoother in the model set to allow for non-linear relationships with time. In all models, the smoothing parameter was limited to a simple spline (k=3) to avoid overfitting. Mean annual rainfall was included as a linear predictor in all models, and any effects were presented as predictions at the 10th and 90th percentile of mean annual rainfall across the TSF chronosequence, representing post-fire reproductive trajectories for 'low' (~720 mm) and 'high' (~790 mm) rainfall sites, respectively.

Herbivory was included as a two-level factor variable (absence or presence of kangaroo herbivores) in model sets for shrub species only (i.e., excluding *B. attenuata* and *B. prionotes*) as we lacked a strong a priori expectation of the effects of herbivory from kangaroos (generally <2 m tall) on tree species that are typically >4 m tall at maturity. A two-way interaction between log-transformed TSF and herbivory was included in the model set for *G. tomentosum* only to explore if effects of herbivory varied by TSF. Replication of different herbivory levels across the range of log-transformed TSF was not considered to be adequate for the other shrub species and therefore was only included as an additive effect in other model sets. An identifier for the year of survey was included as a random smoother in all models for species where measurements were recorded in two successive years to account for repeat measures and any annual variation in environmental conditions (e.g., rainfall) other than an increase in TSF by 1 year.

Modelling of flowering rate and flower counts was conducted separately for male and female plants of the dioecious species *A. humilis*. Top-ranking model comparisons are presented for models on female data only. Only female plants produce cones and seeds and so modelling of cone counts was necessarily restricted to female plant data. Juvenile period was calculated from the flowering rate of female plants. The sex ratio was, on average, 45% females and 55% males across all populations (excluding non-reproductive individuals), or 49% females and 51% males after the post-fire maturation period (i.e., after 4 years) (Figure S2).

#### **2.5.2 | Time Since Fire as a Predictor of Reproduction**

To assess the strength of TSF as a predictor of reproduction, we compared GAMMs with single predictors of either TSF or plant size (height, canopy volume or effective DBH) for each of the three reproductive attributes measured. Models using plant size as the predictor represent the mechanistic relationship between TSF and reproduction, where the growth of plants following fire enables greater access to resources and an increase in reproductive output. For single-cohort populations (i.e., fire-killed species), we would expect that models using single predictors of TSF and plant size would explain similar amounts of variation (i.e., *R*<sup>2</sup>) and have a similar weight of evidence (i.e., AICc and ωAICc). However, for multi-cohort populations (usually resprouters, but also possible for some fire-killed species), we would expect that models using size would explain much more variation and have a much greater weight of evidence than models using TSF.

GAMMs were constructed as outlined above, where models of TSF or size alone were compared using *FSSgam*. Size measurements (height, canopy volume, effective DBH) were log-transformed to optimise the distribution of values across the predictor range and improve model fit. For the dioecious species (*A. humilis*), modelling was conducted separately for male and female plants, with top-ranking model comparisons presented for female data only.

#### **3 | Results**

#### **3.1 | Flowering Rates and Juvenile Periods**

TSF consistently appeared in top-ranked models of flowering rates for all species (Table 2). Flowering rate generally increased rapidly in the first few years after fire and stabilised thereafter (Figure 2). *Acacia pulchella* was the only species with an apparent decline in flowering rate in longer unburnt sites; in sites older than 30 years, predicted flowering rate fell below 50%, however,

6 of 21 | *Austral Ecology*, 2025


<!-- PAGE BREAK -->

**TABLE 2** | Top-ranking generalised additive mixed models (GAMMs) for predicting flowering rates for the six study species.

| Species | Model | ΔAICc | ωAICc | R<sup>2</sup> | edf |
|---|---|---|---|---|---|
| *Gompholobium tomentosum* | log(TSF) × Herbivory + Rainfall | 0 | 1 | 0.70 | 7.72 |
| *Acacia pulchella* | log(TSF) + Rainfall | 0 | 0.83 | 0.33 | 3.98 |
| | log(TSF) + Rainfall + Herbivory | 3.13 | 0.17 | 0.34 | 4.98 |
| *Hibbertia hypericoides* | log(TSF) + Herbivory | 0 | 0.88 | 0.48 | 4.88 |
| | log(TSF) + Herbivory + Rainfall | 3.97 | 0.12 | 0.48 | 5.87 |
| *Allocasuarina humilis* | log(TSF) | 0 | 0.84 | 0.92 | 3.80 |
| | log(TSF) + Herbivory | 4.05 | 0.11 | 0.90 | 4.86 |
| *Banksia prionotes* | log(TSF) | 0 | 0.82 | 0.27 | 3.92 |
| | log(TSF) + Rainfall | 3.08 | 0.18 | 0.27 | 4.90 |
| *Banksia attenuata* | log(TSF) + Rainfall | 0 | 1 | 0.52 | 4.45 |

*Note:* Predictor variables included time since fire (TSF, log-transformed), the presence or absence of dominant herbivores (Herbivory) and mean annual rainfall (Rainfall). Models <5 ΔAICc are presented with AICc model weights (ωAICc), variance explained (*R*<sup>2</sup> ) and effective degrees of freedom (edf) reported for model comparison. For *Allocasuarina humilis*, models presented are for female data only.

**FIGURE 2** | Relationships between time (years) since fire and flowering rate (% population flowering) for (A) two fire-killed shrubs (*Gompholobium tomentosum* and *Acacia pulchella*), (B) two resprouting shrubs (*Hibbertia hypericoides* and *Allocasuarina humilis*), (C) a fire-killed, serotinous tree (*Banksia prionotes*) and (D) a resprouting, serotinous tree (*B. attenuata*). Solid and dashed lines represent top-ranked generalised additive mixed model fits (ΔAICc=0), and shaded ribbons represent 95% confidence intervals. Horizontal grey lines indicate when half of the individuals in a population are flowering. Relationships for *A. humilis* are presented separately for male and female plants.

confidence interval bands are wide at sites older than 20 years and so this result is interpreted with caution (Figure 2A). Predicted times to 50% flowering ranged from 1 to 4.4 years, corresponding to minimum tolerable fire intervals (2×juvenile period rule of thumb) of 2 to 8.8 years (Table 3). Mean predicted juvenile period for fire-killed species (2.6 ± 0.7 years [SE]) was similar to that for resprouting species (3.0 ± 1.0 years; Table 3). For all species other than the two resprouting shrubs, there was considerable site-to-site variation in flowering rate at any given TSF, as reflected in 95% confidence intervals (Figure 2A,C,D). For these species, 12% of sites older than predicted juvenile periods had <50% of plants flowering.

*Austral Ecology*, 2025 | 7 of 21


<!-- PAGE BREAK -->

**TABLE 3** | Predicted juvenile period (years), estimated minimum tolerable fire interval (TFI, 2×juvenile period) and percent of maximum flower and cone counts at minimum TFI for the six study species based on top-ranked generalised additive mixed models.

| Species | Fire-related functional type | Juvenile period (95% CI) | Min TFI | Percent (%) of max flower count at min TFI | Percent (%) of max cone count at min TFI |
|---|---|---|---|---|---|
| *Gompholobium tomentosum* | Fire-killed shrub | 1.5<sup>a</sup> (1.5<sup>a</sup>—3.7) | 3.0 | 27 | — |
| *Acacia pulchella* | Fire-killed shrub | 2.3 (1.9–2.6) | 4.6 | 84 | — |
| *Hibbertia hypericoides* | Resprouting shrub | 1<sup>a</sup> (1<sup>a</sup>–1<sup>a</sup>) | 2.0 | 22 | — |
| *Allocasuarina humilis* | Resprouting shrub | 3.5 (2.4–5.1) | 7.0 | 68 | 45 |
| *Banksia prionotes* | Fire-killed tree | 4.0 (2.1<sup>a</sup>–11.8) | 8.0 | 56 | 91 |
| *Banksia attenuata* | Resprouting tree | 4.4 (1.8–8.5) | 8.8 | 73 | 57 |

*Note:* Juvenile period is equal to the time required following fire for at least half a population to flower and 2×juvenile period is a common metric to estimate the minimum tolerable fire interval. For *Allocasuarina humilis*, data are for females only.

<sup>a</sup>Predictions are >50% at the youngest site sampled and therefore predictions are given as the youngest age.

**FIGURE 3** | Relationship between time (years) since fire and flowering rate (% population flowering) as a function of (A) herbivory and (B) high (90th percentile) vs. low (10th percentile) mean annual rainfall where present in top-ranked generalised additive models (ΔAICc=0, Table 2). Solid and dashed lines represent top-ranked generalised additive mixed model fits (ΔAICc=0), and shaded ribbons represent 95% confidence intervals. Horizontal grey lines indicate when half of the individuals in a population are flowering.

Herbivory appeared in the top-ranked models of flowering rate for *Gompholobium tomentosum* and *Hibbertia hypericoides* (Table 2). *Gompholobium tomentosum* showed an interactive effect of herbivory and TSF, with flowering rate lower in young sites (<10 years old) where herbivores are present, but with little effect of herbivory on flowering rate thereafter (Figure 3A). Herbivory appears as an additive term in the top-ranked model for *H. hypericoides* where the presence of herbivores was associated with a reduction in the predicted flowering rate by 13%, on average, across all ages (Figure 3A).

Mean annual rainfall appeared in the top-ranked models of flowering rate for *G. tomentosum*, *Acacia pulchella* and *Banksia attenuata* (Table 2). Models predicted that the

8 of 21 | *Austral Ecology*, 2025


<!-- PAGE BREAK -->

**TABLE 4** | Predicted juvenile periods (years) as affected by the presence or absence of herbivory, and high (90th percentile) versus low (10th percentile) average annual rainfall. Predictions based on species-specific GAMMs. Blank cells indicate where covariates were not included in top-ranked models.

| Species | Juvenile period (95% confidence interval): Herbivory Absent | Herbivory Present | Rainfall Low | Rainfall High |
|---|---|---|---|---|
| *Gompholobium tomentosum* | 1.5<sup>a</sup> (1.5<sup>a</sup>–1.5<sup>a</sup>) | 4.3 (1.9–6.6) | 4.2 (1.5<sup>a</sup>–15.9) | 1.5<sup>a</sup> (1.5<sup>a</sup>–2.5) |
| *Acacia pulchella* | — | — | 3.0 (2.0–5.0) | 1.8<sup>a</sup> (1.8<sup>a</sup>–2.3) |
| *Hibbertia hypericoides* | 1<sup>a</sup> (1<sup>a</sup>–1<sup>a</sup>) | 1<sup>a</sup> (1<sup>a</sup>–1.3<sup>a</sup>) | — | — |
| *Banksia prionotes* | — | — | — | — |
| *Banksia attenuata* | — | — | 2.3 (1.3<sup>a</sup>–5.5) | 8.0 (3.1–19.2) |

<sup>a</sup>Predictions are >50% at the youngest site sampled and therefore predictions are given as the youngest age.

**TABLE 5** | Top-ranking generalised additive mixed models (GAMMs) for predicting flower and cone counts per plant for each of the six study species.

| Species | Model | ΔAICc | ωAICc | R<sup>2</sup> | edf |
|---|---|---|---|---|---|
| Flower count | | | | | |
| *Gompholobium tomentosum* | log(TSF) + Rainfall | 0 | 0.58 | 0.26 | 4.00 |
| | log(TSF) | 1.39 | 0.29 | 0.30 | 3.59 |
| | log(TSF) + Rainfall + Herbivory | 3.84 | 0.09 | 0.26 | 5.00 |
| *Acacia pulchella* | log(TSF) + Rainfall | 0 | 0.66 | 0.47 | 3.74 |
| | log(TSF) | 1.93 | 0.25 | 0.16 | 2.73 |
| *Hibbertia hypericoides* | log(TSF) | 0 | 0.78 | 0.31 | 3.00 |
| | log(TSF) + Herbivory | 3.52 | 0.13 | 0.30 | 4.00 |
| | log(TSF) + Rainfall | 4.61 | 0.08 | 0.31 | 4.00 |
| *Allocasuarina humilis* | log(TSF) | 0 | 0.99 | 0.51 | 3.92 |
| *Banksia prionotes* | log(TSF) | 0 | 0.77 | 0.29 | 3.00 |
| | log(TSF) + Rainfall | 2.46 | 0.23 | 0.31 | 4.00 |
| *Banksia attenuata* | log(TSF) | 0 | 0.86 | 0.15 | 3.00 |
| | log(TSF) + Rainfall | 3.59 | 0.14 | 0.14 | 4.00 |
| Cone count | | | | | |
| *Allocasuarina humilis* | log(TSF) | 0 | 0.97 | 0.51 | 3.81 |
| *Banksia prionotes* | log(TSF) | 0 | 0.87 | 0.34 | 3.82 |
| | log(TSF) + Rainfall | 3.71 | 0.14 | 0.35 | 4.68 |
| *Banksia attenuata* | log(TSF) | 0 | 0.84 | 0.36 | 3.00 |
| | log(TSF) + Rainfall | 3.25 | 0.17 | 0.37 | 4.00 |

*Note:* Predictor variables included time since fire (TSF, log-transformed), the presence or absence of dominant herbivores (Herbivory) and mean annual rainfall (Rainfall). Models <5 ΔAICc are presented with AICc model weights (ωAICc), variance explained (*R*<sup>2</sup> ) and effective degrees of freedom (edf) reported for model comparison. For *Allocasuarina humilis*, models presented are for female data only.

flowering rate was 23% lower, on average, in low mean annual rainfall sites (10th percentile, ~720 mm/year) compared to high mean annual rainfall sites (90th percentile, ~790 mm/year) across all ages for the two fire-killed shrubs (*G. tomentosum* and *A. pulchella*) (Figure 3B), although this effect was not significant for *A. pulchella* (*t* = 1.221, *p* = 0.245). Models predicted the opposite effect of mean annual rainfall for *B. attenuata* (i.e., higher flowering rate in lower rainfall sites) (Figure 3B) (*t* = −2.259, *p* = 0.035).

Herbivory and low rainfall were associated with an increase in the predicted juvenile period for *G. tomentosum* by 2.6–2.7 years compared to where herbivores were absent and in higher mean annual rainfall sites (Table 4). Low mean annual rainfall increased

*Austral Ecology*, 2025 | 9 of 21


<!-- PAGE BREAK -->

the juvenile period for *A. pulchella* by 2.2 years (Table 4). While herbivory was found to impact the flowering rate of *H. hypericoides*, post-fire recovery was so rapid as to not alter the predicted juvenile period (Table 4). High mean annual rainfall increased the juvenile period of *B. attenuata* by 5.7 years (Table 4).

#### **3.2 | Flower and Cone Counts**

TSF consistently appeared in top-ranked models of mean flower count and mean cone count per plant for all species (Table 5). Models suggested that mean flower count increased steadily with increasing TSF for most species except *A. pulchella* (Figure 4). *Acacia pulchella* instead showed a rapid increase in flowering until around 5–8 years post-fire, followed by a slight decline thereafter (Figure 4A). Similarly, female plants of *A. humilis* showed an increase in flowering until around 10–15 years post-fire, followed by a slight decline thereafter (Figure 4B). Male plants of *A. humilis* showed a steady increase in flowering with increasing TSF. The peak mean flower count occurred beyond the predicted minimum tolerable fire interval for all species (Figure 4). At this predicted minimum tolerable fire interval, populations of all species had reached 22%–84% of their peak flower count (Table 3).

Mean annual rainfall appeared in the top-ranked models of mean flower count for the two fire-killed shrub species (*G. tomentosum* and *A. pulchella*) (Table 5). Models predicted that mean flower count was 61% lower in low rainfall sites (10th percentile) compared to high rainfall sites (90th percentile) for these two species across all ages (Figure 5). Herbivory did not appear in any top-ranked models of mean flower count (Table 5).

Populations of *A. humilis* and *B. prionotes* first produced cones 3–4 years post-fire, and mean cone count increased up until 10–15 years post-fire, after which mean cone count was highly variable, with weak evidence of decline in the longer absence of fire (Figure 6). Populations of *B. attenuata* had produced cones even in the youngest sites sampled (1–2 years post-fire), and mean cone count increased steadily with increasing TSF (Figure 6). At the time of their respective predicted minimum tolerable fire intervals, populations of all three serotinous species had reached 45%–91% of their peak cone count (Table 3). Mean annual rainfall did not appear in any top-ranked models for cone counts of these three species (Table 5).

Canopy seed bank density, expressed as the number of cones per hectare, showed a similar although more pronounced nonlinear pattern for *B. prionotes* (Figure S3). On average, seed bank density for *B. prionotes* increased rapidly post-fire up to a maximum of approximately 5500 cones per ha around 10 years and declined thereafter to <1000 cones per ha after 30 years. These seed bank dynamics appear to be driven primarily by changes in plant density (Figure S4), especially a decline in the density of reproductive intermediate-sized trees (2–10 cm DBH) in older sites (Figure S5A), with a minor influence of a decline in reproductive output across various sizes with increasing TSF (Figure S5B).

**FIGURE 4** | Relationships between time (years) since fire and mean flower count per plant for (A) two fire-killed shrubs (*Gompholobium tomentosum* and *Acacia pulchella*), (B) two resprouting shrubs (*Hibbertia hypericoides* and *Allocasuarina humilis*), (C) a fire-killed, serotinous tree (*Banksia prionotes*) and (D) a resprouting, serotinous tree (*B. attenuata*). Solid and dashed lines represent top-ranked generalised additive mixed model fits (ΔAICc=0), and shaded ribbons represent 95% confidence intervals. Vertical blue lines indicate juvenile period (dashed) and corresponding minimum tolerable fire interval estimates (solid) given in Table 3. Relationships for *A. humilis* are presented separately for male and female plants.

10 of 21 | *Austral Ecology*, 2025

<!-- PAGE BREAK -->

**FIGURE 5** | Relationships between time (years) since fire and mean flower count per plant as a function of high (90th percentile) vs. low (10th percentile) mean annual rainfall where present in top-ranked generalised additive models (Table 5). Solid and dashed lines represent top-ranked generalised additive mixed model fits (ΔAICc=0), and shaded ribbons represent 95% confidence intervals. Vertical blue lines indicate juvenile period (dashed) and corresponding minimum tolerable fire interval estimates (solid) given in Table 3.

**FIGURE 6** | Relationships between time (years) since fire and mean cone count per plant for the three serotinous (canopy seed bank) species (only female plants for *A. humilis*). *Banksia prionotes* is killed by fire, while the others resprout—therefore data are for mixed seedling and resprouting populations for resprouters. Solid black lines represent top-ranked generalised additive mixed model fits (ΔAICc=0), and shaded ribbons represent 95% confidence intervals. Vertical blue lines indicate juvenile period (dashed) and corresponding minimum tolerable fire interval estimates (solid) given in Table 3.

Canopy seed bank density for *B. attenuata* followed a similar trend to cones per plant, showing an increase from an average of around 500–600 cones per ha in the first five years after fire to an average of around 800–1000 cones per ha in sites older than 20 years (Figure S3). In contrast to *B. prionotes*, seed bank dynamics for the resprouter *B. attenuata* appear to be driven primarily by an increase in individual reproductive output (cones per plant) with increasing TSF (especially in the most productive, largest (>8 cm DBH) trees; Figure S6B), rather than any changes in tree density of this reproductive cohort (Figures S4 and S6A).

#### **3.3 | Time Since Fire Versus Size as a Predictor of Reproduction**

Models using size as a predictor of each of three reproductive attributes were almost always supported by a greater weight of evidence than those using TSF (Table 6). Models of the flowering rate of *A. humilis* showed similar support for size and TSF as the best predictor, although size was still ranked higher than TSF based on AICc (Table 6). This indicates that TSF is not a strong predictor of reproduction in comparison to the underlying mechanistic relationship between size and reproduction. In all but one case (*A. humilis* flowering rate), models using size as a predictor explained greater variation in the data (*R*<sup>2</sup>) than models using TSF (Table 6).

For all species, predicted flowering rate increased rapidly with an increase in size in small plants, with no evidence of a decrease in flowering rate in the largest, and presumably oldest, plants observed (Figure 7). The predicted height at which 50% of individuals were flowering was approximately 12 cm (95% CI [9.6, 16.2]) for *G. tomentosum* and 58 cm (95% CI [54.3, 61.5]) for *A. pulchella* (Figure 7). The predicted canopy volume at 50% flowering was approximately 0.008 m<sup>3</sup> (95% CI [0.002, 0.04]) for *H. hypericoides* and 0.14 m<sup>3</sup> (95% CI [0.03, 0.40]) for *A. humilis* (approximately equivalent to a plant with dimensions of 25 × 25 × 25 cm and 65 × 65 × 65 cm, respectively; Figure 7). For the tree species, predicted DBH at 50% flowering was 3.3 cm (95% CI [1.9, 5.8]) for *B. attenuata* and 2.9 cm (95% CI [2.5, 3.3]) for *B. prionotes* (Figure 7).

For *A. pulchella*, predicted flower count initially increased with size for plants up to approximately 150 cm tall, but any further increase in size (and presumably age) did not necessarily translate into higher predicted flower counts (Figure 8A).

*Austral Ecology*, 2025 | 11 of 21


<!-- PAGE BREAK -->

**TABLE 6** | Top-ranking generalised additive mixed models (GAMMs) for predicting individual-level flowering rate, flower count and cone count according to size (height, canopy volume, or DBH) or TSF (time since fire).

| Species | Model | ΔAICc | ωAICc | R<sup>2</sup> | edf |
|---|---|---|---|---|---|
| Flowering rate | | | | | |
| *Gompholobium tomentosum* | log(Height) | 0 | 1 | 0.31 | 3.86 |
| | log(TSF) | 249.27 | 0 | 0.07 | 3.94 |
| *Acacia pulchella* | log(Height) | 0 | 1 | 0.54 | 2.52 |
| | log(TSF) | 454.33 | 0 | 0.08 | 2.98 |
| *Hibbertia hypericoides* | log(Canopy volume) | 0 | 1 | 0.35 | 3.67 |
| | log(TSF) | 194.47 | 0 | 0.10 | 3.78 |
| *Allocasuarina humilis* | log(Canopy volume) | 0 | 0.73 | 0.26 | 3.79 |
| | log(TSF) | 1.94 | 0.27 | 0.40 | 3.64 |
| *Banksia prionotes* | log(DBH) | 0 | 1 | 0.39 | 3.88 |
| | log(TSF) | 317.50 | 0 | 0.03 | 3.92 |
| *Banksia attenuata* | log(DBH) | 0 | 1 | 0.46 | 3.46 |
| | log(TSF) | 217.85 | 0 | 0.13 | 3.00 |
| Flower count | | | | | |
| *Gompholobium tomentosum* | log(Height) | 0 | 1 | 0.18 | 3.91 |
| | log(TSF) | 491.95 | 0 | 0.06 | 3.96 |
| *Acacia pulchella* | log(Height) | 0 | 1 | 0.14 | 2.99 |
| | log(TSF) | 516.88 | 0 | 0.06 | 2.98 |
| *Hibbertia hypericoides* | log(Canopy volume) | 0 | 1 | 0.17 | 3.37 |
| | log(TSF) | 643.24 | 0 | 0.10 | 3.00 |
| *Allocasuarina humilis* | log(Canopy volume) | 0 | 1 | 0.13 | 3.74 |
| | log(TSF) | 108.42 | 0 | 0.03 | 3.96 |
| *Banksia prionotes* | log(DBH) | 0 | 1 | 0.32 | 3.96 |
| | log(TSF) | 539.98 | 0 | 0.04 | 3.00 |
| *Banksia attenuata* | log(DBH) | 0 | 1 | 0.36 | 3.00 |
| | log(TSF) | 479.71 | 0 | 0.02 | 3.00 |
| Cone count | | | | | |
| *Allocasuarina humilis* | log(Canopy volume) | 0 | 1 | 0.22 | 3.96 |
| | log(TSF) | 125.98 | 0 | 0.09 | 3.97 |
| *Banksia prionotes* | log(DBH) | 0 | 1 | 0.11 | 3.97 |
| | log(TSF) | 493.60 | 0 | 0.02 | 3.95 |
| *Banksia attenuata* | log(DBH) | 0 | 1 | 0.25 | 3.90 |
| | log(TSF) | 259.61 | 0 | 0.05 | 3.32 |

*Note:* AICc model weights (ωAICc), variance explained (*R*<sup>2</sup>) and effective degrees of freedom (edf) reported for model comparison. For *Allocasuarina humilis*, models presented are for female data only.

For all other species, predicted flower counts continued to increase with size where the largest plants observed had the highest flower count (Figure 8A). For *A. humilis*, male plants had higher predicted flower counts than female plants of the same size (Figure 8A).

Predicted cone counts for *A. humilis* and *B. prionotes* initially increased with size but reached a threshold beyond which any increase in size did not translate into an increase in cone count (Figure 8B). In comparison, predicted cone counts for *B. attenuata* continued to increase with size up to a maximum of 4–5

12 of 21 | *Austral Ecology*, 2025


<!-- PAGE BREAK -->

**FIGURE 7** | Relationships between plant size and flowering rate for all six study species. Maximum canopy height (cm), canopy volume (m<sup>3</sup>, ellipsoid form) or effective DBH (cm) was used as the best representative of size given each species' typical growth form. Solid black lines represent generalised additive mixed model fits, and shaded ribbons represent 95% confidence intervals.

cones per plant for trees 40–50 cm diameter at breast height (Figure 8B). Maximum predicted cone count for *B. prionotes* barely exceeded one cone per plant, although individuals held up to 10 cones (Figure 8B).

#### **4 | Discussion**

#### **4.1 | Juvenile Periods and Tolerable Fire Intervals**

The shape of post-fire reproductive trajectories provides direct evidence of fire frequencies that permit species persistence and is critical information for the conservation and management of fire-prone ecosystems globally, especially with ongoing climate and fire regime change. We modelled reproduction in six woody plant species with a variety of fire-related traits across a range of fire ages in Banksia woodlands and found juvenile periods of 1–4 years, with little difference attributable to fire response type. Minimum tolerable fire intervals under average growing conditions based on primary juvenile periods for fire-killed species and a mix of primary and secondary juvenile periods for resprouters ranged from approximately 3–8 years and 2–9 years, respectively. Although there was some evidence of decline in reproduction in the oldest sites (>30 years since the last fire), reproductive capacity was likely still adequate for post-fire seedling recruitment after these long fire intervals. Variation in juvenile periods and reproductive output across all fire ages were associated with variation in growth forms and with changes in site productivity (rainfall) and herbivory. Taken together, our observations of rapid post-fire reproductive recovery and no fatal decline in reproduction in the long absence of fire are consistent with the suggestion that Banksia woodlands are adapted to mixed-severity fire regimes including widely varying intervals, where species have the capacity to cope with short and long fire intervals (Miller, Enright, Fontaine et al. 2024).

The species studied here, potentially representing a larger suite of Banksia woodland species with similar growth forms, fire response and seed bank storage modes, would all likely tolerate fire intervals of 10 years under average growing conditions, and the most rapidly maturing would likely tolerate intervals as short as 5 years under average growing conditions. While juvenile period data for resprouters is important for understanding effects on reproduction from seed, which is crucial for long-term population persistence, minimum tolerable fire intervals for resprouters based on the juvenile period method disregard the often-overriding contribution of resprouting to the post-fire recovery of species with this capability. Resprouters, therefore, may be able to tolerate even shorter intervals (i.e., less than 5 years) if resprouting capacity develops rapidly post-fire. However, several repeated short fire intervals (less than 5 years) may preclude recruitment and erode adult resprouting capacity

*Austral Ecology*, 2025 | 13 of 21


<!-- PAGE BREAK -->

**FIGURE 8** | Relationships between (A) plant size and flower count, and (B) plant size and cone count (serotinous species only). Maximum canopy height (cm), canopy volume (m<sup>3</sup>, ellipsoid form) or effective DBH (cm) was used as the best representative of size given each species' typical growth form. Solid or dashed lines represent generalised additive mixed model fits, and shaded ribbons represent 95% confidence intervals. Relationships between plant size and flower count for *A. humilis*, a dioecious species, are presented separately for male and female plants.

(Enright et al. 2011; Fairman, Nitschke, and Bennett 2016), acting as a separate mechanism of sensitivity to short fire intervals (i.e., separate to immaturity risk). Rather than resprouters, a more appropriate focus for understanding community-level minimum tolerable fire intervals is the slowest maturing, fire-killed species (*B. prionotes*). *Banksia prionotes* likely requires longer intervals of at least 8–10 years for sufficient post-fire recruitment where it occurs, especially where low rainfall delays or reduces flowering and seed production. Current managed fire interval objectives of 13–33 years for risk reduction (Ritchie et al. 2021) should, therefore, support the persistence of the woody plant functional types studied here; however, continued regional warming and drying associated with climate change may pose a threat of shortening wildfire intervals, consistent with the interval squeeze concept *sensu* (Enright et al. 2015).

Our juvenile period and minimum tolerable fire interval findings are consistent with evidence from the region on the same or similar species (Enright et al. 2014; Wilson et al. 2014). However, corresponding minimum fire interval recommendations (8–16 years) suggested by Wilson et al. (2014) are based on population-level maturity of resprouters (a combination of primary and secondary juvenile periods) which, as explained above, are not the primary focus of the juvenile period approach as they largely recover via resprouting. Instead, minimum fire intervals based on juvenile period data for fire-killed species

14 of 21 | *Austral Ecology*, 2025


<!-- PAGE BREAK -->

presented in Wilson et al. (2014) are up to 8–10 years for the most sensitive, slow-maturing species, which is consistent with our findings.

Suggested minimum tolerable fire intervals for fire-killed serotinous species (including *B. prionotes*) in drier (less productive) shrublands north of our study region range from 10 to 15 years for high versus low post-fire winter rainfall years, respectively (Enright et al. 2014). As our minimum tolerable interval estimates (2–9 years) suggest, minimum tolerable fire intervals should be somewhat shorter in the more productive (higher rainfall) Banksia woodlands. Consistent with this hypothesis, our estimates of minimum tolerable fire intervals of around 3–5 years for fire-killed shrubs with soil seed banks are somewhat shorter than the equivalent 5–6 years reported in Enright et al. (2014). Interestingly, however, estimates for resprouting shrubs show little difference between the two regions; resprouting shrubs with canopy seed banks showed minimum tolerable intervals of around 5–7 years and resprouting shrubs with soil seed banks showed little risk of even the shortest intervals sampled (Enright et al. 2014). Post-fire growth and maturation rates of fire-killed shrubs, which regenerate from seedlings, are strongly contingent on environmental productivity (Gosper et al. 2022), whereas post-fire growth rates in resprouting shrubs may be less contingent on environmental conditions during the post-fire period as already-established plants draw on stored energy reserves for post-fire growth and reproduction (Clarke et al. 2013), acknowledging again that seedling recruitment is not the major form of post-fire recovery for resprouters. A strength of the analysis of Enright et al. (2014) is that estimates of minimum tolerable fire intervals were based on robust, direct measures of resprouter survival and seedling recruitment, and therefore we suggest that further targeted study of seed availability and subsequent post-fire seedling recruitment at various fire intervals in Banksia woodlands is warranted to confirm minimum tolerable fire intervals and further explore variation along environmental gradients.

Additional evidence is also needed to test the assumptions of the juvenile period approach for estimating minimum intervals, including whether the 2× rule of thumb (Gill and Nicholls 1989) adequately covers natural variation in (1) seed bank accumulation rates and (2) flowering, pollination and seed set for species with different traits. At our estimated minimum tolerable fire intervals, populations had reached 22%–84% of their predicted maximum flowering output, and serotinous species had produced cones over at least 3–4 years and had reached 45%–91% of their predicted maximum canopy seed bank accumulation. Variation in post-fire reproductive attributes among species potentially indicates that the efficacy of the 2× approximation of minimum tolerable fire intervals varies between species. Perhaps species with soil-stored seed banks might be more adequately covered by the 2× approximation than those with canopy seed banks, as species with soil-stored seed may possess a residual seed bank after fire (i.e., seed banks are not completely exhausted by fire) (Auld and Denham 2006) and do not have to produce a persistent woody fruit requiring resources like serotinous species (Cramer and Midgley 2009; Tonnabel et al. 2012). Our results also demonstrate substantial variation in reproduction owing to varying environmental conditions, suggesting that, in some cases, the 2× approximation may be inadequate to account for delays in reproduction. For example, for *G. tomentosum*, the presence of herbivores and low mean annual rainfall delayed the juvenile period beyond the estimated minimum tolerable fire interval under average growing conditions.

#### **4.2 | Post-Fire Reproduction**

Fire-killed species are generally considered to have longer primary juvenile periods than the secondary juvenile periods of co-occurring resprouters (Gosper, Prober, and Yates 2013; Harvey et al. 2017), but we observed little difference. Similar juvenile periods for these species groups, however, do not necessarily mean that they have equivalent reproductive trajectories or would be expected to have similar fire interval responses given differences in other traits. For example, resprouters may have a much lower maximum reproductive output at peak maturity compared to co-occurring fire-killed species owing to differences in resource allocation to reproduction versus energy storage (Enright and Lamont 1989). Also, by the onset of reproductive maturity, resprouters have likely developed a strong resprouting capacity, potentially surviving through several fires before reaching a highly reproductive stage (Enright and Lamont 1992), although resprouting and reproductive capacity may be eroded by a series of short fire intervals (Enright et al. 2011; Fairman, Nitschke, and Bennett 2016). In contrast, fire-killed species may require several years after reaching reproductive maturity to develop adequate reproductive capacity for recovery after subsequent fires and therefore could be at risk of decline at the same intervals at which resprouters can readily resprout. There is an obvious advantage for fire-killed species in fire-prone habitats to reach maximum reproductive capacity as quickly as possible, and probably soon after the onset of reproduction, as indicated by our juvenile period data.

For the fire-killed species with the longest juvenile period studied here (*B. prionotes*), some plants produced cones following the first year of flowering (4 years post-fire), and the corresponding estimated minimum tolerable fire interval (8 years) allowed populations to reach, on average, 56% of their maximum flower production and 91% of their maximum canopy seed bank size. For a related, fire-killed *Banksia* species, Enright, Lamont, and Marsula (1996) similarly showed that plants began producing cones after the first year of flowering and produced an increasing number of cones in the following few years. Despite being the slowest-maturing, fire-killed species in this study, and probably in Banksia woodlands generally, *B. prionotes* appears to have a relatively short juvenile period compared to other fire-killed species in southwestern Australia (Gosper et al. 2022; Harvey et al. 2017; Wooller, Wooller, and Brown 2002). Populations of *B. prionotes* also often occur in discrete stands such that a conservative minimum interval of 10 years, under average growing conditions, may not necessarily be relevant to apply to the entire landscape, or where fires are sufficiently patchy or of low severity to allow established individuals to survive fire (Burrows and Middleton 2016). Intervals less than 10 years are relatively rare on the Swan Coastal Plain, especially in areas with managed fire regimes, although changing climate regimes and increasing human disturbance do not necessarily preclude such intervals (Fontaine 2022).

*Austral Ecology*, 2025 | 15 of 21


<!-- PAGE BREAK -->

Our findings are consistent with previous efforts from the region in quantifying post-fire seed production in the resprouting *B. attenuata* in showing that mature trees are capable of producing cones in the first year or two after fire because they can resprout epicormically (Densmore and Clingan 2019; Valentine et al. 2014). Post-fire cone production is mediated by fire severity, where there are minimal interruptions to reproduction after low severity fire, but trees may take several years to regain the same level of cone production after high severity fire (Densmore and Clingan 2019). By the time of the species-specific minimum tolerable fire interval estimated here (~9 years), Valentine et al. (2014) estimated that mature adults (>2 m tall) had accumulated, on average, approximately 6 cones per plant, which is higher than estimates presented here (~1 cone per plant). Our dataset includes smaller juvenile plants and a subset of our data on *B. attenuata* trees >2 m tall shows cone counts across a similar range of values to Valentine et al. (2014). Johnston, Stock, and Mawson (2016) and Densmore and Clingan (2019) report around 1.3 and 7 times higher estimates of *B. attenuata* mean canopy seed bank density (cones per ha), respectively, than we find here (mean 746 cones per ha; Figure S3). However, Johnston, Stock, and Mawson (2016) included higher rainfall sites on the Swan Coastal Plain and Densmore and Clingan (2019) reported on the entire crop of cones for ease of recording regardless of whether they had closed follicles or not, where, in both cases, it would be reasonable to expect higher canopy seed bank estimates. Interestingly, the much higher estimates of cones per ha reported by Densmore and Clingan (2019) can be explained by the weakly serotinous nature of *B. attenuata* in the region (Cowling and Lamont 1985), where most seeds are released from cones within two years of seed maturity, but opened cones are likely retained on the plant for many years, and could therefore give the impression of a much larger canopy seed bank. Johnston, Stock, and Mawson (2016) reported a similar trend of gradually increasing seed bank size with increasing time since fire for *B. attenuata* and a similar range of values for cones per ha for *B. prionotes*.

We show that plants of fire-killed shrubs that regenerate via seed following fire gain reproductive capacity quickly. Likewise, Monk, Pate, and Loneragan (1981) observed that the fire-killed *A. pulchella* began producing flowers and seeds in the second year after fire, and achieved maximum seed production shortly thereafter (3–4 years post-fire). These observations differ from those for fire-killed Proteaceae shrubs from southeastern Australia where cone and seed production was not observed for a few years after first flowering, and was slower overall (Jenkins, Morrison, and Auld 2010). For fast-growing species such as *A. pulchella*, a doubling of the juvenile period as a general rule of thumb for estimating the minimum tolerable fire interval may be adequate to sustain populations under average growing conditions, even if this only allows for one or two additional years of seed production. Rapid post-fire reproductive maturity and abundant seed production are important mechanisms to cope with short fire intervals for species adapted to frequent canopy scorch, whether that be understorey shrubs scorched in all but the lowest severity fires, or trees burnt in crown fire regimes (Enright, Lamont, and Marsula 1996; Gauthier, Bergeron, and Simon 1996). Likewise, soil-stored seed banks, variable seed dormancy and residual seedbanks are traits that allow species to cope with short fire intervals. Banksia woodlands may be adapted to mixed severity fire regimes where understorey and overstorey components experience a range of low, moderate and high severity fire at widely varying intervals, potentially as short as 5–10 years in the understorey (Hobbs and Atkins 1990; Miller, Enright, Fontaine et al. 2024).

Our findings for the resprouting shrub *A. humilis* are consistent with expectations for dioecious species in that patterns of post-fire flowering appear to be driven by the costs of male versus female reproduction (Barrett and Hough 2012; Obeso 2002). Flower and pollen production in male plants is less costly than flower, cone and seed production in female plants and so we would expect to observe precocious male flowering (Field, Pickup, and Barrett 2013). In comparison to female plants, male *A. humilis* plants had a shorter juvenile period (2.5 vs. 3.5 years on average), produced more flowers per plant on average across all fire ages (927 vs. 269) and produced more flowers on average at any given plant size.

Wilson et al. (2014) provided an estimate of 40 years for the maximum tolerable fire interval for Banksia woodlands based on the maximum longevity of serotinous, fire-killed *Banksia* species. However, *Banksia* longevity was derived for a different species (*B. hookeriana*) from a nearby region with different climate and fire regimes, and for a species that grows as a tall shrub rather than a tree, and therefore presumably has a shorter lifespan (Cowling and Lamont 1985). We expect *Banksia* tree longevity in the range of 40–60 years for *B. prionotes* (fire-killed) and to exceed 100 years for *B. attenuata* (resprouter). Over the approximately 35-year chronosequence studied here, we found no evidence of decline in reproduction for *B. attenuata*, but some evidence for a minor decline in reproduction in *B. prionotes* which appears primarily driven by a decline in plant density of mature stages with a minor contribution from a decline in reproductive output per plant. Although *B. prionotes* can have low levels of inter-fire seedling recruitment (Miller, Enright, Fontaine et al. 2024), this input of non-reproductive individuals does not appear to have a noticeable effect on population-level reproduction (Figure S5). There is little evidence of major population senescence in *B. prionotes*, and therefore, maximum tolerable intervals are likely to exceed 40 years, which are very rare regardless (Wilson et al. 2014).

#### **4.3 | Reproduction Under Varying Environmental and Demographic Conditions**

Environmental productivity (mean annual rainfall) and the presence or absence of herbivory were found to be important factors associated with post-fire reproductive trajectories (Burrows, Wardell-Johnson, and Ward 2008; Gosper et al. 2022; McCaw 2008). In sites with low mean rainfall (low productivity) or herbivore presence, predicted juvenile periods were delayed by up to 3 years, and therefore minimum tolerable fire intervals by up to 6 years for fire-killed understorey shrubs (*A. pulchella* and *G. tomentosum*). Low mean rainfall also decreased flower production by up to 61% for the same species. For short-lived species, this may represent a doubling (or more) of the minimum fire-free period required for population replacement, and potentially a reduction in lifetime reproductive output.

16 of 21 | *Austral Ecology*, 2025


<!-- PAGE BREAK -->

While these data pertain to mean rainfall and the prevailing presence or absence of herbivores, our results suggest that delayed reproductive maturity and reduced reproductive output could occur under abrupt environmental changes such as the introduction of native or non-native herbivores, or the increasing severity of drought conditions associated with climate change (Gosper et al. 2022; Matusick et al. 2018). Modelling suggests that primary juvenile periods for serotinous obligate seeders (here represented by *B. prionotes*) could more than double in the study area under 2050 climate change scenarios, including lower mean annual rainfall (Gosper et al. 2022), potentially requiring longer fire intervals to conserve vulnerable populations. In general, we sampled across a relatively narrow mean annual rainfall gradient (~150 mm difference) compared to the variation present in the broader region, and in particular, our sampling of *B. prionotes* populations occurred across a very narrow range (30 mm difference). It is not surprising, therefore, that we did not detect an effect of rainfall for *B. prionotes*; however, if sampling was repeated across a wider rainfall gradient (spatial or temporal), we would expect to detect slower maturity rates under low rainfall. This is a broad concern for fire-killed species which rely on post-fire recruitment from seeds for persistence, and is consistent with the concept of 'interval squeeze' where populations are vulnerable to decline with the simultaneous shortening of fire intervals and reduced seed production and post-fire recruitment associated with climate change impacts (Enright et al. 2015). Invasive grassy weeds are also a significant threat in Banksia woodlands (Ritchie et al. 2021), and may pose an additional limitation on population recovery if weeds reduce post-fire seedling recruitment or delay maturation and reproductive maturity.

The effects of varying mean annual rainfall on flowering rate (juvenile period) provided a curious result for *B. attenuata*, where populations in high mean rainfall sites appeared to mature more slowly than populations in low mean rainfall sites. Rather than higher rainfall delaying maturation, we believe this relates to differences in the demographic structure of populations under varying rainfall regimes altering population-level calculations. In the study area, higher rainfall and longer growing seasons likely facilitate higher rates of inter-fire seedling recruitment (Miller, Enright, Fontaine et al. 2024), although not to a level that would result in densification or canopy closure that would, in turn, preclude recruitment of shade-intolerant seedlings and probably reduce reproductive output. Flowering rates reported here are a composite of reproduction (or lack thereof) in seedlings, juveniles and adults, and therefore a higher proportion of non-reproductive seedlings and juveniles resulting from higher recruitment will lower flowering rate estimates.

Canopy seed banks (closed cone counts per plant) for both *Banksia* species were very low, with *B. attenuata* generally having less than two seed-bearing cones per plant on average, and *B. prionotes* generally less than one. Low cone counts can be explained by a combination of the weakly serotinous nature of these *Banksia* species in the study area, and demographic structures with a high proportion of juvenile plants with little to no reproduction (Figures S5 and S6). Cowling and Lamont (1985) reported a gradient in the degree of serotiny of *Banksia* species in the region with populations in our study area being weakly or non-serotinous, meaning that the majority of the accumulated canopy seed bank originates from the most recent seed crop minus any losses from disease and predation. Whelan and Ayre (2020) likewise reported very low canopy seed bank accumulation for a serotinous *Banksia* shrub species from southeastern Australia. Both weakly serotinous *Banksia* species studied here develop multi-cohort populations, especially in the absence of fire (Hobbs and Atkins 1990; Miller, Enright, Fontaine et al. 2024). Like the effect of rainfall on *B. attenuata* flowering rate noted above, a high proportion of non-reproductive juvenile plants lowers population-level seed bank size estimates which likely underestimates the reproductive potential of mature individuals. While mature individuals have the potential to contribute much larger seed banks, weak serotiny will ultimately limit the maximum size of the canopy seed bank. This contrasts with the seed bank dynamics of highly serotinous *Banksia* species in ecosystems with more regular crown fire regimes where canopy seed banks can accumulate over many years (Enright, Lamont, and Marsula 1996).

Top-ranked models explained up to 92% of variation in the data (mean = 43%, inter-quartile range = 30%–51%; Table 2, Table 5), leaving, in some cases, substantial variation unexplained by the variables considered in this study. More detailed analyses of the effects of interannual weather variation and spatially varying site variables (e.g., soil type, aspect, elevation) could explain greater variation in the data and provide a deeper understanding of the drivers of reproduction. The analysis presented here using mean annual rainfall could also be extended to quantify the effects of varying rainfall at different demographic stages—for example, during seedling establishment (1–2 years post-fire), floral initiation and fruit development—to assess the sensitivity of post-fire reproduction to extreme dry climate conditions. Such analyses could help predict scenarios or sites under which fire managers may need to consider longer managed fire intervals to accommodate delayed juvenile periods under increasingly common droughts and heatwave events (Matusick et al. 2018; Ruthrof et al. 2021).

#### **4.4 | Time Since Fire Versus Size as a Predictor of Reproduction**

While we found that TSF was a clear indicator of reproduction, we also show that plant size is a much stronger predictor of reproductive capacity as also reported elsewhere by Andrus et al. (2020), Gauthier, Bergeron, and Simon (1993) and von Takach Dukai, Lindenmayer, and Banks (2018). Many plant species that inhabit fire-prone environments (especially fire-killed species in stand-replacing fire regimes) are often assumed to follow a specific post-fire trajectory where a single, post-fire seedling cohort matures and grows larger at a similar rate (Gill and McMahon 1986). However, this assumption may weaken in non-crown fire regimes, or for multi-cohort populations resulting from inter-fire recruitment, post-fire resprouting, or both. Inter-fire recruitment is evident for most of the species studied here (Hobbs and Atkins 1990; Miller, Enright, Fontaine et al. 2024), and therefore, population-level metrics of reproduction may be more closely related to varying demographic structure or environmental conditions rather than TSF.

We acknowledge TSF and post-fire juvenile periods as simplistic yet useful indicators of post-fire reproductive maturity, but here we show that the effects of other environmental and demographic conditions can introduce substantial variation into species 

*Austral Ecology*, 2025 | 17 of 21


<!-- PAGE BREAK -->

responses, and therefore are important to consider when making decisions about fire intervals that may impact species persistence (Gosper et al. 2022). As originally recognised, the juvenile period approach for estimating minimum tolerable fire intervals can provide rapid and low-cost guidance for fire management planning, but advances in ecological understanding and technology for measuring vegetation attributes should allow for the development of more sophisticated models for predicting variation in reproduction by including multiple environmental and demographic variables. Other metrics of species reproductive maturity and minimum tolerable fire intervals that may provide useful alternative or supplemental information for fire managers include the assessment of (1) the reproductive output (and density) of the largest individuals as the plants that contribute most to the reproductive capacity of the population and (2) average understorey plant height and litter cover as surrogates of plant growth and fuel accumulation. Ongoing advances in the mapping of vegetation structure from remote sensing data (e.g., through airborne or terrestrial laser scanning) (Moudrý et al. 2023; Turner et al. 2023) may provide an opportunity to measure plant size and density across large areas and combine with environmental and demographic data, such as that presented in this study, to calculate metrics of reproduction at a similar landscape scale to traditional fire age mapping currently used extensively in fire management planning.

#### **Author Contributions**

**Russell G. Miller:** conceptualization, data curation, formal analysis, investigation, methodology, visualization, writing – original draft, writing – review and editing. **Joseph B. Fontaine:** conceptualization, formal analysis, funding acquisition, investigation, methodology, visualization, writing – review and editing. **Ben P. Miller:** conceptualization, formal analysis, funding acquisition, investigation, methodology, visualization, writing – review and editing. **Neal J. Enright:** conceptualization, formal analysis, funding acquisition, investigation, methodology, visualization, writing – review and editing. **David J. Merritt:** conceptualization, formal analysis, investigation, methodology, visualization, writing – review and editing.

#### **Acknowledgements**

We thank the undergraduate students who assisted with field data collection. We acknowledge the Whadjuk and Pindjarup Noongar peoples as the Traditional Owners of the land on which this work was conducted, and their continuing connection to land, sea, and community. We pay our respects to them, their culture and their elders past and present. Open access publishing facilitated by Murdoch University, as part of the Wiley - Murdoch University agreement via the Council of Australian University Librarians.

#### **Conflicts of Interest**

The authors declare no conflicts of interest.

#### **Data Availability Statement**

Data are available from Miller, Enright, Merritt et al. (2024).

#### **References**

- Andrus, R. A., B. J. Harvey, A. Hoffman, and T. T. Veblen. 2020. "Reproductive Maturity and Cone Abundance Vary With Tree Size and Stand Basal Area for Two Widely Distributed Conifers." *Ecosphere* 11: e03092. https://doi.org/10.1002/ecs2.3092.
- Auld, T. D., and A. J. Denham. 2006. "How Much Seed Remains in the Soil After Fire?" *Plant Ecology* 187: 15–24. https://doi.org/10.1007/s11258-006-9129-0.
- Australian Bureau of Meteorology. 2020. "Climate Data Online" [Online]. Accessed 06 December 2019. http://www.bom.gov.au/climate/data/.
- Barrett, S. C. H., and J. Hough. 2012. "Sexual Dimorphism in Flowering Plants." *Journal of Experimental Botany* 64: 67–82. https://doi.org/10.1093/jxb/ers308.
- Bell, D. T. 2001. "Ecological Response Syndromes in the Flora of Southwestern Western Australia: Fire Resprouters Versus Reseeders." *Botanical Review* 67: 417–440.
- Bond, W. 1980. "Fire and Senescent Fynbos in the Swartberg, Southern Cape." *Southern African Forestry Journal* 114: 68–71. https://doi.org/10.1080/00382167.1980.9629837.
- Bond, W. J., F. I. Woodward, and G. F. Midgley. 2005. "The Global Distribution of Ecosystems in a World Without Fire." *New Phytologist* 165: 525–538. https://doi.org/10.1111/j.1469-8137.2004.01252.x.
- Bowman, D. M. J. S., B. P. Murphy, D. L. J. Neyland, G. J. Williamson, and L. D. Prior. 2014. "Abrupt Fire Regime Change May Cause Landscape-Wide Loss of Mature Obligate Seeder Forests." *Global Change Biology* 20: 1008–1015.https://doi.org/10.1111/gcb.12433.
- Bradstock, R. A., and B. J. Kenny. 2003. "An Application of Plant Functional Types to Fire Management in a Conservation Reserve in Southeastern Australia." *Journal of Vegetation Science* 14: 345–354. https://doi.org/10.1111/j.1654-1103.2003.tb02160.x.
- Brown, K., G. Paczkowska, and N. Gibson. 2016. "Mitigating Impacts of Weeds and Kangaroo Grazing Following Prescribed Fire in a Banksia Woodland." *Ecological Management & Restoration* 17: 133–139. https://doi.org/10.1111/emr.12208.
- Burnham, K. P., and D. R. Anderson. 2002. *Model Selection and Multimodel Inference: A Practical Information-Theoretic Approach*. New York: Springer.
- Burnham, K. P., D. R. Anderson, and K. P. Huyvaert. 2011. "AIC Model Selection and Multimodel Inference in Behavioral Ecology: Some Background, Observations, and Comparisons." *Behavioral Ecology and Sociobiology* 65: 23–35. https://doi.org/10.1007/s00265-010-1029-6.
- Burrows, N., and L. McCaw. 2013. "Prescribed Burning in Southwestern Australian Forests." *Frontiers in Ecology and the Environment* 11: e25– e34.https://doi.org/10.1890/120356.
- Burrows, N. D., and T. Middleton. 2016. "Mechanisms Enabling a Fire Sensitive Plant to Survive Frequent Fires in South-West Australian Eucalypt Forests." *Fire Ecology* 12: 26–40. https://doi.org/10.4996/fireecology.1201026.
- Burrows, N. D., B. Ward, and A. D. Robinson. 1995. "Jarrah Forest Fire History From Stem Analysis and Anthropological Evidence." *Australian Forestry* 58: 7–16.https://doi.org/10.1080/00049158.1995.10674636.
- Burrows, N. D., G. Wardell-Johnson, and B. Ward. 2008. "Post-Fire Juvenile Period of Plants in South-West Australia Forests and Implications for Fire Management." *Journal of the Royal Society of Western Australia* 91: 163–174.
- Burrows, N. D., and G. W. Wardell-Johnson. 2003. "Fire and Plant Interactions in Forested Ecosystems of South-West Western Australia." In *Fire in Ecosystems of South-West Western Australia*, edited by I. Abbott and N. D. Burrows. Leiden, The Netherlands: Backhuys Publishers.
- City of Joondalup. 2015. "Hepburn Heights Conservation Area Management Plan." Unpublished report prepared for the City of Joondalup, Joondalup, Western Australia.
- City of Nedlands. 2014. "Shenton Bushland Management Plan 2013– 2018." Unpublished report prepared for the City of Nedlands, Nedlands, Western Australia.

18 of 21 | *Austral Ecology*, 2025


<!-- PAGE BREAK -->

- Clarke, P. J., M. J. Lawes, J. J. Midgley, et al. 2013. "Resprouting as a Key Functional Trait: How Buds, Protection and Resources Drive Persistence After Fire." *New Phytologist* 197: 19–35. https://doi.org/10.1111/nph.12001.
- Clarke, P. J., M. J. Lawes, B. P. Murphy, et al. 2015. "A Synthesis of Postfire Recovery Traits of Woody Plants in Australian Ecosystems." *Science of the Total Environment* 534: 31–42. https://doi.org/10.1016/j.scitotenv.2015.04.002.
- Commonwealth of Australia. 2016. *Banksia Woodlands of the Swan Coastal Plain Ecological Community in Community and Species Profile and Threats Database*. Canberra, Australia: Department of the Environment and Energy. http://www.environment.gov.au/sprat.
- Cowling, R. M., and B. B. Lamont. 1985. "Variation in Serotiny of Three *Banksia* Species Along a Climatic Gradient." *Australian Journal of Ecology* 10: 345–350.
- Cramer, M. D., and J. J. Midgley. 2009. "Maintenance Costs of Serotiny Do Not Explain Weak Serotiny." *Austral Ecology* 34: 653–662. https://doi.org/10.1111/j.1442-9993.2009.01971.x.
- Densmore, V. S., and E. S. Clingan. 2019. "Prescribed Burning in a Mediterranean-Climate Region Mitigates the Disturbance by Bushfire to a Critical Food Resource for an Endangered Bird, the Carnaby's Cockatoo." *Fire Ecology* 15: 36.https://doi.org/10.1186/s42408-019-0054-8.
- Dodd, J., and E. A. Griffin. 1989. "Floristics of the Banksia Woodlands." *Journal of the Royal Society of Western Australia* 71: 89–90.
- Ecoscape (Australia Pty Ltd). 2008. "Koondoola Regional Bushland Management Plan." Unpublished report prepared for the City of Wanneroo, Perth, Western Australia.
- Enright, N. J., and J. B. Fontaine. 2014. "Climate Change and the Management of Fire-Prone Vegetation in Southwest and Southeast Australia." *Geographical Research* 52: 34–44. https://doi.org/10.1111/1745-5871.12026.
- Enright, N. J., J. B. Fontaine, D. M. J. S. Bowman, R. A. Bradstock, and R. J. Williams. 2015. "Interval Squeeze: Altered Fire Regimes and Demographic Responses Interact to Threaten Woody Species Persistence as Climate Changes." *Frontiers in Ecology and the Environment* 13: 265– 272. https://doi.org/10.1890/140231.
- Enright, N. J., J. B. Fontaine, B. B. Lamont, B. P. Miller, and V. C. Westcott. 2014. "Resistance and Resilience to Changing Climate and Fire Regime Depend on Plant Functional Traits." *Journal of Ecology* 102: 1572–1581. https://doi.org/10.1111/1365-2745.12306.
- Enright, N. J., J. B. Fontaine, V. C. Westcott, J. C. Lade, and B. P. Miller. 2011. "Fire Interval Effects on Persistence of Resprouter Species in Mediterranean-Type Shrublands." *Plant Ecology* 212: 2071–2083. https://doi.org/10.1007/s11258-011-9970-7.
- Enright, N. J., and D. Goldblum. 1999. "Demography of a Non-Sprouting and Resprouting *Hakea* Species (Proteaceae) in Fire-Prone *Eucalyptus* Woodlands of Southeastern Australia in Relation to Stand Age, Drought and Disease." *Plant Ecology* 144: 71–82.
- Enright, N. J., D. A. Keith, M. F. Clarke, and B. P. Miller. 2012. "Fire Regimes in Australian Sclerophyllous Shrubby Ecosystems: Heathlands, Heathy Woodlands and Mallee Woodlands." In *Flammable Australia: Fire Regimes, Biodiversity and Ecosystems in a Changing World*, edited by R. A. Bradstock, A. M. Gill, and R. J. Williams, 215– 234. Collingwood, Australia: CSIRO Publishing.
- Enright, N. J., and B. B. Lamont. 1989. "Seed Banks, Fire Season, Safe Sites and Seedling Recruitment in Fire Co-Occurring Banksia Species." *Journal of Ecology* 77: 1111–1122. https://doi.org/10.2307/2260826.
- Enright, N. J., and B. B. Lamont. 1992. "Recruitment Variability in the Resprouting Shrub *Banksia Attenuata* and Non-Sprouting Congeners in the Northern Sandplain Heaths of Southwestern Australia." *Acta Oecologica* 13: 727–741.
- Enright, N. J., B. B. Lamont, and R. Marsula. 1996. "Canopy Seed Bank Dynamics and Optimum Fire Regime for the Highly Serotinous Shrub, *Banksia Hookeriana*." *Journal of Ecology* 84: 9–17.
- Enright, N. J., and I. Thomas. 2008. "Pre-European Fire Regimes in Australian Ecosystems." *Geography Compass* 2: 979–1011. https://doi.org/10.1111/j.1749-8198.2008.00126.x.
- Fairman, T. A., C. R. Nitschke, and L. T. Bennett. 2016. "Too Much, Too Soon? A Review of the Effects of Increasing Wildfire Frequency on Tree Mortality and Regeneration in Temperate Eucalypt Forests." *International Journal of Wildland Fire* 25: 831–848. https://doi.org/10.1071/WF15010.
- Field, D. L., M. Pickup, and S. C. H. Barrett. 2013. "Ecological Context and Metapopulation Dynamics Affect Sex-Ratio Variation Among Dioecious Plant Populations." *Annals of Botany* 111: 917–923. https://doi.org/10.1093/aob/mct040.
- Fisher, R., S. K. Wilson, T. M. Sin, A. C. Lee, and T. J. Langlois. 2018. "A Simple Function for Full-Subsets Multiple Regression in Ecology With R." *Ecology and Evolution* 8: 6104–6113. https://doi.org/10.1002/ece3.4134.
- Fontaine, J. 2022. *Yanchep Bushfire Analysis - Black Summer Final Report*. Melbourne, Australia: Bushfire and Natural Hazards CRC. https://www.naturalhazards.com.au/resources/publications/report/yanchep-bushfire-analysis.
- Fowler, W. M., R. J. Standish, N. J. Enright, and J. B. Fontaine. 2023. "Extinction Debt Varies in Two Threatened Mediterranean-Type Woodland Communities Undergoing Rapid Urbanisation." *Australian Journal of Botany* 71: 421–433.https://doi.org/10.1071/BT22134.
- Gallagher, R. V., S. Allen, B. D. E. Mackenzie, et al. 2021. "High Fire Frequency and the Impact of the 2019–2020 Megafires on Australian Plant Diversity." *Diversity and Distributions* 27: 1166–1179. https://doi.org/10.1111/ddi.13265.
- Gauthier, S., Y. Bergeron, and J.-P. Simon. 1993. "Cone Serotiny in Jack Pine: Ontogenetic, Positional, and Environmental Effects." *Canadian Journal of Forest Research* 23: 394–401. https://doi.org/10.1139/x93-057.
- Gauthier, S., Y. Bergeron, and J.-P. Simon. 1996. "Effects of Fire Regime on the Serotiny Level of Jack Pine." *Journal of Ecology* 84: 539–548. https://doi.org/10.2307/2261476.
- Gibson, N., B. Keighery, G. Keighery, A. Burbidge, and M. Lyon. 1994. "A Floristic Survey of the Southern Swan Coastal Plain." Unpublished report for the Australian Heritage Commission prepared by the Department of Conservation and Land Management and the Conservation Council of Western Australia (Inc.).
- Gill, A. M. 1981. "Coping With Fire." In *The Biology of Australian Plants*, edited by J. S. Pate and A. J. McComb, 65–87. Nedlands, Western Australia: University of Western Australia.
- Gill, A. M., and A. McMahon. 1986. "A Post-Fire Chronosequence of Cone, Follicle and Seed Production in *Banksia Ornata*." *Australian Journal of Botany* 34: 425–433.
- Gill, A. M., and A. O. Nicholls. 1989. "Monitoring Fire-Prone Flora in Reserves for Nature Conservation." In *Fire Management for Nature Conservation. Proceedings of a National Workshop*, edited by N. D. Burrows, W. L. McCaw, and G. Friend, 137–152. Perth, Western Australia, Busselton, Western Australia: Department of Conservation and Land Management.
- Gosper, C. R., B. P. Miller, R. V. Gallagher, et al. 2022. "Mapping Risk to Plant Populations From Short Fire Intervals via Relationships Between Maturation Period and Environmental Productivity." *Plant Ecology* 223: 769–787. https://doi.org/10.1007/s11258-022-01229-6.
- Gosper, C. R., S. M. Prober, and C. J. Yates. 2013. "Estimating Fire Interval Bounds Using Vital Attributes: Implications of Uncertainty and

*Austral Ecology*, 2025 | 19 of 21


<!-- PAGE BREAK -->

Among-Population Variability." *Ecological Applications* 23: 924–935. https://doi.org/10.1890/12-0621.1.
- Government of Western Australia. 2000. *Bush Forever - Keeping the Bush in the City*. Perth, WA: Department of Environmental Protection.
- Harrison, S. P., I. C. Prentice, K. J. Bloomfield, et al. 2021. "Understanding and Modelling Wildfire Regimes: An Ecological Perspective." *Environmental Research Letters* 16: 125008. https://doi.org/10.1088/1748-9326/ac39be.
- Harvey, J. M., A. J. M. Hopkins, M. A. Langley, C. R. Gosper, M. R. Williams, and C. J. Yates. 2017. "Long-Term Studies of Post-Fire Reproduction in an Australian Shrubland and Woodland." *Australian Journal of Botany* 65: 339–347. https://doi.org/10.1071/BT17011.
- He, T., and B. B. Lamont. 2018. "Baptism by Fire: The Pivotal Role of Ancient Conflagrations in Evolution of the Earth's Flora." *National Science Review* 5: 237–254. https://doi.org/10.1093/nsr/nwx041.
- Hobbs, R. J., and L. Atkins. 1990. "Fire Related Dynamics of a Banksia Woodland in South-Western Western Australia." *Australian Journal of Botany* 38: 97–110.https://doi.org/10.1071/BT9900097.
- Howard, T., N. Burrows, T. Smith, G. Daniel, and L. McCaw. 2020. "A Framework for Prioritising Prescribed Burning on Public Land in Western Australia." *International Journal of Wildland Fire* 29: 314–325. https://doi.org/10.1071/WF19029.
- Hurvich, C. M., and C.-L. Tsai. 1989. "Regression and Time Series Model Selection in Small Samples." *Biometrika* 76: 297–307. https://doi.org/10.1093/biomet/76.2.297.
- Jenkins, M. E., D. A. Morrison, and T. D. Auld. 2010. "Estimating Seed Bank Accumulation and Dynamics in Three Obligate-Seeder Proteaceae Species." *arXiv* preprint. https://doi.org/10.48550/arXiv.1001.4914.
- Johnston, T. R., W. D. Stock, and P. R. Mawson. 2016. "Foraging by Carnaby's Black-Cockatoo in Banksia Woodland on the Swan Coastal Plain, Western Australia." *Emu - Austral Ornithology* 116: 284–293. https://doi.org/10.1071/MU15080.
- Jones, M. W., J. T. Abatzoglou, S. Veraverbeke, et al. 2022. "Global and Regional Trends and Drivers of Fire Under Climate Change." *Reviews of Geophysics* 60: e2020RG000726. https://doi.org/10.1029/2020RG000726.
- Keeley, J. E., C. J. Fotheringham, and M. Baer-Keeley. 2006. "Demographic Patterns of Postfire Regeneration in Mediterranean-Climate Shrubland of California." *Ecological Monographs* 76: 235–255. https://doi.org/10.1890/0012-9615(2006)076[0235:DPOPRI]2.0.CO;2.
- Keeley, J. E., G. Ne'eman, and C. J. Fotheringham. 1999. "Immaturity Risk in a Fire-Dependent Pine." *Journal of Mediterranean Ecology* 1: 41–48.
- Keeley, J. E., J. G. Pausas, P. W. Rundel, W. J. Bond, and R. A. Bradstock. 2011. "Fire as an Evolutionary Pressure Shaping Plant Traits." *Trends in Plant Science* 16: 406–411. https://doi.org/10.1016/j.tplants.2011.04.002.
- Kraaij, T., R. M. Cowling, B. W. Van Wilgen, and A. Schutte-Vlok. 2013. "Proteaceae Juvenile Periods and Post-Fire Recruitment as Indicators of Minimum Fire Return Interval in Eastern Coastal Fynbos." *Applied Vegetation Science* 16: 84–94. https://doi.org/10.1111/j.1654-109X.2012.01209.x.
- Lamont, B. B. 2022. "Historical Links Between Climate and Fire on Species Dispersion and Trait Evolution." *Plant Ecology* 223: 711–732. https://doi.org/10.1007/s11258-022-01232-x.
- Le Breton, T. D., M. B. Lyons, R. H. Nolan, T. Penman, G. J. Williamson, and M. K. Ooi. 2022. "Megafire-Induced Interval Squeeze Threatens Vegetation at Landscape Scales." *Frontiers in Ecology and the Environment* 20: 327–334.https://doi.org/10.1002/fee.2482.
- Lullfitz, A., C. Pettersen, R. Reynolds, et al. 2020. "The Noongar of South-Western Australia: A Case Study of Long-Term Biodiversity Conservation in a Matrix of Old and Young Landscapes." *Biological Journal of the Linnean Society* 133: 432–448. https://doi.org/10.1093/biolinnean/blaa097.
- Matusick, G., K. X. Ruthrof, J. Kala, N. C. Brouwers, D. D. Breshears, and G. E. S. J. Hardy. 2018. "Chronic Historical Drought Legacy Exacerbates Tree Mortality and Crown Dieback During Acute Heatwave-Compounded Drought." *Environmental Research Letters* 13: 95002. https://doi.org/10.1088/1748-9326/aad8cb.
- McCaw, L. 2008. "Variation in Age to First Flowering and Fruiting of *Banksia Baxteri* and *Banksia Coccinea* at the Stirling Range, South-Western Australia." *Journal of the Royal Society of Western Australia* 91: 269–273.
- Miller, R., N. Enright, D. Merritt, B. Miller, and J. Fontaine. 2024. "Post-Fire Plant Reproductive Trajectories Under Varying Rainfall and Herbivory in Banksia Woodlands." Zenodo.
- Miller, R. G., N. J. Enright, J. B. Fontaine, D. J. Merritt, and B. P. Miller. 2024. "Plant Life-History Data as Evidence of an Historical Mixed-Severity Fire Regime in Banksia Woodlands." *Australian Journal of Botany* 72: 1–19. https://doi.org/10.1071/BT23098.
- Monk, D., J. Pate, and W. Loneragan. 1981. "Biology of *Acacia pulchella* R.Br. With Special Reference to Symbiotic Nitrogen Fixation." *Australian Journal of Botany* 29: 579–592. https://doi.org/10.1071/BT9810579.
- Morgan, J. W., M. A. McCarthy, and E. Willocks. 2021. "Does Intraspecific Variation in Demography Have Implications for Fire Management of an Obligate-Seeder Shrub Across Its Geographic Range?" *Austral Ecology* 46: 315–323. https://doi.org/10.1111/aec.12981.
- Moudrý, V., A. F. Cord, L. Gábor, et al. 2023. "Vegetation Structure Derived From Airborne Laser Scanning to Assess Species Distribution and Habitat Suitability: The Way Forward." *Diversity and Distributions* 29: 39–50. https://doi.org/10.1111/ddi.13644.
- Muir, A. M., P. A. Vesk, and G. Hepworth. 2014. "Reproductive Trajectories Over Decadal Time-Spans After Fire for Eight Obligate-Seeder Shrub Species in South-Eastern Australia." *Australian Journal of Botany* 62: 369–378. https://doi.org/10.1071/BT14117.
- Murphy, B. P., R. A. Bradstock, M. M. Boer, et al. 2013. "Fire Regimes of Australia: A Pyrogeographic Model System." *Journal of Biogeography* 40: 1048–1058. https://doi.org/10.1111/jbi.12065.
- Natural Area Consulting. 2012. "Star Swamp Bushland Reserve Environmental Management Plan." Unpublished report prepared for the City of Stirling, Whiteman, Western Australia.
- Obeso, J. R. 2002. "The Costs of Reproduction in Plants." *New Phytologist* 155: 321–348. https://doi.org/10.1046/j.1469-8137.2002.00477.x.
- Pausas, J. G., and J. E. Keeley. 2014. "Evolutionary Ecology of Resprouting and Seeding in Fire-Prone Ecosystems." *New Phytologist* 204: 55–65. https://doi.org/10.1111/nph.12921.
- Plucinski, M. P. 2014. "The Timing of Vegetation Fire Occurrence in a Human Landscape." *Fire Safety Journal* 67: 42–52. https://doi.org/10.1016/j.firesaf.2014.05.012.
- Prior, L. D., W. L. McCaw, P. F. Grierson, B. P. Murphy, and D. M. J. S. Bowman. 2011. "Population Structures of the Widespread Australian Conifer *Callitris columellaris* are a Bio-Indicator of Continental Environmental Change." *Forest Ecology and Management* 262: 252–262. https://doi.org/10.1016/j.foreco.2011.03.030.
- R Core Team. 2020. *R: A Language and Environment for Statistical Computing*. Vienna, Austria: R Foundation for Statistical Computing.
- Ramalho, C. E., E. Laliberté, P. Poot, and R. J. Hobbs. 2014. "Complex Effects of Fragmentation on Remnant Woodland Plant Communities of a Rapidly Urbanizing Biodiversity Hotspot." *Ecology* 95: 2466–2478. https://doi.org/10.1890/13-1239.1.
- Ritchie, A. L., L. N. Svejcar, B. M. Ayre, et al. 2021. "A Threatened Ecological Community: Research Advances and Priorities for Banksia

20 of 21 | *Austral Ecology*, 2025


<!-- PAGE BREAK -->

Woodlands." *Australian Journal of Botany* 69: 53–84. https://doi.org/10.1071/BT20089.
- Rodrigues, U., A. Lullfitz, L. Coyne, et al. 2022. "Indigenous Knowledge, Aspiration, and Potential Application in Contemporary Fire Mitigation in Southwest Australia." *Human Ecology* 50: 963–980. https://doi.org/10.1007/s10745-022-00359-9.
- Ruthrof, K. X., J. B. Fontaine, D. D. Breshears, J. P. Field, and C. D. Allen. 2021. "Extreme Events Trigger Terrestrial and Marine Ecosystem Collapses in the Southwestern USA and Southwestern Australia." In *Ecosystem Collapse and Climate Change*, edited by J. G. Canadell and R. B. Jackson, 187–217. Cham: Springer International Publishing.
- Schwilk, D. W., and D. D. Ackerly. 2001. "Flammability and Serotiny as Strategies: Correlated Evolution in Pines." *Oikos* 94: 326–336. https://doi.org/10.1034/j.1600-0706.2001.940213.x.
- Symonds, M. R. E., and A. Moussalli. 2011. "A Brief Guide to Model Selection, Multimodel Inference and Model Averaging in Behavioural Ecology Using Akaike's Information Criterion." *Behavioral Ecology and Sociobiology* 65: 13–21. https://doi.org/10.1007/s00265-010-1037-6.
- Tangney, R., R. G. Miller, J. B. Fontaine, W. P. Veber, K. X. Ruthrof, and B. P. Miller. 2022. "Vegetation Structure and Fuel Dynamics in Fire-Prone, Mediterranean-Type Banksia Woodlands." *Forest Ecology and Management* 505: 119891. https://doi.org/10.1016/j.foreco.2021.119891.
- Tonnabel, J., T. J. M. Van Dooren, J. Midgley, et al. 2012. "Optimal Resource Allocation in a Serotinous Non-Resprouting Plant Species Under Different Fire Regimes." *Journal of Ecology* 100: 1464–1474. https://doi.org/10.1111/j.1365-2745.2012.02023.x.
- Treurnicht, M., J. Pagel, K. J. Esler, et al. 2016. "Environmental Drivers of Demographic Variation Across the Global Geographical Range of 26 Plant Species." *Journal of Ecology* 104: 331–342. https://doi.org/10.1111/1365-2745.12508.
- Turner, B. L., P. E. Hayes, and E. Laliberté. 2018. "A Climosequence of Chronosequences in Southwestern Australia." *European Journal of Soil Science* 69: 69–85.https://doi.org/10.1111/ejss.12507.
- Turner, R. S., O. J. D. Lasne, K. N. Youngentob, S. Shokirov, H. L. Osmond, and L. E. B. Kruuk. 2023. "Use of Airborne Laser Scanning to Assess Effects of Understorey Vegetation Structure on Nest-Site Selection and Breeding Performance in an Australian Passerine Bird." *Remote Sensing in Ecology and Conservation* 9: 787–802. https://doi.org/10.1002/rse2.342.
- Valentine, L. E., R. Fisher, B. A. Wilson, et al. 2014. "Time Since Fire Influences Food Resources for an Endangered Species, Carnaby's Cockatoo, in a Fire-Prone Landscape." *Biological Conservation* 175: 1–9. https://doi.org/10.1016/j.biocon.2014.04.006.
- von Takach Dukai, B., D. B. Lindenmayer, and S. C. Banks. 2018. "Environmental Influences on Growth and Reproductive Maturation of a Keystone Forest Tree: Implications for Obligate Seeder Susceptibility to Frequent Fire." *Forest Ecology and Management* 411: 108–119. https://doi.org/10.1016/j.foreco.2018.01.014.
- Western Australian Herbarium. 1998. "Florabase—the Western Australian Flora." [Online]. Accessed October 13, 2022. https://florabase.dbca.wa.gov.au/.
- Whelan, R. J., and D. J. Ayre. 2020. "Long Inter-Fire Intervals Do Not Guarantee a Large Seed Bank in a Serotinous Shrub (*Banksia spinulosa* Sm.)." *Journal of Ecology* 108: 1690–1702. https://doi.org/10.1111/1365-2745.13357.
- Wilson, B. A., J. Kuehs, L. E. Valentine, T. Sonneman, and K. M. Wolfe. 2014. "Guidelines for Ecological Burning Regimes in Mediterranean Ecosystems: A Case Study in Banksia Woodlands in Western Australia." *Pacific Conservation Biology* 20: 57–74. https://doi.org/10.1071/PC140057.
- Wood, S. N. 2017. *Generalised Additive Models: An Introduction With R*. New York, USA: Chapman and Hall/CRC.
- Wooller, S. J., R. D. Wooller, and K. L. Brown. 2002. "Regeneration by Three Species of Banksia on the South Coast of Western Australia in Relation to Fire Interval." *Australian Journal of Botany* 50: 311–317. https://doi.org/10.1071/BT01078.
- Zammit, C., and M. Westoby. 1987. "Population Structure and Reproductive Status of Two Banksia Shrubs at Various Times After Fire." *Vegetatio* 70: 11–20. https://doi.org/10.1007/BF00040753.

#### **Supporting Information**

Additional supporting information can be found online in the Supporting Information section.

*Austral Ecology*, 2025 | 21 of 21

<!-- md_opt: model=claude-opus-5-5; date=2026-10-07; md_sha256=f8968e673623038e9b0b0b880513dd676b7d79019272e51309f7023afc1de74d; pdf_sha256=80a2d6bc021b12a259e8565a22395f36d0c394f860f3f4f9bc8a3225384037b7; pdf_pages=21; fixes=120 (Tables 1-6 rebuilt as pipe tables (rows split by wrapped names and multi-line headers fixed; Table 1 footnote added); ellipsoid equation moved to its place and rebuilt; narrow no-break spaces normalised; internal page links and split URL links removed; author superscripts; units spaced and superscripted; tables and figure captions placed in PDF order; Fig. 1 map labels added; page footers added; misplaced Wooller reference restored; 104 references split one per item); unresolved=none -->
