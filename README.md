[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-7f7980b617ed060a017424585567c406b6ee15c891e84e1186181d67ecf80aa0.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=10872673)
# final-project
I would like to scrape Prince George's County food inspection data weekly and create a news app that people can check to see what food service places in their city has been having the most non-compliance or critical inspection results recently.

Here is a link to the data: https://data.princegeorgescountymd.gov/Health/Food-Inspection/umjn-t2iz/data

Something about this data is that it is organized by both restuarant/address and also by city and zip code. While county or zip code is a helpful way to search for food service locations in an area relevant to a user, I don't think it's fair to think of it as county level when doing analyses. For example, if on a heat map, College Park has the most non-compliance or critical inspection results, that isn't saying anything about College Park as a whole. That doesn't matter. What matters is that (hypothetically) Xfinity center is responsible for 80% of critical inspection results. Or that (hypothetically) all of those results are becase of improper handwashing stations. That's what I'm trying to figure out: How can I organize this to be easily searchable and relevant while also making sure I'm getting in the most important analyses?

I do think it would be helpful to have a page for every neighborhood because that would be usable for residents. I'm just trying to figuer out how to balance resident/user curiosity while also telling stories I think are important in the data.

I guess I just have to figure out what the biggest story in this data is and center the app around that. 

How are you defining a unique record: I want every inspection to have a unique record

What is the schedule of data updates: I would like this to update weekly I think. But also, I would like to store the data in yearly csvs rather than have all updates go into one csv. 

How will those updates be done - incrementally or wholesale: I want the updates and the unique IDs to be wholesale, not incremental. This is because I want to be able to combine the yearly csvs to do analyses on this data over years.

Are there parts of the data that you would not display or make searchable: I'm nervous about neighborhood/zip code level data being misinterpretted. So maybe I will allow people to look at things in specific neighborhoods but I'll do no analyses on a neighborhood /zipcode level. 

