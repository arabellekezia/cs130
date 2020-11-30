import React, { useState } from "react";

import { StyleSheet } from "react-native";

import colors from "../config/colors";

import Screen from "../components/Screen";
import Stopwatch from "../components/Stopwatch";

function FitnessTimerScreen({ navigation }) {
  // TO DO: change so that stopwatch keeps start and end times
  return (
    <Screen style={styles.container}>
      <Stopwatch
        onStop={({ elapsedTime, startTime, endTime }) => {
          console.log(
            `Navigate to manual sleep input form screen-- Elapsed time (milliseconds): ${startTime}`
          );
          navigation.navigate("SleepEntryForm", {
            startTime: startTime,
            endTime: endTime,
          });
        }}
      />
    </Screen>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: colors.background,
  },
});
export default FitnessTimerScreen;
