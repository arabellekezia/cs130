import React from 'react';
import { Dimensions, SafeAreaView, ScrollView, StyleSheet, View } from 'react-native';

import AppText from '../components/AppText';
import TitleText from '../components/TitleText';
import HeaderText from '../components/HeaderText';
import AppBarChart from '../components/AppBarChart';
import SummaryItem from '../components/SummaryItem';

import moment from "moment";
import ListItemComponent from '../components/ListItemComponent';
import DailyBreakdownList from '../components/DailyBreakdownList';

//TODO: change this hard coded thing
const daysinWeekBreakdown = [
  {
    title: "Sunday",
    description: "2000 Cals",
  },
  {
    title: "Monday",
    description: "2000 Cals",
  },
  {
    title: "Tuesday",
    description: "2000 Cals",
  },
  {
    title: "Wednesday",
    description: "2000 Cals",
  },
  {
    title: "Thursday",
    description: "2000 Cals",
  },
  {
    title: "Friday",
    description: "2000 Cals",
  },
  {
    title: "Saturday",
    description: "2000 Cals",
  },
];


function WeeklyNutritionScreen(props) {
  const currentWeek = getDaysInWeek();
  const calAvg = calculateAverage(mockCalData.datasets[0].data);
  const calGoal = getCalorieGoal();
  const calDiff = (calGoal - calAvg).toFixed(0);


  return (
    <SafeAreaView>
      <ScrollView alwaysBounceVertical={false} contentContainerStyle={styles.container}>
        <TitleText style={styles.pagetitle} children="Weekly Nutrition" />
        <AppText style={styles.dateheader} children={getWeeklyHeader(currentWeek)} />
        <HeaderText style={styles.header} children={"Summary"} />

        <View style={styles.chartcontainer}>
          <AppText style={{marginLeft: 10,}}>
            You consumed an average of
            <AppText style={styles.boldtext} children={` ${calAvg} Calories `} />
            per day this week.
          </AppText> 
          <AppBarChart 
            style={styles.barChart}
            yAxisSuffix="min"
            data={mockCalData}
            color={(opacity = 1) => `rgba(0, 0, 255, ${opacity})`}
            //scaleDimensions={0.9}
          />
          <AppText>
            Your daily calorie goal was
            <AppText style={styles.boldtext} children={` ${calGoal} Calories.`} /> 
          </AppText>
          {printCalDiffText(calDiff)}
        </View>
        <HeaderText style={styles.header} children={"Macronutrient Averages"} />
        <View style={styles.sleepsummary}>
          {/* TODO: This portion should be changed to accomodate calculations from backend data*/}
          <SummaryItem
            name="baguette"
            size={40}
            detail="200"
            unit="grams"
            label="Average Carbs"
            style={styles.summaryindividual}
          />
          <SummaryItem
            name="sausage"
            size={40}
            detail="140"
            unit="grams"
            label="Average Protein"
            style={styles.summaryindividual}
          />
          <SummaryItem
            name="hamburger"
            size={40}
            detail="50"
            unit="grams"
            label="Average     Fat"
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
    marginVertical: 10,
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
    backgroundColor: "#d5f7f7", //should change accordingly
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

function getCalorieGoal() {
  //TODO: change this for integration
  const calorieGoal = 2100;
  return calorieGoal;
}

function calculateAverage(dataset) {
  const arrAvg = dataset.reduce((a,b) => a + b, 0) / dataset.length;
  const arrTrunc = arrAvg.toFixed(0);
  return arrTrunc;
};

function printCalDiffText(diff) {
  if (diff > 0) {
    return(
      <AppText>
        Your average daily consumption was
        <AppText style={styles.boldtext} children={` ${diff} Calories `}/>
        less than your goal.
      </AppText>
    );

  } else {
    return(
      <AppText>
        Your average daily consumption was
        <AppText style={styles.boldtext} children={` ${Math.abs(diff)} Calories `}/>
        more than your goal.
      </AppText>
    );

  }
}

const mockCalData = {
  labels: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
  datasets: [
    {
      data: [2000, 1800, 2483, 1589, 2307, 2108, 2089],
      strokeWidth: 2, // optional
    },
  ],
};


export default WeeklyNutritionScreen;