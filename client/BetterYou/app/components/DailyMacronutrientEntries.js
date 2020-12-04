import React from "react";
import { StyleSheet, View } from "react-native";

import IndivMacroCard from "./IndivMacroCard";

function DailyMacronutrientEntries({ style, entries }) {
  return (
    <View style={{ ...styles.container, ...style }}>
      {entries.map((entry, key) => {
        const {
          macroName,
          percentage,
          foods,
        } = entry;
        return (
          <IndivMacroCard 
            key={key}
            style={styles.entry}
            macroName={macroName}
            percentage={percentage}
            foods={foods}
          />
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    justifyContent: "center",
    alignItems: "center",
    width: "100%",
  },
  entry: {
    marginVertical: 14,
    borderWidth: 1,
    borderRadius: 10,
  },
});

export default DailyMacronutrientEntries;
