---
title: "Cleaning in the Query"
author: "Tony Dunsworth, Ph.D."
date: "2025-08-31"
categories: [data science, analyses, data issues]
execute: 
  eval: false
---

When I started actively working in data science, like everyone else, I heard the old maxim that a data scientist spends about 80% of their time cleaning data. Well, I can report that in many cases, that's true. I'm currently facing a lot of that right now in building a new dataset for some new reports and dashboards that I'm designing. I'm starting the data cleaning process in the [SQL](https://www.ibm.com/think/topics/structured-query-language) statement. I believe that it's a lot faster in the end. Once I have the query where I want it, then many of the following steps are pretty easy. 

For this dataset, I have three tables from which I will pull data. The first is the master incident table. This contains most of the data that I need for my reports. The second is an extension to the first table. I only want one column from that table and, honestly, I don't know how often I would use it. However, for a few types of analyses, it could be very handy. The other table that I want to use is a log of activities in a call and the details associated with each activity. Most of the data is fairly straightforward. Some of the derived data, however, isn't as straight forward as I would like. That data consists of the deltas between timestamps. We use those for operational assessment. 

One of the main reasons that I want to do most of my cleaning in the SQL query itself is that I can control the output and standardize it easier. I am more confident with SQL at this stage because I've been writing SQL for nearly 20 years in some form. Having written a lot of queries and them progressively more complex and detailed, it feel more natural for me. I admit, I believe that every data scientist should be fluent in writing SQL queries of all types. I also believe that cleaning in the query will save me a considerable amount of time when I'm building my reports and dashboards. That doesn't mean that there aren't challenges in cleaning the data before it goes into my dataset. The rest of this post will discuss some of those issues. 


When I started writing the first iteration of this query, and I'm currently on my seventh iteration of it, I started then and now with two columns as my foundations. The first is the incident number. I can designate it an ID field in my dataset. 
