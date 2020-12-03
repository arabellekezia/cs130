import React, { useEffect, useState } from "react";
import {
  Dimensions,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  View,
} from "react-native";

import AppText from "../components/AppText";
import TitleText from "../components/TitleText";
import HeaderText from "../components/HeaderText";
import AppBarChart from "../components/AppBarChart";
import SummaryItem from "../components/SummaryItem";

import moment from "moment";
import DailyBreakdownList from "../components/DailyBreakdownList";

import DateUtils from "../utils/date";
import SleepService from "../services/SleepService";
import GoalsService from "../services/GoalsService";

const daysinWeekBreakdown = [
  {
    title: "Sunday",
    description: "6 Hours",
  },
  {
    title: "Monday",
    description: "6 Hours",
  },
  {
    title: "Tuesday",
    description: "6 Hours",
  },
  {
    title: "Wednesday",
    description: "6 Hours",
  },
  {
    title: "Thursday",
    description: "6 Hours",
  },
  {
    title: "Friday",
    description: "6 Hours",
  },
  {
    title: "Saturday",
    description: "6 Hours",
  },
];

function WeeklySleepScreen() {
  const [isReady, setReady] = useState(false);
  const [weeklySleep, setWeeklySleep] = useState([]);
  const [weeklyBreakdown, setWeeklyBreakdown] = useState([]);
  const [sleepGoal, setSleepGoal] = useState([]);
  const [sleepAvg, setSleepAvg] = useState(0);
  const [sleepDiff, setSleepDiff] = useState(0);
  const [avgBedTime, setAvgBedtime] = useState("");
  const [avgWakeTime, setAvgWaketime] = useState("");

  const currentWeek = getDaysInWeek();

  useEffect(() => {
    loadSleepData();
  }, []);

  const loadSleepData = async () => {
    try {
      setReady(false);

      const sleepData = await SleepService.getWeeklySleepEntries();
      console.log(sleepData);
      const aggregate = getTotalHoursPerDay(sleepData);
      const hours = aggregate.map((d) => d.hours);
      setWeeklySleep(aggregate.map((d) => d.hours));
      setWeeklyBreakdown(
        aggregate.map((d) => {
          return {
            title: d.title,
            description: `${roundToOne(d.hours)} hours`,
          };
        })
      );
      const goal = await getSleepGoal();
      setSleepGoal(goal);

      const avg = calculateAverage(hours);
      setSleepAvg(avg);
      const diff = roundToOne(goal - avg);
      setSleepDiff(diff);

      const avgBed = getAverageBedOrWakeTime(sleepData, "SleepTime");
      setAvgBedtime({ time: avgBed.format("hh:mm"), unit: avgBed.format("A") });

      const avgWake = getAverageBedOrWakeTime(sleepData, "WakeupTime");
      setAvgWaketime({
        time: avgWake.format("hh:mm"),
        unit: avgWake.format("A"),
      });
      setReady(true);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <SafeAreaView>
      {isReady && (
        <ScrollView
          alwaysBounceVertical={false}
          contentContainerStyle={styles.container}
        >
          <TitleText style={styles.pageTitle} children="Sleep Trends" />
          <AppText
            style={styles.dateHeader}
            children={getWeeklyHeader(currentWeek)}
          />
          <HeaderText
            style={styles.sectionHeader}
            children={"Weekly Summary"}
          />
          <View style={styles.chartcontainer}>
            <AppText style={styles.smallSummaryText}>
              You averaged
              <AppText
                style={styles.boldtext}
                children={` ${sleepAvg} hours `}
              />
              of sleep this week.
            </AppText>
            <AppBarChart
              style={styles.barChart}
              yAxisSuffix="min"
              data={createSleepChartData(weeklySleep)}
              color={(opacity = 1) => `rgba(0, 0, 255, ${opacity})`}
              //scaleDimensions={0.9}
            />
            <AppText style={styles.smallSummaryText}>
              Your goal was
              <AppText
                style={styles.boldtext}
                children={` ${sleepGoal} hours `}
              />
              of sleep.
            </AppText>
            {printSleepDiffText(sleepDiff)}
          </View>

          <HeaderText style={styles.sectionHeader} children={"Average Stats"} />
          <View style={styles.sleepsummary}>
            <SummaryItem
              name="power-sleep"
              size={40}
              detail={avgBedTime.time}
              unit={avgBedTime.unit}
              label={`Average\nbedtime`}
              iconBackgroundColor="#d5f7f7"
              style={styles.summaryindividual}
            />
            <SummaryItem
              name="alarm"
              size={40}
              detail={avgWakeTime.time}
              unit={avgWakeTime.unit}
              label={`Average\nwake time`}
              iconBackgroundColor="#d5f7f7"
              style={styles.summaryindividual}
            />
            <SummaryItem
              name="sleep"
              size={40}
              detail={sleepAvg}
              unit="Hours"
              label={`Average\nduration`}
              iconBackgroundColor="#d5f7f7"
              style={styles.summaryindividual}
            />
          </View>

          <HeaderText
            style={styles.sectionHeader}
            children={"Daily Breakdown"}
          />
          <DailyBreakdownList entries={weeklyBreakdown} type="DailySleep" />
        </ScrollView>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  barChart: {
    alignItems: "center",
  },
  boldtext: {
    fontWeight: "bold",
  },
  chartcontainer: {
    width: Dimensions.get("window").width * 0.9,
  },
  container: {
    backgroundColor: "white",
    alignItems: "center",
    justifyContent: "center",
  },
  dateHeader: {
    alignSelf: "flex-start",
    marginLeft: "5%",
    fontSize: 18,
  },
  sectionHeader: {
    alignSelf: "flex-start",
    marginHorizontal: 20,
    marginTop: "10%",
    marginBottom: "5%",
  },
  smallSummaryText: {
    marginLeft: 10,
  },
  pageTitle: {
    alignSelf: "flex-start",
    marginTop: "5%",
    marginLeft: "5%",
    marginBottom: 8,
  },
  sleepsummary: {
    flexDirection: "row",
    justifyContent: "space-evenly",
    width: "90%",
  },
  summaryindividual: {
    borderWidth: 1,
    borderRadius: 10,
    marginHorizontal: 5,
    backgroundColor: "#d5f7f7",
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

function getWeeklyHeader(currentWeek) {
  return `${currentWeek[0].format("MMM D")} - ${currentWeek[6].format(
    "MMM D, YYYY"
  )}`;
}

async function getSleepGoal() {
  try {
    const sleepGoal = await GoalsService.getGoal("SleepHours");
    return sleepGoal;
  } catch (err) {
    throw new Error(err);
  }
}

function calculateAverage(dataset) {
  const arrAvg = dataset.reduce((a, b) => a + b, 0) / (moment().day() + 1);
  const arrTrunc = arrAvg.toFixed(1);
  return arrTrunc;
}

function printSleepDiffText(diff) {
  if (diff > 0) {
    return (
      <AppText style={styles.smallSummaryText}>
        On average, you slept
        <AppText style={styles.boldtext} children={` ${diff} hours `} />
        less than your goal.
      </AppText>
    );
  } else {
    return (
      <AppText style={styles.smallSummaryText}>
        On average, you slept
        <AppText
          style={styles.boldtext}
          children={` ${Math.abs(diff)} hours `}
        />
        more than your goal.
      </AppText>
    );
  }
}

/**
 *
 * @param {*} weeklySleep : 2-dimensional array of daily sleep
 */
function getTotalHoursPerDay(weeklySleep) {
  let dataSet = [];

  for (let i = 0; i < weeklySleep.length; i++) {
    const days = [
      "Sunday",
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
    ];

    const dayOfWeek = days[i];
    let totalMinutes = 0;
    for (let j = 0; j < weeklySleep[i].length; j++) {
      totalMinutes += weeklySleep[i][j].Minutes;
    }

    dataSet[i] = { title: dayOfWeek, hours: roundToOne(totalMinutes / 60) };
  }

  return dataSet;
}

function getAverageBedOrWakeTime(weeklySleep, type) {
  // extract the hours and minutes of the day.
  // create new date objects of today, and set the hours and day to that.
  // get the unix timestamp
  // average it
  // create new datetime object with the averaged time
  // get the hours and minutes of the day
  let totalMinutes = 0;
  let count = 0;
  for (let i = 0; i < weeklySleep.length; i++) {
    for (let j = 0; j < weeklySleep[i].length; j++) {
      if (weeklySleep[i][j].Nap === 0) {
        const time = moment(weeklySleep[i][j][type] * 1000);
        totalMinutes += time.minute() + time.hour() * 60;
        count++;
      }
    }
  }
  let averageMinutes = count ? totalMinutes / count : 0;
  let hourValue = Math.floor(averageMinutes / 60);
  let minuteValue = averageMinutes % 60;
  return moment().hour(hourValue).minute(minuteValue);
}

const mockSleepData = {
  labels: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
  datasets: [
    {
      data: [6.5, 8.2, 4, 3.6, 5, 8, 10],
      strokeWidth: 2, // optional
    },
  ],
};

function roundToOne(num) {
  return +(Math.round(num + "e+1") + "e-1");
}

function createSleepChartData(data) {
  return {
    labels: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    datasets: [
      {
        data: data,
        strokeWidth: 2, // optional
      },
    ],
  };

  function roundToOne(num) {
    return +(Math.round(num + "e+1") + "e-1");
  }
}

export default WeeklySleepScreen;
