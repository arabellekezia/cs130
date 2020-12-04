import React from "react";
import { useWindowDimensions, StyleSheet, Platform } from "react-native";

import { LineChart } from "react-native-chart-kit";

/**
 * This component is made so we can utilize LineChart from react-native-chart-kit in our other components much more easily.
 * @param { Object } data Data that is accepted by LineChart to process
 * @param { Function => string } [color = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`] Sets the color of the lines
 * @param { Function => string } [labelColor = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`] Sets the color of the labels
 * @param { string } [backgroundColor = "#ffffff"] Sets background color of chart
 * @param { boolean } bezier Setting this to true creates a line graph with smooth lines
 * @param { number } [scaleDimensions = 1] Number with which to scale the chart size
 * @param { string } [yAxisSuffix = ""] Append text to horizontal labels 
 * @returns {LineChart} A LineChart with the following paramters added and consistent configuration for the whole application
 */
function AppLineChart({
  data,
  color = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
  labelColor = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
  backgroundColor = "#ffffff",
  bezier,
  scaleDimensions = 1,
  yAxisSuffix = "",
}) {
  return (
    <LineChart
      data={data}
      width={scaleDimensions * useWindowDimensions().width}
      height={scaleDimensions * 200}
      yAxisSuffix={yAxisSuffix}
      chartConfig={{
        backgroundColor: backgroundColor,
        backgroundGradientFrom: backgroundColor,
        backgroundGradientTo: backgroundColor,
        decimalPlaces: 0,
        color: color,
        labelColor: labelColor,
        propsForDots: {
          r: "5",
          strokeWidth: "2",
          stroke: backgroundColor,
        },
      }}
      bezier={bezier}
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

export default AppLineChart;
