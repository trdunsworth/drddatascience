---
title: "How to Start - Asking the First Question"
author: "Tony Dunsworth, Ph.D."
date: "2025-04-12"
categories: [examples, analyses]
execute: 
  eval: false
---




I recently wrote about a presentation that I gave at [Randolph Macon College](https://rmc.edu) concerning using data analyses in 9-1-1 centres. During the Q&A section, someone asked me how I would recommend getting started. My answer, then and now, is pick a question and dive into that and new questions will start coming. 

I thought, perhaps, I should come up with an example of what I mean. In our centre, our medical director has requested that we do quality checks on every cardiac arrest call that we receive. So, here is the starting question: what can we learn about the cardiac arrest calls in the city? With that as the opening question, the first step is collecting the data. To start, I plan on collecting four datasets. I can create all of them using SQL. Since I work on SQL Server or T-SQL flavoured databases, the query, for our dispatch software's databases looks something like this:




::: {.cell}

```{.sql .cell-code}
USE Reporting_System;
GO

DECLARE @time1 DATETIME2;

SET @time1 = '2025-01-01 00:00:00.0000000';

-- This query will retrieve all cardiac arrest calls from this year.

SELECT Master_Incident_Number,
    Response_Date,
    Address,
    Latitude,
    Longitude,
    Time_PhonePickUp,
    Time_FirstCallTakingKeystroke,
    Time_CallEnteredQueue,
    Time_First_Unit_Assigned,
    Time_CallTakingComplete
FROM Response_Master_Incident
WHERE Response_Date > @time1
    AND Problem LIKE 'CARDIAC ARREST%'
    AND Master_Incident_Number != ''
ORDER BY Response_Date;

-- This query will retrieve  all cardiac arrest calls from the past 1, 3, & 5 years

SELECT Master_Incident_Number,
    Response_Date,
    Address,
    Latitude,
    Longitude,
    Time_PhonePickUp,
    Time_FirstCallTakingKeystroke,
    Time_CallEnteredQueue,
    Time_First_Unit_Assigned,
    Time_CallTakingComplete
FROM Response_Master_Incident
WHERE Response_Date BETWEEN DATEADD(YEAR, -1, @time1) AND @time1
    AND Problem LIKE 'CARDIAC ARREST%'
    AND Master_Incident_Number != ''
ORDER BY Response_Date;
```
:::




These queries will generate the four datasets that I would want for the full analysis. I would save the output to csv files and name them cardiac_arrest_cy.csv, cardiac_arrest_1y.csv, cardiac_arrest_3y.csv, and cardiac_arrest_5y.csv. 

Personally, I want to start with current data so I can get a feel for the data. To do some of my work, I would add some columns to the dataset. I can do it programmatically or through the SQL Query. I prefer to do it in the query like so:




::: {.cell}

```{.sql .cell-code}
USE Reporting_System;
GO

DECLARE @time1 DATETIME2;

SET @time1 '2025-01-01';

-- This query will retrieve all cardiac arrest calls from this year

SELECT Master_Incident_Number AS [Call_ID],
    Response_Date AS [Start_Time],
    Address,
    Latitude,
    Longitude,
    Time_PhonePickUp AS [Phone_Start],
    Time_FirstCallTakingKeystroke AS [Keybiard_Start],
    Time_CallEnteredQueue AS [Dispatchable],
    Time_First_Unit_Assigned AS [Dispatched],
    Time_CallTakingComplete AS [Phone_Stop],
    DATEDIFF(SECOND, Response_Date, Time_CallEnteredQueue) AS Call_Entry_Time,
    DATEDIFF(SECOND, Time_CallEnteredQueue, Time_First_Unit_Assigned) AS Call_Queue_Time,
    DATEDIFF(SECOND, Response_Date, Time_CallTakingComplete) AS Call_Processing_Time
FROM Response_Master_Incident
WHERE Response_Date > @time1
  AND  Problem = 'CARDIAC ARREST'
ORDER BY Response_Date;
```
:::




This gives us a columns of elapsed times to determine how long it took us to make the call dispatchable, how long it took to dispatch the call to the first unit, and how long we spent on the phone with the caller.

Now we load the dataset, for this I'm using the R programming language. We can do it in Python as well, but I've been working with R a lot longer. 




::: {.cell}

```{.r .cell-code}
df_cacy <- read.csv("cardiac_arrest_cy.csv", header = TRUE, sep = ",", stringsAsFactors = TRUE)
```
:::




Now that we have the dataset loaded, we can go through the dataset to clean it up. Most of these calls *should* have all of the components that we've selected. If there are things missing, then we can go in and clean those up to remove missing data points. For this dataset, this is the code I would use to clean up any missing values:




::: {.cell}

```{.r .cell-code}
# Check the data
str(df_cacy)
nrow(df_cacy)
head(df_cacy, n = 10)
colnames(df_cacy)
spec(df_cacy)

# Use the naniar package to check for missing values. This creates a graphical view of the missing data
gg_miss_var(df_cacy)

# Use this code to create a quick table of those missing value counts
apply(X = is.na(df_cacy), MARGIN = 2, FUN = sum)

# This code replaces missing values with an entry
df_cacy$Call_ID <- tidyr::replace_na(df_cacy$Call_ID, "NOT RECORDED")
df_cacy$Start_Time <- tidyr::replace_na(df_cacy$Start_Time, "1970-01-01 00:00:00") # This is the Unix Time start value
df_cacy$Address <- tidyr::replace_na(df_cacy$Address, "NOT RECORDED")
df_cacy$Latitude <- tidyr::replace_na(df_cacy$Latitude, 388048)
df_cacy$Longitude <- tidyr::replace_na(df_cacy$Longitude, 770469)
df_cacy$Ready_To_Dispatch <- tidyr::replace_na(df_cacy$Ready_To_Dispatch, "1970-01-01 00:00:00")
df_cacy$First_Unit_Assigned <- tidyr::replace_na(df_cacy$First_Unit_Assigned, "1970-01-01 00:00:00")
df_cacy$Stop_Time <- tidyr::replace_na(df_cacy$Stop_Time, "1970-01-01 00:00:00")
df_cacy$Call_Entry_Time <- tidyr::replace_na(df_cacy$Call_Entry_Time, -1) # This makes any elapsed time that is missing a value we can eliminate in the next cleaning step.
df_cacy$Call_Queue_Time <- tidyr::replace_na(df_cacy$Call_Queue_Time, -1)
df_cacy$Call_Processing_Time <- tidyr::replace_na(df_cacy$Call_Processing_Time, -1)
```
:::




This should clean the data of any missing values. This is also the start of new questions. How much data is missing? Where is it missing at? Finally, why is the data missing? Most of the data is likely not missing at random. I expect that most of the missing data comes from calls that were not completed. When the other three benchmark datasets are compared, we can see how the percentage of calls missing data compares over 1, 3, and 5 years. If the comparisons are in line, then you move on, if they aren't, there's question number 4, what's different now?

The next thing that I check for would be negative values in the final three columns, Call_Entry_Time, Call_Queue_Time, and Call_Processing_Time. These varables represent the elapsed times between events in the centre that measure our telecommunicators actions. If we see any values in these variables that are negative, then we know, instantly, that the calls have been closed then reopened. The fifth questions becomes why are some calls being reopened? My recommendation is to take those calls, and the calls with missing values if they can be proven to be full calls, and create a new dataset. That list can be exported to an Excel spreadsheet and used for future investigation. This is the first potential project that has been generated by this work.


Depending on the number of calls that exist in this dataset, I would remove the same calls from my master datasets and continue with the research without them. My benchmark is no more than 5 percent of the calls removed. If it appears that we're going to go over 5 percent, we have another question, why are there so many calls with these defects? 

*In a quick glance after running the queries, I found that none of my entries for this year had any missing data and that historical data had missing data in the Time_First_Unit_Assigned column. These would be calls that were received, but never ran for whatever reason. This is what I expected to see in real data.*

Once the call list has been cleaned, the next step that I recommend is to look at individual variables. I prefer to start with the numeric variables and create a summary. I have a custom summary that I use for my analyses. I feel like it serves my needs and gives me some insights that I will confirm when I create visuals for others. That summary can be found here:




::: {.cell}

```{.r .cell-code}
# Custom summary function
custom_summary <- function(column) {
  c(
    Minimum = round(min(column, na.rm = TRUE), 2),
    Mean = round(mean(column, na.rm = TRUE), 2),
    Median = round(median(column, na.rm = TRUE), 2),
    Q1 = round(quantile(column, 0.25, na.rm = TRUE), 2),
    Q3 = round(quantile(column, 0.75, na.rm = TRUE), 2),
    P90th = round(quantile(column, 0.90. na.rm = TRUE), 2),
    Maximum = round(max(column, na.rm = TRUE), 2),
    Std_Dev = round(sd(column, na.rm = TRUE), 2),
    Variance = round(var(column, na.rm = TRUE), 2),
    Skewness = round(e1071::skewness(column, na.rm = TRUE), 2),
    Kurtosis = round(e1071::kurtosis(column, na.rm = TRUE), 2)
  )
}
```
:::




This custom summary gives me a very good picture of the data prior to creating any visualizations. The minimum and maximum values give me a good range for the data, while the mean and median paint a picture of the central tendencies of the data. The standard deviation and variance can give me some information about the overall spread of the data, the skewness and kurtosis values give me the shape of the distribution, and the Q1 and Q3 values suggest the boundaries for outlier identification. All of this together now gives me a good numeric '*visualization*' of the data and now I can focus on asking new questions of the numeric data.

Additionally, I will want to break the Response_Date column into some constituent components such as the day of the week, the day of the year, the hour, and the week number. These will allow me to create different pictures. To get those, I typically generate them from the SQL Query. That updated query would look like this:




::: {.cell}

```{.sql .cell-code}
SELECT Master_Incident_Number AS [Call_ID],
    Response_Date AS [Start_Time],
    CAST(DATEPART(WEEK, Response_Date) AS NVARCHAR(2)) AS [WeekNo],
    UPPER(FORMAT(Response_Date, 'ddd')) AS [DOW],
    CAST(DATEPART(DAY, Response_Date) AS NVARCHAR(2)) AS [Day],
    CAST(DATEPART(Hour, Response_Date) AS NVARCHAR(2)) AS [Hour],
    Address,
    Time_PhonePickUp AS [Phone_Start],
    Time_FirstCallTakingKeystroke AS [Keybiard_Start],
    Time_CallEnteredQueue AS [Dispatchable],
    Time_First_Unit_Assigned AS [Dispatched],
    Time_CallTakingComplete AS [Phone_Stop],
  DATEDIFF(SECOND, Response_Date, Time_CallEnteredQueue) AS Call_Entry_Time,
  DATEDIFF(SECOND, Time_CallEnteredQueue, Time_First_Unit_Assigned) AS Call_Queue_Time,
  DATEDIFF(SECOND, Response_Date, Time_CallTakingComplete) AS Call_Processing_Time
FROM Response_Master_Incident
WHERE Response_Date > @time1
AND  Problem = 'CARDIAC ARREST'
ORDER BY Response_Date;
```
:::




or you can do it programmatically in R like this:




::: {.cell}

```{.r .cell-code}
# Function to extract day of week (DDD), week number, year, and hour
# This also uses the lubridate library
extract_datetime_features <- function(df_cacy, Response_Date) {
  df %>%
    mutate(
      day_of_week_ddd = wday(!!sym(Response_Date), label = TRUE),
      week_number = isoweek(!!sym(Response_Date)),
      year_number = year(!!sym(Response_Date)),
      hour_of_day = hour(!!sym(Response_Date))
    )
}
```
:::




Either way, thsis allows us new data to generate new questions and answers. Is there a specific day of the week that has more events than others? Is there a certain time of the year that has more events? Are there specific hours out of the day that see more events? These questions could impact staffing, training, and could present opportunities to partner with the local hospitals to create better synergies for positive patient experiences and outcomes. So we're now at 8 questions from our starting point as well as a couple of different projects. And when you take a look at the summaries for each of the elapsed times and compare them to the 1, 3, and 5 year summaries, you can not only see trends but find new questions when doing the comparisons to those benchmarks. 

From here, for the more visually minded, we can create two or three visualizations for each of the three elapsed time columns. I recommend a histogram or density plot, a blox plot, and a QQ plot. The last one will show you, visually, what the skewness and kurtosis told you numerically. This code should create those for you. Just remember that you're doing it for each of the three variables. 




::: {.cell}

```{.r .cell-code}
# Historgram and Density plt
ggplot(df_cacy, aes(x = Call_Entry_Time)) + 
  geom_histogram(aes(y = ..density..),
                 colour = 1, fill = "white") +
  geom_density(lwd = 1, colour = 4,
               fill = 4, alpha = 0.25)

# QQ Plot
ggqqplot(df_cacy, x = "Call_Entry_Time", color = "#1c5789", title="QQ Plot of TimeToQueue", ylab = "Call Entry Time")

## Box Plot
box1 <- df_cacy %>% ggplot(aes(x=DOW, y=Call_Entry_Time)) +
  geom_boxplot() +
  scale_fill_brewer(palette="Dark2") +
  ggtitle("Boxplot of Call Entry Times by Day")

box1
```
:::




Comparing the results of the current year to the benchmarks gives you visual verification of what you've seen numerically. These are also great for the subsequent reports because your audience is now able to visualize what you're telling them. This may lead to additional questions about the internal working of the data. This could add to the question and project totals that you have generated. 

Visualizations are not simply for numeric data. We can create boxplots for the factor or categorical data. For example, this allows us to look at each day of the week and see how many cardiac arrest calls we have for each day of the week. 




::: {.cell}

```{.r .cell-code}
df_cacy$DOW <- factor(df_cacy$DOW, levels = c("SUN","MON","TUE","WED","THU","FRI","SAT"))

# ggplot2
barDOW <- df_cacy %>% ggplot(aes(x=DOW, fill=DOW)) +
  geom_bar() +
  scale_fill_viridis(discrete = TRUE, option = "H") +
  ggtitle("Count of calls per day of the week") +
  geom_text(
    stat = 'count', 
    aes(label = after_stat(count)), 
    vjust = -0.5  # Adjusts the vertical position of the count
  )

barDOW
```
:::




If anything stands out in this, we can also check that against the benchmark datasets and determine if this normal or if it's standing out for a different reason. This can also be generated for each hour of the day with minor changes to the code. This leads us to another plot that can be visually appealing while also giving us some excellent information. We can use a ridgeline plot to give us a count of events per hour per doy. Are there specific times and days which see more events than others. It's likely that we would see different patters if we examined traffic stops. I expect, if we ran this out, we would not see any particular combination stand out.




::: {.cell}

```{.r .cell-code}
# Aggregate data to get counts per hour per day
hourly_calls <- df_cacy %>%
  group_by(DOW, Hour) %>%
  dplyr::tally(name = "CallCount")

# Create the Ridgeline Plot
ridge_plot <- ggplot(hourly_calls, aes(x = Hour, y = DOW, height = CallCount, group = DOW, fill = DOW)) + # Add fill aesthetic
  geom_density_ridges(stat = "identity", scale = 0.9, rel_min_height = 0.01) +
    scale_x_continuous(breaks = 0:23) + # Set breaks for each hour
  scale_y_discrete(limits = rev) + # Reverse order of days for better readability
  scale_fill_viridis(discrete = TRUE, option = "H") + # Use viridis scale
  labs(title = "Call Count by Hour and Day of Week",
       x = "Hour of Day",
       y = "Day of Week",
       fill = "Day of Week") + # Add legend title
  theme_ridges(font_size = 20, grid = TRUE)

ridge_plot
```
:::




Another thing we can do is look at the geographic distribution of cardiac arrests in the city. Where do we have more of them? that might help us position our resources better and assist us with patient care by ensuring that people at those locations are properly trained in CPR to help get hands on chest faster which increases the likelihood of survival. This code will create and display a map of the City with the locations marked. Hovering over any individual data point will also give us call information so we can see other details. 




::: {.cell}

```{.r .cell-code}
# Convert integer coordinates to decimal degrees
# For latitude: Divide by 1,000,000 and keep positive (Northern hemisphere)
# For longitude: Divide by 1,000,000 and make negative (Western hemisphere for Alexandria)
calls_with_coords <- df_cacy %>%
  mutate(
    lat = Latitude / 1000000,
    long= -1 * (Longitude / 1000000)  # Negative for western hemisphere
  )

# Create the map
alexandria_map <- leaflet(calls_with_coords) %>%
  # Add base map tiles
  addProviderTiles(providers$CartoDB.Positron) %>%
  # Set the view to center on Alexandria, VA
  setView(lng = -77.0469, lat = 38.8048, zoom = 13) %>%
  # Add markers for each call
  addCircleMarkers(
    ~long, ~lat,
    color = '#1c5789',
    radius = 6,
    stroke = FALSE,
    fillOpacity = 0.7,
    popup = ~paste("<b>Call ID:</b>", Master_Incident_Number, "<br>",
                   "<b>Date:</b>", Response_Date, "<br>",
                   "<b>Address:</b>", Address, "<br>",
                   "<b>Seconds To Queue:</b>", Call_Entry_Time, "<br>",
                   "<b>Seconds To DispatchL</b>", Call_Queue_Time, "<b>",
                   "<b>Seconds On Call:</b>", Call_Process_Time, "<br>")
  ) %>%
  # Add a title
  addControl(
    html = "<h3>Cardiac Arrest Calls<br>Alexandria, VA</h3>",
    position = "topright"
  )

# Display the map
alexandria_map

# Save the map for inclusion in reports
saveWidget(alexandria_map, "alexandria_calls_map.html", selfcontained = TRUE)

# Optional: If you want to analyze call density by neighborhood or district
# This creates a clustered view that can help identify hotspots
cluster_map <- leaflet(calls_with_coords) %>%
  # Add base map tiles
  addProviderTiles(providers$CartoDB.Positron) %>%
  # Set the view to center on Alexandria, VA
  setView(lng = -77.0469, lat = 38.8048, zoom = 13) %>%
  # Add clustered markers
  addMarkers(
    ~longitude, ~latitude,
    popup = ~paste("<b>Call ID:</b>", Master_Incident_Number, "<br>",
                   "<b>Date:</b>", Response_Date, "<br>",
                   "<b>Address:</b>", Address, "<br>",
                   "<b>Seconds To Queue:</b>", Call_Entry_Time, "<br>",
                   "<b>Seconds To DispatchL</b>", Call_Queue_Time, "<b>",
                   "<b>Seconds On Call:</b>", Call_Process_Time, "<br>"),
    clusterOptions = markerClusterOptions(),
    label = ~as.character(Master_Incident_Number)
  ) %>%
  # Add a title
  addControl(
    html = "<h3>Clustered Call Locations<br>Alexandria, VA</h3>",
    position = "topright"
  )

# Uncomment to save the cluster map
# saveWidget(cluster_map, "alexandria_calls_cluster_map.html", selfcontained = TRUE)
```
:::




We have set this up to show us where all of the calls are and when we hover over an individual call, it will give us information about the call including the master incident number, the address, the date and time of when it was generated, and the amount of time that passed before it went to queue, was dispatcahed, and how long we were on the call. Seeing the geographic clusters will likely identify nursing homes or other care facilities, so if we see clusters in other places, we may want to look into why a cluster of cardiac arrests are there. These clusters can also be compared against the benchmarks to see if they look the same. If they don't, we can start asking why we have a new cluster. That increases the number of questions that we can ask and the number of projects we have in front of us.

A final example of a new research project would be to create a binary variable in hand with deeper research to determine if calls were originally coded as cardiac arrests or if they were coded and dispatched as something else and changed to cardiac arrests later in the process. That examination could show how accurate we were in triaging and handling these calls. I will leave that code for another day and another post.

From here, you can go anywhere you want to and find answers to the questions that you've found. I hope that this showed exactly how you can start with one question, what can we learn about cardiac arrests, and turn it into many questions and projects that show how much is left to know.