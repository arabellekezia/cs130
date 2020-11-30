import React from "react";
import { SafeAreaView, StyleSheet, View, ScrollView } from "react-native";
import AppText from "../components/AppText";
import AppBarChart from "../components/AppBarChart";

import moment from "moment";
import SegmentedControlTab from "react-native-segmented-control-tab";
import TitleText from "../components/TitleText";
import DailyFitnessEntries from "../components/DailyFitnessEntries";
import HeaderText from "../components/HeaderText";
import DailyBreakdownList from "../components/DailyBreakdownList";

const BarchartType = Object.freeze({ ACTIVE_TIME: 0, CALORIES_BURNED: 1 });
const { totalActiveTime, totalCaloriesBurned } = getWeeklyStats();

//TODO: change this hard coded thing
const daysinWeekBreakdown = [
  {
    title: "Sunday",
    description: "540 Cals",
  },
  {
    title: "Monday",
    description: "540 Cals",
  },
  {
    title: "Tuesday",
    description: "540 Cals",
  },
  {
    title: "Wednesday",
    description: "540 Cals",
  },
  {
    title: "Thursday",
    description: "540 Cals",
  },
  {
    title: "Friday",
    description: "540 Cals",
  },
  {
    title: "Saturday",
    description: "540 Cals",
  },
];

function WeeklyFitnessScreen() {
  const currentWeek = getDaysInWeek();

  const [selectedChartType, setSelectedChartType] = React.useState(
    BarchartType.ACTIVE_TIME
  );

  return (
    <SafeAreaView>
      <ScrollView alwaysBounceVertical={false} contentContainerStyle={styles.container}>
        <TitleText style={styles.header} children="Fitness Trends" />
        <FitnessBarChart
          selectedChartType={selectedChartType}
          currentWeek={currentWeek}
        />
        <SegmentedControlTab
          tabsContainerStyle={{ width: "80%" }}
          values={["Active time", "Calories burned"]}
          selectedIndex={selectedChartType}
          onTabPress={(chartType) => setSelectedChartType(chartType)}
        />
        {/* for loop over this when we make the actual response */}
        {/* To Evan, I feel like we could leave the logged entries to the daily ones and have like a list of the days in summary.
            From there we can have navigations to allow transition from this weekly screen to a breakdown of each day.
            I will try to get to it when I'm applying navigations and if it's too difficult we can keep this, if not I think this
            would prevent the Daily pages of fitness being too repetitive with the weekly ones.
        */}
        {/*
        <DailyFitnessEntries
          style={styles.dailyEntries}
          day="Sunday, Nov. 22"
          entries={[
            {
              iconName: "walk",
              startTime: "7:00 PM",
              activity: "Walking",
              caloriesBurned: 238,
              duration: "00:20:07",
            },
            {
              iconName: "swim",
              startTime: "7:00 PM",
              activity: "Swimming",
              caloriesBurned: 238,
              duration: "00:20:07",
            },
          ]}
        />
        <DailyFitnessEntries
          style={styles.dailyEntries}
          day="Sunday, Nov. 22"
          entries={[
            {
              iconName: "walk",
              startTime: "7:00 PM",
              activity: "Walking",
              caloriesBurned: 238,
              duration: "00:20:07",
            },
            {
              iconName: "swim",
              startTime: "7:00 PM",
              activity: "Swimming",
              caloriesBurned: 238,
              duration: "00:20:07",
            },
          ]}
        />
        */}
        <HeaderText style={styles.header} children={"Daily Breakdowns"} />
        <DailyBreakdownList 
          entries={daysinWeekBreakdown}
        />
      </ScrollView>
    </SafeAreaView>
  );
}

function FitnessBarChart({ selectedChartType, currentWeek }) {
  const totalWeeklyMetric =
    selectedChartType === BarchartType.ACTIVE_TIME
      ? `${totalActiveTime} Active Minutes`
      : `${totalCaloriesBurned} Calories Burned`;

  const barChartData =
    selectedChartType === BarchartType.ACTIVE_TIME
      ? activeTimeData
      : caloriesBurnedData;

  const barChartColor =
    selectedChartType === BarchartType.ACTIVE_TIME
      ? (opacity = 1) => `rgba(0, 0, 255, ${opacity})`
      : (opacity = 1) => `rgba(255, 0, 0, ${opacity})`;

  return (
    <View style={styles.barChartContainer}>
      <AppText
        style={styles.weekHeader}
        children={getWeeklyHeader(currentWeek)}
      />
      <AppText style={styles.weeklyMetric} children={totalWeeklyMetric} />
      <AppBarChart
        style={styles.barChart}
        yAxisSuffix="min"
        data={barChartData}
        color={barChartColor}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: "white",
    alignItems: "center",
    justifyContent: "center",
  },
  header: {
    alignSelf: "flex-start",
    marginTop: "10%",
    marginLeft: "5%",
    marginBottom: 12,
  },
  barChartContainer: {
    marginVertical: 10,
    alignItems: "center",
    justifyContent: "center",
  },
  weekHeader: {
    fontSize: 19,
    fontWeight: "bold",
    marginBottom: 2,
  },
  weeklyMetric: {
    textAlign: "center",
    fontSize: 15,
  },
  barChart: {
    marginVertical: 10,
  },
  dailyEntries: {
    marginVertical: 10,
  },
});

function getDaysInWeek() {
  const weekStart = moment().startOf("week");
  const days = [];
  for (let i = 0; i <= 6; i++) {
    days.push(moment(weekStart).add(i, "days"));
  }
  return days;
}

function getWeeklyStats() {
  return { totalActiveTime: 150, totalCaloriesBurned: 1000 };
}

function getWeeklyHeader(currentWeek) {
  return `${currentWeek[0].format("MMM D")} - ${currentWeek[6].format("MMM D, YYYY")}`;
}

const activeTimeData = {
  labels: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
  datasets: [
    {
      data: [60, 20, 30, 30, 0, 20, 26],
      strokeWidth: 2, // optional
    },
  ],
};

const caloriesBurnedData = {
  labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
  datasets: [
    {
      data: [500, 200, 150, 200, 300, 400, 60],
      strokeWidth: 2, // optional
    },
  ],
};

export default WeeklyFitnessScreen;
