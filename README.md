This repository was created for the creation and upkeep of the Streamlit interactive dashboard for the DSSI '26 Chicago 311 Project.

                                            Predicting Chicago 311 Service Requests
Our Partner:

The City of Chicago. Chicago's 311 system is the front door for non-emergency city services: residents call, use the web portal, or use the CHI311 app to report potholes, broken street lights, graffiti, rodents, missed garbage pickups, tree issues, and dozens of other concerns. Requests are routed to the responsible departments (Streets and Sanitation, CDOT, Water Management, Buildings, Animal Care and Control, and others), which deliver the actual services. The City publishes every request as open data.

Our Motivation:

311 demand is seasonal and uneven. Potholes spike after winter freeze-thaw cycles, weeds and yard-waste requests climb in summer, rodent and tree issues follow their own rhythms, and overall volume shifts year to year. Because the departments that fulfill these requests have finite crews, equipment, and budgets, the City needs to plan resources ahead of time rather than react after backlogs form.
Just as important is where demand falls. Chicago's neighborhoods differ widely in the mix and volume of requests they generate. Anticipating demand at the local level helps ensure resources are allocated equitably so that no geography or neighborhood gets left behind — turning 311 from a reactive queue into a forward-looking planning tool.


Provided materials:

A monthly panel of 311 request counts derived from the City's public data. Each row is a place-and-month — a community area in a given month (plus citywide total rows) — with one column per request type giving how many of that type were created there that month. It covers 2019–2025 for 55 of the most common request types across Chicago's 77 community areas (stable, official neighborhood units).


The task:

Forecast future monthly 311 request volume from its recent history. The data gives you everything known up to a given month; you predict what comes next.

There are two goals, in order of difficulty.

**Goal 1** — forecast citywide demand
Predict the citywide monthly request volume (the COMMUNITY_AREA == 0 rows), type by type. This is the core forecasting problem — one time series per request type — and where everyone should begin. Get a model working, validated, and beating a simple baseline here before moving on.

**Goal 2** — forecast demand by community area
Once citywide forecasting works, predict demand for each of the 77 community areas (the COMMUNITY_AREA 1–77 rows). This is harder because:

it's many more, noisier series (77 areas × types instead of one citywide series per type), and small areas have low, choppy counts;
demand patterns differ by neighborhood, so a single model may not transfer;
it's the level that matters most for equitable planning — making sure resources reach the places that will need them.
