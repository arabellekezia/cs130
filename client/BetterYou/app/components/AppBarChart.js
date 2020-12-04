import React from "react";
import { useWindowDimensions, StyleSheet, Platform } from "react-native";

import { BarChart } from "react-native-chart-kit";

/**
 * This component is made so we can utilize BarChart from react-native-chart-kit in our other components much more easily.
 * @param { StyleSheet } style Any additional styles
 * @param { Object } data Data that is accepted by BarChart to process
 * @param { Function } [color = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`] Sets the color of the bars
 * @param { Function } [labelColor = (opacity = 1) => `rgba(0, 0, 0, ${opacity})`] Sets the color of the labels
 * @param { string } [backgroundColor = "#ffffff"] Sets background color of chart
 * @param { number } [scaleDimensions = 1] Number with which to scale the chart size
 * @param { string } [yAxisSuffix = ""] Append text to horizontal labels 
 * @returns {BarChart} A barchart with the following paramters added
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
