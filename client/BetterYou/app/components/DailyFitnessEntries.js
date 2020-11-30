import React from "react";
import { StyleSheet, View } from "react-native";
import FitnessEntry from "./FitnessEntry";
import AppText from "./AppText";

function DailyFitnessEntries({ style, day, entries, headerTextStyle }) {
  return (
    <View style={{ ...styles.container, ...style }}>
      <View style={styles.headerContainer}>
        <AppText
          style={{ ...styles.headerText, ...headerTextStyle }}
          children={day}
        />
      </View>
      {entries.map((entry, key) => {
        const {
          iconName,
          startTime,
          activity,
          duration,
          caloriesBurned,
        } = entry;
        return (
          <FitnessEntry
            key={key}
            style={styles.entry}
            iconName={iconName}
            startTime={startTime}
            activity={activity}
            duration={duration}
            caloriesBurned={caloriesBurned}
          />
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    justifyContent: "center",
    alignItems: "flex-start",
    width: "100%",
  },
  headerContainer: {
    flexDirection: "row",
    justifyContent: "flex-start",
    alignItems: "center",
    borderBottomColor: "#dddddd",
    borderBottomWidth: 1,
    width: "100%",
  },
  headerText: {
    marginVertical: 12,
    marginLeft: 10,
    fontWeight: "bold",
    fontSize: 18,
  },
  entry: {
    marginVertical: 14,
    marginLeft: 10,
  },
});

export default DailyFitnessEntries;
