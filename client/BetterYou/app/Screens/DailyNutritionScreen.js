import React from 'react';
import { View, SafeAreaView, StyleSheet, ScrollView } from 'react-native';

import AppText from '../components/AppText';
import TitleText from '../components/TitleText';
import AppPieChart from '../components/AppPieChart';
import AppProgressRing from '../components/AppProgressRing';

import moment from "moment";
import SegmentedControlTab from "react-native-segmented-control-tab";

//import IndivMacroCard from '../components/IndivMacroCard';
import DailyMacronutrientEntries from '../components/DailyMacronutrientEntries';

const chartOptions = Object.freeze({ CALORIES: 0, MACRONUTRIENTS: 1 });

function DailyNutritionScreen() {
  const currentDay = getToday();

  const [selectedChartType, setSelectedChartType] = React.useState(
    chartOptions.CALORIES
  );

  return (
    <SafeAreaView>
      <ScrollView
        alwaysBounceVertical={false}
        contentContainerStyle={styles.container}
      >
        <TitleText style={styles.pageTitle} children="Nutrition" />
        <AppText style={styles.dateHeader} children={currentDay} />

        <DailyNutritionCharts selectedChartType={selectedChartType} />

        <SegmentedControlTab
          tabsContainerStyle={{ width: "80%" }}
          values={["Total Calories", "Macronutrients"]}
          selectedIndex={selectedChartType}
          onTabPress={(chartType) => setSelectedChartType(chartType)}
        />

        <DailyMacronutrientEntries
          style={styles.macronutrientCardContainer}
          entries={[
            //these are just hard coded, TODO: have to adapt this when backend integration happens
            {
              macroName: "Carbohydrates",
              percentage: "40%",
              foods: getFoods(),
            },
            {
              macroName: "Protein",
              percentage: "40%",
              foods: getFoods(),
            },
            {
              macroName: "Fat",
              percentage: "20%",
              foods: getFoods(),
            },
          ]}
        />
      </ScrollView>
    </SafeAreaView>
  );
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
  chartContainer: {
    marginBottom: 15,
    alignItems: "center",
    justifyContent: "center",
    height: 270, //this height is hardcoded but I think will be fine in the grand scheme
  },
  dateHeader: {
    alignSelf: "flex-start",
    marginLeft: "5%",
    fontSize: 18,
    marginBottom: 24,
  },
  pageTitle: {
    alignSelf: "flex-start",
    marginTop: "5%",
    marginLeft: "5%",
    marginBottom: 8,
  },
  macronutrientCardContainer: {
    marginTop: 20,
  },
  overfillpercent: {
    fontWeight: "bold",
    color: "red",
  },
});

function getToday() {
  //making this function in case this has to work with backend if not might simplify later
  return moment().format("dddd, MMMM Do");
};

//placeholder for backend integration
function getCalories() {
  const currentCals = 2500;   //hardcoded; will change later
  const goalCals = 2100;      //same
  const currentToGoalRatio = currentCals / goalCals;
  const percentage = (currentToGoalRatio * 100).toFixed(1);
  return { calRatio: currentToGoalRatio, currentCalories: currentCals, calorieGoal: goalCals, calPercent: percentage };
};

function getFoods() {
  //hardcoded for now
  const foods = {
    foodarray: [
      {
        name: "Chicken and Ricefakuyefhakwyefgakuygfrakueryfgkuaeyfgakueryg",
        grams: 100
      },
      {
        name: "Cheese Pizza",
        grams: 150
      },
      {
        name: "Hamburger",
        grams: 200
      },
      {
        name: "KBBQ",
        grams: 300
      }
    ]
  }

  return foods;
};

function DailyNutritionCharts({selectedChartType}) {
  if (selectedChartType === chartOptions.CALORIES) {
    if (progressRingData.data[0] > 1) { //if we go over the calorie limit we display a different color to indicate it
      const percentOver = [progressRingData.data[0] % 1] //this was a way to prevent some weird glitch with the progress ring when it goes over 100%
      //console.log(percentOver)
      return (
        <View style={styles.chartContainer}>
          <AppText>
            You consumed
            <AppText style={styles.boldtext} children={` ${getCalories().currentCalories} `} />
            calories
          </AppText>
          <AppText>
            out of your
            <AppText style={styles.boldtext} children={` ${getCalories().calorieGoal} `} />
            calorie budget
          </AppText>
          <AppProgressRing 
            data={percentOver}
            radius={70}
            strokeWidth={14}
            color={(opacity = 1) => `rgba(255, 0, 0, ${opacity})`}
            hideLegend={true}
            backgroundColor={styles.container.backgroundColor}
          />
          <AppText>
            You have filled
            <AppText style={styles.overfillpercent} children={` ${getCalories().calPercent}% `} />
            of your calorie budget
          </AppText>
        </View>
      );
    } else {
      return (
        <View style={styles.chartContainer}>
          <AppText>
            You consumed
            <AppText style={styles.boldtext} children={` ${getCalories().currentCalories} `} />
            calories
          </AppText>
          <AppText>
            out of your
            <AppText style={styles.boldtext} children={` ${getCalories().calorieGoal} `} />
            calorie budget
          </AppText>
          <AppProgressRing 
            data={progressRingData}
            radius={70}
            strokeWidth={14}
            color={(opacity = 1) => `rgba(0, 0, 255, ${opacity})`}
            hideLegend={true}
            backgroundColor={styles.container.backgroundColor}
          />
          <AppText>
            You have filled
            <AppText style={styles.boldtext} children={` ${getCalories().calPercent}% `} />
            of your calorie budget
          </AppText>
        </View>
      );
    }
  }
  else {
    return (
      <View style={styles.chartContainer}>
        <AppText style={styles.boldtext} children="Macronutrient Breakdowns (in grams): " />
        <AppPieChart 
          data={mockPieChartData}
          accessor="percentage"
          paddingLeft="15"
        />
      </View>
    );  
  }
};

const mockPieChartData = [
  {
    name: "Carbs",
    percentage: 100,
    color: "rgba(131, 167, 234, 1)",
    legendFontColor: "#000",
    legendFontSize: 12,
  },
  {
    name: "Protein",
    percentage: 100,
    color: "#eeaaee",
    legendFontColor: "#000",
    legendFontSize: 12,
  },
  {
    name: "Fat",
    percentage: 50,
    color: "red",
    legendFontColor: "#000",
    legendFontSize: 12,
  },
];

const progressRingData = {
  //labels: ["Calories"], // optional
  data: [getCalories().calRatio], //hard coded for now will change
};

export default DailyNutritionScreen;