---
title: "Why is Staffing So Hard?"
author: "Tony Dunsworth, Ph.D."
date: "2026-03-13"
categories: [data science, analyses, hosting, thoughts]
execute:
  eval: false
---

## Is staffing hard?

During a day when I didn't feel so good, I saw an interesting poll question on LinkedIn. The poster asked if PSAPs were considering predictive staffing tools. Since I've been working on the same thing in different ways for a while, I reached out to the poster and we're going to meet in the near future to discuss how they are looking to approach the problem versus how I've been approaching it. So, I thought I would share some of my thoughts on how to approach this because I know I've looked at the issue differently than most people. It's always good to get another perspective and see how that might influence my own work.

Yes, the short answer is staffing is hard. There are several non-trivial variables that have to be addressed to estimate how many people you need to staff any centre, let alone a PSAP. Since many centres and consultants use some version of the Erlang family, I started using that as a framework for how to consider the problem. For the Erlang-C model, you need to estimate the arrival rate of calls, the average handling time of calls, and the acceptable level of service (e.g., percentage of calls answered within a certain time frame). I did my dissertation on the first part of that, estimating the arrival rate of calls. 

### Arrival Rates - Forecasting

How many calls do you get? How many do you expect to receive in the future? These are questions that exist for a PSAP, but most centres do not know how to write a forecast. The standard suggestion is to take your most recent data and add a reasonable percentage, between 3 and 5 percent, and report that as the forecasted call volume. After that, you assume the busiest hour is the base for the day and account for your shifts.

The problem with this is that it creates a static forecast that doesn't address many other factors. For me, outside of the D.C. metro area, do Washington Commanders games have an impact on call volumes in thed suburbs? What impact does the weather have on call volumes? Do certain types of calls increase during certain times of the year? Are there any trends in the data that suggest call volumes are increasing or decreasing over time? These are all questions that can be addressed with a more dynamic forecasting model that takes into account historical data, seasonal trends, and other relevant factors. The biggest challenge in that is that most centres 