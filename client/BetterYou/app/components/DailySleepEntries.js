import React from "react";
import { StyleSheet, View } from "react-native";
import AppText from "./AppText";

import SleepEntry from "./SleepEntry";

function DailySleepEntries({ style, entries, headerText, headerTextStyle }) {
  return (
    <View style={{ ...styles.container, ...style }}>
      <View style={styles.headerContainer}>
        <AppText
          style={{ ...styles.headerText, ...headerTextStyle }}
          children={headerText}
        />
      </View>
      {entries.map((entry, key) => {
        const { sleeptime, waketime, minutes } = entry;
        return (
          <SleepEntry
            key={key}
            style={styles.entry}
            sleeptime={sleeptime}
            waketime={waketime}
            minutes={minutes}
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
});

export default DailySleepEntries;
