import React from "react";
import { useWindowDimensions, StyleSheet, Platform } from "react-native";

import { BarChart } from "react-native-chart-kit";

function AppBarChart({
  data,
  color = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
  labelColor = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
  backgroundColor = "#ffffff",
  scaleDimensions = 1,
  yAxisSuffix = "",
}) {
  return (
    <BarChart
      data={data}
      width={scaleDimensions * useWindowDimensions().width}
      height={scaleDimensions * 200}
      yAxisSuffix={yAxisSuffix}
      fromZero
      withInnerLines={false}
      showBarTops={false}
      showValuesOnTopOfBars
      chartConfig={{
        backgroundColor: backgroundColor,
        backgroundGradientFrom: backgroundColor,
        backgroundGradientTo: backgroundColor,
        barPercentage: 0.4,
        barRadius: 6,
        decimalPlaces: 0,
        color: color,
        labelColor: labelColor,
      }}
      style={styles.container}
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

export default AppBarChart;
