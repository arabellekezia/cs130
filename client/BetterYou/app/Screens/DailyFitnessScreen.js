import React, { useEffect } from "react";
import { View, SafeAreaView, ScrollView, StyleSheet, Text } from "react-native";

import AppText from "../components/AppText";
import TitleText from "../components/TitleText";
import AppPieChart from "../components/AppPieChart";

import moment from "moment";
import SegmentedControlTab from "react-native-segmented-control-tab";
import ProgressCircle from "react-native-progress-circle";
import DailyFitnessEntries from "../components/DailyFitnessEntries";
import FitnessService from "../services/FitnessService";
import GoalsService from "../services/GoalsService";
const momentDurationFormatSetup = require("moment-duration-format");

const chartOptions = Object.freeze({ ACTIVE_TIME: 0, CALORIES_BURNED: 1 });

function DailyFitnessScreen({ route }) {
  const date = route.params ? route.params.date : Date.now();
  const [isReady, setIsReady] = React.useState(false);
  const [selectedChartType, setSelectedChartType] = React.useState(
    chartOptions.ACTIVE_TIME
  );
  const [dailyEntries, setDailyEntries] = React.useState([]);
  const [stats, setStats] = React.useState(undefined);

  // Fetch daily entries
  useEffect(() => {
    async function getDailyEntries() {
      const [entries, activeTimeGoal] = await Promise.all([
        FitnessService.getDailyFitnessEntries(moment(date)),
        GoalsService.getActiveTimeGoal(),
      ]);
      setDailyEntries(entries);

      const computedStats = computeAggregatedStatistics(
        entries,
        activeTimeGoal
      );
      setStats(computedStats);
      setIsReady(true);
    }
    getDailyEntries();
  }, []);

  return (
    <SafeAreaView>
      <ScrollView
        alwaysBounceVertical={false}
        contentContainerStyle={styles.container}
      >
        <TitleText style={styles.pageTitle} children="Fitness" />
        <AppText style={styles.dateHeader} children={getToday(date)} />

        {isReady && (
          <DailyFitnessChart
            selectedChartType={selectedChartType}
            stats={stats}
            pieChartData={formatPieChartData(
              dailyEntries,
              stats.totalCaloriesBurned
            )}
          />
        )}

        <SegmentedControlTab
          tabsContainerStyle={{ width: "80%" }}
          values={["Active time", "Calories burned"]}
          selectedIndex={selectedChartType}
          onTabPress={(chartType) => setSelectedChartType(chartType)}
        />

        <View style={styles.logHeaderContainer}>
          <View style={styles.headerTextContainer}>
            <AppText style={styles.logHeaderText} children={"Activity log"} />
          </View>
        </View>

        {isReady && (
          <DailyFitnessEntries
            headerTextStyle={{ marginVertical: 0, fontSize: 0 }}
            entries={formatActivityLog(dailyEntries)}
          />
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

function DailyFitnessChart({ selectedChartType, stats, pieChartData }) {
  const {
    totalActiveTime,
    totalCaloriesBurned,
    activeTimeGoal,
    goalPercentage,
  } = stats;

  if (selectedChartType === chartOptions.ACTIVE_TIME) {
    return (
      <ActiveMinutesProgressCircle
        goalPercentage={goalPercentage}
        activeTime={totalActiveTime}
        activeTimeGoal={activeTimeGoal}
      />
    );
  } else {
    return (
      <View style={styles.chartContainer}>
        <AppText
          style={styles.totalMetricsText}
          children={`${totalCaloriesBurned.toFixed(0)} Calories Burned `}
        />
        <AppPieChart
          data={pieChartData}
          accessor="percentage"
          paddingLeft="15"
          absolute={true}
        />
      </View>
    );
  }
}

function ActiveMinutesProgressCircle({
  goalPercentage,
  activeTime,
  activeTimeGoal,
}) {
  const progressCircleHeader = `Active time of ${activeTime.toFixed(
    0
  )} minutes`;
  return (
    <View style={styles.chartContainer}>
      <AppText
        style={styles.totalMetricsText}
        children={progressCircleHeader}
      />
      <ProgressCircle
        percent={goalPercentage}
        radius={100}
        borderWidth={10}
        color={goalPercentage >= 100 ? "#7ff587" : "#3399FF"}
        bgColor={goalPercentage >= 100 ? "#f7fff8" : "#f2fdff"}
        shadowColor="#999"
      >
        <Text style={styles.percentage}>{goalPercentage.toFixed(1)}%</Text>
        <Text>of your daily goal of</Text>
        <Text style={styles.dailyGoal}>{activeTimeGoal} Minutes</Text>
      </ProgressCircle>
    </View>
  );
}

function getToday(date) {
  //making this function in case this has to work with backend if not might simplify later
  return moment(date).format("dddd, MMMM Do");
}

function computeAggregatedStatistics(entries, activeTimeGoal) {
  let totalActiveTime = 0;
  let totalCaloriesBurned = 0;
  entries.forEach((entry) => {
    totalActiveTime += entry.Minutes;
    totalCaloriesBurned += entry.CaloriesBurned;
  });
  return {
    totalActiveTime,
    totalCaloriesBurned,
    activeTimeGoal,
    goalPercentage: (totalActiveTime / activeTimeGoal) * 100,
  };
}

function formatActivityLog(entries) {
  const activityNameToIconName = new Map([
    ["Cycling", "bike"],
    ["Hiking", "hiking"],
    ["Jogging", "run"],
    ["Sprinting", "run-fast"],
    ["Swimming", "swim"],
    ["Walking", "walk"],
    ["Weightlifting", "dumbbell"],
  ]);
  entries = entries.map((entry) => {
    return {
      iconName: activityNameToIconName.get(entry.WorkoutType),
      startTime: moment.unix(entry.Datetime).local().format("hh:mm A"),
      activity: entry.WorkoutType,
      caloriesBurned: entry.CaloriesBurned.toFixed(1),
      duration: moment
        .duration(entry.Minutes, "minutes")
        .format("h[h] m[m] s[s]"),
    };
  });
  return entries;
}

function getCaloriesBurnedByActivity(entries) {
  let result = {};
  entries.forEach((entry) => {
    if (result.hasOwnProperty(entry.WorkoutType)) {
      result[entry.WorkoutType] += entry.CaloriesBurned;
    } else {
      result[entry.WorkoutType] = entry.CaloriesBurned;
    }
  });
  return result;
}

function formatPieChartData(entries, totalCaloriesBurned) {
  const caloriesBurned = getCaloriesBurnedByActivity(entries);
  const pieChartColors = [
    "rgb(233, 91, 84)",
    "rgb(251, 206, 74)",
    "rgb(60, 175, 133)",
    "rgb(48, 159, 219)",
    "rgb(133, 78, 155)",
    "rgb(255, 115, 0)",
    "rgb(124, 221, 221)",
  ];

  let index = 0;
  const data = [];
  for (const activity in caloriesBurned) {
    data.push({
      name: activity,
      percentage: Math.round(caloriesBurned[activity]),
      color: pieChartColors[index],
      legendFontColor: "#000",
      legendFontSize: 12,
    });
    index++;
  }
  return data;
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: "white",
    alignItems: "center",
    justifyContent: "center",
  },
  dateHeader: {
    alignSelf: "flex-start",
    marginLeft: "5%",
    marginBottom: 24,
    fontSize: 18,
  },
  header: {
    alignSelf: "flex-start",
    marginLeft: "5%",
    marginBottom: 10,
    fontSize: 24,
  },
  headerTextContainer: {
    flex: 1,
    flexDirection: "row",
    justifyContent: "flex-start",
    alignContent: "center",
  },
  headerTextStyle: {
    flexDirection: "row",
    alignItems: "flex-start",
    justifyContent: "flex-start",
    fontSize: 25,
  },
  logHeaderContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: "10%",
    marginBottom: "2%",
  },
  logHeaderText: {
    fontSize: 28,
    fontWeight: "bold",
    marginLeft: 12,
  },
  pageTitle: {
    alignSelf: "flex-start",
    marginTop: "5%",
    marginLeft: "5%",
    marginBottom: 12,
  },
  totalMetricsText: {
    textAlign: "center",
    fontSize: 20,
    marginBottom: 20,
    fontWeight: "bold",
  },
  chartContainer: {
    marginBottom: 15,
    alignItems: "center",
    justifyContent: "center",
    height: 270,
  },
  percentage: {
    fontWeight: "bold",
    fontSize: 36,
    textAlign: "center",
    padding: 10,
  },
  dailyGoal: {
    fontWeight: "bold",
    fontSize: 16,
    textAlign: "center",
    padding: 10,
  },
});

export default DailyFitnessScreen;
