import React from "react";

import { StyleSheet } from "react-native";

import colors from "../config/colors";

import Screen from "../components/Screen";
import Stopwatch from "../components/Stopwatch";

function FitnessTimerScreen(props) {
  return (
    <Screen style={styles.container}>
      <Stopwatch
        onStop={(elapsedTimeInMilliseconds) =>
          console.log(
            `Navigate to manual input form screen-- Elapsed time (milliseconds): ${elapsedTimeInMilliseconds}`
          )
        }
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
