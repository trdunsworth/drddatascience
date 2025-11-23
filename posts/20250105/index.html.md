---
title: "So where does the data take me?"
author: "Tony Dunsworth"
date: "2025-01-05"
categories: [news, analytics, 911]
---

So, over the _dead_ week between Christmas and New Year's Day, I started working on a new reporting template. The goal is to create a new archive of weekly and monthly reports for my 911 centre in a [Quarto](https://quarto.org) blog format. Currently, I'm working on a sample report for management to see what the audience will like. I also want to use the sample to illustrate what needs to happen with the reports. 

An example of this is in our datasets, we trap the time stamps at various points in the life of the service call. Some of these include the start of the call, when it was available to be dispatched, when the first units were assigned, and when the call was disconnected. In the data cleaning process, we have identified some of the deltas between time stamps come out negative. Obviously, you **cannot** dispatch a call before it enters the queue. This means that when we find them, we have to address them in some fashion. 