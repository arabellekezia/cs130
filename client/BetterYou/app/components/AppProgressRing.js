import React from "react";
import { useWindowDimensions, StyleSheet, Platform } from "react-native";

import { ProgressChart } from "react-native-chart-kit";

function AppProgressRing({
  data,
  color = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
  labelColor = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
  strokeWidth = 16,
  radius = 32,
  backgroundColor = "#ffffff",
  scaleDimensions = 1,
  hideLegend,
}) {
  return (
    <ProgressChart
      data={data}
      width={scaleDimensions * useWindowDimensions().width}
      height={scaleDimensions * 200}
      strokeWidth={strokeWidth}
      radius={radius}
      chartConfig={{
        backgroundColor: backgroundColor,
        backgroundGradientFrom: backgroundColor,
        backgroundGradientTo: backgroundColor,
        color: color,
        labelColor: labelColor,
      }}
      style={styles.container}
      hideLegend={hideLegend}
    />
  );
}

const styles = StyleSheet.create({
  container: {
    marginVertical: 8,
    ...Platform.select({
      ios: {
        // // styles for box shadow
        // shadowOpacity: 0.1,
        // shadowRadius: 5,
        // shadowColor: "#000",
        // shadowOffset: { height: 1, width: 1 },
      },
      android: {
        // android styles
      },
    }),
  },
});

export default AppProgressRing;
