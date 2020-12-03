import React from "react";
import {
  SafeAreaView,
  StyleSheet,
  View,
  ScrollView,
  ActivityIndicator,
} from "react-native";
import AppText from "../components/AppText";
import AppBarChart from "../components/AppBarChart";

import SegmentedControlTab from "react-native-segmented-control-tab";
import TitleText from "../components/TitleText";
import HeaderText from "../components/HeaderText";
import DailyBreakdownList from "../components/DailyBreakdownList";
import DateUtils from "../utils/date";
import FitnessService from "../services/FitnessService";
import moment from "moment";
import { useIsFocused } from "@react-navigation/native";

const BarchartType = Object.freeze({ ACTIVE_TIME: 0, CALORIES_BURNED: 1 });

function WeeklyFitnessScreen() {
  const currentWeek = DateUtils.getDaysInWeek();

  const [selectedChartType, setSelectedChartType] = React.useState(
    BarchartType.ACTIVE_TIME
  );

  const [stats, setStats] = React.useState({});
  const [isReady, setIsReady] = React.useState(false);

  const isFocused = useIsFocused();

  // Fetch weekly entries
  React.useEffect(() => {
    async function getWeeklyEntries() {
      const entries = await FitnessService.getWeeklyFitnessEntries();
      setStats(getCumulativeStats(entries));
      //setIsReady(true);
    }

    let mounted = true;

    getWeeklyEntries().then(() => {
      if (mounted) {
        setIsReady(true);
      }
    });

    return function cleanup() {
      mounted = false;
    };
  }, [isFocused]);

  return (
    <SafeAreaView>
      {!isReady && <ActivityIndicator animating={true} size="large" />}

      {isReady && (
        <ScrollView
          alwaysBounceVertical={false}
          contentContainerStyle={styles.container}
        >
          <TitleText style={styles.pageTitle} children="Fitness Trends" />
          <AppText
            style={styles.dateHeader}
            children={getWeeklyHeader(currentWeek)}
          />
          <FitnessBarChart
            selectedChartType={selectedChartType}
            totalActiveTime={stats.totalActiveTime}
            totalCaloriesBurned={stats.totalCaloriesBurned}
            activeTimeData={stats.activeTimeData}
            caloriesBurnedData={stats.caloriesBurnedData}
          />
          <SegmentedControlTab
            tabsContainerStyle={{ width: "80%" }}
            values={["Active time", "Calories burned"]}
            selectedIndex={selectedChartType}
            onTabPress={(chartType) => setSelectedChartType(chartType)}
          />
          <HeaderText
            style={styles.dailyBreakdownHeader}
            children={"Daily Breakdown"}
          />
          <DailyBreakdownList
            entries={stats.dailyBreakdownData}
            type="DailyFitness"
          />
        </ScrollView>
      )}
    </SafeAreaView>
  );
}

function FitnessBarChart({
  selectedChartType,
  totalActiveTime,
  totalCaloriesBurned,
  activeTimeData,
  caloriesBurnedData,
}) {
  const barChartTitle =
    selectedChartType === BarchartType.ACTIVE_TIME
      ? "Active Minutes Per Day"
      : "Calories Burned Per Day";

  const totalWeeklyMetric =
    selectedChartType === BarchartType.ACTIVE_TIME
      ? `${totalActiveTime.toFixed(0)} minutes`
      : `${totalCaloriesBurned.toFixed(0)} calories`;

  const averageWeeklyMetric =
    selectedChartType === BarchartType.ACTIVE_TIME
      ? `${(totalActiveTime / (moment().day() + 1)).toFixed(0)} minutes`
      : `${(totalCaloriesBurned / (moment().day() + 1)).toFixed(0)} calories`;

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
      <AppText style={styles.weeklyMetric} children={barChartTitle} />
      <AppBarChart
        style={styles.barChart}
        yAxisSuffix="min"
        data={barChartData}
        color={barChartColor}
      />
      {/* TODO: find average active time during the week */}
      <View style={styles.smallSummaryContainer}>
        {selectedChartType === BarchartType.ACTIVE_TIME && (
          <AppText>
            You exercised for a total of
            <AppText
              style={styles.boldtext}
              children={` ${totalWeeklyMetric} `}
            />
            this week.
          </AppText>
        )}
        {selectedChartType === BarchartType.ACTIVE_TIME && (
          <AppText>
            On average, that's about
            <AppText
              style={styles.boldtext}
              children={` ${averageWeeklyMetric} `}
            />
            per day.
          </AppText>
        )}
        {selectedChartType === BarchartType.CALORIES_BURNED && (
          <AppText>
            You burned a total of
            <AppText
              style={styles.boldtext}
              children={` ${totalWeeklyMetric} `}
            />
            this week.
          </AppText>
        )}
        {selectedChartType === BarchartType.CALORIES_BURNED && (
          <AppText>
            On average, that's about
            <AppText
              style={styles.boldtext}
              children={` ${averageWeeklyMetric} `}
            />
            per day.
          </AppText>
        )}
      </View>
    </View>
  );
}

function getCumulativeStats(entries) {
  let totalCaloriesBurned = 0;
  let totalActiveTime = 0;
  const dayOfWeekLabels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  const activeTimeData = {
    labels: dayOfWeekLabels,
    datasets: [{ data: [], strokeWidth: 2 }],
  };
  const caloriesBurnedData = {
    labels: dayOfWeekLabels,
    datasets: [{ data: [], strokeWidth: 2 }],
  };
  const dailyBreakdownData = [
    { title: "Sunday" },
    { title: "Monday" },
    { title: "Tuesday" },
    { title: "Wednesday" },
    { title: "Thursday" },
    { title: "Friday" },
    { title: "Saturday" },
  ];

  entries.forEach((entry, index) => {
    totalCaloriesBurned += entry.caloriesBurned;
    totalActiveTime += entry.activeTime;
    activeTimeData.datasets[0].data.push(entry.activeTime.toFixed(0));
    caloriesBurnedData.datasets[0].data.push(entry.caloriesBurned.toFixed(0));
    dailyBreakdownData[index].description = `${entry.activeTime.toFixed(
      0
    )} minutes`;
  });
  return {
    totalCaloriesBurned,
    totalActiveTime,
    activeTimeData,
    caloriesBurnedData,
    dailyBreakdownData,
  };
}

function getWeeklyHeader(currentWeek) {
  return `${currentWeek[0].format("MMM D")} - ${currentWeek[6].format(
    "MMM D, YYYY"
  )}`;
}

const styles = StyleSheet.create({
  boldtext: {
    fontWeight: "bold",
  },
  container: {
    backgroundColor: "white",
    alignItems: "center",
    justifyContent: "center",
  },
  pageTitle: {
    alignSelf: "flex-start",
    marginTop: "5%",
    marginLeft: "5%",
    marginBottom: 8,
  },
  dateHeader: {
    alignSelf: "flex-start",
    marginLeft: "5%",
    fontSize: 18,
    marginBottom: 24,
  },
  dailyBreakdownHeader: {
    alignSelf: "flex-start",
    marginTop: "10%",
    marginHorizontal: 20,
    marginBottom: 20,
  },
  barChartContainer: {
    marginVertical: 10,
    alignItems: "center",
    justifyContent: "center",
  },
  weeklyMetric: {
    textAlign: "center",
    fontSize: 18,
    fontWeight: "bold",
  },
  smallSummaryContainer: {
    marginVertical: 10,
    alignItems: "center",
    justifyContent: "center",
  },
  barChart: {
    marginVertical: 10,
  },
  dailyEntries: {
    marginVertical: 10,
  },
});

export default WeeklyFitnessScreen;
