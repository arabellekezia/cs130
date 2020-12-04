import React from "react";
import { useWindowDimensions, StyleSheet, Platform } from "react-native";

import { StackedBarChart } from "react-native-chart-kit";

/**
 * This component is made so we can utilize StackedBarChart from react-native-chart-kit in our other components much more easily.
 * @param { Object } data Data that is accepted by BarChart to process
 * @param { Function => string } [color = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`] Sets the color of the bars
 * @param { Function => string } [labelColor = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`] Sets the color of the labels
 * @param { string } [backgroundColor = "#ffffff"] Sets background color of chart
 * @param { number } [scaleDimensions = 1] Number with which to scale the chart size
 * @param { string } [yAxisSuffix = ""] Append text to horizontal labels 
 * @param { number } [barPercentage = 0.4] Defines the percent (0-1) of the available width each bar width in a chart
 * @returns {StackedBarChart} A StackedBarChart with the following paramters added and consistent configuration for the whole application
 */

function AppStackedBarChart({
  data,
  color = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
  labelColor = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
  backgroundColor = "#ffffff",
  scaleDimensions = 1,
  yAxisSuffix = "",
  barPercentage = 0.4,
}) {
  return (
    <StackedBarChart
      data={data}
      width={scaleDimensions * useWindowDimensions().width}
      height={scaleDimensions * 200}
      yAxisSuffix={yAxisSuffix}
      chartConfig={{
        backgroundColor: backgroundColor,
        backgroundGradientFrom: backgroundColor,
        backgroundGradientTo: backgroundColor,
        barPercentage: barPercentage,
        decimalPlaces: 0,
        propsForBackgroundLines: { opacity: 0 },
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

export default AppStackedBarChart;
