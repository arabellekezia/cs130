import React from 'react';
import { View, SafeAreaView, ScrollView, StyleSheet, Text, TouchableOpacity } from 'react-native';

import AppText from '../components/AppText';
import TitleText from '../components/TitleText';
import AppPieChart from "../components/AppPieChart";

import moment from "moment";
import SegmentedControlTab from "react-native-segmented-control-tab";
import ProgressCircle from 'react-native-progress-circle'
import DailyFitnessEntries from "../components/DailyFitnessEntries";
import Icon from '../components/Icon';

const chartOptions = Object.freeze({ ACTIVE_TIME: 0, CALORIES_BURNED: 1 });
const { totalActiveTime, totalCaloriesBurned } = getFitnessStats();

function DailyFitnessScreen(props) {
  const currentDay = getToday();

  const [selectedChartType, setSelectedChartType] = React.useState(
    chartOptions.ACTIVE_TIME
  );
  
  return (
    <SafeAreaView>
      <ScrollView
        alwaysBounceVertical={false}
        contentContainerStyle={styles.container}
      >
        <TitleText style={styles.pageTitle} children="Fitness" />
        <AppText style={styles.dateHeader} children={currentDay} />

        <DailyFitnessChart selectedChartType={selectedChartType} />

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
          <View style={styles.entryButtonContainer}>
            <TouchableOpacity
              onPress={() => {
                console.log("move to fitness entry types screen");
              }}
              activeOpacity={0.7}
            >
              <Icon
                name="plus-box"
                size={36}
                iconScale={1}
                iconColor="#7e7e7e"
                backgroundColor="white"
              />
            </TouchableOpacity>
          </View>
        </View>

        <DailyFitnessEntries
          headerTextStyle={{ marginVertical: 0, fontSize: 0 }}
          entries={getFitnessEntries()}
        />
      </ScrollView>
    </SafeAreaView>
  );
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
    fontSize: 18
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
  entryButtonContainer: {
    flex: 1, 
    flexDirection: "row", 
    justifyContent: "flex-end", 
    alignContent: "center",
    marginRight: 12
  }, 
  logHeaderContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginTop: "10%", 
    marginBottom: "2%"
  },
  logHeaderText: {
    fontSize: 28,
    fontWeight: "bold",
    marginLeft: 12
  },
  pageTitle: {
    alignSelf: "flex-start",
    marginTop: "10%",
    marginLeft: "5%",
    marginBottom: 12,
  },
});

function getToday() {
  //making this function in case this has to work with backend if not might simplify later
  return moment().format("dddd, MMMM Do")
};

function getFitnessStats() {
  //hard coded rn TODO: backend integration
  const totalActiveTime = 100;
  const totalCaloriesBurned = 400;
  const goalActiveTime = 100;
  const totalToGoal = totalActiveTime / goalActiveTime;
  const percentage = (totalToGoal * 100);
  const percentToDisplay = (totalToGoal * 100).toFixed(1);
  return { 
    totalActiveTime, 
    totalCaloriesBurned, 
    goalActiveTime, 
    totalToGoal,
    percentage,
    percentToDisplay,
  };
}

function getFitnessEntries() {
  //TODO: change this from hard-coded
  const entry = [
    {
      iconName: "walk",
      startTime: "7:00 PM",
      activity: "Walking",
      caloriesBurned: 238,
      duration: "00:20:07",
    },
    {
      iconName: "swim",
      startTime: "8:00 PM",
      activity: "Swimming",
      caloriesBurned: 238,
      duration: "00:20:07",
    },
  ]

  return entry;
};

function DailyFitnessChart({selectedChartType}) {
  const totalMetrics =
    selectedChartType === chartOptions.ACTIVE_TIME
      ? `${totalActiveTime} Active Minutes`
      : `${totalCaloriesBurned} Calories Burned`;

  const styles = StyleSheet.create({
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
      height: 270, //this height is hardcoded but I think will be fine in the grand scheme
    },
    percentage: { 
      fontWeight: "bold", 
      fontSize: 36, 
      textAlign: "center", 
      padding: 10 
    }, 
    dailyGoal: { 
      fontWeight: "bold", 
      fontSize: 16, 
      textAlign: "center", 
      padding: 10 
    }
  })

  if (selectedChartType === chartOptions.ACTIVE_TIME) {
    if (activeTimeData.data[0] >= 1) { //if we go over the goal, we display a different color to indicate it
      return (
        <View style={styles.chartContainer}>
          <AppText style={styles.totalMetricsText} children={totalMetrics} />
          <ProgressCircle
            percent={getFitnessStats().percentage}
            radius={100}
            borderWidth={10}
            color="#7ff587"
            shadowColor="#999"
            bgColor="#f7fff8"
          >
            <Text style={styles.percentage}>
              {getFitnessStats().percentToDisplay}%
            </Text>
            <Text>
              of your daily goal of 
            </Text>
            <Text style={styles.dailyGoal}>
              {getFitnessStats().goalActiveTime} Minutes
            </Text>
          </ProgressCircle>
        </View>
      );
    } else {
      return (
        <View style={styles.chartContainer}>
          <AppText style={styles.totalMetricsText} children={totalMetrics} />
          <ProgressCircle
            percent={getFitnessStats().percentage}
            radius={100}
            borderWidth={10}
            color="#3399FF"
            shadowColor="#999"
            bgColor="#f2fdff"
          >
            <Text style={styles.percentage}>
              {getFitnessStats().percentToDisplay}%
            </Text>
            <Text>
              of your goal of 
            </Text>
            <Text style={styles.dailyGoal}>
              {getFitnessStats().goalActiveTime} Minutes
            </Text>
          </ProgressCircle>
        </View>
      );
    }
  }
  else {
    return (
      <View style={styles.chartContainer}>
        <AppText style={styles.totalMetricsText} children= {`${getFitnessStats().totalCaloriesBurned} Calories Burned `} />
        <AppPieChart 
          data={caloriesBurnedData}
          accessor="percentage"
          paddingLeft="15"
          absolute={true}
        />
      </View>
    );  
  }
};

//possibly not needed
const activeTimeData = {
  //labels: ["Calories"], // optional
  data: [getFitnessStats().totalToGoal], //hard coded for now will change
  //data: [0.6],
};

//randomly generating 10 colors for the pie chart to use (maybe could be improved)
const piechartColors = [...Array(10)].map(() =>
  'rgb(' + (Math.floor(Math.random() * 256)) + ',' + (Math.floor(Math.random() * 256)) + ',' + (Math.floor(Math.random() * 256)) + ')');


const caloriesBurnedData = [
  //TODO: Change from hardcoded to using grabbed data
  {
    name: "Swimming",
    percentage: 100,
    color: piechartColors[0],
    legendFontColor: "#000",
    legendFontSize: 12,
  },
  {
    name: "Running",
    percentage: 100,
    color: piechartColors[1],
    legendFontColor: "#000",
    legendFontSize: 12,
  },
  {
    name: "Lifting",
    percentage: 50,
    color: piechartColors[2],
    legendFontColor: "#000",
    legendFontSize: 12,
  },
];

export default DailyFitnessScreen;