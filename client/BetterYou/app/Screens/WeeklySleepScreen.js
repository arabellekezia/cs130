import React from 'react';
import { Dimensions, SafeAreaView, ScrollView, StyleSheet, View } from 'react-native';

import AppText from '../components/AppText';
import TitleText from '../components/TitleText';
import HeaderText from '../components/HeaderText';
import AppBarChart from '../components/AppBarChart';
import SummaryItem from '../components/SummaryItem';
//import AppStackedBarChart from '../components/AppStackedBarChart';

import moment from "moment";
import DailyBreakdownList from '../components/DailyBreakdownList';

//TODO: change this hard coded thing
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
  const currentWeek = getDaysInWeek();
  const sleepAvg = calculateAverage(mockSleepData.datasets[0].data);
  const sleepGoal = getSleepGoal();
  const sleepDiff = (sleepGoal - sleepAvg).toFixed(1);

  return (
    <SafeAreaView>
      <ScrollView alwaysBounceVertical={false} contentContainerStyle={styles.container} >
        <TitleText style={styles.pagetitle} children="Weekly Sleep Trends" />
        <AppText style={styles.dateheader} children={getWeeklyHeader(currentWeek)} />
        <HeaderText style={styles.header} children={"Summary"} />

        <View style={styles.chartcontainer}>
          <AppText style={{marginLeft: 10,}}>
            You averaged
            <AppText style={styles.boldtext} children={` ${sleepAvg} hours `} />
            of sleep this week.
          </AppText> 
          <AppBarChart 
            style={styles.barChart}
            yAxisSuffix="min"
            data={mockSleepData}
            color={(opacity = 1) => `rgba(0, 0, 255, ${opacity})`}
            //scaleDimensions={0.9}
          />
          <AppText>
            Your goal was
            <AppText style={styles.boldtext} children={` ${sleepGoal} hours `} />
            of sleep. 
          </AppText>
          {printSleepDiffText(sleepDiff)}
        </View>

        <HeaderText style={styles.header} children={"Average Stats"} />
        <View style={styles.sleepsummary}>
          {/* TODO: This portion should be changed to accomodate calculations from backend data*/}
          <SummaryItem
            name="power-sleep"
            size={40}
            detail="11:34"
            unit="PM"
            label="Average Bedtime"
            style={styles.summaryindividual}
          />
          <SummaryItem
            name="alarm"
            size={40}
            detail="7:10"
            unit="AM"
            label="Average Wake Time"
            style={styles.summaryindividual}
          />
          <SummaryItem
            name="sleep"
            size={40}
            detail={sleepAvg}
            unit="Hours"
            label="Average    Time Slept"
            style={styles.summaryindividual}
          />
        </View>
        
        <HeaderText style={styles.header} children={"Daily Breakdowns"} />
        <DailyBreakdownList 
          entries={daysinWeekBreakdown}
        />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  barChart: {
    //marginVertical: 10,
    alignItems: "center",
  },
  boldtext: {
    fontWeight: "bold",
  },
  chartcontainer: {
    width: Dimensions.get('window').width * .9,
    marginBottom: 15,
    //flex: 1,
  },
  container: {
    backgroundColor: "white",
    alignItems: "center",
    justifyContent: "center",
  },
  dateheader: {
    alignSelf: "flex-start",
    marginLeft: "7%",
    marginBottom: 12,
  },
  header: {
    alignSelf: "flex-start",
    marginLeft: "7%",
    marginBottom: 10,
  },
  pagetitle: {
    alignSelf: "flex-start",
    marginTop: "10%",
    marginLeft: "5%",
    marginBottom: 12,
  },
  sleepsummary: {
    flexDirection: "row",
    justifyContent: "space-evenly",
    //flex: 1,
    width: "90%",
    marginBottom: 25,
  },
  summaryindividual: {
    borderWidth: 1,
    borderRadius: 10,
    marginHorizontal: 5,
    backgroundColor: "#d5f7f7",
  },
})

function getDaysInWeek() {
  const weekStart = moment().startOf("week");
  const days = [];
  for (let i = 0; i <= 6; i++) {
    days.push(moment(weekStart).add(i, "days"));
  }
  return days;
}

function getWeeklyHeader(currentWeek) {
  return `${currentWeek[0].format("MMM D")} - ${currentWeek[6].format("MMM D, YYYY")}`;
}

function getSleepGoal() {
  //TODO: make this not hard coded
  const sleepGoal = 7;
  
  return sleepGoal;
}

function calculateAverage(dataset) {
  const arrAvg = dataset.reduce((a,b) => a + b, 0) / dataset.length;
  const arrTrunc = arrAvg.toFixed(1);
  return arrTrunc;
};

function printSleepDiffText(diff) {
  if (diff > 0) {
    return(
      <AppText>
        On average, you slept
        <AppText style={styles.boldtext} children={` ${diff} hours `}/>
        less than your goal.
      </AppText>
    );

  } else {
    return(
      <AppText>
        On average, you slept
        <AppText style={styles.boldtext} children={` ${Math.abs(diff)} hours `}/>
        more than your goal.
      </AppText>
    );

  }
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


export default WeeklySleepScreen;