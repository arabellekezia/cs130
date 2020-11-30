import React from 'react';
import { View, SafeAreaView, ScrollView, StyleSheet, Text } from 'react-native';

import AppText from '../components/AppText';
import TitleText from '../components/TitleText';
import AppPieChart from '../components/AppPieChart';
import AppProgressRing from '../components/AppProgressRing';

import moment from "moment";
import SegmentedControlTab from "react-native-segmented-control-tab";
import ProgressCircle from 'react-native-progress-circle'
import DailyFitnessEntries from '../components/DailyFitnessEntries';
import HeaderText from '../components/HeaderText';
import TextButton from '../components/TextButton';

const chartOptions = Object.freeze({ ACTIVE_TIME: 0, CALORIES_BURNED: 1 });
const { totalActiveTime, totalCaloriesBurned } = getFitnessStats();

function DailyFitnessScreen(props) {
  const currentDay = getToday();

  const [selectedChartType, setSelectedChartType] = React.useState(
    chartOptions.ACTIVE_TIME
  );
  
  return (
    <SafeAreaView>
      <ScrollView alwaysBounceVertical={false} contentContainerStyle={styles.container}>
        <TitleText style={styles.pagetitle} children="Today's Fitness Logs" />
        <AppText style={styles.dateheader} children={currentDay} />
        <HeaderText style={styles.header} children={"Stats"} />

        <DailyFitnessChart selectedChartType={selectedChartType} />

        <SegmentedControlTab
          tabsContainerStyle={{ width: "80%" }}
          values={["Active time", "Calories burned"]}
          selectedIndex={selectedChartType}
          onTabPress={(chartType) => setSelectedChartType(chartType)}
        />

        <View style={styles.logheader}>
          <HeaderText style={styles.logheadertext} children={"Logs"} />
          <TextButton 
            name={"Add to Fitness Log"}
            onPress={() => console.log("move to fitnessentrytypescreen")}
            style={styles.addbutton}
          />
        </View>
        
        <DailyFitnessEntries
          style={styles.dailyEntries}
          //day={currentDay}
          entries={getFitnessEntries()}
        />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  addbutton:{
    //width: "50%",
    //alignSelf: "flex-end",
  },
  chartContainer: {
    //marginTop: 2,
    marginBottom: 15,
    alignItems: "center",
    justifyContent: "center",
    height: 270,  //this height is hardcoded but I think will be fine in the grand scheme
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
  dailyEntries: {
    marginVertical: -20,
  },
  logheader: {
    flexDirection: "row",
    //alignSelf: "flex-start",
    justifyContent: "space-between",
    //marginLeft: "7%",
    width: "90%",
    //marginBottom: 10,
    marginTop: 25,
    fontSize: 25,
  },
  logheadertext: {
    marginTop: 10,
    fontSize: 25,
  },
  pagetitle: {
    alignSelf: "flex-start",
    marginTop: "10%",
    marginLeft: "5%",
    marginBottom: 12,
  },
  header: {
    alignSelf: "flex-start",
    marginLeft: "7%",
    marginBottom: 10,
    fontSize: 25,
  },
  totalmetrictext: {
    textAlign: "center",
    fontSize: 25,
    marginBottom: 15,
    fontWeight: "bold"
  },
})

function getToday() {
  //making this function in case this has to work with backend if not might simplify later
  return moment().format("MMM Do YYYY")
};

function getFitnessStats() {
  //hard coded rn TODO: backend integration
  const totalActiveTime = 120;
  const totalCaloriesBurned = 400;
  const goalActiveTime = 100;
  const totalToGoal = totalActiveTime / goalActiveTime;
  const percent = (totalToGoal * 100);
  const percentToDispaly = (totalToGoal * 100).toFixed(1);
  return { 
    totalActiveTime: totalActiveTime, 
    totalCaloriesBurned: totalCaloriesBurned, 
    goalActiveTime: goalActiveTime, 
    totalToGoal: totalToGoal,
    percentage: percent,
    percentToDispaly: percentToDispaly,
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

  if (selectedChartType === chartOptions.ACTIVE_TIME) {
    if (activeTimeData.data[0] > 1) { //if we go over the goal, we display a different color to indicate it
      return (
        <View style={styles.chartContainer}>
          <AppText style={styles.totalmetrictext} children={totalMetrics} />
          <ProgressCircle
            percent={getFitnessStats().percentage}
            radius={100}
            borderWidth={10}
            color="#7ff587"
            shadowColor="#999"
            bgColor="#fff"
          >
            <Text style={{ fontWeight: "bold", fontSize: 25, textAlign: "center", padding: 10 }}>
              {getFitnessStats().percentToDispaly}%
            </Text>
            <Text>
              from your goal of 
            </Text>
            <Text style={{ fontWeight: "bold", fontSize: 20, textAlign: "center", padding: 10 }}>
              {getFitnessStats().goalActiveTime} Minutes
            </Text>
          </ProgressCircle>
        </View>
      );
    } else {
      return (
        <View style={styles.chartContainer}>
          <AppText style={styles.totalmetrictext} children={totalMetrics} />
          <ProgressCircle
            percent={getFitnessStats().percentage}
            radius={100}
            borderWidth={10}
            color="#3399FF"
            shadowColor="#999"
            bgColor="#fff"
          >
            <Text style={{ fontWeight: "bold", fontSize: 25, textAlign: "center", padding: 10 }}>
              {getFitnessStats().percentToDispaly}%
            </Text>
            <Text>
              from your goal of 
            </Text>
            <Text style={{ fontWeight: "bold", fontSize: 20, textAlign: "center", padding: 10 }}>
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
        <AppText style={styles.totalmetrictext} children= {`${getFitnessStats().totalCaloriesBurned} Calories Burned `} />
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