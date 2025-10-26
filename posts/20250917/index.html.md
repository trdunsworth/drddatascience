---
title: "Stochasticity in Time-Series, Dissertation part 1"
author: "Tony Dunsworth, Ph.D."
date: "2025-09-18"
categories: [data science, analyses, data issues]
execute: 
  eval: false
---

## Background

It's been nearly a year since I defended my dissertation. In that time, I've found that people are intrested in knowing what it's about until I try to explain it, then they feel that they don't understand it and the discussions get lost. So, while I was playing FreeCell solitaire this morning, I thought of an experiment that could help me work with forecasting stochastic processes, including adding conformal predictions to the mixture. Part of it is because I want to keep my data science skills sharp. I also realized that this would work well as a better explanation of my dissertation also. So my plan is to split everything into three parts. This part is going to discuss stochasticity and how it plays a part of forecasting. The second part will be focused low-code and zero-shot forecasting models. The final part will be marrying these together, like I did in my dissertation, for 9-1-1 centres and how my dissertation can serve as a foundation for future research on both forecasting polystochastic processes and finding even better ways to address forecasting in centers and why it will be important.

### Simple Stochasticity

This all started with a weird thought playing FreeCell. When I started playing, years ago, I was happy anytime that I had scores under 100 moves. Now, the more I've played and improved, I am annoyed whenever I have a count above 90. That certainly is a big difference. It made me wonder, had I thought of it earlier, could I have built a dataset that charted my progress and then forecast things such as which days are going to be more challenging?

Ultimately, this is a simple stochastic process. The "mother-ship" selects a deal at random each day. There are a finite number of choices, according to a quick search, there are $1.75^{64}$ possibilities. The program, as part of the trivia, points out that some deals are unwinnable. So the rules that the "mother-ship" must follow also includes, for the daily challenges, the exclusion of unwinnable deals. The program also attaches the daily deal number to the day it is presented, so even if I don't complete the daily deal, I'm guaranteed to see the same daily deal that my wife or other players saw the same day. This introduces the stochastic element through the determination of limiting factors. If the daily deal were truly random, then unwinnable deals would be possible and the deal offered would change when presented to the player depending on when it was accessed.

My analytical interest, had I started earlier would be to use my prior results to see how my play has improved over time and see if I can forecast how well I can do in the future. I also am curious to see if there is an underlying pattern of when really challenging deals are presented to players. I could correlate my wife's results with mine to see if a second pattern emerges. This yields the possibility of two separate types of stochastic forecasts. It also allows me to create pattern recognition analyses that may shed some insight into the algorithm the company employs to select the deal for each day. This works well because my wife and I approach the puzzles in different ways, so if something is challenging to both of our styles, then it's likely that is really difficult. If it is easy for one of us, the it might not be so difficult. Is it simply a random number generator with some values removed? Or are there other parameters that are added which restrict the lists enough to ensure a player doesn't perceive repeated deals or perhaps you can ascertain the size of the potential pool of deals.

### Double Stochasticity

This is most generally found in many commercial call centres. Most accurately, it can be described as a [Cox Process](https://www.sciencedirect.com/topics/mathematics/cox-process). In this scenario, we have a number of calls arriving at a defined rate, but each call is randomly placed and any one call does not impact or effect the next call. The best example to describe a Cox Process in a 9-1-1 centre is that there are a random non-negative number of calls that arrive per time unit, typically an hour. Additionally, the decision of any one individual is neither influenced by or influences the decision of another individual to call the centre.

#### The next Stochastic level

Additionally, because of the nature of Primary {{< acr PSAP >}}s, there is an additional level of stochasticity regarding how the call for service arrives to the centre. Calls may arrive from 9-1-1 telephone lines, administrative, non-emergency, lines, {{< acr SMS >}} text messages, {{< acr TDD >}}/{{< acr TTY >}} devices, radio communications from officers, or even public walk-ups for centres that have a window for the public, like the county that I live in. This additional stochasticity can magnify the challenges for both forecasting and queue development. So, when we're trying to build models to describe this behaviour, we have to account for the additional factors that are present.

### Application to the Dissertation

In my dissertation, I wanted to examine how to forecast inbound call volumes for PSAPs because it's the first stage in a larger body of work that I hope to complete. I want to find a forecasting model that works