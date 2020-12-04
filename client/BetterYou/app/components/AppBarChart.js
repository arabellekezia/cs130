import React from "react";
import { useWindowDimensions, StyleSheet, Platform } from "react-native";

import { BarChart } from "react-native-chart-kit";

/**
 * This component is made so we can utilize BarChart from react-native-chart-kit in our other components much more easily.
 * @module
 * @param { Object } ParameterObj The Object that encompasses all the parameters
 * @param { StyleSheet } ParameterObj.style Any additional styles
 * @param { Object } ParameterObj.data Data that is accepted by BarChart to process
 * @param { Function => string } [ParameterObj.color = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`] Sets the color of the bars
 * @param { Function => string } [ParameterObj.labelColor = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`] Sets the color of the labels
 * @param { string } [ParameterObj.backgroundColor = "#ffffff"] Sets background color of chart
 * @param { number } [ParameterObj.scaleDimensions = 1] Number with which to scale the chart size
 * @param { string } [ParameterObj.yAxisSuffix = ""] Append text to horizontal labels 
 * @returns {BarChart} A barchart with the following paramters added and consistent configuration for the whole application
 */

function AppBarChart({
  style,
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
      withInnerLines={true}
      showBarTops={false}
      withHorizontalLabels={false}
      showValuesOnTopOfBars
      chartConfig={{
        backgroundColor: backgroundColor,
        backgroundGradientFrom: backgroundColor,
        backgroundGradientTo: backgroundColor,
        barPercentage: 0.4,
        barRadius: 4,
        decimalPlaces: 0,
        color: color,
        labelColor: labelColor,
        fillShadowGradientOpacity: 0.7, //changes the opacity of the gradient
      }}
      style={{  ...styles.container, ...style  }}
    />
  );
}

const styles = StyleSheet.create({
  container: {
    marginVertical: 8,
    marginRight: "10%",
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
