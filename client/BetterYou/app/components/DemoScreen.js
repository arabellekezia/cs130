import React from "react";
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

import Constants from "expo-constants";
import SummaryItem from "./SummaryItem";

function DemoScreen(props) {
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

  return (
    <React.Fragment>
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
      </ScrollView>
    </React.Fragment>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop: Constants.statusBarHeight,
  },
});

export default DemoScreen;
