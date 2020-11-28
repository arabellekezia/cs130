import React, { useState } from "react";
import { ScrollView, View, StyleSheet } from "react-native";
import AppText from "./AppText";
import HeaderText from "./HeaderText";
import Icon from "./Icon";
import IconButton from "./IconButton";
import TitleText from "./TitleText";
import TextButton from "./TextButton";
import AppLineChart from "./AppLineChart";
import AppBarChart from "./AppBarChart";
import AppProgressRing from "./AppProgressRing";
import AppStackedBarChart from "./AppStackedBarChart";
import Stopwatch from "./Stopwatch";
import Screen from "./Screen";

import SummaryItem from "./SummaryItem";
import AppPieChart from "./AppPieChart";
import AppTextInput from "./AppTextInput";
import DailyFitnessEntries from "./DailyFitnessEntries";

import DropDownPicker from "react-native-dropdown-picker";

function DemoScreen(props) {
  const [name, setName] = useState("");
  const [selectedIndex, setSelectedIndex] = React.useState(0);

  const data = {
    labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    datasets: [
      {
        data: [6.5, 4, 6, 5, 7, 6, 8],
        // color: (opacity = 1) => `rgba(0, 0, 255, ${opacity})`, // optional
        strokeWidth: 2, // optional
      },
      // {
      //   data: [5, 4, 3, 3, 8, 4, 5],
      //   // color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`, // optional
      //   strokeWidth: 2, // optional
      // },
    ],
    legend: ["Hours Slept"], // optional
  };

  const progressRingData = {
    labels: ["Swim", "Bike", "Run"], // optional
    data: [0.4, 0.6, 0.8],
  };

  const pieChartData = [
    {
      name: "Running",
      population: 21500000,
      color: "rgba(131, 167, 234, 1)",
      legendFontColor: "#000",
      legendFontSize: 12,
    },
    {
      name: "Cycling",
      population: 2800000,
      color: "#eeaaee",
      legendFontColor: "#000",
      legendFontSize: 12,
    },
    {
      name: "Weightlifting",
      population: 527612,
      color: "red",
      legendFontColor: "#000",
      legendFontSize: 12,
    },
    {
      name: "Swimming",
      population: 8538000,
      color: "#da29ad",
      legendFontColor: "#000",
      legendFontSize: 12,
    },
  ];

  const stackedBarData = {
    labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    legend: ["L1", "L2", "L3"],
    data: [
      [...Array(3)].map(() => Math.floor(Math.random() * 9)),
      [...Array(3)].map(() => Math.floor(Math.random() * 9)),
      [...Array(3)].map(() => Math.floor(Math.random() * 9)),
      [...Array(3)].map(() => Math.floor(Math.random() * 9)),
      [...Array(3)].map(() => Math.floor(Math.random() * 9)),
      [...Array(3)].map(() => Math.floor(Math.random() * 9)),
      [...Array(3)].map(() => Math.floor(Math.random() * 9)),
    ],
    barColors: ["#da29ad", "#eeaaee", "red"],
  };

  return (
    <Screen>
      <ScrollView style={styles.container}>
        <View
          style={{
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <TitleText style={{ color: "red" }}>Hello!</TitleText>
          <HeaderText style={{ color: "blue" }}>Hello!</HeaderText>
          <AppText style={{ color: "green" }}>Hello!</AppText>
          <Icon
            name="food-variant"
            size={30}
            backgroundColor="white"
            iconColor="black"
            iconScale={1}
          />
          <IconButton
            name="food-variant"
            size={40}
            iconColor="red"
            label="nutrition"
            fontSize={10}
            onPress={() => console.log("icon pressed")}
          />
          <TextButton
            name={"Click me"}
            onPress={() => console.log("pressed")}
          />
          <SummaryItem
            name="food-variant"
            size={40}
            detail="11:34"
            unit="PM"
            label="Average BedTime"
          />
        </View>
        <AppTextInput
          placeholder="First name"
          icon="account"
          onChangeText={(text) => setName(text)}
        />
        <TextButton name={"Submit"} onPress={() => console.log(name)} />

        <AppLineChart
          data={data}
          color={(opacity = 1) => `rgba(0, 0, 255, ${opacity})`}
        />
        <AppBarChart
          data={data}
          color={(opacity = 1) => `rgba(0, 0, 0, ${opacity})`}
        />
        <AppProgressRing
          data={progressRingData}
          radius={20}
          strokeWidth={14}
          color={(opacity = 1) => `rgba(0, 0, 255, ${opacity})`}
        />
        <AppPieChart
          data={pieChartData}
          accessor="population"
          paddingLeft="15"
        />
        <AppStackedBarChart data={stackedBarData} />
        <DropDownPicker
          items={[
            { label: "Item 1", value: "item1" },
            { label: "Item 2", value: "item2" },
          ]}
          defaultValue="item1"
          containerStyle={{ height: 40 }}
          style={{ backgroundColor: "#fafafa" }}
          dropDownStyle={{ backgroundColor: "#fafafa" }}
          onChangeItem={(item) => console.log(item.label, item.value)}
        />

        <Stopwatch onStop={(result) => console.log(result)} />
        <DailyFitnessEntries
          day="Sunday, Nov. 15"
          entries={[
            {
              iconName: "walk",
              startTime: "7:00 PM",
              activity: "Walking",
              caloriesBurned: 238,
              duration: "00:20:07",
            },
            {
              iconName: "swim",
              startTime: "7:00 PM",
              activity: "Swimming",
              caloriesBurned: 238,
              duration: "00:20:07",
            },
          ]}
        />
      </ScrollView>
    </Screen>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 10,
  },
  activity: {
    marginBottom: 40,
    marginLeft: 10,
  },
});

export default DemoScreen;
