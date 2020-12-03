import React, { useEffect, useState } from "react";
import { View, SafeAreaView, StyleSheet, ScrollView } from 'react-native';

import AppText from "../components/AppText";
import TitleText from "../components/TitleText";
import AppPieChart from "../components/AppPieChart";
import AppProgressRing from "../components/AppProgressRing";

import moment from "moment";
import SegmentedControlTab from "react-native-segmented-control-tab";

import NutritionService from "../services/NutritionService";
import GoalsService from "../services/GoalsService";

import DailyMacronutrientEntries from "../components/DailyMacronutrientEntries";
import DateUtils from "../utils/date";

const chartOptions = Object.freeze({ CALORIES: 0, MACRONUTRIENTS: 1 });

function DailyNutritionScreen({ route }) {
  const date = route.params ? route.params.date : Date.now();

  const [selectedChartType, setSelectedChartType] = React.useState(
    chartOptions.CALORIES
  );

  const [isReady, setReady] = useState(false);
  const [mealEntries, setMealEntries] = useState([]);
  const [calStats, setCalStats] = useState({});
  const [macroStats, setMacroStats] = useState({});

  useEffect(() => {
    loadMealEntriesAndStats();
  }, []);

  const loadMealEntriesAndStats = async () => {
    setReady(false);
    const { entries, calStats, macroStats } = await getTodaysMealsAndStats(date);

    setMealEntries(entries);
    setCalStats(calStats);
    setMacroStats(macroStats)

    setReady(true);
  };

  const progressRingData = {
    //labels: ["Calories"], // optional
    data: [calStats.calRatio], 
  };

  const pieChartData = [
    {
      name: "Carbs",
      grams: macroStats.Carbs,
      color: "rgba(131, 167, 234, 1)",
      legendFontColor: "#000",
      legendFontSize: 12,
    },
    {
      name: "Protein",
      grams: macroStats.Protein,
      color: "#eeaaee",
      legendFontColor: "#000",
      legendFontSize: 12,
    },
    {
      name: "Fat",
      grams: macroStats.Fat,
      color: "red",
      legendFontColor: "#000",
      legendFontSize: 12,
    },
  ];

  return (
    <SafeAreaView>
      {isReady && (
      <ScrollView
        alwaysBounceVertical={false}
        contentContainerStyle={styles.container}
      >
        <TitleText style={styles.pageTitle} children="Nutrition" />
        <AppText style={styles.dateHeader} children={getToday(date)} />

        <DailyNutritionCharts 
          selectedChartType={selectedChartType} 
          calStats={calStats} 
          progressRingData={progressRingData}
          pieChartData={pieChartData}
        />

        <SegmentedControlTab
          tabsContainerStyle={{ width: "80%" }}
          values={["Total Calories", "Macronutrients"]}
          selectedIndex={selectedChartType}
          onTabPress={(chartType) => setSelectedChartType(chartType)}
        />

        <DailyMacronutrientEntries
          style={styles.macronutrientCardContainer}
          entries={[
            {
              macroName: "Carbohydrates",
              percentage: `${macroStats.CarbPer}%`,
              foods: pairFoodAndMacro(mealEntries, "Carbs"),
            },
            {
              macroName: "Protein",
              percentage: `${macroStats.ProteinPer}%`,
              foods: pairFoodAndMacro(mealEntries, "Protein"),
            },
            {
              macroName: "Fat",
              percentage: `${macroStats.FatPer}%`,
              foods: pairFoodAndMacro(mealEntries, "Fat"),
            },
          ]}
        />
      </ScrollView>
      )}
    </SafeAreaView>
  );
}


function getToday(date) {
  //making this function in case this has to work with backend if not might simplify later
  return moment(date).format("dddd, MMMM Do");
}

async function getTodaysMealsAndStats(date) {
  try {
    //fetching mealList
    const mealList = await NutritionService.getDailyMealEntries(moment(date));
    /* currently there is a problem that fooditems stored by barcode is showing barcode instead of name */

    //calculating calorie stats
    const currentCals = sumCalories(mealList);
    const goalCals = await GoalsService.getCalorieGoal();
    const currentToGoalRatio = currentCals / goalCals;
    const percentage = (currentToGoalRatio * 100).toFixed(1);

    //calculating macro stats
    const macroStats = calcMacroStats(mealList);

    return { 
      entries: mealList, 
      calStats: {current: currentCals, goal: goalCals, calRatio: currentToGoalRatio , calPercent: percentage}  ,
      macroStats: macroStats
    };
  } catch (err) {
    console.log(err);
  }
};

function sumCalories(list) {
  let calsum = 0;
  for (const index in list) {
    calsum += Math.round(list[index].Cals);
  }

  return calsum;
};

function calcMacroStats(foodList) {
  let totalCarbs = 0;
  let totalProtein = 0;
  let totalFat = 0;
  
  for (const index in foodList) {
    totalCarbs += Math.round(foodList[index].Carbs);
    totalProtein += Math.round(foodList[index].Protein);
    totalFat += Math.round(foodList[index].Fat);
  }
  
  let total = totalCarbs + totalProtein + totalFat;
  const carbPer = total !== 0 ? (totalCarbs / total * 100).toFixed(1) : 0;
  const proteinPer = total !== 0 ? (totalProtein / total * 100).toFixed(1) : 0;
  const fatPer = total !== 0 ? (totalFat / total * 100).toFixed(1) : 0;

  return { Carbs: totalCarbs, Protein: totalProtein, Fat: totalFat, 
           CarbPer: carbPer, ProteinPer: proteinPer, FatPer: fatPer,
  };
};

function pairFoodAndMacro(foodList, macroType) {
  const pairedList = { foodarray: [] };
  for (const index in foodList) {
    pairedList.foodarray.push({ name: foodList[index].Item, grams: Math.round(foodList[index][macroType]) });
  }

  return pairedList;
};

function DailyNutritionCharts({selectedChartType, calStats, progressRingData, pieChartData}) {
  if (selectedChartType === chartOptions.CALORIES) {
    if (progressRingData.data[0] > 1) {
      //if we go over the calorie limit we display a different color to indicate it
      const percentOver = [progressRingData.data[0] % 1]; //this was a way to prevent some weird glitch with the progress ring when it goes over 100%
      //console.log(percentOver)
      return (
        <View style={styles.chartContainer}>
          <AppText>
            You consumed
            <AppText style={styles.boldtext} children={` ${calStats.current} `} />
            calories
          </AppText>
          <AppText>
            out of your
            <AppText style={styles.boldtext} children={` ${calStats.goal} `} />
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
            <AppText style={styles.overfillpercent} children={` ${calStats.calPercent}% `} />
            of your calorie budget
          </AppText>
        </View>
      );
    } else {
      return (
        <View style={styles.chartContainer}>
          <AppText>
            You consumed
            <AppText style={styles.boldtext} children={` ${calStats.current} `} />
            calories
          </AppText>
          <AppText>
            out of your
            <AppText style={styles.boldtext} children={` ${calStats.goal} `} />
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
            <AppText style={styles.boldtext} children={` ${calStats.calPercent}% `} />
            of your calorie budget
          </AppText>
        </View>
      );
    }
  } else {
    return (
      <View style={styles.chartContainer}>
        <AppText style={styles.boldtext} children="Macronutrient Breakdowns (in grams): " />
        <AppPieChart 
          data={pieChartData}
          accessor="grams"
          paddingLeft="15"
          absolute
        />
      </View>
    );
  }
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
    height: 270,
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

export default DailyNutritionScreen;
