import React, { useEffect, useState } from "react";
import { Dimensions, SafeAreaView, ScrollView, StyleSheet, View } from 'react-native';

import AppText from '../components/AppText';
import TitleText from '../components/TitleText';
import HeaderText from '../components/HeaderText';
import AppBarChart from '../components/AppBarChart';
import SummaryItem from '../components/SummaryItem';

import moment from "moment";
import DailyBreakdownList from '../components/DailyBreakdownList';

import NutritionService from "../services/NutritionService";
import GoalsService from "../services/GoalsService";


function WeeklyNutritionScreen(props) {
  const currentWeek = getDaysInWeek();

  const [isReady, setReady] = useState(false);
  const [stats, setStats] = useState({});
  const [daysInWeekBreakdown, setDaysInWeekBreakdown] = useState([]);
  const [calAvg, setCalAvg] = useState(0);
  const [calGoal, setcalGoal] = useState(0);
  const [calDiff, setCalDiff] = useState(0);
  const [carbsAvg, setCarbsAvg] = useState(0);
  const [proteinAvg, setProteinAvg] = useState(0);
  const [fatAvg, setFatAvg] = useState(0);

  useEffect(() => {
    loadNutritionStats();
  }, []);

  const loadNutritionStats = async () => {
    setReady(false);
    const weeklyNutritionStats = await NutritionService.getWeeklyNutritionEntries();
    //console.log(weeklyNutritionStats)
    setStats(weeklyNutritionStats);

    //further breakdowns for calories
    const breakdown = getDailyCals(weeklyNutritionStats);
    setDaysInWeekBreakdown(breakdown);
    const calAverage = calculateAverage(weeklyNutritionStats, "dailyCals");
    setCalAvg(calAverage);
    const calGoal = await getCalorieGoal();
    setcalGoal(calGoal);
    setCalDiff(Math.round(calGoal - calAverage));

    //getting averages for macronutrients
    setCarbsAvg(calculateAverage(weeklyNutritionStats, "dailyCarbs"));
    setProteinAvg(calculateAverage(weeklyNutritionStats, "dailyProtein"));
    setFatAvg(calculateAverage(weeklyNutritionStats, "dailyFat"));

    setReady(true);
  };


  return (
    <SafeAreaView>
      {isReady && (
      <ScrollView
        alwaysBounceVertical={false}
        contentContainerStyle={styles.container}
      >
        <TitleText style={styles.pageTitle} children="Nutritional Trends" />
        <AppText
          style={styles.dateHeader}
          children={getWeeklyHeader(currentWeek)}
        />
        <HeaderText style={styles.sectionHeader} children={"Weekly Summary"} />

        <View style={styles.chartcontainer}>
          <AppText style={styles.smallSummaryText}>
            You consumed an average of
            <AppText
              style={styles.boldtext}
              children={` ${calAvg} Calories `}
            />
            per day this week.
          </AppText>
          <AppBarChart
            style={styles.barChart}
            yAxisSuffix="min"
            data={createChartData(stats)}
            color={(opacity = 1) => `rgba(0, 0, 255, ${opacity})`}
            //scaleDimensions={0.9}
          />
          <AppText style={styles.smallSummaryText}>
            Your daily calorie goal was
            <AppText
              style={styles.boldtext}
              children={` ${calGoal} Calories.`}
            />
          </AppText>
          {printCalDiffText(calDiff)}
        </View>
        <HeaderText
          style={styles.sectionHeader}
          children={"Macronutrient Averages"}
        />
        <View style={styles.sleepsummary}>
          {/* TODO: This portion should be changed to accomodate calculations from backend data*/}
          <SummaryItem
            name="baguette"
            size={40}
            detail={carbsAvg}
            unit="grams"
            label={`Average\nCarbs`}
            style={styles.summaryindividual}
            iconBackgroundColor="#d5f7f7"
          />
          <SummaryItem
            name="sausage"
            size={40}
            detail={proteinAvg}
            unit="grams"
            label={`Average\nProtein`}
            style={styles.summaryindividual}
            iconBackgroundColor="#d5f7f7"
          />
          <SummaryItem
            name="hamburger"
            size={40}
            detail={fatAvg}
            unit="grams"
            label={`Average\nFat`}
            style={styles.summaryindividual}
            iconBackgroundColor="#d5f7f7"
          />
        </View>

        <HeaderText style={styles.sectionHeader} children={"Daily Breakdown"} />
        <DailyBreakdownList 
          entries={daysInWeekBreakdown} 
          type="DailyNutrition"
        />
      </ScrollView>
      )}
    </SafeAreaView>
  );
}

// funciton to get the breakdown data necessary for the small summary info on daily breakdown
function getDailyCals(stats) {
  return [
    {
      title: "Sunday",
      description: `${Math.round(stats[0].dailyCals)} Cals`,
    },
    {
      title: "Monday",
      description: `${Math.round(stats[1].dailyCals)} Cals`,
    },
    {
      title: "Tuesday",
      description: `${Math.round(stats[2].dailyCals)} Cals`,
    },
    {
      title: "Wednesday",
      description: `${Math.round(stats[3].dailyCals)} Cals`,
    },
    {
      title: "Thursday",
      description: `${Math.round(stats[4].dailyCals)} Cals`,
    },
    {
      title: "Friday",
      description: `${Math.round(stats[5].dailyCals)} Cals`,
    },
    {
      title: "Saturday",
      description: `${Math.round(stats[6].dailyCals)} Cals`,
    },
  ];
};

//function to create the weekly chart data of calorie summary
function createChartData(stats) {
  const chartData = [];

  stats.forEach((day) => {
    chartData.push(Math.round(day.dailyCals));
  });

  return {
    labels: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    datasets: [
      {
        data: chartData,
        strokeWidth: 2, // optional
      },
    ],
  }
};

//getting days in week
function getDaysInWeek() {
  const weekStart = moment().startOf("week");
  const days = [];
  for (let i = 0; i <= 6; i++) {
    days.push(moment(weekStart).add(i, "days"));
  }
  return days;
}

//formatting the weekly header
function getWeeklyHeader(currentWeek) {
  return `${currentWeek[0].format("MMM D")} - ${currentWeek[6].format("MMM D, YYYY")}`;
}

//fetching calorie goals
async function getCalorieGoal() {
  const calorieGoal = await GoalsService.getCalorieGoal();
  return calorieGoal;
}

// helper function to calculate the average of whatever unit passed, parsed from the dataset
function calculateAverage(dataset, unit) {
  const arrayToAverage = [];
  dataset.forEach((day) => {
    arrayToAverage.push(Math.round(day[unit]));
  });

  const arrAvg = arrayToAverage.reduce((a,b) => a + b, 0) / arrayToAverage.length;
  const arrTrunc = Math.round(arrAvg);
  return arrTrunc;
};

// function to render the small differences in text depending on whether you went above or below the calorie goal
function printCalDiffText(diff) {
  if (diff > 0) {
    return(
      <AppText style={styles.smallSummaryText}>
        Your average daily consumption was
        <AppText style={styles.boldtext} children={` ${diff} Calories `}/>
        less than your goal.
      </AppText>
    );

  } else {
    return(
      <AppText style={styles.smallSummaryText}>
        Your average daily consumption was
        <AppText style={styles.boldtext} children={` ${Math.abs(diff)} Calories `}/>
        more than your goal.
      </AppText>
    );

  }
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
    backgroundColor: "#d5f7f7", //should change accordingly
  },
  smallSummaryText: {
    marginLeft: 10,
  },
});


export default WeeklyNutritionScreen;